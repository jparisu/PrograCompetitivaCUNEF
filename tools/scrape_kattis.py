#!/usr/bin/env python3
"""Scrape the Kattis affiliation standings and store them as JSON with history.

This script fetches the public affiliation page on Kattis (by default the CUNEF
affiliation, ``https://open.kattis.com/affiliations/cunef.edu``), parses the
members/users table and appends today's snapshot to a single JSON file that
holds the full history of snapshots. The ranking web page under
``docs/ranklist/`` renders trends from that file.

Output JSON schema (a single file that accumulates history)::

    {
      "affiliation": "cunef.edu",
      "url": "https://open.kattis.com/affiliations/cunef.edu",
      "updated": "2026-07-21T10:30:00+00:00",   # ISO-8601, last write time
      "snapshots": [
        {
          "date": "2026-07-21",                  # YYYY-MM-DD
          "members": [
            {
              "rank": 1,
              "name": "Ada Lovelace",
              "handle": "ada",                   # from /users/<handle>, may be null
              "score": 123.4,
              "solved": 88                       # may be null
            }
          ]
        }
      ]
    }

Snapshots are kept sorted by date ascending. Running the scraper again on the
same date REPLACES that date's snapshot instead of duplicating it.

Because Kattis markup can change, the parser is defensive: it inspects the
table header to locate columns, logs warnings when something is missing and
keeps going instead of crashing.

Examples::

    # Scrape the default CUNEF affiliation into the default file.
    python tools/scrape_kattis.py

    # Verbose, print what was parsed without writing anything.
    python tools/scrape_kattis.py --dry-run -v

    # Backfill a specific date and anonymize member identities.
    python tools/scrape_kattis.py --date 2026-01-01 --anonymize

    # Point at a different affiliation and output file.
    python tools/scrape_kattis.py \
        --url https://open.kattis.com/affiliations/example.edu \
        --output docs/assets/data/standings.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
from datetime import date as date_cls, datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    sys.exit(
        "Missing dependencies. Install the tooling deps with:\n"
        "    pip install -r tools/requirements.txt"
    )

# Reuse the repo-relative paths from the shared helpers when available so the
# default output lives next to the rest of the site assets.
try:
    from common import DOCS_DIR, REPO_ROOT
except Exception:  # pragma: no cover - keep the scraper runnable standalone
    REPO_ROOT = Path(__file__).resolve().parent.parent
    DOCS_DIR = REPO_ROOT / "docs"

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
DEFAULT_AFFILIATION = "cunef.edu"
DEFAULT_URL = f"https://open.kattis.com/affiliations/{DEFAULT_AFFILIATION}"
DEFAULT_OUTPUT = DOCS_DIR / "assets" / "data" / "standings.json"
DEFAULT_TIMEOUT = 30.0
MAX_PAGES = 50  # safety cap when following pagination
USER_AGENT = (
    "PrograCompetitivaCUNEF-standings-bot/1.0 "
    "(+https://github.com/jparisu/PrograCompetitivaCUNEF; educational use)"
)

# Exit codes.
EXIT_OK = 0
EXIT_NETWORK = 2
EXIT_PARSE = 3
EXIT_IO = 4
EXIT_USAGE = 5

log = logging.getLogger("scrape_kattis")

# Header keywords (lower-case) used to map table columns to fields. Kattis has
# historically used English labels; we accept a few variants defensively.
HEADER_ALIASES = {
    "rank": {"rank", "#", "pos", "position"},
    "name": {"name", "user", "username", "member"},
    "score": {"score", "points", "rating"},
    "solved": {"solved", "problems", "ac", "accepted", "# solved"},
}


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #
def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _parse_float(text: str) -> float | None:
    """Extract the first number from a cell like ``123.4`` or ``1,234.5``."""
    if not text:
        return None
    m = re.search(r"-?\d[\d,]*\.?\d*", text.replace(" ", " "))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _parse_int(text: str) -> int | None:
    value = _parse_float(text)
    return int(value) if value is not None else None


def _extract_handle(cell) -> str | None:
    """Return the ``<handle>`` from any ``/users/<handle>`` link in the cell."""
    if cell is None:
        return None
    for a in cell.find_all("a", href=True):
        m = re.search(r"/users/([^/?#]+)", a["href"])
        if m:
            return m.group(1)
    return None


def _map_columns(header_cells: list[str]) -> dict[str, int]:
    """Map field name -> column index using the header row labels."""
    mapping: dict[str, int] = {}
    normalized = [_clean_text(h).lower() for h in header_cells]
    for field, aliases in HEADER_ALIASES.items():
        for idx, label in enumerate(normalized):
            if label in aliases or any(label == a for a in aliases):
                mapping[field] = idx
                break
    # Fuzzy fallback: substring match for anything still unmapped.
    for field, aliases in HEADER_ALIASES.items():
        if field in mapping:
            continue
        for idx, label in enumerate(normalized):
            if any(a in label for a in aliases):
                mapping[field] = idx
                break
    return mapping


def _find_standings_table(soup: BeautifulSoup):
    """Pick the most likely standings table: the one with the most data rows."""
    tables = soup.find_all("table")
    if not tables:
        return None
    best = None
    best_rows = -1
    for table in tables:
        rows = table.find_all("tr")
        if len(rows) > best_rows:
            best, best_rows = table, len(rows)
    return best


def parse_members(html: str) -> list[dict]:
    """Parse a single standings page into a list of member dicts.

    Never raises on missing columns: logs a warning and fills ``None``.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = _find_standings_table(soup)
    if table is None:
        log.warning("no <table> found on page")
        return []

    # Header cells: prefer <thead>, else the first row with <th>.
    header_cells: list[str] = []
    thead = table.find("thead")
    if thead:
        header_cells = [_clean_text(th.get_text()) for th in thead.find_all(["th", "td"])]
    if not header_cells:
        first = table.find("tr")
        if first:
            header_cells = [_clean_text(c.get_text()) for c in first.find_all(["th", "td"])]

    columns = _map_columns(header_cells)
    if not columns:
        log.warning(
            "could not map any known column from header %r; "
            "falling back to positional guess (rank, name, score, solved)",
            header_cells,
        )
        columns = {"rank": 0, "name": 1, "score": 2, "solved": 3}
    else:
        log.debug("column mapping: %s (header=%r)", columns, header_cells)

    # Body rows: prefer <tbody>, else every <tr> that isn't the header.
    body = table.find("tbody")
    if body:
        rows = body.find_all("tr")
    else:
        all_rows = table.find_all("tr")
        rows = all_rows[1:] if header_cells else all_rows

    members: list[dict] = []
    for i, tr in enumerate(rows):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        # Skip rows that are clearly not data (e.g. a repeated header).
        if all(c.name == "th" for c in cells):
            continue

        def cell(field: str):
            idx = columns.get(field)
            if idx is None or idx >= len(cells):
                return None
            return cells[idx]

        name_cell = cell("name")
        name = _clean_text(name_cell.get_text()) if name_cell is not None else ""
        handle = _extract_handle(name_cell) if name_cell is not None else None

        rank_cell = cell("rank")
        rank = _parse_int(rank_cell.get_text()) if rank_cell is not None else None
        if rank is None:
            rank = i + 1  # positional fallback; standings are already ordered

        score_cell = cell("score")
        score = _parse_float(score_cell.get_text()) if score_cell is not None else None
        if score is None:
            log.warning("row %d (%r): missing/unparsable score; defaulting to 0.0", i, name)
            score = 0.0

        solved_cell = cell("solved")
        solved = _parse_int(solved_cell.get_text()) if solved_cell is not None else None

        if not name and handle is None:
            log.warning("row %d: no name and no handle; skipping", i)
            continue

        members.append(
            {
                "rank": int(rank),
                "name": name or (handle or ""),
                "handle": handle,
                "score": float(score),
                "solved": solved,
            }
        )

    return members


