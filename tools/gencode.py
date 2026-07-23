#!/usr/bin/env python3
"""Generate the ``clean`` and ``contest`` code styles from the hand-written ``full``.

Model (see ``.devs/v2-design.md`` §4-§5)
========================================

Every algorithm ships exactly one *hand-written* source per language: the
``full`` style (fully commented, with a header doc-string). The other two styles
are **derived** from it, so authors never keep three copies in sync:

    full  --(strip comments/docstrings)-->  clean  --(shorten locals)-->  contest

* ``full``    — hand-written, always. Never touched by this script.
* ``clean``   — ``full`` with every comment and doc-string removed, blank lines
                and trailing whitespace dropped. Safe for both languages.
* ``contest`` — a compact form derived from ``clean``:
    - **Python**: local variables, function arguments and helper (nested) function
      names are renamed to short names (``a``, ``b``, ``c`` …) *consistently*,
      while the public API (the class/``type`` and functions named in
      ``meta.yaml``'s ``signature``), imported names, attribute names, builtins
      and keywords are preserved. Type annotations are also stripped (they are
      kept in ``full``/``clean``). Rewritten with :func:`ast.unparse` and
      re-parsed to guarantee it is still valid Python.
    - **C++**: identifiers are **NOT** renamed. Safe renaming of C++ locals needs
      a real C++ parser (macros, ADL, overloading, templates, references escaping
      through pointers, …), which is out of scope for a stdlib tool and would
      risk silently miscompiling snippets. So the C++ ``contest`` file is simply
      the ``clean`` file with blank lines removed and trailing whitespace
      stripped — a compact but guaranteed-correct form. Authors who want tighter
      C++ ``contest`` code write it by hand (the documented escape hatch).

Ownership / safety rules
========================

* **Existing files are never overwritten by default.** A normal run only creates
  the files that are *missing*; anything already on disk is left untouched, so an
  author can keep a customised ``clean``/``contest`` version. Pass ``--force`` to
  regenerate existing files too.
* Generated files start with the ``AUTO-GENERATED`` marker header
  (:func:`common.autogen_header`).
* A file carrying a ``no-generate`` directive (a hidden comment ``//! no-generate``
  / ``#! no-generate``) is **never** overwritten, even with ``--force``.
* Per-file directives in the hand-written ``full`` source tune what is derived:
  ``no-clean`` suppresses its ``clean`` style, ``no-contest`` suppresses its
  ``contest`` style. (When ``clean`` is suppressed, ``contest`` is still derived
  in-memory from ``full``.)
* All writes go through :func:`common.write_if_changed`, so ``--check`` is a pure
  dry-run and every file is reported as create / modify (with --force) / kept /
  protected / skipped / unchanged.

Usage
=====

    python tools/gencode.py                 # create only the MISSING clean/contest files
    python tools/gencode.py --force         # also regenerate existing ones (respects no-generate)
    python tools/gencode.py --check         # CI: dry-run, non-zero exit if a file is missing
    python tools/gencode.py --check --force  # dry-run showing which existing files would change
    python tools/gencode.py --algo fenwick-tree
    python tools/gencode.py -v              # verbose (also list unchanged/kept/skipped files)
"""
from __future__ import annotations

import argparse
import ast
import builtins as _builtins
import io
import keyword
import symtable
import sys
import tokenize
from pathlib import Path

# Make ``import common`` work no matter the current working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402


# --------------------------------------------------------------------------- #
# full -> clean  (comment / doc-string stripping)
# --------------------------------------------------------------------------- #
def _normalize_lines(text: str) -> str:
    """Strip trailing whitespace on every line and drop blank/whitespace-only lines."""
    out = [line.rstrip() for line in text.splitlines()]
    out = [line for line in out if line != ""]
    return "\n".join(out) + "\n" if out else ""


