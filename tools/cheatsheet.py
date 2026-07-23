#!/usr/bin/env python3
"""Turn a YAML selection into a KACTL-style LaTeX cheatsheet (and, optionally, a PDF).

The cheatsheet is a compact multi-column reference sheet built from the
per-algorithm code files under ``docs/algorithms/**/code/``. You choose *what*
to include and *how* to render it in a small YAML config; this script resolves
each algorithm to the right code file, injects everything into
``templates/cheatsheet.tex`` and writes a ``.tex`` (and a ``.pdf`` with ``--pdf``
when ``pdflatex`` is available).

Config schema
=============

.. code-block:: yaml

    title: "Chuletario ICPC CUNEF"   # title printed on the sheet
    language: cpp                    # cpp | py   -> global default language
    style: contest                   # full | clean | contest -> global default style
    include_stats: true              # print complexity / use-case under each snippet
    columns: 3                       # number of multicol columns
    algorithms:                      # ordered list; each item is either ...
      - fenwick-tree                 #   ... a bare id (uses the globals), or ...
      - id: bitmask-tsp              #   ... a mapping overriding the globals:
        version: v1                  #       version  (default: meta.current_version)
        style: clean                 #       style    (default: global style)
        language: cpp                #       language (default: global language)

For each item the algorithm is resolved via ``common.iter_algorithms()``; the
code file read is ``<base>.<version>.<style>.<ext>`` inside the algorithm's
``code/`` directory. If that file is missing the item is warned about and
skipped.

Examples
========

.. code-block:: bash

    # Default: build templates/cheatsheet.example.yaml into build/cheatsheet.tex
    python tools/cheatsheet.py

    # A custom selection, forcing Python + the "clean" style, compiled to PDF:
    python tools/cheatsheet.py --config mi_chuleta.yaml --out build/chuleta \\
        --language py --style clean --pdf

    # Everything the repo has, C++ contest style, into one big sheet:
    python tools/cheatsheet.py --all --language cpp --style contest --pdf
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import common
from common import LANGUAGES, STYLES

TEMPLATE_PATH = common.REPO_ROOT / "templates" / "cheatsheet.tex"
DEFAULT_CONFIG = common.REPO_ROOT / "templates" / "cheatsheet.example.yaml"
DEFAULT_OUT = common.REPO_ROOT / "build" / "cheatsheet"

# listings `language=` value per extension.
LST_LANGUAGE = {"cpp": "C++", "py": "Python"}


# --------------------------------------------------------------------------- #
# LaTeX helpers
# --------------------------------------------------------------------------- #
_LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(text: str) -> str:
    """Escape LaTeX special characters in normal (non-verbatim) text."""
    out = []
    for ch in str(text):
        out.append(_LATEX_ESCAPES.get(ch, ch))
    return "".join(out)


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
class ConfigError(Exception):
    pass


def load_config(path: Path) -> dict:
    if not path.exists():
        raise ConfigError(f"config file not found: {path}")
    cfg = common.load_yaml(path)
    if not isinstance(cfg, dict):
        raise ConfigError(f"config must be a YAML mapping: {path}")

    cfg.setdefault("title", "Cheatsheet")
    cfg.setdefault("language", "cpp")
    cfg.setdefault("style", "contest")
    cfg.setdefault("include_stats", True)
    cfg.setdefault("columns", 3)
    cfg.setdefault("algorithms", [])

    if cfg["language"] not in LANGUAGES:
        raise ConfigError(
            f"config: language must be one of {sorted(LANGUAGES)}, got {cfg['language']!r}"
        )
    if cfg["style"] not in STYLES:
        raise ConfigError(f"config: style must be one of {STYLES}, got {cfg['style']!r}")
    try:
        cfg["columns"] = int(cfg["columns"])
    except (TypeError, ValueError):
        raise ConfigError(f"config: columns must be an integer, got {cfg['columns']!r}")
    if cfg["columns"] < 1:
        raise ConfigError("config: columns must be >= 1")
    if not isinstance(cfg["algorithms"], list):
        raise ConfigError("config: 'algorithms' must be a list")
    return cfg


def normalize_item(item, cfg: dict) -> dict:
    """Turn a config algorithm entry (str or mapping) into a resolved dict."""
    if isinstance(item, str):
        item = {"id": item}
    elif isinstance(item, dict):
        item = dict(item)
    else:
        raise ConfigError(f"algorithm entry must be a string or mapping, got {item!r}")

    if "id" not in item:
        raise ConfigError(f"algorithm entry missing 'id': {item!r}")

    lang = item.get("language", cfg["language"])
    style = item.get("style", cfg["style"])
    if lang not in LANGUAGES:
        raise ConfigError(f"{item['id']}: language must be one of {sorted(LANGUAGES)}")
    if style not in STYLES:
        raise ConfigError(f"{item['id']}: style must be one of {STYLES}")
    return {
        "kind": "snippet",
        "id": item["id"],
        "version": item.get("version"),  # None -> current_version
        "style": style,
        "language": lang,
    }


def meta_cheatsheet_items(algo: common.Algorithm, cfg: dict) -> list[dict]:
    """Resolve an algorithm's optional ``cheatsheet:`` list into render items.

    Each entry is a mapping ``{file, title, language}`` naming a source file to
    include verbatim (relative to the algorithm folder, or its ``code/`` dir).
    This is the granular opt-in used by ``article`` pages (and any snippet that
    wants to show specific files rather than its canonical implementation).
    """
    raw = algo.meta.get("cheatsheet")
    if not raw:
        return []
    if not isinstance(raw, list):
        raise ConfigError(f"{algo.id}: meta 'cheatsheet' must be a list")
    items: list[dict] = []
    for entry in raw:
        if not isinstance(entry, dict) or "file" not in entry:
            raise ConfigError(
                f"{algo.id}: each 'cheatsheet' entry must be a mapping with a 'file' key"
            )
        lang = entry.get("language", cfg["language"])
        if lang not in LANGUAGES:
            raise ConfigError(f"{algo.id}: cheatsheet language must be one of {sorted(LANGUAGES)}")
        items.append({
            "kind": "file",
            "id": algo.id,
            "file": entry["file"],
            "title": entry.get("title") or algo.name("es"),
            "language": lang,
        })
    return items


# --------------------------------------------------------------------------- #
# Algorithm resolution
# --------------------------------------------------------------------------- #
def find_code_file(algo: common.Algorithm, version: str, style: str, ext: str) -> Path | None:
    """Return the ``<base>.<version>.<style>.<ext>`` file, or None if absent.

    The ``<base>`` differs per algorithm (fenwick, tsp, convex_hull, ...), so we
    glob for any file carrying the requested version/style/ext suffix.
    """
    matches = sorted(algo.code_dir.glob(f"*.{version}.{style}.{ext}"))
    return matches[0] if matches else None


def stats_line(algo: common.Algorithm, lang_ui: str = "es") -> str:
    """Build a one-line 'complexity / use-case' string from meta.stats (LaTeX-escaped)."""
    stats = algo.meta.get("stats") or {}
    parts: list[str] = []

    complexity = stats.get("complexity") or {}
    if isinstance(complexity, dict):
        comp = ", ".join(f"{k}: {v}" for k, v in complexity.items())
        if comp:
            parts.append(comp)

    use_case = stats.get("use_case")
    if isinstance(use_case, dict):
        use_case = use_case.get(lang_ui) or use_case.get("es") or use_case.get("en")
    if use_case:
        parts.append(str(use_case))

    return latex_escape("  |  ".join(parts))


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def render_algorithm_block(algo: common.Algorithm, resolved: dict, cfg: dict,
                           *, verbose: bool) -> str | None:
    """Render one algorithm into a LaTeX block, or None if its code file is missing."""
    version = resolved["version"] or algo.current_version
    style = resolved["style"]
    ext = resolved["language"]

    code_file = find_code_file(algo, version, style, ext)
    if code_file is None:
        expected = common.build_code_filename("<base>", version, style, ext)
        print(
            f"warning: no code file for '{algo.id}' "
            f"(looked for {expected} in {algo.code_dir.relative_to(common.REPO_ROOT)}); skipping",
            file=sys.stderr,
        )
        return None

    # Strip hidden comments (//! / #!, incl. the AUTO-GENERATED header) — they
    # must not appear in the cheatsheet.
    code = common.strip_hidden_comments(code_file.read_text(encoding="utf-8"), ext)
    if verbose:
        print(f"  + {algo.id}: {code_file.relative_to(common.REPO_ROOT)}")

    lst_lang = LST_LANGUAGE.get(ext, "")
    lang_opt = f"[language={lst_lang}]" if lst_lang else ""

    lines = [f"\\csalgo{{{latex_escape(algo.name('es'))}}}"]
    if cfg["include_stats"]:
        line = stats_line(algo)
        if line:
            lines.append(f"\\csstats{{{line}}}")
    lines.append(f"\\begin{{lstlisting}}{lang_opt}")
    lines.append(code.rstrip("\n"))
    lines.append("\\end{lstlisting}")
    return "\n".join(lines)


def render_file_block(algo: common.Algorithm, resolved: dict, *, verbose: bool) -> str | None:
    """Render one explicit ``cheatsheet:`` file entry into a LaTeX block."""
    ext = resolved["language"]
    rel = resolved["file"]
    candidates = [algo.directory / rel, algo.code_dir / rel]
    code_file = next((p for p in candidates if p.is_file()), None)
    if code_file is None:
        print(
            f"warning: cheatsheet file for '{algo.id}' not found "
            f"(looked for {rel} under {algo.directory.relative_to(common.REPO_ROOT)}); skipping",
            file=sys.stderr,
        )
        return None

    code = common.strip_hidden_comments(code_file.read_text(encoding="utf-8"), ext)
    if verbose:
        print(f"  + {algo.id}: {code_file.relative_to(common.REPO_ROOT)}")

    lst_lang = LST_LANGUAGE.get(ext, "")
    lang_opt = f"[language={lst_lang}]" if lst_lang else ""
    lines = [
        f"\\csalgo{{{latex_escape(resolved['title'])}}}",
        f"\\begin{{lstlisting}}{lang_opt}",
        code.rstrip("\n"),
        "\\end{lstlisting}",
    ]
    return "\n".join(lines)


def build_items(cfg: dict, use_all: bool) -> list[dict]:
    """Return the ordered list of resolved algorithm items to render."""
    if use_all:
        return [
            normalize_item(algo.id, cfg) for algo in common.iter_algorithms()
        ]
    return [normalize_item(item, cfg) for item in cfg["algorithms"]]


def render_body(items: list[dict], cfg: dict, *, verbose: bool) -> tuple[str, int]:
    """Render every item; return (body_latex, included_count)."""
    algos_by_id = {a.id: a for a in common.iter_algorithms()}
    blocks: list[str] = []
    for resolved in items:
        algo = algos_by_id.get(resolved["id"])
        if algo is None:
            print(f"warning: unknown algorithm id '{resolved['id']}'; skipping", file=sys.stderr)
            continue
        if resolved.get("kind") == "file":
            block = render_file_block(algo, resolved, verbose=verbose)
        else:
            block = render_algorithm_block(algo, resolved, cfg, verbose=verbose)
        if block is not None:
            blocks.append(block)
    return "\n\n".join(blocks), len(blocks)


def render_document(cfg: dict, body: str) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template
        .replace("%%TITLE%%", latex_escape(cfg["title"]))
        .replace("%%NUMCOLUMNS%%", str(cfg["columns"]))
        .replace("%%BODY%%", body)
    )


# --------------------------------------------------------------------------- #
# PDF compilation
# --------------------------------------------------------------------------- #
def compile_pdf(tex_path: Path, *, verbose: bool) -> bool:
    """Compile ``tex_path`` to a PDF next to it. Return True on success."""
    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        print(
            "note: 'pdflatex' not found on PATH; wrote the .tex only.\n"
            "      Install a LaTeX distribution (e.g. TeX Live) to produce a PDF, "
            "or compile the .tex yourself.",
            file=sys.stderr,
        )
        return False

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        job = tex_path.stem
        work_tex = tmp_dir / f"{job}.tex"
        work_tex.write_text(tex_path.read_text(encoding="utf-8"), encoding="utf-8")
        cmd = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"{job}.tex"]
        # Run twice so multicol balancing / references settle.
        for i in range(2):
            proc = subprocess.run(
                cmd, cwd=tmp_dir, capture_output=True,
                text=True, encoding="utf-8", errors="replace",
            )
            if proc.returncode != 0:
                print(f"error: pdflatex failed (pass {i + 1}).", file=sys.stderr)
                log = tmp_dir / f"{job}.log"
                tail = ""
                if log.exists():
                    tail = "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-25:])
                print(tail or proc.stdout[-2000:], file=sys.stderr)
                return False
        produced = tmp_dir / f"{job}.pdf"
        if not produced.exists():
            print("error: pdflatex reported success but produced no PDF.", file=sys.stderr)
            return False
        pdf_path = tex_path.with_suffix(".pdf")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(produced, pdf_path)
        if verbose:
            print(f"  compiled {pdf_path.relative_to(common.REPO_ROOT) if pdf_path.is_relative_to(common.REPO_ROOT) else pdf_path}")
    return True


# --------------------------------------------------------------------------- #
# Orchestrator entry point (used by tools/gen.py)
# --------------------------------------------------------------------------- #
DEFAULT_SITE_TEX = common.DOCS_DIR / "cheatsheet" / "cheatsheet.tex"


def generate(check: bool = False) -> list[common.Change]:
    """Build the DEFAULT cheatsheet (every algorithm that has code) and write it
    to docs/cheatsheet/cheatsheet.tex. On a real run (not --check) it also
    compiles the PDF if pdflatex is available. Returns the .tex Change.

    Presentation (title, columns, language, style, stats) comes from
    templates/cheatsheet.example.yaml; the algorithm list is ignored — ALL
    algorithms with a matching code file are included.
    """
    try:
        cfg = load_config(DEFAULT_CONFIG)
    except ConfigError:
        cfg = {"title": "Chuletario ICPC CUNEF", "language": "cpp", "style": "contest",
               "include_stats": True, "columns": 3, "algorithms": []}

    items = []
    for algo in common.iter_algorithms():
        # An explicit meta `cheatsheet:` list wins for any format (article or
        # snippet): include exactly the files it names.
        explicit = meta_cheatsheet_items(algo, cfg)
        if explicit:
            items.extend(explicit)
            continue
        # Articles have no canonical snippet — skip unless they opted in above.
        if algo.is_article:
            continue
        resolved = normalize_item(algo.id, cfg)
        version = resolved["version"] or algo.current_version
        if find_code_file(algo, version, resolved["style"], resolved["language"]):
            items.append(resolved)   # only items that actually have code to show

    body, _ = render_body(items, cfg, verbose=False)
    doc = render_document(cfg, body)
    change = common.write_if_changed(DEFAULT_SITE_TEX, doc, check)

    if not check and change.action != "unchanged" and shutil.which("pdflatex"):
        compile_pdf(DEFAULT_SITE_TEX, verbose=False)

    return [change]


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cheatsheet.py",
        description=(
            "Generate a KACTL-style LaTeX cheatsheet (and optionally a PDF) from a "
            "YAML selection of algorithms. See the module docstring / the example "
            "config templates/cheatsheet.example.yaml for the config schema."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Config schema (YAML):\n"
            "  title:         str                     title printed on the sheet\n"
            "  language:      cpp | py                global default language\n"
            "  style:         full | clean | contest  global default code style\n"
            "  include_stats: bool                    print complexity/use-case per snippet\n"
            "  columns:       int                     number of multicol columns\n"
            "  algorithms:    list                    ordered; each item is a bare id\n"
            "                                          or a mapping with keys:\n"
            "                                          id, version, style, language\n\n"
            "Examples:\n"
            "  python tools/cheatsheet.py\n"
            "  python tools/cheatsheet.py --config mi_chuleta.yaml --out build/chuleta --pdf\n"
            "  python tools/cheatsheet.py --all --language cpp --style contest --pdf\n"
        ),
    )
    parser.add_argument(
        "--config", type=Path, default=DEFAULT_CONFIG,
        help="path to the YAML selection file (default: templates/cheatsheet.example.yaml)",
    )
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUT,
        help="output path WITHOUT extension; the script appends .tex/.pdf "
             "(default: build/cheatsheet)",
    )
    parser.add_argument(
        "--pdf", action="store_true",
        help="also compile a PDF (requires pdflatex on PATH; otherwise just the .tex)",
    )
    parser.add_argument(
        "--language", choices=sorted(LANGUAGES),
        help="override the config's global language for every item",
    )
    parser.add_argument(
        "--style", choices=STYLES,
        help="override the config's global style for every item",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="ignore the config's algorithm list and include ALL algorithms "
             "using the global defaults",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="print each resolved algorithm and code file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        cfg = load_config(args.config)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Global CLI overrides.
    if args.language:
        cfg["language"] = args.language
    if args.style:
        cfg["style"] = args.style

    if args.verbose:
        print(f"config: {args.config}")
        print(f"  title={cfg['title']!r} language={cfg['language']} style={cfg['style']} "
              f"columns={cfg['columns']} include_stats={cfg['include_stats']} all={args.all}")

    try:
        items = build_items(cfg, args.all)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not items:
        print("warning: no algorithms selected (empty 'algorithms' list and no --all).",
              file=sys.stderr)

    body, included = render_body(items, cfg, verbose=args.verbose)
    if included == 0:
        body = "% (no algorithms rendered — every selected item was missing or skipped)"

    document = render_document(cfg, body)

    tex_path = args.out.with_suffix(".tex")
    tex_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path.write_text(document, encoding="utf-8")
    shown = tex_path.relative_to(common.REPO_ROOT) if tex_path.is_relative_to(common.REPO_ROOT) else tex_path
    print(f"wrote {shown}  ({included} algorithm(s))")

    if args.pdf:
        if compile_pdf(tex_path, verbose=args.verbose):
            pdf_path = tex_path.with_suffix(".pdf")
            shown_pdf = pdf_path.relative_to(common.REPO_ROOT) if pdf_path.is_relative_to(common.REPO_ROOT) else pdf_path
            print(f"wrote {shown_pdf}")
        else:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
