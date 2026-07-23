/*
 * topics.js — builds the table on the Temas page (#topics-table).
 *
 * One row per topic: icon + name (linked to that topic's section on the page),
 * a short description, and three columns (Técnica / Algoritmo / Estructura)
 * listing the topic's elements as badges COLOURED BY DIFFICULTY (level).
 * Reuses the shared Catalog.
 */
(function () {
  "use strict";

  function levelBadge(item) {
    var a = document.createElement("a");
    a.className = "cat-badge cat-lvl--" + item.level + (item.wip ? " cat-badge--wip" : "");
    a.href = Catalog.url(item);
    a.textContent = Catalog.name(item) + (item.wip ? " 🏗️" : "");
    a.title = Catalog.LEVEL_LABELS[item.level] || item.level;
    return a;
  }

  function typeCell(items, type) {
    var td = document.createElement("td");
    var xs = items.filter(function (i) { return i.type === type; });
    if (!xs.length) {
      var s = document.createElement("span"); s.className = "matrix__empty"; s.textContent = "—";
      td.appendChild(s);
    } else {
      xs.forEach(function (i) { td.appendChild(levelBadge(i)); });
    }
    return td;
  }

  function buildTable(data, state) {
    var table = document.createElement("table");
    table.className = "matrix topics-table";

    var thead = document.createElement("thead"), htr = document.createElement("tr");
    ["Tema", "Descripción"].concat(Catalog.TYPES.map(function (t) { return Catalog.TYPE_LABELS[t]; }))
      .forEach(function (h) { var th = document.createElement("th"); th.textContent = h; htr.appendChild(th); });
    thead.appendChild(htr); table.appendChild(thead);

    var tbody = document.createElement("tbody");
    Catalog.TOPIC_IDS.forEach(function (tid) {
      var topic = Catalog.TOPICS[tid];
      var items = data.filter(function (i) {
        return i.topic === tid && Catalog.passes(i, state);
      });

      var tr = document.createElement("tr");
      var th = document.createElement("th"); th.scope = "row"; th.className = "topics__name";
      var a = document.createElement("a"); a.href = "#" + tid;
      a.textContent = topic.icon + " " + topic.label;
      th.appendChild(a); tr.appendChild(th);

      var desc = document.createElement("td"); desc.className = "topics__desc";
      desc.textContent = topic.desc || "";
      tr.appendChild(desc);

      Catalog.TYPES.forEach(function (t) { tr.appendChild(typeCell(items, t)); });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  }

  function init() {
    var mount = document.getElementById("topics-table");
    if (!mount) return;
    Catalog.load().then(function (data) {
      mount.innerHTML = "";

      var fmount = document.createElement("div");
      fmount.className = "cat-filters";
      mount.appendChild(fmount);

      var sc = document.createElement("div"); sc.className = "matrix__scroll";
      mount.appendChild(sc);

      function render() {
        sc.innerHTML = "";
        sc.appendChild(buildTable(data, state));
      }

      // Topic = rows, type = columns, level = the colour legend, so only the
      // "Estado" (WIP) toggle is worth exposing here.
      var state = Catalog.makeFilters(
        fmount, { showLevel: false, showType: false, showTopic: false }, render
      );
      render();
    }).catch(function () { mount.innerHTML = "<p>No se pudo cargar la tabla de temas.</p>"; });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