def strip_cpp_comments(src: str) -> str:
    """Remove ``//`` and ``/* */`` comments with a state machine.

    String (``"..."``) and char (``'...'``) literals are respected (including
    backslash escapes), so a ``//`` or ``/*`` inside a literal is never treated
    as a comment and the literal is copied through verbatim. Preprocessor lines
    (``#include`` …) are ordinary text to this pass and are preserved; only a
    trailing comment on such a line is removed.

    Note: C++ raw string literals ``R"(...)"`` are NOT specially handled. None of
    the current sources use them; add handling here if that changes.
    """
    out: list[str] = []
    i, n = 0, len(src)
    state = "normal"  # normal | line | block | string | char
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if state == "normal":
            if c == "/" and nxt == "/":
                state = "line"; i += 2; continue
            if c == "/" and nxt == "*":
                state = "block"; i += 2; continue
            if c == '"':
                state = "string"; out.append(c); i += 1; continue
            if c == "'":
                state = "char"; out.append(c); i += 1; continue
            out.append(c); i += 1; continue
        if state == "line":
            if c == "\n":
                state = "normal"; out.append(c)
            i += 1; continue
        if state == "block":
            if c == "*" and nxt == "/":
                state = "normal"; i += 2; continue
            if c == "\n":
                out.append("\n")  # keep line breaks so layout survives
            i += 1; continue
        # inside a string or char literal: copy verbatim, honour escapes
        out.append(c)
        if c == "\\":
            if nxt:
                out.append(nxt); i += 2; continue
            i += 1; continue
        if (state == "string" and c == '"') or (state == "char" and c == "'"):
            state = "normal"
        i += 1
    return "".join(out)


def clean_cpp(full_src: str) -> str:
    """C++ ``full`` -> ``clean``: strip comments, blank lines and trailing whitespace."""
    return _normalize_lines(strip_cpp_comments(full_src))


