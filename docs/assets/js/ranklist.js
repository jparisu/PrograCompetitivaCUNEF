/*
 * Ranking page (docs/ranklist/) — vanilla JS, no external libraries.
 *
 * Loads docs/assets/data/standings.json (a history of dated snapshots),
 * renders the latest standings sorted by score, and — for the selected
 * comparison window (day / week / year) — shows each member's change in
 * position and points relative to the newest snapshot that is at least one
 * window older than the current one.
 *
 * The fetch path is page-relative ("../assets/data/standings.json"): the page
 * lives at /ranklist/, so it resolves to /assets/data/standings.json and keeps
 * working under a preview prefix such as /pr-preview/pr-N/ranklist/.
 */
(function () {
  "use strict";

  var DATA_URL = "../assets/data/standings.json";

  // Days subtracted from the current snapshot date for each window.
  var WINDOW_DAYS = { day: 1, week: 7, year: 365 };

  document.addEventListener("DOMContentLoaded", function () {
    var container = document.getElementById("ranklist");
    if (!container) {
      return; // Not on the ranking page.
    }

    fetch(DATA_URL, { cache: "no-cache" })
      .then(function (resp) {
        if (!resp.ok) {
          throw new Error("HTTP " + resp.status);
        }
        return resp.json();
      })
      .then(function (data) {
        init(container, data);
      })
      .catch(function (err) {
        renderError(container, err);
      });
  });

  function init(container, data) {
    var snapshots = (data && Array.isArray(data.snapshots)) ? data.snapshots.slice() : [];
    if (snapshots.length === 0) {
      renderMessage(container, "No hay datos de clasificación disponibles todavía.");
      return;
    }

    // Sort snapshots by date ascending (be defensive: the file should already be).
    snapshots.sort(function (a, b) {
      return String(a.date).localeCompare(String(b.date));
    });

    var current = snapshots[snapshots.length - 1];
    if (!current || !Array.isArray(current.members) || current.members.length === 0) {
      renderMessage(container, "La última instantánea no contiene miembros.");
      return;
    }

    var state = {
      container: container,
      snapshots: snapshots,
      current: current,
      isSample: !!(data && data.sample),
      window: getInitialWindow()
    };

    wireButtons(state);
    render(state);
  }

  function getInitialWindow() {
    var active = document.querySelector(".ranklist-btn.is-active");
    if (active && active.getAttribute("data-window")) {
      return active.getAttribute("data-window");
    }
    return "week";
  }

  function wireButtons(state) {
    var buttons = document.querySelectorAll(".ranklist-btn");
    Array.prototype.forEach.call(buttons, function (btn) {
      btn.addEventListener("click", function () {
        var win = btn.getAttribute("data-window");
        if (!win || !WINDOW_DAYS.hasOwnProperty(win)) {
          return;
        }
        state.window = win;
        Array.prototype.forEach.call(buttons, function (b) {
          b.classList.toggle("is-active", b === btn);
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        render(state);
      });
    });
  }

  // Find the newest snapshot whose date is <= (current date - window days),
  // excluding the current snapshot itself. Returns null if none qualifies.
  function findComparison(state) {
    var currentDate = parseDate(state.current.date);
    if (!currentDate) {
      return null;
    }
    var cutoff = new Date(currentDate.getTime());
    cutoff.setDate(cutoff.getDate() - WINDOW_DAYS[state.window]);

    var best = null;
    for (var i = 0; i < state.snapshots.length; i++) {
      var snap = state.snapshots[i];
      if (snap === state.current) {
        continue;
      }
      var d = parseDate(snap.date);
      if (!d) {
        continue;
      }
      if (d.getTime() <= cutoff.getTime()) {
        if (!best || d.getTime() > parseDate(best.date).getTime()) {
          best = snap;
        }
      }
    }
    return best;
  }

  function render(state) {
    var container = state.container;
    container.innerHTML = "";

    // Members sorted by score descending; ties broken by solved then name.
    var members = state.current.members.slice().sort(function (a, b) {
      return (b.score - a.score) ||
             ((b.solved || 0) - (a.solved || 0)) ||
             displayName(a).localeCompare(displayName(b));
    });

    var maxScore = members.reduce(function (m, x) {
      return Math.max(m, x.score || 0);
    }, 0) || 1;

    var comparison = findComparison(state);
    var prevIndex = comparison ? indexMembers(comparison.members) : null;
    // Position within the comparison snapshot (also sorted by score desc).
    var prevRanks = comparison ? rankByScore(comparison.members) : null;

    if (state.isSample) {
      container.appendChild(buildBanner(
        "Datos de ejemplo: esta clasificación es ficticia y sirve para la vista previa."
      ));
    }
    container.appendChild(buildMeta(state, comparison));

    var list = document.createElement("ol");
    list.className = "ranklist__rows";

    members.forEach(function (m, i) {
      var position = i + 1;
      list.appendChild(buildRow(m, position, maxScore, prevIndex, prevRanks));
    });

    container.appendChild(list);
  }

  function buildRow(m, position, maxScore, prevIndex, prevRanks) {
    var li = document.createElement("li");
    li.className = "ranklist__row";

    // Position number.
    var pos = document.createElement("div");
    pos.className = "ranklist__pos";
    pos.textContent = "#" + position;
    li.appendChild(pos);

    // Name / handle + solved count.
    var main = document.createElement("div");
    main.className = "ranklist__main";

    var nameEl = document.createElement("div");
    nameEl.className = "ranklist__name";
    nameEl.textContent = displayName(m);
    if (m.handle) {
      var handleEl = document.createElement("span");
      handleEl.className = "ranklist__handle";
      handleEl.textContent = "@" + m.handle;
      nameEl.appendChild(document.createTextNode(" "));
      nameEl.appendChild(handleEl);
    }
    main.appendChild(nameEl);

    // Progress bar (width = score / maxScore).
    var bar = document.createElement("div");
    bar.className = "ranklist__bar";
    var fill = document.createElement("div");
    fill.className = "ranklist__bar-fill";
    var pct = Math.max(0, Math.min(100, (m.score / maxScore) * 100));
    fill.style.width = pct.toFixed(1) + "%";
    bar.appendChild(fill);
    main.appendChild(bar);

    li.appendChild(main);

    // Stats: points + solved.
    var stats = document.createElement("div");
    stats.className = "ranklist__stats";
    var pts = document.createElement("div");
    pts.className = "ranklist__points";
    pts.textContent = formatScore(m.score) + " pts";
    stats.appendChild(pts);
    if (m.solved !== null && m.solved !== undefined) {
      var solved = document.createElement("div");
      solved.className = "ranklist__solved";
      solved.textContent = m.solved + " resueltos";
      stats.appendChild(solved);
    }
    li.appendChild(stats);

    // Change vs comparison snapshot.
    li.appendChild(buildChange(m, position, prevIndex, prevRanks));

    return li;
  }

  function buildChange(m, position, prevIndex, prevRanks) {
    var box = document.createElement("div");
    box.className = "ranklist__change";

    if (!prevIndex) {
      // No comparison snapshot available for this window.
      var none = document.createElement("span");
      none.className = "ranklist__arrow ranklist__arrow--same";
      none.textContent = "—";
      none.title = "Sin histórico para esta ventana";
      box.appendChild(none);
      return box;
    }

    var key = memberKey(m);
    var prev = prevIndex[key];

    if (!prev) {
      var badge = document.createElement("span");
      badge.className = "ranklist__badge ranklist__badge--new";
      badge.textContent = "nuevo";
      box.appendChild(badge);
      return box;
    }

    var prevPos = prevRanks[key];
    var delta = prevPos - position; // positive => improved (moved up)

    var arrow = document.createElement("span");
    arrow.className = "ranklist__arrow";
    if (delta > 0) {
      arrow.classList.add("ranklist__arrow--up");
      arrow.textContent = "▲ " + delta; // ▲
      arrow.title = "Sube " + delta + " posición(es)";
    } else if (delta < 0) {
      arrow.classList.add("ranklist__arrow--down");
      arrow.textContent = "▼ " + Math.abs(delta); // ▼
      arrow.title = "Baja " + Math.abs(delta) + " posición(es)";
    } else {
      arrow.classList.add("ranklist__arrow--same");
      arrow.textContent = "="; // sin cambio
      arrow.title = "Misma posición";
    }
    box.appendChild(arrow);

    // Points gained in the window.
    var gain = (m.score || 0) - (prev.score || 0);
    var gained = document.createElement("span");
    gained.className = "ranklist__gain";
    if (gain > 0) {
      gained.classList.add("ranklist__gain--up");
      gained.textContent = "+" + formatScore(gain);
    } else if (gain < 0) {
      gained.classList.add("ranklist__gain--down");
      gained.textContent = formatScore(gain);
    } else {
      gained.classList.add("ranklist__gain--same");
      gained.textContent = "+0";
    }
    gained.title = "Puntos ganados en esta ventana";
    box.appendChild(gained);

    return box;
  }

  function buildMeta(state, comparison) {
    var meta = document.createElement("p");
    meta.className = "ranklist__updated";
    var txt = "Clasificación a fecha " + state.current.date + ".";
    if (comparison) {
      txt += " Comparando con la instantánea del " + comparison.date + ".";
    } else {
      txt += " No hay una instantánea suficientemente antigua para esta ventana.";
    }
    meta.textContent = txt;
    return meta;
  }

  function buildBanner(text) {
    var el = document.createElement("p");
    el.className = "ranklist__banner";
    el.textContent = text;
    return el;
  }

  // Index members of a snapshot by key -> member object.
  function indexMembers(members) {
    var idx = {};
    (members || []).forEach(function (m) {
      idx[memberKey(m)] = m;
    });
    return idx;
  }

  // Position (1-based) of each member when sorted by score descending.
  function rankByScore(members) {
    var sorted = (members || []).slice().sort(function (a, b) {
      return (b.score - a.score) ||
             ((b.solved || 0) - (a.solved || 0)) ||
             displayName(a).localeCompare(displayName(b));
    });
    var ranks = {};
    sorted.forEach(function (m, i) {
      ranks[memberKey(m)] = i + 1;
    });
    return ranks;
  }

  function memberKey(m) {
    if (m.handle) {
      return "h:" + m.handle;
    }
    return "n:" + (m.name || "");
  }

  function displayName(m) {
    return m.name || m.handle || "(anónimo)";
  }

  function parseDate(str) {
    if (!str) {
      return null;
    }
    var parts = String(str).split("-");
    if (parts.length !== 3) {
      return null;
    }
    var y = parseInt(parts[0], 10);
    var mo = parseInt(parts[1], 10);
    var d = parseInt(parts[2], 10);
    if (isNaN(y) || isNaN(mo) || isNaN(d)) {
      return null;
    }
    return new Date(y, mo - 1, d);
  }

  function formatScore(n) {
    if (n === null || n === undefined || isNaN(n)) {
      return "0";
    }
    // Show one decimal unless the value is an integer.
    return (Math.round(n * 10) % 10 === 0) ? String(Math.round(n)) : n.toFixed(1);
  }

  function renderMessage(container, text) {
    container.innerHTML = "";
    var p = document.createElement("p");
    p.className = "ranklist-empty";
    p.textContent = text;
    container.appendChild(p);
  }

  function renderError(container, err) {
    container.innerHTML = "";
    var p = document.createElement("p");
    p.className = "ranklist-error";
    p.textContent = "No se pudo cargar la clasificación (" +
      (err && err.message ? err.message : "error desconocido") + ").";
    container.appendChild(p);
  }
})();
