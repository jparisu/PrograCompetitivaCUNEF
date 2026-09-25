/*
 * Ranking page (docs/ranklist/) — vanilla JS, no external libraries.
 *
 * Loads standings.json (a history of dated snapshots) from the standing-data
 * branch and renders one snapshot as a list of rows, annotating each member with
 * the change in position and points relative to an earlier snapshot.
 *
 * Which two snapshots are compared depends on the active range mode:
 *   - "preset" (default): current = the newest snapshot; baseline = the newest
 *     snapshot that is at least one window (day / week / month / year) older.
 *   - "custom": the user gives a start and/or end date, and we compare the FIRST
 *     snapshot inside that range against the LAST one. Both ends are clamped
 *     inside the range, so the table shows exactly the change that happened
 *     within it. An empty end means "up to the newest", an empty start means
 *     "from the oldest".
 *
 * Rows can be sorted by any column (see SORTS). Sorting only reorders the rows:
 * the "#" each member shows is always their real rank by score in the displayed
 * snapshot, never the row index, so sorting by name does not renumber anyone.
 *
 * The data is fetched from the `standing-data` branch of the repository, NOT
 * from the built site. That branch is an orphan holding a single standings.json,
 * written weekly by .github/workflows/kattis.yml; `main` is protected, so the
 * bot cannot commit there. Reading the branch directly means a scrape is live as
 * soon as it is pushed — the site never has to be rebuilt for new standings.
 *
 * There is deliberately NO fallback to a copy inside the site. A stale but
 * plausible-looking table would hide a broken pipeline; a visible error does not.
 * So if the fetch fails, the page says so (see renderError).
 */