def clean_python(full_src: str) -> str:
    """Python ``full`` -> ``clean``: drop comments (tokenize) and doc-strings (ast).

    Multi-line (triple-quoted) string literals that are *not* doc-strings are
    left byte-for-byte intact, so blank-line collapsing and trailing-space
    stripping can never corrupt string contents.
    """
    tree = ast.parse(full_src)

    # Line numbers occupied by module/class/function doc-strings (removed).
    docstring_lines: set[int] = set()

    def mark_docstring(node: ast.AST) -> None:
        body = getattr(node, "body", None)
        if not body or len(body) <= 1:
            return  # keep a lone doc-string body, else the block would be empty
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            for ln in range(first.lineno, (first.end_lineno or first.lineno) + 1):
                docstring_lines.add(ln)

    mark_docstring(tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            mark_docstring(node)

    # Where each line's comment starts, and which lines belong to a multi-line
    # string literal (leave those verbatim).
    comment_col: dict[int, int] = {}
    protected_lines: set[int] = set()
    for tok in tokenize.generate_tokens(io.StringIO(full_src).readline):
        if tok.type == tokenize.COMMENT:
            row, col = tok.start
            comment_col[row] = min(col, comment_col.get(row, col))
        elif tok.type == tokenize.STRING and tok.start[0] != tok.end[0]:
            for ln in range(tok.start[0], tok.end[0] + 1):
                protected_lines.add(ln)

    result: list[str] = []
    for idx, line in enumerate(full_src.splitlines(), start=1):
        if idx in docstring_lines:
            continue
        if idx in protected_lines:
            result.append(line)  # inside a multi-line string: do not touch
            continue
        if idx in comment_col:
            line = line[: comment_col[idx]]
        line = line.rstrip()
        if line == "":
            continue
        result.append(line)
    return "\n".join(result) + "\n" if result else ""


# --------------------------------------------------------------------------- #
# clean -> contest
# --------------------------------------------------------------------------- #
def _signature_api_names(meta: dict) -> set[str]:
    """Public identifiers declared in ``meta.yaml``'s ``signature`` (never renamed).

    Handles both signature shapes seen in the repo:
      * structured:  ``type: FenwickTree`` + ``constructor``/``methods`` strings.
      * free-form:   ``es``/``en`` strings like ``"tsp(dist) -> ..."``.
    """
    import re

    names: set[str] = set()
    sig = meta.get("signature")
    if not isinstance(sig, dict):
        return names

    def first_callable(text: str) -> None:
        m = re.search(r"([A-Za-z_]\w*)\s*\(", text)
        if m:
            names.add(m.group(1))

    typ = sig.get("type")
    if isinstance(typ, str) and typ.strip():
        names.add(typ.strip())
    ctor = sig.get("constructor")
    if isinstance(ctor, str):
        first_callable(ctor)
    for method in sig.get("methods", []) or []:
        if isinstance(method, str):
            first_callable(method)
    for key in ("es", "en"):
        val = sig.get(key)
        if isinstance(val, str):
            first_callable(val)
    return names


def _short_name_generator(avoid: set[str]):
    """Yield ``a, b, ... z, aa, ab, ...`` skipping any name in ``avoid``."""
    import itertools
    import string

    for size in itertools.count(1):
        for combo in itertools.product(string.ascii_lowercase, repeat=size):
            name = "".join(combo)
            if name not in avoid and not keyword.iskeyword(name):
                yield name


class _Renamer(ast.NodeTransformer):
    def __init__(self, mapping: dict[str, str]):
        self.mapping = mapping

    def visit_Name(self, node: ast.Name):
        if node.id in self.mapping:
            node.id = self.mapping[node.id]
        return node

    def visit_arg(self, node: ast.arg):
        if node.arg in self.mapping:
            node.arg = self.mapping[node.arg]
        return node

    def _rename_def(self, node):
        # Rename only nested/local helper functions (top-level names are in the
        # preserved module scope and never enter the mapping).
        if node.name in self.mapping:
            node.name = self.mapping[node.name]
        self.generic_visit(node)
        return node

    visit_FunctionDef = _rename_def
    visit_AsyncFunctionDef = _rename_def


class _AnnotationStripper(ast.NodeTransformer):
    """Remove Python type annotations (kept in full/clean, dropped for contest)."""

    @staticmethod
    def _strip_args(args: ast.arguments) -> None:
        for group in (getattr(args, "posonlyargs", []), args.args, args.kwonlyargs):
            for a in group or []:
                a.annotation = None
        if args.vararg:
            args.vararg.annotation = None
        if args.kwarg:
            args.kwarg.annotation = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        node.returns = None
        self._strip_args(node.args)
        self.generic_visit(node)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_AnnAssign(self, node: ast.AnnAssign):
        # `x: T = v`  ->  `x = v`  ;  a bare `x: T` declaration is dropped.
        if node.value is not None:
            return ast.copy_location(ast.Assign(targets=[node.target], value=node.value), node)
        return None


def contest_python(clean_src: str, api_names: set[str]) -> str:
    """Python ``clean`` -> ``contest``: rename function-locals to short names.

    Renames variables that are *local to a function scope* (params, assigned
    locals, and nested helper-function names). Preserves everything else:
    module-level names (the public API lives here), class members / attribute
    names, imported names, builtins, keywords, and the ``signature`` names.
    Falls back to the unchanged ``clean`` source if anything goes wrong.
    """
    try:
        tree = ast.parse(clean_src)
    except SyntaxError:
        return _normalize_lines(clean_src)

    # Every identifier already present anywhere in the module -> never reuse one
    # of these as a fresh short name (guarantees renaming can't capture a name).
    used: set[str] = set(dir(_builtins)) | set(keyword.kwlist) | set(keyword.softkwlist)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.arg):
            used.add(node.arg)
        elif isinstance(node, ast.Attribute):
            used.add(node.attr)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            used.add(node.name)
        elif isinstance(node, ast.alias):
            used.add((node.asname or node.name.split(".")[0]))
        elif isinstance(node, ast.keyword) and node.arg:
            used.add(node.arg)

    # Scope analysis: which names are function-locals, which are module/class
    # bound (kept), imported (kept), or declared global (kept).
    module_bound: set[str] = set()
    class_bound: set[str] = set()
    imported: set[str] = set()
    declared_global: set[str] = set()
    func_local: set[str] = set()

    def walk_scopes(scope):
        yield scope
        for child in scope.get_children():
            yield from walk_scopes(child)

    try:
        table = symtable.symtable(clean_src, "<contest>", "exec")
    except SyntaxError:
        return _normalize_lines(clean_src)

    for scope in walk_scopes(table):
        stype = scope.get_type()
        for sym in scope.get_symbols():
            name = sym.get_name()
            if sym.is_imported():
                imported.add(name)
            try:
                if sym.is_declared_global():
                    declared_global.add(name)
            except AttributeError:  # pragma: no cover
                pass
            if stype == "module":
                if sym.is_local():
                    module_bound.add(name)
            elif stype == "class":
                class_bound.add(name)
            else:  # function / lambda / comprehension scope
                if sym.is_local() and not sym.is_imported():
                    func_local.add(name)

    preserve = (
        module_bound
        | class_bound
        | imported
        | declared_global
        | api_names
        | {"self", "cls"}
        | set(dir(_builtins))
        | set(keyword.kwlist)
        | set(keyword.softkwlist)
    )
    renamable = sorted(
        n for n in func_local if n not in preserve and n.isidentifier()
    )

    gen = _short_name_generator(used)
    mapping = {name: next(gen) for name in renamable}

    if mapping:
        tree = _Renamer(mapping).visit(tree)

    # contest drops type annotations (they stay in full/clean).
    tree = _AnnotationStripper().visit(tree)
    ast.fix_missing_locations(tree)

    try:
        out = ast.unparse(tree)
    except Exception:  # pragma: no cover - unparse is very robust
        return _normalize_lines(clean_src)

    # Verify the generated source is still valid Python before handing it out.
    try:
        ast.parse(out)
    except SyntaxError:  # pragma: no cover - defensive
        return _normalize_lines(clean_src)

    return out.rstrip("\n") + "\n"


