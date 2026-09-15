/*
 * matrix.js — "Mapa de contenidos": a table with one row per difficulty level
 * and one column per type (técnica / algoritmo / estructura). Each cell holds
 * the matching items as linked badges. Rows are tinted by level.
 *
 * The matrix itself encodes level (rows) and type (columns), so its filter bar
 * only exposes the remaining dimensions — Tema (topic) and Estado (WIP) — via
 * the shared Catalog filter widget. Reuses the shared Catalog data.
 */
(function () {
  "use strict";

  function badge(item) {
    var a = document.createElement("a");
    // Colour by difficulty (level), like every other table — easier to read than
    // per-type colours (the type is already the column).
    a.className = "cat-badge cat-lvl--" + item.level + (item.wip ? " cat-badge--wip" : "");
    a.href = Catalog.url(item);
    var ti = Catalog.topicInfo(item);
    a.textContent = (ti ? ti.icon + " " : "") + Catalog.name(item) + (item.wip ? " 🏗️" : "");
    if (ti) a.title = ti.title;
    return a;
  }

  function buildTable(data, state) {
    var table = document.createElement("table");
    table.className = "matrix";

    var thead = document.createElement("thead");
    var htr = document.createElement("tr");
    htr.appendChild(document.createElement("th")); // corner
    Catalog.TYPES.forEach(function (t) {
      var th = document.createElement("th");
      th.textContent = Catalog.TYPE_LABELS[t];
      htr.appendChild(th);
    });
    thead.appendChild(htr);
    table.appendChild(thead);

    var tbody = document.createElement("tbody");
    Catalog.LEVELS.forEach(function (lv) {
      var tr = document.createElement("tr");
      tr.className = "matrix__row matrix__row--" + lv;

      var th = document.createElement("th");
      th.scope = "row";
      th.className = "matrix__level";
      th.textContent = Catalog.LEVEL_LABELS[lv];
      tr.appendChild(th);

      Catalog.TYPES.forEach(function (t) {
        var td = document.createElement("td");
        td.className = "matrix__cell";
        var items = data.filter(function (it) {
          return it.level === lv && it.type === t && Catalog.passes(it, state);
        });
        if (!items.length) {
          var dash = document.createElement("span");
          dash.className = "matrix__empty";
          dash.textContent = "—";
          td.appendChild(dash);
        } else {
          items.forEach(function (it) { td.appendChild(badge(it)); });
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  }

  function init() {
    var mount = document.getElementById("content-matrix");
    if (!mount) return;

    Catalog.load().then(function (data) {
      mount.innerHTML = "";

      var fmount = document.createElement("div");
      fmount.className = "cat-filters";
      mount.appendChild(fmount);

      var scroller = document.createElement("div");
      scroller.className = "matrix__scroll";
      mount.appendChild(scroller);

      function render() {
        scroller.innerHTML = "";
        scroller.appendChild(buildTable(data, state));
      }

      // Rows = level, columns = type -> only Tema + Estado are worth filtering.
      var state = Catalog.makeFilters(
        fmount, { showLevel: false, showType: false }, render
      );
      render();
    }).catch(function () {
      mount.innerHTML = '<p class="matrix__error">No se pudo cargar el mapa de contenidos.</p>';
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
