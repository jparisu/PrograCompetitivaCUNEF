#!/usr/bin/env python3
"""Generate the MkDocs ``nav:`` from every item's ``meta.yaml``.

The site's left-sidebar navigation used to be a ~90-line hand-maintained list in
``mkdocs.yml`` that duplicated the name/level/type/order already stored in each
``meta.yaml`` — and forgetting to add a new page there broke the ``mkdocs build
--strict`` CI. This script removes that duplication: it reads every item under
``docs/content/**`` and rewrites the ``nav:`` block of ``mkdocs.yml`` in place,
**grouped by level** (Base → Experto), labelling each entry with its type.

Only the ``nav:`` block is generated. Everything in ``mkdocs.yml`` *above* the
sentinel line::

    # === AUTO-GENERATED NAV — do not edit below (run: python tools/gen.py generate) ===

is hand-maintained and left untouched; everything from that sentinel to EOF is
owned by this script. The fixed scaffold pages (home, "empezar aquí", ranking,
cheatsheet, contributing) are defined in ``SCAFFOLD_*`` below.

Ordering within a level is ``(difficulty, name)`` — both from ``meta.yaml`` — so
the order is itself derived, not hand-curated. Items that ship ``cpp.md`` /
``python.md`` sub-pages get them nested under the item (the "En C++" / "En
Python" entries). WIP items are included (they are greyed out client-side by
``nav-wip.js``).

Every write goes through ``common.write_if_changed`` so ``--check`` is an
accurate dry-run (and exits non-zero when the nav is stale), matching the other
generators.

Examples
--------
    python tools/gennav.py            # rewrite the nav block in mkdocs.yml
    python tools/gennav.py --check    # CI dry-run: fail if the nav is stale
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency 'pyyaml'. Install: pip install -r tools/requirements.txt")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

MKDOCS_YML = common.REPO_ROOT / "mkdocs.yml"

SENTINEL = (
    "# === AUTO-GENERATED NAV — do not edit below "
    "(run: python tools/gen.py generate) ==="
)

# Fixed scaffold entries that are NOT derived from meta.yaml. Edit these here.
SCAFFOLD_TOP = [
    {"Inicio": "index.md"},
    {"Empezar aquí": "start/onboarding.md"},
]
# The landing/overview pages shown at the top of the "Contenidos" section.
CONTENIDOS_LANDING = [
    "content/index.md",  # bare page -> section index (navigation.indexes)
    {"Temas": "content/topics/index.md"},
    {"Mapa de contenidos": "content/matrix.md"},
    {"Grafo de dependencias": "content/graph.md"},
]
SCAFFOLD_BOTTOM = [
    {"Ranking": "ranklist/index.md"},
    {"Chuletario": "cheatsheet/index.md"},
    {
        "Contribuir": [
            {"Cómo contribuir": "contributing/index.md"},
            {"ToDo": "contributing/todo.md"},
            {"Sugerencias e incidencias": "contributing/issues.md"},
            {"Git y GitHub": "contributing/git-github.md"},
            {"Añadir un algoritmo": "contributing/add-algorithm.md"},
            {"Scripts del proyecto": "contributing/scripts.md"},
            {"Autores": "contributing/authors.md"},
        ]
    },
]


def _rel(path: Path) -> str:
    """Path relative to docs/, POSIX-style (what mkdocs nav expects)."""
    return path.relative_to(common.DOCS_DIR).as_posix()


def _label(algo: common.Algorithm) -> str:
    type_label = common.TYPE_LABELS.get(algo.type, algo.type)
    return f"{algo.name('es')} — {type_label}"


def _item_entry(algo: common.Algorithm):
    """One nav entry for an item, nesting cpp.md/python.md sub-pages if present."""
    index_rel = _rel(algo.directory / "index.md")
    children = [index_rel]
    cpp = algo.directory / "cpp.md"
    py = algo.directory / "python.md"
    if cpp.is_file() and py.is_file():
        children.append({"En C++": _rel(cpp)})
        children.append({"En Python": _rel(py)})
        return {_label(algo): children}
    # No language sub-pages: a plain "title: path" entry.
    return {_label(algo): index_rel}


def _sort_key(algo: common.Algorithm):
    diff = algo.meta.get("difficulty")
    try:
        diff = float(diff)
    except (TypeError, ValueError):
        diff = 99.0
    return (diff, algo.name("es").lower())


def build_nav() -> list:
    algos = common.iter_algorithms()
    by_level: dict[str, list[common.Algorithm]] = {lvl: [] for lvl in common.LEVELS}
    for a in algos:
        lvl = a.meta.get("level")
        if lvl in by_level:
            by_level[lvl].append(a)
        else:
            print(f"  warning: {a.id} has no/invalid level {lvl!r}; skipped from nav",
                  file=sys.stderr)

    contenidos = [{"Contenidos": list(CONTENIDOS_LANDING)}]
    for lvl in common.LEVELS:
        section = [_rel(common.DOCS_DIR / "content" / "levels" / lvl / "index.md")]
        for a in sorted(by_level[lvl], key=_sort_key):
            section.append(_item_entry(a))
        contenidos.append({common.LEVEL_LABELS[lvl]: section})

    nav = list(SCAFFOLD_TOP)
    nav.append({"Contenidos": contenidos})
    nav.extend(SCAFFOLD_BOTTOM)
    return nav


def render(nav: list) -> str:
    """Return the full text that should follow the sentinel (sentinel + nav YAML)."""
    body = yaml.safe_dump(
        {"nav": nav}, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    return f"{SENTINEL}\n{body}"


def generate(check: bool = False) -> list[common.Change]:
    text = MKDOCS_YML.read_text(encoding="utf-8")
    idx = text.find(SENTINEL)
    if idx == -1:
        sys.exit(
            f"Sentinel not found in {MKDOCS_YML.name}. Add this line where the nav "
            f"should start:\n    {SENTINEL}"
        )
    head = text[:idx]  # everything before the sentinel (hand-maintained)
    if not head.endswith("\n"):
        head += "\n"
    new_text = head + render(build_nav())
    return [common.write_if_changed(MKDOCS_YML, new_text, check)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gennav.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Dry-run: do not write; exit non-zero if the nav is stale (CI mode).",
    )
    args = parser.parse_args(argv)

    changes = generate(check=args.check)
    pending = common.print_plan(changes, check=args.check, title="gennav: mkdocs.yml nav from meta.yaml")
    if args.check and pending:
        print("\nnav out of date. Run: python tools/gennav.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
