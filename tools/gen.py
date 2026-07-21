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
    code      -> tools/gencode.py     (clean/contest styles from full)
    tests     -> tools/gentests.py    (test/cases/*.in|*.out from meta examples)
    overview  -> tools/genoverview.py (docs/assets/data/algorithms.json)

Note: the Kattis scraper (tools/scrape_kattis.py) and the cheatsheet builder
(tools/cheatsheet.py) are NOT part of this orchestrator — the first needs network
access and the second needs an explicit config; run them on their own.
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
}


def _load(module_name: str):
    return __import__(module_name)


def _run_step(module_name: str, takes_algo: bool, check: bool, algo: str | None):
    module = _load(module_name)
    if not hasattr(module, "generate"):
        raise SystemExit(f"tools/{module_name}.py does not expose generate(); cannot orchestrate it.")
    if takes_algo:
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
        changes = _run_step(module_name, takes_algo, check, args.algo)
        total_pending += common.print_plan(changes, check=check, title=title)

    print()
    if check and total_pending:
        print(f"{total_pending} file(s) out of date. Run: python tools/gen.py generate")
        return 1
    if check:
        print("All derived files are up to date.")
    else:
        print(f"Done ({total_pending} file(s) written).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
