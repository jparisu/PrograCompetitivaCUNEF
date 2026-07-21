/*
 * overview-table.js — interactive "Resumen" table for the algorithms overview.
 *
 * Vanilla JS, no dependencies. On load, if #overview-table exists it fetches the
 * generated data file (page-relative: ../assets/data/algorithms.json, so it also
 * resolves correctly under /pr-preview/pr-N/) and renders a table with:
 *   - sortable columns (click header; numeric for difficulty, string otherwise),
 *   - a text filter (name/tags/techniques) plus level and technique <select>s,
 *   - per-column show/hide checkboxes,
 *   - draggable headers to reorder columns.
 *
 * The data file is written by tools/genoverview.py. If it is missing/unreadable
 * a message is shown in the container instead of throwing.
 */
(function () {
  "use strict";

  var LEVEL_ORDER = ["base", "beginner", "intermediate", "advanced", "expert"];
  var LEVEL_LABELS = {
    base: "Base",
    beginner: "Principiante",
    intermediate: "Intermedio",
    advanced: "Avanzado",
    expert: "Experto",
  };
  var LANG_LABELS = { cpp: "C++", py: "Python" };

  // Column definitions. `key` maps to a data field; `sortValue` yields a
  // comparable value; `render` builds the cell's DOM content.
  var COLUMNS = [
    {
      key: "name",
      label: "Nombre",
      numeric: false,
      sortValue: function (r) { return nameOf(r).toLowerCase(); },
      render: function (r) {
        var a = document.createElement("a");
        a.href = r.url || "#";
        a.textContent = nameOf(r);
        return a;
      },
    },
    {
      key: "level",
      label: "Nivel",
      numeric: false,
      sortValue: function (r) {
        var i = LEVEL_ORDER.indexOf(r.level);
        return i === -1 ? 99 : i;
      },
      render: function (r) {
        var span = document.createElement("span");
        span.className = "ov-badge ov-badge--" + (r.level || "unknown");
        span.textContent = LEVEL_LABELS[r.level] || r.level || "—";
        return span;
      },
    },
    {
      key: "difficulty",
      label: "Dificultad",
      numeric: true,
      sortValue: function (r) {
        var v = parseFloat(r.difficulty);
        return isNaN(v) ? -Infinity : v;
      },
      render: function (r) {
        return document.createTextNode(
          r.difficulty === null || r.difficulty === undefined ? "—" : String(r.difficulty)
        );
      },
    },
    {
      key: "techniques",
      label: "Técnicas",
      numeric: false,
      sortValue: function (r) { return (r.techniques || []).join(", ").toLowerCase(); },
      render: function (r) { return chips(r.techniques, "ov-chip"); },
    },
    {
      key: "complexity",
      label: "Complejidad",
      numeric: false,
      sortValue: function (r) { return (r.complexity || "").toLowerCase(); },
      render: function (r) {
        var code = document.createElement("code");
        code.textContent = r.complexity || "—";
        return code;
      },
    },
    {
      key: "languages",
      label: "Lenguajes",
      numeric: false,
      sortValue: function (r) { return (r.languages || []).join(", "); },
      render: function (r) {
        var labels = (r.languages || []).map(function (l) { return LANG_LABELS[l] || l; });
        return chips(labels, "ov-lang");
      },
    },
    {
      key: "tags",
      label: "Tags",
      numeric: false,
      sortValue: function (r) { return (r.tags || []).join(", ").toLowerCase(); },
      render: function (r) { return chips(r.tags, "ov-chip ov-chip--tag"); },
    },
  ];

  function nameOf(r) {
    if (r && r.name) {
      if (typeof r.name === "string") return r.name;
      return r.name.es || r.name.en || r.id || "";
    }
    return (r && r.id) || "";
  }

  function chips(items, cls) {
    var frag = document.createDocumentFragment();
    if (!items || !items.length) {
      frag.appendChild(document.createTextNode("—"));
      return frag;
    }
    items.forEach(function (it) {
      var s = document.createElement("span");
      s.className = cls;
      s.textContent = it;
      frag.appendChild(s);
    });
    return frag;
  }

  // ------------------------------------------------------------------ state
  var state = {
    data: [],
    order: COLUMNS.map(function (c) { return c.key; }), // column display order
    visible: {},                                        // key -> bool
    sortKey: "level",
    sortDir: 1,                                          // 1 asc, -1 desc
    text: "",
    level: "",
    technique: "",
  };
  COLUMNS.forEach(function (c) { state.visible[c.key] = true; });

  function colByKey(key) {
    for (var i = 0; i < COLUMNS.length; i++) {
      if (COLUMNS[i].key === key) return COLUMNS[i];
    }
    return null;
  }

  // ------------------------------------------------------------------ filtering
  function matchesText(row, text) {
    if (!text) return true;
    var hay = [
      nameOf(row),
      (row.tags || []).join(" "),
      (row.techniques || []).join(" "),
    ].join(" ").toLowerCase();
    return hay.indexOf(text.toLowerCase()) !== -1;
  }

  function filtered() {
    return state.data.filter(function (r) {
      if (!matchesText(r, state.text)) return false;
      if (state.level && r.level !== state.level) return false;
      if (state.technique && (r.techniques || []).indexOf(state.technique) === -1) return false;
      return true;
    });
  }

  function sorted(rows) {
    var col = colByKey(state.sortKey);
    if (!col) return rows;
    var copy = rows.slice();
    copy.sort(function (a, b) {
      var va = col.sortValue(a);
      var vb = col.sortValue(b);
      var cmp;
      if (col.numeric) {
        cmp = va - vb;
      } else if (typeof va === "number" && typeof vb === "number") {
        cmp = va - vb;
      } else {
        cmp = String(va).localeCompare(String(vb), "es");
      }
      if (cmp === 0) {
        // stable tie-break by name so re-sorts are deterministic
        cmp = nameOf(a).localeCompare(nameOf(b), "es");
      }
      return cmp * state.sortDir;
    });
    return copy;
  }

  // ------------------------------------------------------------------ rendering
  var container;

  function orderedVisibleColumns() {
    return state.order
      .map(colByKey)
      .filter(function (c) { return c && state.visible[c.key]; });
  }

  function render() {
    var cols = orderedVisibleColumns();
    var rows = sorted(filtered());

    var table = document.createElement("table");
    table.className = "ov-table";

    // --- header
    var thead = document.createElement("thead");
    var htr = document.createElement("tr");
    cols.forEach(function (col) {
      var th = document.createElement("th");
      th.dataset.key = col.key;
      th.className = "ov-th";
      th.setAttribute("draggable", "true");
      th.setAttribute("scope", "col");

      var label = document.createElement("span");
      label.className = "ov-th-label";
      label.textContent = col.label;
      th.appendChild(label);

      var ind = document.createElement("span");
      ind.className = "ov-sort-ind";
      if (state.sortKey === col.key) {
        ind.textContent = state.sortDir === 1 ? "▲" : "▼";
        th.classList.add("ov-sorted");
        th.setAttribute("aria-sort", state.sortDir === 1 ? "ascending" : "descending");
      } else {
        ind.textContent = "";
        th.setAttribute("aria-sort", "none");
      }
      th.appendChild(ind);

      label.addEventListener("click", function () { onSort(col.key); });
      wireDrag(th, col.key);
      htr.appendChild(th);
    });
    thead.appendChild(htr);
    table.appendChild(thead);

    // --- body
    var tbody = document.createElement("tbody");
    if (!rows.length) {
      var tr = document.createElement("tr");
      var td = document.createElement("td");
      td.colSpan = cols.length || 1;
      td.className = "ov-empty";
      td.textContent = "No hay algoritmos que coincidan con el filtro.";
      tr.appendChild(td);
      tbody.appendChild(tr);
    } else {
      rows.forEach(function (r) {
        var tr = document.createElement("tr");
        cols.forEach(function (col) {
          var td = document.createElement("td");
          td.className = "ov-td ov-td--" + col.key;
          td.dataset.label = col.label;
          td.appendChild(col.render(r));
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }
    table.appendChild(tbody);

    var count = document.createElement("p");
    count.className = "ov-count";
    count.textContent = rows.length + " de " + state.data.length + " algoritmos";

    container.textContent = "";
    var scroller = document.createElement("div");
    scroller.className = "ov-scroll";
    scroller.appendChild(table);
    container.appendChild(scroller);
    container.appendChild(count);
  }

  function onSort(key) {
    if (state.sortKey === key) {
      state.sortDir *= -1;
    } else {
      state.sortKey = key;
      state.sortDir = 1;
    }
    render();
  }

  // ------------------------------------------------------------------ drag reorder
  var dragKey = null;
  function wireDrag(th, key) {
    th.addEventListener("dragstart", function (e) {
      dragKey = key;
      th.classList.add("ov-dragging");
      if (e.dataTransfer) {
        e.dataTransfer.effectAllowed = "move";
        try { e.dataTransfer.setData("text/plain", key); } catch (err) {}
      }
    });
    th.addEventListener("dragend", function () {
      th.classList.remove("ov-dragging");
      dragKey = null;
      var all = th.parentNode ? th.parentNode.querySelectorAll(".ov-drop-target") : [];
      Array.prototype.forEach.call(all, function (n) { n.classList.remove("ov-drop-target"); });
    });
    th.addEventListener("dragover", function (e) {
      if (dragKey && dragKey !== key) {
        e.preventDefault();
        if (e.dataTransfer) e.dataTransfer.dropEffect = "move";
        th.classList.add("ov-drop-target");
      }
    });
    th.addEventListener("dragleave", function () {
      th.classList.remove("ov-drop-target");
    });
    th.addEventListener("drop", function (e) {
      e.preventDefault();
      th.classList.remove("ov-drop-target");
      if (!dragKey || dragKey === key) return;
      moveColumn(dragKey, key);
      render();
    });
  }

  function moveColumn(fromKey, toKey) {
    if (fromKey === toKey) return;
    if (state.order.indexOf(fromKey) === -1 || state.order.indexOf(toKey) === -1) return;
    // Remove the dragged key, then insert it just before its drop target.
    state.order = state.order.filter(function (k) { return k !== fromKey; });
    var targetIdx = state.order.indexOf(toKey);
    state.order.splice(targetIdx, 0, fromKey);
  }

  // ------------------------------------------------------------------ controls
  function populateSelect(sel, values, current) {
    if (!sel) return;
    // keep the first ("all") option, drop the rest
    while (sel.options.length > 1) sel.remove(1);
    values.forEach(function (v) {
      var opt = document.createElement("option");
      opt.value = v.value;
      opt.textContent = v.label;
      sel.appendChild(opt);
    });
    if (current) sel.value = current;
  }

  function buildControls() {
    var filterInput = document.getElementById("ov-filter");
    var levelSel = document.getElementById("ov-level");
    var techSel = document.getElementById("ov-technique");
    var colsBox = document.getElementById("ov-columns");

    // levels present in the data, in canonical order
    var levelsPresent = LEVEL_ORDER.filter(function (lv) {
      return state.data.some(function (r) { return r.level === lv; });
    });
    populateSelect(levelSel, levelsPresent.map(function (lv) {
      return { value: lv, label: LEVEL_LABELS[lv] || lv };
    }), state.level);

    // techniques present, sorted alphabetically, unique
    var techSet = {};
    state.data.forEach(function (r) {
      (r.techniques || []).forEach(function (t) { techSet[t] = true; });
    });
    var techs = Object.keys(techSet).sort(function (a, b) { return a.localeCompare(b, "es"); });
    populateSelect(techSel, techs.map(function (t) {
      return { value: t, label: t };
    }), state.technique);

    if (filterInput) {
      filterInput.addEventListener("input", function () {
        state.text = filterInput.value;
        render();
      });
    }
    if (levelSel) {
      levelSel.addEventListener("change", function () {
        state.level = levelSel.value;
        render();
      });
    }
    if (techSel) {
      techSel.addEventListener("change", function () {
        state.technique = techSel.value;
        render();
      });
    }

    // show/hide column checkboxes
    if (colsBox) {
      COLUMNS.forEach(function (col) {
        var id = "ov-col-" + col.key;
        var label = document.createElement("label");
        label.className = "ov-col-toggle";

        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.id = id;
        cb.checked = state.visible[col.key];
        cb.addEventListener("change", function () {
          state.visible[col.key] = cb.checked;
          render();
        });

        var span = document.createElement("span");
        span.textContent = col.label;

        label.appendChild(cb);
        label.appendChild(span);
        colsBox.appendChild(label);
      });
    }
  }

  // ------------------------------------------------------------------ boot
  function showMessage(msg) {
    container.textContent = "";
    var p = document.createElement("p");
    p.className = "ov-error";
    p.textContent = msg;
    container.appendChild(p);
  }

  function init() {
    container = document.getElementById("overview-table");
    if (!container) return;

    fetch("../assets/data/algorithms.json", { cache: "no-cache" })
      .then(function (resp) {
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        return resp.json();
      })
      .then(function (data) {
        if (!Array.isArray(data)) throw new Error("formato inesperado");
        state.data = data;
        buildControls();
        render();
      })
      .catch(function (err) {
        showMessage(
          "No se pudo cargar la tabla de algoritmos (algorithms.json). " +
          "Ejecuta 'python tools/genoverview.py' para generarla. Detalle: " +
          (err && err.message ? err.message : err)
        );
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