def contest_cpp(clean_src: str) -> str:
    """C++ ``clean`` -> ``contest``: no identifier renaming (see module docstring).

    Just re-applies the compact normalization (blank lines removed, trailing
    whitespace stripped). The result is guaranteed to compile identically to the
    ``clean`` file.
    """
    return _normalize_lines(clean_src)


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
_CLEANERS = {"cpp": clean_cpp, "py": clean_python}


def _strip_autogen_header(text: str, ext: str) -> str:
    """Drop the leading AUTO-GENERATED marker block from a generated file body.

    The header is written with the *hidden*-comment prefix (``//!`` / ``#!``), so
    only leading lines starting with that exact prefix are removed. This must NOT
    swallow real code that merely starts with ``#`` (e.g. a C++ ``#include``) or
    ``//`` — hence the prefix check rather than a generic comment check.
    """
    prefix = common.HIDDEN_PREFIX.get(ext)
    lines = text.splitlines(keepends=True)
    if not prefix or not lines or common.AUTOGEN_TOKEN not in lines[0]:
        return text
    i = 0
    while i < len(lines) and lines[i].lstrip().startswith(prefix):
        i += 1
    return "".join(lines[i:])


def _emit(path: Path, content: str, ext: str, check: bool, force: bool) -> common.Change:
    """Decide whether to write ``content`` to ``path`` and report the outcome.

    Policy (see the module docstring):
      * missing file            -> always created;
      * exists, identical       -> unchanged;
      * exists, has no-generate  -> protected (never overwritten, even with --force);
      * exists, differs, no force -> kept (NOT overwritten; --force to regenerate);
      * exists, differs, --force -> modified.
    """
    if not path.exists():
        return common.write_if_changed(path, content, check)  # create
    existing = path.read_text(encoding="utf-8")
    if "no-generate" in common.find_directives(existing, ext):
        return common.Change(path, "protected", detail="no-generate directive")
    if existing == content:
        return common.Change(path, "unchanged")
    if force:
        return common.write_if_changed(path, content, check)  # modify / would modify
    return common.Change(path, "keep", detail="exists & differs — use --force to regenerate")


