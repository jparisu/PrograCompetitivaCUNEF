/*
 * overview-table.js — interactive catalogue table.
 *
 * Data + filtering come from the shared window.Catalog (same module the graph
 * and the matrix use), so the multi-select "type"/"level" filtering logic is
 * defined once and reused. This file adds the table-specific bits: sortable and
 * resizable columns, show/hide columns, a text search, and a requirements
 * column that links each prerequisite to its page.
 *
 * A page can lock the level with  <div id="overview-table" data-level="...">.
 */
(function () {
  "use strict";

  var BY_ID = {};                        // id -> item, for requirement links
  var DEFAULT_WIDTHS = {
    name: 300, type: 110, level: 120, difficulty: 95,
    requirements: 220, complexity: 160, languages: 110, tags: 190,
  };

  var container, filterState;
  var state = {
    data: [],
    order: null,          // set once columns exist
    visible: {},
    sortKey: "level",
    sortDir: 1,
    text: "",
    widths: {},
  };

  function nameOf(r) { return Catalog.name(r); }

  function chips(items, cls) {
    var frag = document.createDocumentFragment();
    if (!items || !items.length) { frag.appendChild(document.createTextNode("—")); return frag; }
    items.forEach(function (it) {
      var s = document.createElement("span");
      s.className = cls;
      s.textContent = it;
      frag.appendChild(s);
    });
    return frag;
  }

  function reqLinks(ids) {
    var frag = document.createDocumentFragment();
    if (!ids || !ids.length) { frag.appendChild(document.createTextNode("—")); return frag; }
    ids.forEach(function (id, i) {
      if (i) frag.appendChild(document.createTextNode(", "));
      var e = BY_ID[id];
      if (e) {
        var a = document.createElement("a");
        a.href = Catalog.url(e);
        a.textContent = Catalog.name(e);
        frag.appendChild(a);
      } else {
        var s = document.createElement("span");
        s.className = "ov-req-missing";
        s.textContent = id;
        frag.appendChild(s);
      }
    });
    return frag;
  }

  var COLUMNS = [
    {
      key: "name", label: "Nombre",
      sortValue: function (r) { return nameOf(r).toLowerCase(); },
      render: function (r) {
        var frag = document.createDocumentFragment();
        var ti = Catalog.topicInfo(r);
        if (ti) {
          var ic = document.createElement("a");
          ic.className = "topic-icon topic-icon--link";
          ic.textContent = ti.icon; ic.title = ti.title; ic.href = Catalog.topicHref(r);
          frag.appendChild(ic);
          frag.appendChild(document.createTextNode(" "));
        }
        var a = document.createElement("a");
        a.href = Catalog.url(r);
        a.textContent = nameOf(r);
        frag.appendChild(a);
        if (r.wip) {
          var cr = document.createElement("span");
          cr.className = "wip-crane"; cr.textContent = " 🏗️"; cr.title = "En construcción";
          frag.appendChild(cr);
        }
        return frag;
      },
    },
    {
      key: "type", label: "Tipo",
      sortValue: function (r) { return Catalog.TYPE_LABELS[r.type] || r.type || ""; },
      render: function (r) {
        var s = document.createElement("span");
        s.className = "ov-type ov-type--" + (r.type || "unknown");
        s.textContent = Catalog.TYPE_LABELS[r.type] || r.type || "—";
        return s;
      },
    },
    {
      key: "level", label: "Nivel", numeric: true,
      sortValue: function (r) { var i = Catalog.LEVELS.indexOf(r.level); return i === -1 ? 99 : i; },
      render: function (r) {
        var s = document.createElement("span");
        s.className = "ov-badge ov-badge--" + (r.level || "unknown");
        s.textContent = Catalog.LEVEL_LABELS[r.level] || r.level || "—";
        return s;
      },
    },
    {
      key: "difficulty", label: "Dificultad", numeric: true,
      sortValue: function (r) { var v = parseFloat(r.difficulty); return isNaN(v) ? -Infinity : v; },
      render: function (r) {
        return document.createTextNode(
          r.difficulty === null || r.difficulty === undefined ? "—" : String(r.difficulty));
      },
    },
    {
      key: "requirements", label: "Requisitos",
      sortValue: function (r) { return (r.prereq || []).join(", ").toLowerCase(); },
      render: function (r) { return reqLinks(r.prereq); },
    },
    {
      key: "complexity", label: "Complejidad",
      sortValue: function (r) { return (r.complexity || "").toLowerCase(); },
      render: function (r) { var c = document.createElement("code"); c.textContent = r.complexity || "—"; return c; },
    },
    {
      key: "languages", label: "Lenguajes",
      sortValue: function (r) { return (r.languages || []).join(", "); },
      render: function (r) {
        var labels = (r.languages || []).map(function (l) { return l === "cpp" ? "C++" : l === "py" ? "Python" : l; });
        return chips(labels, "ov-lang");
      },
    },
    {
      key: "tags", label: "Tags",
      sortValue: function (r) { return (r.tags || []).join(", ").toLowerCase(); },
      render: function (r) { return chips(r.tags, "ov-chip ov-chip--tag"); },
    },
  ];

  function colByKey(k) { for (var i = 0; i < COLUMNS.length; i++) if (COLUMNS[i].key === k) return COLUMNS[i]; return null; }

  function matchesText(r) {
    if (!state.text) return true;
    var hay = [nameOf(r), (r.tags || []).join(" "), (r.techniques || []).join(" ")].join(" ").toLowerCase();
    return hay.indexOf(state.text.toLowerCase()) !== -1;
  }

  function filtered() {
    return state.data.filter(function (r) {
      return matchesText(r) && Catalog.passes(r, filterState);
    });
  }

  function sorted(rows) {
    var col = colByKey(state.sortKey);
    if (!col) return rows;
    return rows.slice().sort(function (a, b) {
      var va = col.sortValue(a), vb = col.sortValue(b), cmp;
      if (col.numeric || (typeof va === "number" && typeof vb === "number")) cmp = va - vb;
      else cmp = String(va).localeCompare(String(vb), "es");
      if (cmp === 0) cmp = nameOf(a).localeCompare(nameOf(b), "es");
      return cmp * state.sortDir;
    });
  }

  function orderedVisibleColumns() {
    return state.order.map(colByKey).filter(function (c) { return c && state.visible[c.key]; });
  }

  function addResizer(th, key, index, colgroup, cols, table) {
    var res = document.createElement("span");
    res.className = "ov-resizer";
    res.addEventListener("mousedown", function (e) {
      e.preventDefault(); e.stopPropagation();
      var startX = e.clientX, startW = state.widths[key] || DEFAULT_WIDTHS[key] || 140;
      th.draggable = false;
      function move(ev) {
        var w = Math.max(60, startW + (ev.clientX - startX));
        state.widths[key] = w;
        if (colgroup.children[index]) colgroup.children[index].style.width = w + "px";
        var t = 0; cols.forEach(function (c) { t += state.widths[c.key] || DEFAULT_WIDTHS[c.key] || 140; });
        table.style.width = t + "px";
      }
      function up() { document.removeEventListener("mousemove", move); document.removeEventListener("mouseup", up); th.draggable = true; }
      document.addEventListener("mousemove", move); document.addEventListener("mouseup", up);
    });
    th.appendChild(res);
  }

  var dragKey = null;
  function wireDrag(th, key) {
    th.addEventListener("dragstart", function (e) { dragKey = key; th.classList.add("ov-dragging"); if (e.dataTransfer) { e.dataTransfer.effectAllowed = "move"; try { e.dataTransfer.setData("text/plain", key); } catch (x) {} } });
    th.addEventListener("dragend", function () { th.classList.remove("ov-dragging"); dragKey = null; });
    th.addEventListener("dragover", function (e) { if (dragKey && dragKey !== key) { e.preventDefault(); th.classList.add("ov-drop-target"); } });
    th.addEventListener("dragleave", function () { th.classList.remove("ov-drop-target"); });
    th.addEventListener("drop", function (e) {
      e.preventDefault(); th.classList.remove("ov-drop-target");
      if (!dragKey || dragKey === key) return;
      state.order = state.order.filter(function (k) { return k !== dragKey; });
      state.order.splice(state.order.indexOf(key), 0, dragKey);
      render();
    });
  }

  function render() {
    var cols = orderedVisibleColumns();
    var rows = sorted(filtered());

    var table = document.createElement("table");
    table.className = "ov-table";
    table.style.tableLayout = "fixed";

    var colgroup = document.createElement("colgroup");
    var totalW = 0;
    cols.forEach(function (col) {
      var w = state.widths[col.key] || DEFAULT_WIDTHS[col.key] || 140;
      var c = document.createElement("col"); c.style.width = w + "px";
      colgroup.appendChild(c); totalW += w;
    });
    table.style.width = totalW + "px";
    table.appendChild(colgroup);

    var thead = document.createElement("thead");
    var htr = document.createElement("tr");
    cols.forEach(function (col, colIndex) {
      var th = document.createElement("th");
      th.className = "ov-th"; th.dataset.key = col.key; th.setAttribute("draggable", "true"); th.setAttribute("scope", "col");
      var label = document.createElement("span"); label.className = "ov-th-label"; label.textContent = col.label; th.appendChild(label);
      var ind = document.createElement("span"); ind.className = "ov-sort-ind";
      if (state.sortKey === col.key) { ind.textContent = state.sortDir === 1 ? "▲" : "▼"; th.classList.add("ov-sorted"); }
      th.appendChild(ind);
      label.addEventListener("click", function () {
        if (state.sortKey === col.key) state.sortDir *= -1; else { state.sortKey = col.key; state.sortDir = 1; }
        render();
      });
      wireDrag(th, col.key);
      addResizer(th, col.key, colIndex, colgroup, cols, table);
      htr.appendChild(th);
    });
    thead.appendChild(htr); table.appendChild(thead);

    var tbody = document.createElement("tbody");
    if (!rows.length) {
      var tr = document.createElement("tr"); var td = document.createElement("td");
      td.colSpan = cols.length || 1; td.className = "ov-empty"; td.textContent = "No hay elementos que coincidan con el filtro.";
      tr.appendChild(td); tbody.appendChild(tr);
    } else {
      rows.forEach(function (r) {
        var tr = document.createElement("tr");
        if (r.wip) tr.className = "ov-row--wip";
        cols.forEach(function (col) {
          var td = document.createElement("td"); td.className = "ov-td ov-td--" + col.key; td.dataset.label = col.label;
          td.appendChild(col.render(r)); tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }
    table.appendChild(tbody);

    var count = document.createElement("p"); count.className = "ov-count";
    count.textContent = rows.length + " de " + state.data.length + " elementos";

    container.textContent = "";
    var scroller = document.createElement("div"); scroller.className = "ov-scroll"; scroller.appendChild(table);
    container.appendChild(scroller); container.appendChild(count);
  }

  function buildControls() {
    var controls = document.getElementById("ov-controls");
    var search = document.getElementById("ov-filter");
    if (search) search.addEventListener("input", function () { state.text = search.value; render(); });

    if (controls) {
      var fmount = document.createElement("div"); fmount.className = "cat-filters";
      controls.insertBefore(fmount, controls.firstChild);
      var locked = container.getAttribute("data-level") || undefined;
      filterState = Catalog.makeFilters(fmount, { lockedLevel: locked }, function () { render(); });
    } else {
      filterState = { types: new Set(Catalog.TYPES), levels: new Set(Catalog.LEVELS) };
    }

    var colsBox = document.getElementById("ov-columns");
    if (colsBox) {
      COLUMNS.forEach(function (col) {
        var label = document.createElement("label"); label.className = "ov-col-toggle";
        var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = state.visible[col.key];
        cb.addEventListener("change", function () { state.visible[col.key] = cb.checked; render(); });
        var span = document.createElement("span"); span.textContent = col.label;
        label.appendChild(cb); label.appendChild(span); colsBox.appendChild(label);
      });
    }
  }

  function init() {
    container = document.getElementById("overview-table");
    if (!container) return;
    state.order = COLUMNS.map(function (c) { return c.key; });
    COLUMNS.forEach(function (c) { state.visible[c.key] = true; });

    Catalog.load().then(function (data) {
      state.data = data;
      BY_ID = {};
      data.forEach(function (e) { BY_ID[e.id] = e; });
      buildControls();
      render();
    }).catch(function (err) {
      container.textContent = "";
      var p = document.createElement("p"); p.className = "ov-error";
      p.textContent = "No se pudo cargar la tabla (" + (err && err.message ? err.message : "error") + ").";
      container.appendChild(p);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