def _next_page_url(html: str, current_url: str) -> str | None:
    """Best-effort discovery of a ``?page=N`` next link."""
    soup = BeautifulSoup(html, "html.parser")
    # Explicit rel="next".
    link = soup.find("a", rel="next")
    if link and link.get("href"):
        return urljoin(current_url, link["href"])
    # A link whose text is "Next" / "»".
    for a in soup.find_all("a", href=True):
        text = _clean_text(a.get_text()).lower()
        if text in {"next", "next »", "»", "siguiente"} and "page=" in a["href"]:
            return urljoin(current_url, a["href"])
    return None


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #
def fetch_all_members(url: str, timeout: float) -> list[dict]:
    """Fetch every page of the standings and return the combined member list.

    Raises ``requests.RequestException`` on network failure.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    members: list[dict] = []
    seen_handles: set[str] = set()
    seen_urls: set[str] = set()
    page_url: str | None = url

    for page_no in range(1, MAX_PAGES + 1):
        if page_url is None or page_url in seen_urls:
            break
        seen_urls.add(page_url)
        log.info("fetching page %d: %s", page_no, page_url)
        resp = session.get(page_url, timeout=timeout)
        resp.raise_for_status()
        page_members = parse_members(resp.text)
        log.info("  parsed %d members", len(page_members))

        added = 0
        for m in page_members:
            key = m["handle"] or f"{m['name']}#{m['rank']}"
            if key in seen_handles:
                continue
            seen_handles.add(key)
            members.append(m)
            added += 1

        # Stop paginating if a page adds nothing new (avoids infinite loops).
        if added == 0 and page_no > 1:
            log.debug("page %d added no new members; stopping pagination", page_no)
            break

        page_url = _next_page_url(resp.text, page_url)

    # Re-sort by score desc as the authoritative order and renumber ranks so the
    # combined multi-page list is consistent.
    members.sort(key=lambda m: (-m["score"], m["rank"]))
    for i, m in enumerate(members, start=1):
        m["rank"] = i
    return members


# --------------------------------------------------------------------------- #
# Anonymization
# --------------------------------------------------------------------------- #
def anonymize_members(members: list[dict]) -> list[dict]:
    """Replace names with ``Estudiante N`` and handles with a short stable hash."""
    out = []
    for i, m in enumerate(members, start=1):
        seed = m.get("handle") or m.get("name") or str(i)
        short = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
        out.append(
            {
                "rank": m["rank"],
                "name": f"Estudiante {i}",
                "handle": short if m.get("handle") is not None else None,
                "score": m["score"],
                "solved": m.get("solved"),
            }
        )
    return out


# --------------------------------------------------------------------------- #
# JSON history handling
# --------------------------------------------------------------------------- #
def load_history(path: Path, url: str, affiliation: str) -> dict:
    """Load the existing JSON file or return a fresh skeleton."""
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"existing output file is not valid JSON: {exc}") from exc
        data.setdefault("affiliation", affiliation)
        data.setdefault("url", url)
        data.setdefault("snapshots", [])
        if not isinstance(data.get("snapshots"), list):
            raise RuntimeError("existing output file has a non-list 'snapshots' field")
        return data
    return {"affiliation": affiliation, "url": url, "snapshots": []}


def upsert_snapshot(data: dict, snapshot: dict) -> str:
    """Insert or replace the snapshot for its date. Returns 'added'|'replaced'."""
    snapshots = data["snapshots"]
    action = "added"
    for i, snap in enumerate(snapshots):
        if snap.get("date") == snapshot["date"]:
            snapshots[i] = snapshot
            action = "replaced"
            break
    else:
        snapshots.append(snapshot)
    snapshots.sort(key=lambda s: s.get("date", ""))
    return action


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _valid_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"date must be YYYY-MM-DD, got {value!r}")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scrape_kattis.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Scrape a Kattis affiliation standings page and append today's "
            "snapshot to a single JSON history file used by the ranking web page."
        ),
        epilog=(
            "Exit codes:\n"
            f"  {EXIT_OK}  success\n"
            f"  {EXIT_NETWORK}  network/HTTP error\n"
            f"  {EXIT_PARSE}  nothing parsed / parse error\n"
            f"  {EXIT_IO}  input/output (JSON read/write) error\n"
            f"  {EXIT_USAGE}  bad usage\n\n"
            "Examples:\n"
            "  python tools/scrape_kattis.py\n"
            "  python tools/scrape_kattis.py --dry-run -v\n"
            "  python tools/scrape_kattis.py --date 2026-01-01 --anonymize\n"
        ),
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="Affiliation standings URL to scrape (default: the CUNEF affiliation).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON history file to update (default: docs/assets/data/standings.json).",
    )
    parser.add_argument(
        "--date",
        type=_valid_date,
        default=None,
        metavar="YYYY-MM-DD",
        help="Override the snapshot date instead of using today (UTC). "
        "A snapshot with the same date is replaced.",
    )
    parser.add_argument(
        "--anonymize",
        action="store_true",
        help="Privacy option: replace names with 'Estudiante N' and handles "
        "with a short stable hash before storing.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        metavar="SECONDS",
        help=f"HTTP request timeout in seconds (default: {DEFAULT_TIMEOUT:g}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and print the standings but do not write the output file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity (-v info, -vv debug).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    level = logging.WARNING
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    # Resolve the affiliation slug from the URL for the JSON metadata.
    parsed = urlparse(args.url)
    affiliation = DEFAULT_AFFILIATION
    m = re.search(r"/affiliations/([^/?#]+)", parsed.path)
    if m:
        affiliation = m.group(1)

    # Determine the snapshot date. Only touch datetime.now() when not overridden.
    snapshot_date = args.date or date_cls.today().isoformat()

    # 1. Fetch + parse.
    try:
        members = fetch_all_members(args.url, timeout=args.timeout)
    except requests.RequestException as exc:
        log.error("network error while fetching %s: %s", args.url, exc)
        return EXIT_NETWORK
    except Exception as exc:  # unexpected parse-time failure
        log.error("unexpected error while scraping: %s", exc)
        return EXIT_PARSE

    if not members:
        log.error("parsed 0 members from %s (page layout may have changed)", args.url)
        return EXIT_PARSE

    if args.anonymize:
        members = anonymize_members(members)

    log.info("parsed %d members for %s on %s", len(members), affiliation, snapshot_date)

    snapshot = {"date": snapshot_date, "members": members}

    # 2. Dry run: print and stop.
    if args.dry_run:
        print(
            json.dumps(
                {
                    "affiliation": affiliation,
                    "url": args.url,
                    "would_write": str(args.output),
                    "snapshot": snapshot,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        log.info("dry run: nothing written")
        return EXIT_OK

    # 3. Load existing history, upsert, write.
    try:
        data = load_history(args.output, url=args.url, affiliation=affiliation)
    except RuntimeError as exc:
        log.error("%s", exc)
        return EXIT_IO

    # Keep metadata current.
    data["affiliation"] = affiliation
    data["url"] = args.url
    action = upsert_snapshot(data, snapshot)
    data["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        log.error("could not write %s: %s", args.output, exc)
        return EXIT_IO

    print(
        f"{action} snapshot {snapshot_date} "
        f"({len(members)} members) -> {args.output} "
        f"[{len(data['snapshots'])} snapshots total]"
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
