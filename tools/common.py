"""Shared helpers for the tools/ scripts.

Every generation script reads the per-algorithm ``meta.yaml`` files under
``docs/algorithms/**`` and the code files under each ``code/`` directory,
following the conventions documented in ``.devs/v2-design.md``.

This module is the single contract the other scripts build on:

- Paths and constants (``DOCS_DIR``, ``ALGORITHMS_DIR``, ``LEVELS``, ``STYLES``,
  ``LANGUAGES``).
- ``iter_algorithms()`` to walk the algorithm folders.
- Code-file name parsing/building (``parse_code_filename`` / ``build_code_filename``).
- The ``AUTO-GENERATED`` marker helpers.
- ``Change`` + ``write_if_changed`` so every generator reports create/modify/
  unchanged consistently and supports a ``--check`` dry-run.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit(
        "Missing dependency 'pyyaml'. Install the tooling deps with:\n"
        "    pip install -r tools/requirements.txt"
    )

# --------------------------------------------------------------------------- #
# Paths and constants
# --------------------------------------------------------------------------- #
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ALGORITHMS_DIR = DOCS_DIR / "algorithms"
TECHNIQUES_DIR = DOCS_DIR / "techniques"
STRUCTURES_DIR = DOCS_DIR / "structures"

# All roots that hold content items (each item = a folder with a meta.yaml).
CONTENT_DIRS = [ALGORITHMS_DIR, TECHNIQUES_DIR, STRUCTURES_DIR]

# Difficulty levels, in order.
LEVELS = ["base", "beginner", "intermediate", "advanced", "expert"]

# Content types and their display labels (Spanish).
TYPES = ["technique", "algorithm", "structure"]
TYPE_LABELS = {
    "technique": "Técnica",
    "algorithm": "Algoritmo",
    "structure": "Estructura",
}

# Code styles, in generation order (each is derived from the previous one).
STYLES = ["full", "clean", "contest"]

# Supported languages: file extension -> metadata.
LANGUAGES = {
    "cpp": {"name": "C++", "line_comment": "//", "highlight": "cpp"},
    "py": {"name": "Python", "line_comment": "#", "highlight": "python"},
}

# Marker written into auto-generated code files (see gencode.py).
AUTOGEN_TOKEN = "AUTO-GENERATED"

# "Hidden" comment prefixes: comments that stay in the source file but are
# stripped from the rendered docs and the cheatsheet (see strip_hidden_comments).
# The AUTO-GENERATED header uses these, so it never shows to students.
HIDDEN_PREFIX = {"cpp": "//!", "py": "#!"}


def strip_hidden_comments(text: str, ext: str) -> str:
    """Remove 'hidden' comments from source text.

    Hidden comments are ``//!`` line comments and ``/*! ... */`` blocks in C++,
    and ``#!`` line comments in Python. They are used for maintainer notes and
    the AUTO-GENERATED marker, and must NOT appear in the docs or the cheatsheet.
    """
    trailing_nl = text.endswith("\n")
    out: list[str] = []
    in_block = False
    for line in text.splitlines():
        s = line.lstrip()
        if ext == "cpp":
            if in_block:
                if "*/" in line:
                    in_block = False
                continue
            if s.startswith("//!"):
                continue
            if s.startswith("/*!"):
                if "*/" not in s[3:]:
                    in_block = True
                continue
            out.append(line)
        else:  # python (and any '#'-comment language)
            if s.startswith("#!"):
                continue
            out.append(line)
    result = "\n".join(out)
    if trailing_nl and not result.endswith("\n"):
        result += "\n"
    return result


# Recognised "directives": tokens written inside a hidden comment (//! / #!)
# that tune code generation for a single file (see gencode.py):
#   no-clean     in a `full` file  -> do not generate its `clean` style
#   no-contest   in a `full` file  -> do not generate its `contest` style
#   no-generate  in ANY file       -> never overwrite this file (even with --force)
DIRECTIVES = {"no-clean", "no-contest", "no-generate"}


def find_directives(text: str, ext: str) -> set[str]:
    """Return the set of recognised :data:`DIRECTIVES` present in ``text``.

    A directive is any recognised token appearing inside a *hidden* comment
    (``//!`` in C++, ``#!`` in Python), e.g. ``//! no-clean`` or
    ``#! no-generate``. Several may share one comment line
    (``//! no-clean no-contest``). Non-hidden comments are ignored.
    """
    prefix = HIDDEN_PREFIX.get(ext)
    if not prefix:
        return set()
    found: set[str] = set()
    for line in text.splitlines():
        s = line.lstrip()
        if not s.startswith(prefix):
            continue
        for tok in s[len(prefix):].replace(",", " ").split():
            if tok in DIRECTIVES:
                found.add(tok)
    return found


# --------------------------------------------------------------------------- #
# Algorithm model
# --------------------------------------------------------------------------- #
@dataclass
class Algorithm:
    """One algorithm folder: its directory and parsed ``meta.yaml``."""

    directory: Path
    meta: dict

    @property
    def id(self) -> str:
        return self.meta.get("id", self.directory.name)

    @property
    def type(self) -> str:
        return self.meta.get("type", "algorithm")

    @property
    def format(self) -> str:
        """'snippet' (default): one canonical implementation, versioned + tested.
        'article': prose with free-form examples; skipped by codegen/tests/cheatsheet."""
        return self.meta.get("format", "snippet")

    @property
    def is_article(self) -> bool:
        return self.format == "article"

    @property
    def is_wip(self) -> bool:
        return bool(self.meta.get("wip", False))

    @property
    def code_dir(self) -> Path:
        return self.directory / "code"

    @property
    def test_dir(self) -> Path:
        return self.directory / "test"

    @property
    def meta_path(self) -> Path:
        return self.directory / "meta.yaml"

    @property
    def current_version(self) -> str:
        return self.meta.get("current_version", "v1")

    def name(self, lang: str = "es") -> str:
        name = self.meta.get("name", {})
        if isinstance(name, dict):
            return name.get(lang) or name.get("es") or name.get("en") or self.id
        return str(name)

    def languages_present(self) -> list[str]:
        """Extensions (cpp/py) that have at least a ``full`` file for the current version."""
        found = []
        for ext in LANGUAGES:
            base = self.id.replace("-", "_")
            # accept any base name, just check the version/style/ext suffix
            for path in sorted(self.code_dir.glob(f"*.{self.current_version}.full.{ext}")):
                found.append(ext)
                break
        return found


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def iter_algorithms(only: str | None = None) -> list[Algorithm]:
    """Return every algorithm under ``docs/algorithms/**`` sorted by id.

    If ``only`` is given, restrict to the algorithm whose id matches it.
    """
    algos: list[Algorithm] = []
    seen: set[Path] = set()
    for root in CONTENT_DIRS:
        if not root.is_dir():
            continue
        for meta_path in sorted(root.glob("**/meta.yaml")):
            if meta_path in seen:
                continue
            seen.add(meta_path)
            meta = load_yaml(meta_path)
            algo = Algorithm(directory=meta_path.parent, meta=meta)
            if only is None or algo.id == only:
                algos.append(algo)
    algos.sort(key=lambda a: (LEVELS.index(a.meta["level"]) if a.meta.get("level") in LEVELS else 99, a.id))
    return algos


# --------------------------------------------------------------------------- #
# Code file naming: <base>.v<N>.<style>.<ext>
# --------------------------------------------------------------------------- #
def parse_code_filename(filename: str) -> dict | None:
    """Parse ``fenwick.v1.full.cpp`` -> {base, version, style, ext} or None."""
    parts = filename.split(".")
    if len(parts) < 4:
        return None
    ext, style, version = parts[-1], parts[-2], parts[-3]
    base = ".".join(parts[:-3])
    if ext not in LANGUAGES or style not in STYLES or not version.startswith("v"):
        return None
    return {"base": base, "version": version, "style": style, "ext": ext}


def build_code_filename(base: str, version: str, style: str, ext: str) -> str:
    return f"{base}.{version}.{style}.{ext}"


# --------------------------------------------------------------------------- #
# AUTO-GENERATED marker
# --------------------------------------------------------------------------- #
def autogen_header(ext: str, source_filename: str) -> str:
    """Return the marker comment block placed at the top of a generated file.

    Uses the 'hidden' comment prefix (//! / #!) so it never shows in the docs
    or the cheatsheet, while still marking the file as auto-generated.
    """
    c = HIDDEN_PREFIX.get(ext, LANGUAGES[ext]["line_comment"])
    return (
        f"{c} {AUTOGEN_TOKEN} from {source_filename} — do not edit.\n"
        f"{c} To override, replace this file with a hand-written version "
        f"(remove this marker).\n"
    )


def is_autogenerated(path: Path) -> bool:
    """True if the file exists and carries the AUTO-GENERATED marker."""
    if not path.exists():
        return False
    try:
        head = path.read_text(encoding="utf-8")[:400]
    except OSError:
        return False
    return AUTOGEN_TOKEN in head


# --------------------------------------------------------------------------- #
# Change tracking (shared by every generator + the gen.py orchestrator)
# --------------------------------------------------------------------------- #
@dataclass
class Change:
    """A single filesystem change a generator would (or would not) make.

    Actions:
      * ``create``    — file is missing; it will/would be written.  (pending)
      * ``modify``    — file exists and differs; it will/would be overwritten. (pending)
      * ``keep``      — file exists and differs but is NOT overwritten (no --force). (info)
      * ``protected`` — file exists and carries a ``no-generate`` directive; never
                        overwritten, even with --force. (info)
      * ``skip``      — nothing generated for it (e.g. a ``no-clean`` directive). (info)
      * ``unchanged`` — file exists and is already identical. (quiet)
    """

    path: Path
    action: str
    detail: str = ""

    @property
    def relpath(self) -> str:
        try:
            return str(self.path.relative_to(REPO_ROOT))
        except ValueError:
            return str(self.path)


def write_if_changed(path: Path, content: str, check: bool) -> Change:
    """Write ``content`` to ``path`` unless unchanged. In ``check`` mode, never write.

    Returns a :class:`Change` describing what happened (or would happen).
    """
    existed = path.exists()
    old = path.read_text(encoding="utf-8") if existed else None
    if old == content:
        return Change(path, "unchanged")
    action = "modify" if existed else "create"
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return Change(path, action)


_PENDING_ACTIONS = ("create", "modify")
_INFO_ACTIONS = ("keep", "protected", "skip")
_INFO_VERB = {"keep": "kept", "protected": "protected", "skip": "skipped"}


def print_plan(changes: list[Change], *, check: bool, title: str = "") -> int:
    """Print a human-readable plan/summary. Returns the count of *pending* changes.

    Pending = files that will/would actually be written (``create``/``modify``).
    Informational rows (``keep``/``protected``/``skip``) are printed too but not
    counted, so a run that only reports them still succeeds. ``unchanged`` rows
    stay quiet.
    """
    if title:
        print(f"\n=== {title} ===")
    pending = [c for c in changes if c.action in _PENDING_ACTIONS]
    info = [c for c in changes if c.action in _INFO_ACTIONS]
    for c in pending:
        verb = "would create" if check and c.action == "create" else \
               "would modify" if check and c.action == "modify" else \
               c.action
        extra = f"  ({c.detail})" if c.detail else ""
        print(f"  {verb:>13}: {c.relpath}{extra}")
    for c in info:
        extra = f"  ({c.detail})" if c.detail else ""
        print(f"  {_INFO_VERB[c.action]:>13}: {c.relpath}{extra}")
    if not pending and not info:
        print("  everything up to date")
    return len(pending)
