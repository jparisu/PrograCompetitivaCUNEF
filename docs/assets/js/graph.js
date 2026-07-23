/*
 * graph.js — interactive dependency graph (Empezar aquí → Grafo).
 *
 * Builds a Mermaid flowchart from the shared catalogue data and re-renders it as
 * the user toggles type/level filters (Catalog.makeFilters). Nodes are ordered
 * left→right by difficulty (an invisible spine chains one node per level),
 * shaped by type (technique = hexagon, algorithm = rectangle, structure = oval)
 * and coloured by level. Clicking a node opens its page.
 *
 * Mermaid is loaded on demand (ESM) only on this page; if it can't load, a
 * grouped list of links is shown instead so navigation still works.
 */
(function () {
  "use strict";

  var LEVEL_STYLE = {
    base: "fill:#2e7d3226,stroke:#2e7d32,stroke-width:1.5px",
    beginner: "fill:#1e88e526,stroke:#1e88e5,stroke-width:1.5px",
    intermediate: "fill:#f9a82533,stroke:#f9a825,stroke-width:1.5px",
    advanced: "fill:#e5393526,stroke:#e53935,stroke-width:1.5px",
    expert: "fill:#6a1b9a26,stroke:#6a1b9a,stroke-width:1.5px",
  };
  var MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

  function nid(id) { return "n_" + String(id).replace(/[^a-zA-Z0-9]/g, "_"); }

  function nodeDecl(item) {
    var label = Catalog.name(item).replace(/"/g, "'");
    var ti = Catalog.topicInfo(item);
    if (ti) label = ti.icon + " " + label;   // topic icon before the name
    var n = nid(item.id);
    if (item.type === "technique") return n + '{{"' + label + '"}}';
    if (item.type === "structure") return n + '(["' + label + '"])';  // oval
    return n + '["' + label + '"]';                                    // rectangle
  }

  function buildDefinition(items) {
    var shown = new Set(items.map(function (i) { return i.id; }));
    var byLevel = {};
    items.forEach(function (it) { (byLevel[it.level] = byLevel[it.level] || []).push(it); });

    var lines = ["graph LR"];
    items.forEach(function (it) { lines.push("  " + nodeDecl(it)); });

    // real prerequisite edges (only between visible nodes)
    items.forEach(function (it) {
      (it.prereq || []).forEach(function (p) {
        if (shown.has(p)) lines.push("  " + nid(p) + " --> " + nid(it.id));
      });
    });

    // Force strict left→right columns by level. Connect ONE representative node
    // of the previous present level to EVERY node of the current level with an
    // invisible edge; in dagre (Mermaid's LR layout) this pins each node's rank
    // to its level, so even nodes without prerequisites land in the right column
    // and difficulty increases strictly to the right.
    var present = Catalog.LEVELS.filter(function (lv) { return byLevel[lv] && byLevel[lv].length; });
    for (var i = 1; i < present.length; i++) {
      var prevRep = nid(byLevel[present[i - 1]][0].id);
      byLevel[present[i]].forEach(function (it) {
        lines.push("  " + prevRep + " ~~~ " + nid(it.id));
      });
    }

    // colour by level; a "_wip" variant adds a dashed border for unimplemented items
    Object.keys(LEVEL_STYLE).forEach(function (lv) {
      lines.push("  classDef " + lv + " " + LEVEL_STYLE[lv] + ";");
      lines.push("  classDef " + lv + "_wip " + LEVEL_STYLE[lv] + ",stroke-dasharray:6 4;");
    });
    Catalog.LEVELS.forEach(function (lv) {
      var g = byLevel[lv];
      if (!g || !g.length) return;
      var norm = g.filter(function (it) { return !it.wip; }).map(function (it) { return nid(it.id); });
      var wip = g.filter(function (it) { return it.wip; }).map(function (it) { return nid(it.id); });
      if (norm.length) lines.push("  class " + norm.join(",") + " " + lv + ";");
      if (wip.length) lines.push("  class " + wip.join(",") + " " + lv + "_wip;");
    });

    // clickable nodes
    items.forEach(function (it) {
      lines.push('  click ' + nid(it.id) + ' "' + Catalog.url(it) + '" "' + Catalog.name(it) + '"');
    });
    return lines.join("\n");
  }

  function fallbackList(container, items) {
    container.innerHTML = "";
    var msg = document.createElement("p");
    msg.className = "depgraph-fallback-msg";
    msg.textContent = "No se pudo cargar el diagrama; aquí tienes los enlaces:";
    container.appendChild(msg);
    Catalog.LEVELS.forEach(function (lv) {
      var group = items.filter(function (it) { return it.level === lv; });
      if (!group.length) return;
      var h = document.createElement("p");
      h.innerHTML = "<strong>" + Catalog.LEVEL_LABELS[lv] + "</strong>";
      container.appendChild(h);
      var ul = document.createElement("ul");
      group.forEach(function (it) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = Catalog.url(it);
        a.textContent = Catalog.name(it) + " — " + Catalog.TYPE_LABELS[it.type];
        li.appendChild(a);
        ul.appendChild(li);
      });
      container.appendChild(ul);
    });
  }

  function init() {
    var container = document.getElementById("depgraph");
    if (!container) return;
    var filtersMount = document.getElementById("depgraph-filters");

    var mermaidPromise = null;
    function getMermaid() {
      if (!mermaidPromise) {
        var scheme = document.body.getAttribute("data-md-color-scheme");
        mermaidPromise = import(MERMAID_URL).then(function (mod) {
          var mermaid = mod.default;
          mermaid.initialize({
            startOnLoad: false,
            securityLevel: "loose",
            theme: scheme === "slate" ? "dark" : "default",
            flowchart: { nodeSpacing: 25, rankSpacing: 70, useMaxWidth: true },
          });
          return mermaid;
        });
      }
      return mermaidPromise;
    }

    var renderSeq = 0;
    function draw(allItems, state) {
      var items = allItems.filter(function (it) { return Catalog.passes(it, state); });
      container.innerHTML = '<p class="depgraph-loading">Generando el diagrama…</p>';
      if (!items.length) {
        container.innerHTML = '<p class="depgraph-empty">Ningún elemento coincide con los filtros.</p>';
        return;
      }
      var seq = ++renderSeq;
      var def = buildDefinition(items);
      getMermaid().then(function (mermaid) {
        return mermaid.render("depgraph_svg_" + seq, def);
      }).then(function (res) {
        if (seq !== renderSeq) return; // a newer render started
        container.innerHTML = res.svg;
        if (res.bindFunctions) res.bindFunctions(container);
      }).catch(function () {
        if (seq === renderSeq) fallbackList(container, items);
      });
    }

    Catalog.load().then(function (data) {
      var state;
      if (filtersMount) {
        state = Catalog.makeFilters(filtersMount, {}, function (s) { draw(data, s); });
      } else {
        state = { types: new Set(Catalog.TYPES), levels: new Set(Catalog.LEVELS) };
      }
      draw(data, state);
    }).catch(function () {
      container.innerHTML = '<p class="depgraph-empty">No se pudieron cargar los datos.</p>';
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
