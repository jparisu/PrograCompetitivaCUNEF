#!/usr/bin/env python3
"""Generate the machine-readable algorithms index consumed by the overview table.

Every algorithm under ``docs/algorithms/**`` owns a ``meta.yaml`` (the single
source of truth, see ``.devs/v2-design.md`` §3). This script reads all of them
and distils each into a compact JSON record, writing the whole collection to::

    docs/assets/data/algorithms.json

That file is fetched at runtime by ``docs/assets/js/overview-table.js`` to build
the interactive "Resumen" table (sort / filter / show-hide columns). Keeping the
data in a static JSON blob means the page stays a plain client-side app: no build
step at doc-render time, and it works unchanged under GitHub Pages preview paths
like ``/pr-preview/pr-N/``.

Each JSON entry has a stable field order::

    {
      "id":         "fenwick-tree",
      "name":       {"es": "...", "en": "..."},
      "level":      "intermediate",
      "difficulty": 3.0,
      "techniques": ["amortized"],
      "tags":       ["range-query", "point-update", "logn"],
      "prereq":     ["arrays", "prefix-sums-1d"],
      "complexity": "O(log n)",
      "languages":  ["cpp", "py"],
      "url":        "../algorithms/data-structures/fenwick-tree/"
    }

- ``complexity`` is a single representative string picked from
  ``meta.stats.complexity``: the ``time`` field if present, else the first
  value, else "".
- ``languages`` are the extensions (cpp/py) that have a ``full`` code file for
  the algorithm's current version.
- ``url`` is a page-relative link *from* ``/overview/`` *to* the algorithm page,
  derived from the folder's path under ``docs/``.

Entries are sorted by (level order via ``common.LEVELS``, then id).

Every write goes through ``common.write_if_changed`` so ``--check`` is an
accurate dry-run (and exits non-zero when the output is stale), matching the
other generators.

Examples
--------
    python tools/genoverview.py              # (re)write docs/assets/data/algorithms.json
    python tools/genoverview.py --check       # CI dry-run: fail if the file is stale
    python tools/genoverview.py -v            # also print a one-line summary per entry
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402


# Where the generated data file lives, and the page-relative depth of /overview/.
OUTPUT_PATH = common.DOCS_DIR / "assets" / "data" / "algorithms.json"


def _complexity(algo: common.Algorithm) -> str:
    """Pick a single representative complexity string from meta.stats.complexity.

    Prefers the ``time`` field; otherwise the first listed value; otherwise "".
    """
    stats = algo.meta.get("stats") or {}
    complexity = stats.get("complexity") if isinstance(stats, dict) else None
    if not isinstance(complexity, dict) or not complexity:
        return ""
    if complexity.get("time"):
        return str(complexity["time"])
    first = next(iter(complexity.values()), "")
    return str(first) if first else ""


def _languages(algo: common.Algorithm) -> list[str]:
    """Extensions (cpp/py) with a full file for the current version.

    Uses ``Algorithm.languages_present()`` when available, else globs the code
    directory for ``*.<version>.full.<ext>`` files directly.
    """
    present = getattr(algo, "languages_present", None)
    if callable(present):
        return list(present())
    found: list[str] = []
    for ext in common.LANGUAGES:
        if any(algo.code_dir.glob(f"*.{algo.current_version}.full.{ext}")):
            found.append(ext)
    return found


def _url(algo: common.Algorithm) -> str:
    """Page-relative link from /overview/ to the algorithm page.

    The algorithm folder relative to docs/ looks like
    ``algorithms/data-structures/fenwick-tree``; from /overview/ (depth 1) the
    link back up and into it is ``../algorithms/data-structures/fenwick-tree/``.
    """
    rel = algo.directory.relative_to(common.DOCS_DIR).as_posix()
    return f"../{rel}/"


def _name(algo: common.Algorithm) -> dict[str, str]:
    name = algo.meta.get("name", {})
    if isinstance(name, dict):
        es = name.get("es") or name.get("en") or algo.id
        en = name.get("en") or name.get("es") or algo.id
        return {"es": es, "en": en}
    return {"es": str(name), "en": str(name)}


def _entry(algo: common.Algorithm) -> "OrderedDict[str, object]":
    """Build one ordered JSON record for an algorithm."""
    entry: "OrderedDict[str, object]" = OrderedDict()
    entry["id"] = algo.id
    entry["name"] = _name(algo)
    entry["level"] = algo.meta.get("level", "")
    entry["difficulty"] = algo.meta.get("difficulty")
    entry["techniques"] = list(algo.meta.get("techniques") or [])
    entry["tags"] = list(algo.meta.get("tags") or [])
    entry["prereq"] = list(algo.meta.get("prerequisites") or [])
    entry["complexity"] = _complexity(algo)
    entry["languages"] = _languages(algo)
    entry["url"] = _url(algo)
    return entry


def _render(algos: list[common.Algorithm]) -> str:
    """Serialise the algorithm entries to pretty-printed JSON (with trailing newline)."""
    data = [_entry(a) for a in algos]
    # iter_algorithms already sorts by (level order, id); keep that order and do
    # not sort keys so the hand-built field order above is preserved.
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def generate(check: bool = False) -> list[common.Change]:
    """Write docs/assets/data/algorithms.json from every algorithm's meta.yaml.

    Returns the single :class:`common.Change` (create / modify / unchanged) so
    callers can report a plan and decide the exit status. In ``check`` mode
    nothing is written.
    """
    algos = common.iter_algorithms()
    content = _render(algos)
    return [common.write_if_changed(OUTPUT_PATH, content, check)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="genoverview.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Generate docs/assets/data/algorithms.json from every algorithm's "
            "meta.yaml.\n\n"
            "The JSON is the data source for the interactive overview table "
            "(docs/overview/index.md + docs/assets/js/overview-table.js): one "
            "record per algorithm with its name, level, difficulty, techniques, "
            "tags, prerequisites, a representative complexity string, the code "
            "languages present, and a page-relative link to its docs page.\n\n"
            "Entries are sorted by level (base -> expert) then id. Use --check "
            "in CI to fail when the committed JSON is out of date with the "
            "meta.yaml files."
        ),
        epilog=(
            "Examples:\n"
            "  python tools/genoverview.py            # (re)write the JSON\n"
            "  python tools/genoverview.py --check    # dry-run; non-zero if stale\n"
            "  python tools/genoverview.py -v         # print a per-entry summary\n"
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry-run: do not write anything, only report what would change. "
        "Exit non-zero if the JSON is missing or out of date (CI mode).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print a one-line summary per algorithm entry (id, level, "
        "languages, url) in addition to the change plan.",
    )
    args = parser.parse_args(argv)

    changes = generate(check=args.check)

    if args.verbose:
        for a in common.iter_algorithms():
            langs = ",".join(_languages(a)) or "-"
            print(
                f"  {a.id:<22} {a.meta.get('level', '?'):<12} "
                f"[{langs}]  {_url(a)}"
            )

    pending = common.print_plan(
        changes, check=args.check, title="genoverview: algorithms.json from meta.yaml"
    )

    if args.check and pending:
        print(
            f"\n{pending} file(s) out of date. Run: python tools/genoverview.py"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