def generate(check: bool = False, algo: str | None = None,
             force: bool = False) -> list[common.Change]:
    """Generate clean+contest files. Returns every :class:`common.Change`.

    By default *existing* files are never overwritten (so an author can keep a
    customised style): only missing files are created. Pass ``force=True`` to
    also regenerate existing files (except those carrying a ``no-generate``
    directive). Per-file ``no-clean`` / ``no-contest`` directives in the ``full``
    source suppress the corresponding derived style entirely.

    If ``check`` is true nothing is written (dry-run). If ``algo`` is given, only
    that algorithm id is processed.
    """
    changes: list[common.Change] = []

    for a in common.iter_algorithms(only=algo):
        if a.is_article:
            continue  # articles are prose with free-form examples, not a versioned snippet
        code_dir = a.code_dir
        if not code_dir.is_dir():
            continue
        for full_path in sorted(code_dir.glob("*.full.*")):
            parsed = common.parse_code_filename(full_path.name)
            if not parsed or parsed["style"] != "full":
                continue
            ext, base, version = parsed["ext"], parsed["base"], parsed["version"]
            if ext not in _CLEANERS:
                continue

            full_src = full_path.read_text(encoding="utf-8")
            directives = common.find_directives(full_src, ext)
            try:
                clean_body = _CLEANERS[ext](full_src)
            except Exception as exc:  # pragma: no cover - malformed source
                changes.append(
                    common.Change(full_path, "unchanged", detail=f"clean failed: {exc}")
                )
                continue

            clean_name = common.build_code_filename(base, version, "clean", ext)
            contest_name = common.build_code_filename(base, version, "contest", ext)
            clean_path = code_dir / clean_name
            contest_path = code_dir / contest_name

            # --- clean --------------------------------------------------------
            if "no-clean" in directives:
                changes.append(
                    common.Change(clean_path, "skip", detail="no-clean directive in full")
                )
            else:
                clean_content = common.autogen_header(ext, full_path.name) + clean_body
                changes.append(_emit(clean_path, clean_content, ext, check, force))

            # Feed the on-disk clean (respecting any author customisation) into
            # contest generation; fall back to the freshly-derived body if the
            # clean file isn't present (e.g. no-clean, or a check-mode dry run).
            if clean_path.exists():
                clean_source_for_contest = clean_path.read_text(encoding="utf-8")
            else:
                clean_source_for_contest = clean_body

            # --- contest ------------------------------------------------------
            if "no-contest" in directives:
                changes.append(
                    common.Change(contest_path, "skip", detail="no-contest directive in full")
                )
                continue

            body_in = _strip_autogen_header(clean_source_for_contest, ext)
            try:
                if ext == "py":
                    contest_body = contest_python(body_in, _signature_api_names(a.meta))
                else:
                    contest_body = contest_cpp(body_in)
            except Exception as exc:  # pragma: no cover
                changes.append(
                    common.Change(contest_path, "unchanged", detail=f"contest failed: {exc}")
                )
                continue

            contest_content = common.autogen_header(ext, clean_name) + contest_body
            changes.append(_emit(contest_path, contest_content, ext, check, force))

    return changes


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gencode.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Generate the 'clean' and 'contest' code styles from the hand-written\n"
            "'full' style, for every algorithm under docs/algorithms/**.\n\n"
            "Style chain:  full  ->  clean  ->  contest\n"
            "  full     hand-written (never modified by this tool)\n"
            "  clean    comments & doc-strings stripped, blank lines removed\n"
            "  contest  compact form; Python locals renamed to a,b,c,...\n"
            "           (C++ identifiers are NOT renamed -- see the file header).\n\n"
            "Files carrying the AUTO-GENERATED marker are owned by this tool and\n"
            "refreshed in place; any other file is treated as hand-written and is\n"
            "never overwritten."
        ),
        epilog=(
            "Examples:\n"
            "  python tools/gencode.py                 regenerate everything missing/auto\n"
            "  python tools/gencode.py --check         CI dry-run; exit 1 if anything stale\n"
            "  python tools/gencode.py --algo fenwick-tree\n"
            "  python tools/gencode.py -v              also list skipped hand-written files\n"
        ),
    )
    parser.add_argument(
        "--algo",
        metavar="ID",
        default=None,
        help="restrict generation to the algorithm with this meta.yaml 'id'.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="dry-run: write nothing, print the plan, exit non-zero if any file "
        "is missing (or, with --force, out of date). Used by CI.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="also regenerate files that already exist (default: only create "
        "missing ones). Files carrying a 'no-generate' directive are still kept.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="also report unchanged and skipped (hand-written) files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    changes = generate(check=args.check, algo=args.algo, force=args.force)

    title = "gencode (check)" if args.check else "gencode"
    pending = common.print_plan(changes, check=args.check, title=title)

    if args.verbose:
        unchanged = [c for c in changes if c.action == "unchanged"]
        for c in unchanged:
            detail = f"  ({c.detail})" if c.detail else ""
            print(f"    unchanged: {c.relpath}{detail}")

    if args.check and pending:
        print(
            f"\n{pending} file(s) are out of date. Run 'python tools/gencode.py' "
            "and commit the result."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
