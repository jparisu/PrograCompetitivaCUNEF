"""mkdocs-macros module: render the repetitive parts of an item page from its
``<id>.meta.yaml`` + code files, so the prose page never hand-duplicates that data.

Enabled per page (opt-in) with front-matter ``render_macros: true`` — see
``mkdocs.yml`` (``macros`` plugin, ``render_by_default: false``). Pages that do
not opt in are passed through verbatim, so Material/attr-list syntax like
``{ .class }`` or ``{#anchor}`` on other pages is never touched by Jinja.

Macros (call them from an item's ``index.md``):

    {{ metadata() }}            -> the "Metadatos" admonition (type · level ·
                                   difficulty · complexity), from meta.yaml.
    {{ metadata(extra="…") }}   -> same, with an extra ` · **…**` fragment appended.
    {{ code_tabs() }}           -> the C++/Python × full/clean/contest tabs, with
                                   the real (comment-stripped) code embedded from
                                   the item's code/ directory for its current
                                   version. Only the styles/languages present are
                                   emitted.

The code is embedded directly (not via a ``--8<--`` include) so it does not
depend on the build-hook ordering, and hidden ``//!`` / ``#!`` comments are
stripped exactly as the hook does (via ``common.strip_hidden_comments``).
"""
import os
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT / "tools"))
import common  # noqa: E402


def _item_dir(page) -> Path:
    """docs/content/<topic>/<id>/ for the page being rendered."""
    return Path(page.file.abs_src_path).parent


_INDEX = None


def _index_map() -> dict:
    """id -> {name, dir, wip} for every content item (cached). Used to turn a
    prerequisite id into a link to its page (even when that page is WIP)."""
    global _INDEX
    if _INDEX is None:
        _INDEX = {}
        for a in common.iter_algorithms():
            _INDEX[a.id] = {"name": a.name("es"), "dir": a.directory, "wip": a.is_wip}
    return _INDEX


def _link_list(ids, current_dir: Path) -> str:
    """Render `ids` (element ids) as a comma-separated list of links relative to
    `current_dir`. WIP targets are still linked (their stub exists) and marked
    with 🏗️. An id with no matching element is shown as plain code."""
    idx = _index_map()
    out = []
    for pid in ids or []:
        info = idx.get(pid)
        if not info:
            out.append(f"`{pid}`")           # id with no matching element
            continue
        rel = os.path.relpath(info["dir"] / "index.md", current_dir)
        label = info["name"] + (" 🏗️" if info["wip"] else "")
        out.append(f"[{label}]({rel})")
    return ", ".join(out)


def _load_meta(page) -> dict:
    # Each item folder has exactly one "<id>.meta.yaml".
    metas = sorted(_item_dir(page).glob("*.meta.yaml"))
    return common.load_yaml(metas[0]) if metas else {}


def _complexity(meta: dict) -> str:
    stats = meta.get("stats") or {}
    comp = stats.get("complexity") if isinstance(stats, dict) else None
    if not isinstance(comp, dict) or not comp:
        return ""
    if comp.get("time"):
        return str(comp["time"])
    return str(next(iter(comp.values()), "") or "")


def define_env(env):
    @env.macro
    def metadata(complexity: str = None, extra: str = "") -> str:
        """The "Metadatos" admonition. type/level/difficulty are derived from
        meta.yaml; `complexity` overrides the derived value (use it when the
        headline complexity needs nuance, e.g. "O(log n) por operación"), and
        `extra` appends a trailing ` · **…**` fragment (e.g. a technique note)."""
        meta = _load_meta(env.page)
        type_label = common.TYPE_LABELS.get(meta.get("type"), meta.get("type", ""))
        level_label = common.LEVEL_LABELS.get(meta.get("level"), meta.get("level", ""))
        parts = [f"**Tipo:** {type_label}", f"**Nivel:** {level_label}"]
        if meta.get("difficulty") is not None:
            parts.append(f"**Dificultad:** {meta['difficulty']}")
        comp = complexity if complexity is not None else _complexity(meta)
        if comp:
            parts.append(f"**Complejidad:** {comp}")
        line = " · ".join(parts)
        if extra:
            line += " · " + extra
        block = '!!! info "Metadatos"\n    ' + line
        here = _item_dir(env.page)
        reqs = _link_list(meta.get("prerequisites"), here)
        if reqs:
            block += "\n\n    **Requisitos:** " + reqs
        rels = _link_list(meta.get("related"), here)
        if rels:
            block += "\n\n    **Relacionado:** " + rels
        return block

    @env.macro
    def code_tabs(version: str = "") -> str:
        meta = _load_meta(env.page)
        code_dir = _item_dir(env.page) / "code"
        if not code_dir.is_dir():
            return ""
        version = version or meta.get("current_version", "v1")

        # Discover which (lang, style) files exist for this version.
        present: dict[str, list[str]] = {}
        for f in sorted(code_dir.iterdir()):
            info = common.parse_code_filename(f.name)
            if not info or info["version"] != version:
                continue
            present.setdefault(info["ext"], []).append(info["style"])

        lines: list[str] = []
        for ext, meta_lang in common.LANGUAGES.items():  # cpp, then py (dict order)
            styles = [s for s in common.STYLES if s in present.get(ext, [])]
            if not styles:
                continue
            lines.append(f'=== "{meta_lang["name"]}"')
            lines.append("")
            for style in styles:
                matches = list(code_dir.glob(f"*.{version}.{style}.{ext}"))
                if not matches:
                    continue
                body = common.strip_hidden_comments(
                    matches[0].read_text(encoding="utf-8"), ext
                ).rstrip("\n")
                lines.append(f'    === "{style}"')
                lines.append("")
                lines.append(f'        ```{meta_lang["highlight"]}')
                for cl in body.split("\n"):
                    lines.append(("        " + cl) if cl else "")
                lines.append("        ```")
                lines.append("")
        return "\n".join(lines).rstrip("\n")
