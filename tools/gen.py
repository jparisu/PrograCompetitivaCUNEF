#!/usr/bin/env python3
"""Run every autogeneration step in one place.

The individual generators (code styles, test fixtures, overview data) each read
the per-algorithm ``meta.yaml`` and know how to (re)build their derived files.
This orchestrator simply runs them together, in two modes:

    status     dry-run: show which files WOULD be created or modified, and exit
               with a non-zero code if anything is out of date (use this in CI).
    generate   actually create/modify the derived files.

Examples
--------
    python tools/gen.py status
    python tools/gen.py generate
    python tools/gen.py generate --only code,tests
    python tools/gen.py generate --only code --algo fenwick-tree

Steps
-----
    code       -> tools/gencode.py     (clean/contest styles from full)
    tests      -> tools/gentests.py    (test/cases/*.in|*.out from meta examples)
    overview   -> tools/genoverview.py (docs/assets/data/algorithms.json)
    taxonomy   -> tools/gentaxonomy.py (docs/assets/js/taxonomy.js from common.py)
    nav        -> tools/gennav.py      (the mkdocs.yml nav, grouped by level)

The dependency graph and the type/level matrix are now rendered client-side from
algorithms.json (docs/assets/js/graph.js and matrix.js), so there is no graph
generation step here.

Note: the cheatsheet (tools/cheatsheet.py) and the Kattis scraper
(tools/scrape_kattis.py) are NOT part of this orchestrator. The cheatsheet needs
LaTeX and is rebuilt by its own workflow (.github/workflows/cheatsheet.yml) so
ordinary content PRs don't churn docs/cheatsheet/cheatsheet.*; the scraper needs
network access. Run either on its own when needed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

# name -> (human title, module name, takes_algo)
STEPS = {
    "code": ("Code styles (clean / contest)", "gencode", True),
    "tests": ("Test fixtures (cases/*.in|*.out)", "gentests", True),
    "overview": ("Overview data (algorithms.json)", "genoverview", False),
    "taxonomy": ("Front-end taxonomy (assets/js/taxonomy.js)", "gentaxonomy", False),
    "nav": ("Site navigation (mkdocs.yml nav)", "gennav", False),
}


def _load(module_name: str):
    return __import__(module_name)


def validate() -> list[str]:
    """Return a list of human-readable violations of the content contract.

    A non-WIP ``snippet`` element (the default format) is the site's canonical
    "one implementation" page: it MUST ship a ``full`` code file and at least one
    ``examples`` entry (so it can be generated, tested, and put on the cheatsheet).
    ``article`` elements (free-form prose) and ``wip`` placeholders are exempt.
    """
    issues: list[str] = []
    for a in common.iter_algorithms():
        rel = a.meta_path.relative_to(common.REPO_ROOT)
        # Every item (WIP or not) must declare a known topic — a typo silently
        # drops it from the Temas view and breaks its topic-icon link.
        topic = a.meta.get("topic")
        if topic not in common.TOPICS:
            issues.append(
                f"{a.id}: unknown topic {topic!r} in {rel}. "
                f"Use one of: {', '.join(common.TOPIC_IDS)} (defined in tools/common.py)."
            )
        if a.is_article or a.is_wip:
            continue
        has_code = a.code_dir.is_dir() and any(a.code_dir.glob("*.full.*"))
        examples = a.meta.get("examples")
        has_examples = isinstance(examples, list) and any(
            isinstance(e, dict) for e in examples
        )
        if not has_code:
            issues.append(
                f"{a.id}: snippet element has no '*.full.*' code file "
                f"({a.code_dir.relative_to(common.REPO_ROOT)}/). "
                f"Add an implementation, or set 'format: article' / 'wip: true' in {rel}."
            )
        if not has_examples:
            issues.append(
                f"{a.id}: snippet element has no 'examples:' in {rel}. "
                f"Add at least one example, or set 'format: article' / 'wip: true'."
            )
    return issues


def _run_step(module_name: str, takes_algo: bool, check: bool, algo: str | None,
              force: bool = False):
    module = _load(module_name)
    if not hasattr(module, "generate"):
        raise SystemExit(f"tools/{module_name}.py does not expose generate(); cannot orchestrate it.")
    if takes_algo:
        # Only gencode understands --force (existing code files are the ones an
        # author may customise); other derived artifacts always refresh.
        if module_name == "gencode":
            return module.generate(check=check, algo=algo, force=force)
        return module.generate(check=check, algo=algo)
    return module.generate(check=check)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gen.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mode",
        choices=["status", "generate"],
        help="'status' = dry-run (non-zero exit if stale); 'generate' = write files.",
    )
    parser.add_argument(
        "--only",
        metavar="STEPS",
        help="comma-separated subset of steps to run: " + ", ".join(STEPS) + " (default: all).",
    )
    parser.add_argument(
        "--algo",
        metavar="ID",
        help="restrict code/tests to a single algorithm id (ignored by the overview step).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="regenerate existing code files too (default: only create missing "
        "ones, so hand-customised styles are preserved). Files with a "
        "'no-generate' directive are never overwritten. Affects the 'code' step.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="more detailed output.")
    args = parser.parse_args(argv)

    check = args.mode == "status"

    if args.only:
        selected = [s.strip() for s in args.only.split(",") if s.strip()]
        unknown = [s for s in selected if s not in STEPS]
        if unknown:
            parser.error(f"unknown step(s): {', '.join(unknown)}. Choose from: {', '.join(STEPS)}")
    else:
        selected = list(STEPS)

    total_pending = 0
    for name in selected:
        title, module_name, takes_algo = STEPS[name]
        changes = _run_step(module_name, takes_algo, check, args.algo, force=args.force)
        total_pending += common.print_plan(changes, check=check, title=title)

    # Content contract check (only meaningful for a full run, not a --only subset).
    issues = validate() if not args.only else []
    if issues:
        print("\n=== Content validation ===")
        for msg in issues:
            print(f"  ✗ {msg}")

    print()
    if issues:
        print(f"{len(issues)} content violation(s) — see above.")
    if check and (total_pending or issues):
        if total_pending:
            print(f"{total_pending} file(s) out of date. Run: python tools/gen.py generate")
        return 1
    if issues:
        return 1
    if check:
        print("All derived files are up to date.")
    else:
        print(f"Done ({total_pending} file(s) written).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
