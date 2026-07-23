/*
 * todo.js — Contribuir → ToDo: lists every unimplemented (wip) element,
 * grouped and sorted by difficulty (level, then numeric difficulty). Reuses Catalog.
 */
(function () {
  "use strict";

  function init() {
    var mount = document.getElementById("todo-list");
    if (!mount) return;

    Catalog.load().then(function (data) {
      var wip = data.filter(function (x) { return x.wip; });
      wip.sort(function (a, b) {
        var la = Catalog.LEVELS.indexOf(a.level), lb = Catalog.LEVELS.indexOf(b.level);
        if (la !== lb) return (la === -1 ? 99 : la) - (lb === -1 ? 99 : lb);
        var da = parseFloat(a.difficulty) || 0, db = parseFloat(b.difficulty) || 0;
        if (da !== db) return da - db;
        return Catalog.name(a).localeCompare(Catalog.name(b), "es");
      });

      mount.innerHTML = "";
      if (!wip.length) {
        mount.innerHTML = "<p>¡No queda nada por implementar! 🎉</p>";
        return;
      }

      var count = document.createElement("p");
      count.className = "todo-count";
      count.textContent = wip.length + " elementos por implementar";
      mount.appendChild(count);

      var curLevel = null, ul = null;
      wip.forEach(function (it) {
        if (it.level !== curLevel) {
          curLevel = it.level;
          var h = document.createElement("p");
          h.className = "todo-level";
          h.innerHTML = "<strong>" + (Catalog.LEVEL_LABELS[it.level] || it.level) + "</strong>";
          mount.appendChild(h);
          ul = document.createElement("ul");
          ul.className = "todo-ul";
          mount.appendChild(ul);
        }
        var li = document.createElement("li");
        var ti = Catalog.topicInfo(it);
        if (ti) {
          var ic = document.createElement("span");
          ic.className = "topic-icon"; ic.textContent = ti.icon + " "; ic.title = ti.title;
          li.appendChild(ic);
        }
        var a = document.createElement("a");
        a.href = Catalog.url(it); a.textContent = Catalog.name(it);
        li.appendChild(a);
        var meta = document.createElement("span");
        meta.className = "todo-meta";
        meta.textContent = " — " + (Catalog.TYPE_LABELS[it.type] || it.type) +
          " · dif. " + (it.difficulty != null ? it.difficulty : "—");
        li.appendChild(meta);
        ul.appendChild(li);
      });
    }).catch(function () {
      mount.innerHTML = "<p>No se pudo cargar la lista.</p>";
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