(function () {
  "use strict";

  // Raw file on the standing-data branch. `refs/heads/` is spelled out so a tag
  // or another ref of the same name could never resolve here instead.
  var DATA_URL = "https://raw.githubusercontent.com/jparisu/PrograCompetitivaCUNEF" +
                 "/refs/heads/standing-data/standings.json";

  // Days subtracted from the current snapshot date for each preset window.
  var WINDOW_DAYS = { day: 1, week: 7, month: 30, year: 365 };

  // Sortable columns. `get` pulls the value out of a row object (see buildRows);
  // `dir` is the direction applied on the FIRST click of that column, chosen so
  // the first click always shows the most interesting end of the scale.
  // Returning null/undefined sinks a row to the bottom whatever the direction —
  // that is how "nuevo" members (no baseline) and a missing `solved` behave.
  var SORTS = {
    rank: {
      dir: "asc",
      get: function (row) { return row.rank; }
    },
    name: {
      dir: "asc",
      get: function (row) { return displayName(row.member).toLocaleLowerCase("es"); }
    },
    score: {
      dir: "desc",
      get: function (row) { return row.member.score || 0; }
    },
    solved: {
      dir: "desc",
      get: function (row) {
        var s = row.member.solved;
        return (s === null || s === undefined) ? null : s;
      }
    },
    dpos: {
      dir: "desc",
      get: function (row) { return row.deltaPos; }
    },
    dscore: {
      dir: "desc",
      get: function (row) { return row.deltaScore; }
    }
  };

  // Header cells, in grid order. Each entry is one column of .ranklist__row;
  // `keys` holds the sort buttons stacked inside that cell (the stats and change
  // columns each show two values, so they get two buttons).
  var COLUMNS = [
    { cls: "ranklist__pos", keys: [{ key: "rank", label: "#", title: "Posición por puntos" }] },
    { cls: "ranklist__main", keys: [{ key: "name", label: "Nombre", title: "Orden alfabético" }] },
    { cls: "ranklist__stats", keys: [
      { key: "score", label: "Puntos", title: "Puntuación" },
      { key: "solved", label: "Resueltos", title: "Problemas resueltos" }
    ] },
    { cls: "ranklist__change", keys: [
      { key: "dpos", label: "Δ Pos.", title: "Posiciones ganadas en el intervalo" },
      { key: "dscore", label: "Δ Pts.", title: "Puntos ganados en el intervalo" }
    ] }
  ];

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

    var state = {
      container: container,
      snapshots: snapshots,
      isSample: !!(data && data.sample),
      mode: "preset",
      window: getInitialWindow(),
      from: "",
      to: "",
      sortKey: "rank",
      sortDir: SORTS.rank.dir
    };

    wireWindowButtons(state);
    wireDateInputs(state);
    render(state);
  }

  function getInitialWindow() {
    var active = document.querySelector(".ranklist-btn[data-window].is-active");
    if (active && WINDOW_DAYS.hasOwnProperty(active.getAttribute("data-window"))) {
      return active.getAttribute("data-window");
    }
    return "week";
  }

  // --- Controls ------------------------------------------------------------ //

  function windowButtons() {
    return document.querySelectorAll(".ranklist-btn[data-window]");
  }

  function wireWindowButtons(state) {
    var buttons = windowButtons();
    Array.prototype.forEach.call(buttons, function (btn) {
      btn.addEventListener("click", function () {
        var win = btn.getAttribute("data-window");
        if (!WINDOW_DAYS.hasOwnProperty(win)) {
          return;
        }
        // Choosing a preset leaves custom mode and clears the date pickers, so
        // the two ways of picking a range can never disagree on screen.
        state.mode = "preset";
        state.window = win;
        state.from = "";
        state.to = "";
        syncControls(state);
        render(state);
      });
    });
  }

  function wireDateInputs(state) {
    var from = document.getElementById("ranklist-from");
    var to = document.getElementById("ranklist-to");
    var reset = document.getElementById("ranklist-reset");

    // Bound the pickers to the dates we actually have data for.
    var first = state.snapshots[0].date;
    var last = state.snapshots[state.snapshots.length - 1].date;
    [from, to].forEach(function (input) {
      if (!input) {
        return;
      }
      input.setAttribute("min", first);
      input.setAttribute("max", last);
      input.addEventListener("change", function () {
        state.from = from ? from.value : "";
        state.to = to ? to.value : "";
        // Touching a date switches to custom mode; clearing both goes back to
        // the presets rather than leaving an empty custom range selected.
        state.mode = (state.from || state.to) ? "custom" : "preset";
        syncControls(state);
        render(state);
      });
    });

    if (reset) {
      reset.addEventListener("click", function () {
        state.mode = "preset";
        state.from = "";
        state.to = "";
        syncControls(state);
        render(state);
      });
    }

    syncControls(state);
  }

  // Push `state` back onto the controls so they always reflect what is rendered.
  function syncControls(state) {
    var isPreset = state.mode === "preset";
    Array.prototype.forEach.call(windowButtons(), function (btn) {
      var on = isPreset && btn.getAttribute("data-window") === state.window;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });

    var from = document.getElementById("ranklist-from");
    var to = document.getElementById("ranklist-to");
    if (from) {
      from.value = state.from;
    }
    if (to) {
      to.value = state.to;
    }

    var reset = document.getElementById("ranklist-reset");
    if (reset) {
      reset.disabled = isPreset;
    }
  }

  // --- Range selection ----------------------------------------------------- //

  // Resolve the active range to the two snapshots to compare.
  // Returns { current, comparison } or { error } — comparison may be null when
  // the range holds a single snapshot (nothing to compare against).
  function selectRange(state) {
    if (state.mode === "custom") {
      return selectCustomRange(state);
    }
    return selectPresetRange(state);
  }

  function selectCustomRange(state) {
    var from = state.from ? parseDate(state.from) : null;
    var to = state.to ? parseDate(state.to) : null;
    if (from && to && from.getTime() > to.getTime()) {
      return { error: "La fecha inicial es posterior a la final." };
    }

    var inRange = state.snapshots.filter(function (snap) {
      var d = parseDate(snap.date);
      if (!d) {
        return false;
      }
      if (from && d.getTime() < from.getTime()) {
        return false;
      }
      if (to && d.getTime() > to.getTime()) {
        return false;
      }
      return true;
    });

    if (inRange.length === 0) {
      return { error: "No hay instantáneas en el intervalo seleccionado." };
    }
    // First vs last snapshot inside the range: exactly the change it contains.
    return {
      current: inRange[inRange.length - 1],
      comparison: inRange.length > 1 ? inRange[0] : null
    };
  }

  function selectPresetRange(state) {
    var current = state.snapshots[state.snapshots.length - 1];
    var currentDate = parseDate(current.date);
    if (!currentDate) {
      return { current: current, comparison: null };
    }
    var cutoff = new Date(currentDate.getTime());
    cutoff.setDate(cutoff.getDate() - WINDOW_DAYS[state.window]);

    // Newest snapshot at or before the cutoff, excluding `current` itself.
    var best = null;
    for (var i = 0; i < state.snapshots.length; i++) {
      var snap = state.snapshots[i];
      if (snap === current) {
        continue;
      }
      var d = parseDate(snap.date);
      if (!d || d.getTime() > cutoff.getTime()) {
        continue;
      }
      if (!best || d.getTime() > parseDate(best.date).getTime()) {
        best = snap;
      }
    }
    return { current: current, comparison: best };
  }

  // --- Rendering ----------------------------------------------------------- //

  function render(state) {
    var container = state.container;
    container.innerHTML = "";

    if (state.isSample) {
      container.appendChild(buildBanner(
        "Datos de ejemplo: esta clasificación es ficticia y sirve para la vista previa."
      ));
    }

    var range = selectRange(state);
    if (range.error) {
      container.appendChild(buildMessage(range.error));
      return;
    }

    var current = range.current;
    if (!current || !Array.isArray(current.members) || current.members.length === 0) {
      container.appendChild(buildMessage("La instantánea seleccionada no contiene miembros."));
      return;
    }

    container.appendChild(buildMeta(state, current, range.comparison));

    var rows = buildRows(current, range.comparison);
    var maxScore = rows.reduce(function (m, row) {
      return Math.max(m, row.member.score || 0);
    }, 0) || 1;

    sortRows(rows, state.sortKey, state.sortDir);

    container.appendChild(buildHeader(state));

    var list = document.createElement("ol");
    list.className = "ranklist__rows";
    rows.forEach(function (row) {
      list.appendChild(buildRow(row, maxScore));
    });
    container.appendChild(list);
  }

  // One row object per member of the displayed snapshot, carrying everything the
  // sort comparators and the renderer need. deltaPos / deltaScore are null when
  // the member has no counterpart in the baseline snapshot ("nuevo").
  function buildRows(current, comparison) {
    var ranks = rankByScore(current.members);
    var prevIndex = comparison ? indexMembers(comparison.members) : null;
    var prevRanks = comparison ? rankByScore(comparison.members) : null;

    return current.members.map(function (m) {
      var key = memberKey(m);
      var prev = prevIndex ? prevIndex[key] : null;
      return {
        member: m,
        rank: ranks[key],
        hasBaseline: !!prevIndex,
        isNew: !!prevIndex && !prev,
        deltaPos: prev ? (prevRanks[key] - ranks[key]) : null,
        deltaScore: prev ? ((m.score || 0) - (prev.score || 0)) : null
      };
    });
  }

  function sortRows(rows, key, dir) {
    var spec = SORTS[key] || SORTS.rank;
    rows.sort(function (a, b) {
      var av = spec.get(a);
      var bv = spec.get(b);
      var aMissing = (av === null || av === undefined);
      var bMissing = (bv === null || bv === undefined);
      if (aMissing || bMissing) {
        // Rows without a value stay at the bottom in both directions. When
        // NEITHER has one — sorting by a change column with no baseline in the
        // range — fall back to rank so the table keeps a meaningful order
        // instead of the order the members happen to appear in the JSON.
        if (aMissing && bMissing) {
          return a.rank - b.rank;
        }
        return aMissing ? 1 : -1;
      }
      var cmp = (typeof av === "string") ? av.localeCompare(bv, "es") : (av - bv);
      if (dir === "desc") {
        cmp = -cmp;
      }
      // Rank is the tie-break everywhere, so the order is always deterministic.
      return cmp || (a.rank - b.rank);
    });
  }

  function buildHeader(state) {
    var head = document.createElement("div");
    head.className = "ranklist__head";

    var label = document.createElement("span");
    label.className = "ranklist__head-label";
    label.textContent = "Ordenar por:";
    head.appendChild(label);

    COLUMNS.forEach(function (col) {
      var cell = document.createElement("div");
      cell.className = "ranklist__head-cell " + col.cls;
      col.keys.forEach(function (item) {
        cell.appendChild(buildSortButton(state, item));
      });
      head.appendChild(cell);
    });

    return head;
  }

  function buildSortButton(state, item) {
    var active = state.sortKey === item.key;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "ranklist__sort" + (active ? " is-sorted" : "");
    btn.title = item.title + " (clic para ordenar)";
    btn.setAttribute("data-sort", item.key);
    btn.setAttribute("aria-pressed", active ? "true" : "false");

    btn.appendChild(document.createTextNode(item.label));
    var caret = document.createElement("span");
    caret.className = "ranklist__caret";
    caret.setAttribute("aria-hidden", "true");
    caret.textContent = active ? (state.sortDir === "asc" ? "▲" : "▼") : "";
    btn.appendChild(caret);

    btn.addEventListener("click", function () {
      if (state.sortKey === item.key) {
        state.sortDir = (state.sortDir === "asc") ? "desc" : "asc";
      } else {
        state.sortKey = item.key;
        state.sortDir = SORTS[item.key].dir;
      }
      render(state);
    });

    return btn;
  }

  function buildRow(row, maxScore) {
    var m = row.member;
    var li = document.createElement("li");
    li.className = "ranklist__row";

    // Position number — always the rank by score, never the row index.
    var pos = document.createElement("div");
    pos.className = "ranklist__pos";
    pos.textContent = "#" + row.rank;
    li.appendChild(pos);

    // Name / handle + progress bar.
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

    // Change vs the baseline snapshot.
    li.appendChild(buildChange(row));

    return li;
  }

  function buildChange(row) {
    var box = document.createElement("div");
    box.className = "ranklist__change";

    if (!row.hasBaseline) {
      // No baseline snapshot available for this range.
      var none = document.createElement("span");
      none.className = "ranklist__arrow ranklist__arrow--same";
      none.textContent = "—";
      none.title = "Sin histórico para este intervalo";
      box.appendChild(none);
      return box;
    }

    if (row.isNew) {
      var badge = document.createElement("span");
      badge.className = "ranklist__badge ranklist__badge--new";
      badge.textContent = "nuevo";
      box.appendChild(badge);
      return box;
    }

    var delta = row.deltaPos; // positive => improved (moved up)
    var arrow = document.createElement("span");
    arrow.className = "ranklist__arrow";
    if (delta > 0) {
      arrow.classList.add("ranklist__arrow--up");
      arrow.textContent = "▲ " + delta;
      arrow.title = "Sube " + delta + " posición(es)";
    } else if (delta < 0) {
      arrow.classList.add("ranklist__arrow--down");
      arrow.textContent = "▼ " + Math.abs(delta);
      arrow.title = "Baja " + Math.abs(delta) + " posición(es)";
    } else {
      arrow.classList.add("ranklist__arrow--same");
      arrow.textContent = "=";
      arrow.title = "Misma posición";
    }
    box.appendChild(arrow);

    // Points gained across the range.
    var gain = row.deltaScore;
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
    gained.title = "Puntos ganados en este intervalo";
    box.appendChild(gained);

    return box;
  }

  function buildMeta(state, current, comparison) {
    var meta = document.createElement("p");
    meta.className = "ranklist__updated";
    var txt = "Clasificación a fecha " + current.date + ".";
    if (comparison) {
      txt += " Comparando con la instantánea del " + comparison.date + ".";
    } else if (state.mode === "custom") {
      txt += " Solo hay una instantánea en el intervalo: no se puede comparar.";
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

  function buildMessage(text) {
    var p = document.createElement("p");
    p.className = "ranklist-empty";
    p.textContent = text;
    return p;
  }

  // --- Helpers ------------------------------------------------------------- //

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
    container.appendChild(buildMessage(text));
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
