"""MkDocs build hook.

Expands our ``--8<-- "path"`` code includes ourselves (instead of via
pymdownx.snippets) so we can strip 'hidden' comments (``//!`` / ``#!``) from the
embedded code — those must never appear in the rendered docs (they carry the
AUTO-GENERATED marker and maintainer notes). See tools/common.strip_hidden_comments.
"""
import logging
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_DOCS = _ROOT / "docs"
sys.path.insert(0, str(_ROOT / "tools"))
import common  # noqa: E402

log = logging.getLogger("mkdocs.hooks.snippets")

# Matches an include on its own line, capturing its indentation (our code fences
# are indented inside nested content tabs).
_INCLUDE_RE = re.compile(r'^(?P<indent>[ \t]*)--8<--\s+"(?P<path>[^"]+)"[ \t]*$', re.M)


def on_page_markdown(markdown, **kwargs):
    def repl(match):
        indent = match.group("indent")
        rel = match.group("path")
        path = _DOCS / rel
        if not path.is_file():
            log.warning("code include not found: %s", rel)
            return indent + "// missing snippet: " + rel
        ext = path.suffix.lstrip(".")
        body = common.strip_hidden_comments(path.read_text(encoding="utf-8"), ext)
        lines = body.split("\n")
        if lines and lines[-1] == "":
            lines.pop()  # drop the trailing empty line from the final newline
        # Re-indent to the include's column so the code stays inside the fence.
        return "\n".join((indent + ln) if ln else "" for ln in lines)

    return _INCLUDE_RE.sub(repl, markdown)
