#!/usr/bin/env python3
"""Run the generated fixtures against every code variant.

For each algorithm it finds the test cases (``test/cases/NN.in`` + ``NN.out``,
produced by ``gentests.py``) and runs them against every
``(language x version x style)`` code file:

- If the algorithm ships a driver (``test/driver.<ext>``), the code file is
  compiled/loaded THROUGH the driver: the driver ``#include "impl.cpp"`` (C++)
  or ``import impl`` (Python), and this runner copies the chosen variant to
  ``impl.<ext>`` in a temp dir. This is how library-style snippets (a struct or
  a function, with no ``main``) get exercised.
- Otherwise the code file is treated as a self-contained program and run
  directly (e.g. the ``loops`` example, which reads stdin and prints).

Each case's ``.in`` is fed on stdin; stdout is compared (whitespace-normalised)
against the expected ``.out``.

Examples
--------
    python tools/runtests.py                     # everything
    python tools/runtests.py --algo fenwick-tree
    python tools/runtests.py --lang py --style contest -v
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

PY = sys.executable


def normalize(text: str) -> str:
    """Trim trailing spaces per line and surrounding blank lines."""
    return "\n".join(line.rstrip() for line in text.strip("\n").splitlines()).strip()


def versions_for(algo: common.Algorithm) -> list[str]:
    versions = set()
    for f in algo.code_dir.glob("*.full.*"):
        info = common.parse_code_filename(f.name)
        if info:
            versions.add(info["version"])
    return sorted(versions)


def code_file(algo: common.Algorithm, version: str, style: str, ext: str) -> Path | None:
    for f in sorted(algo.code_dir.glob(f"*.{version}.{style}.{ext}")):
        return f
    return None


def load_cases(algo: common.Algorithm) -> list[tuple[Path, Path]]:
    cdir = algo.test_dir / "cases"
    cases = []
    if cdir.is_dir():
        for inp in sorted(cdir.glob("*.in")):
            out = inp.with_suffix(".out")
            if out.exists():
                cases.append((inp, out))
    return cases


def run_variant(algo, version, ext, style, cases, timeout, keep, have_gxx):
    """Build + run one variant. Returns (status, detail) with status in
    PASS / FAIL / SKIP."""
    code = code_file(algo, version, style, ext)
    if not code:
        return ("SKIP", "no file")
    if ext == "cpp" and not have_gxx:
        return ("SKIP", "g++ not found")

    driver = algo.test_dir / f"driver.{ext}"
    tmp = Path(tempfile.mkdtemp(prefix="rt_"))
    try:
        if ext == "cpp":
            if driver.exists():
                shutil.copy(code, tmp / "impl.cpp")
                shutil.copy(driver, tmp / "main.cpp")
            else:
                shutil.copy(code, tmp / "main.cpp")
            exe = tmp / "prog"
            cp = subprocess.run(
                ["g++", "-O2", "-std=c++17", str(tmp / "main.cpp"), "-o", str(exe)],
                capture_output=True, text=True,
            )
            if cp.returncode != 0:
                tail = cp.stderr.strip().splitlines()[-1] if cp.stderr.strip() else "compile error"
                return ("FAIL", f"compile error: {tail}")
            cmd = [str(exe)]
        else:  # py
            if driver.exists():
                shutil.copy(code, tmp / "impl.py")
                shutil.copy(driver, tmp / "main.py")
            else:
                shutil.copy(code, tmp / "main.py")
            cmd = [PY, str(tmp / "main.py")]

        for inp, out in cases:
            try:
                with open(inp) as fh:
                    rp = subprocess.run(cmd, stdin=fh, capture_output=True,
                                        text=True, timeout=timeout, cwd=str(tmp))
            except subprocess.TimeoutExpired:
                return ("FAIL", f"timeout on {inp.name}")
            got, exp = normalize(rp.stdout), normalize(out.read_text())
            if got != exp:
                extra = f" | stderr: {rp.stderr.strip()[:120]}" if rp.stderr.strip() else ""
                return ("FAIL", f"{inp.name}: expected {exp!r}, got {got!r}{extra}")
        return ("PASS", f"{len(cases)} case(s)")
    finally:
        if not keep:
            shutil.rmtree(tmp, ignore_errors=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="runtests.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--algo", metavar="ID", help="restrict to a single algorithm id.")
    parser.add_argument("--lang", choices=["cpp", "py"], help="restrict to one language.")
    parser.add_argument("--style", choices=common.STYLES, help="restrict to one code style.")
    parser.add_argument("--timeout", type=float, default=15.0, help="per-case timeout in seconds (default 15).")
    parser.add_argument("--keep", action="store_true", help="keep the temp build dirs (for debugging).")
    parser.add_argument("-v", "--verbose", action="store_true", help="print each passing variant too.")
    args = parser.parse_args(argv)

    have_gxx = shutil.which("g++") is not None
    if not have_gxx:
        print("warning: g++ not found — C++ variants will be skipped.\n")

    exts = [args.lang] if args.lang else list(common.LANGUAGES)
    styles = [args.style] if args.style else list(common.STYLES)

    total = passed = failed = skipped = 0
    algos = common.iter_algorithms(only=args.algo)
    if not algos:
        print(f"No algorithm matched {args.algo!r}." if args.algo else "No algorithms found.")
        return 1

    for algo in algos:
        if algo.is_article:
            continue  # articles have no tested implementation
        cases = load_cases(algo)
        print(f"\n=== {algo.id} ===")
        if not cases:
            print("  no test cases (add examples to meta.yaml, then run gentests.py) — skipped")
            continue
        for version in versions_for(algo):
            for ext in exts:
                # only if a full file exists for this ext/version
                if not code_file(algo, version, "full", ext):
                    continue
                for style in styles:
                    status, detail = run_variant(algo, version, ext, style, cases,
                                                 args.timeout, args.keep, have_gxx)
                    total += 1
                    label = f"{version} {common.LANGUAGES[ext]['name']:6} {style:7}"
                    if status == "PASS":
                        passed += 1
                        if args.verbose:
                            print(f"  PASS  {label}  ({detail})")
                    elif status == "SKIP":
                        skipped += 1
                        if args.verbose:
                            print(f"  skip  {label}  ({detail})")
                    else:
                        failed += 1
                        print(f"  FAIL  {label}  {detail}")

    print(f"\n{passed} passed, {failed} failed, {skipped} skipped "
          f"({total} variants across {len(algos)} algorithm(s)).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
