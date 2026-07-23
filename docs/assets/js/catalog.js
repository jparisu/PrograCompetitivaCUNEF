/*
 * catalog.js — shared data + filter logic for the whole site.
 *
 * Single source of truth so the overview tables, the per-level pages, the
 * dependency graph and the type/level matrix all reuse the SAME data loading,
 * labels, links and multi-select filtering (no duplicated logic).
 *
 * Exposes window.Catalog:
 *   Catalog.LEVELS / LEVEL_LABELS / TYPES / TYPE_LABELS
 *   Catalog.load()            -> Promise<Array<item>>  (cached)
 *   Catalog.url(item)         -> absolute URL to the item's page
 *   Catalog.name(item)        -> display name (es)
 *   Catalog.makeFilters(mount, options, onChange) -> state {types:Set, levels:Set}
 *       options.lockedLevel : if set, the level group is hidden and fixed to it.
 *       options.lockedType  : if set, the type group is hidden and fixed to it.
 *   Catalog.passes(item, state) -> bool
 */
window.Catalog = (function () {
  "use strict";

  // Taxonomy (levels, types, topics, language labels) is the SINGLE source of
  // truth in tools/common.py, mirrored to the browser as window.Taxonomy by
  // tools/gentaxonomy.py -> assets/js/taxonomy.js (loaded before this file).
  // Edit the taxonomy there, not here.
  var T = window.Taxonomy || {};
  var LEVELS = T.LEVELS || [];
  var LEVEL_LABELS = T.LEVEL_LABELS || {};
  var TYPES = T.TYPES || [];
  var TYPE_LABELS = T.TYPE_LABELS || {};
  var TOPICS = T.TOPICS || {};
  var LANG_LABELS = T.LANG_LABELS || {};

  var TOPIC_IDS = T.TOPIC_IDS || Object.keys(TOPICS);
  var TOPIC_LABELS = {};
  TOPIC_IDS.forEach(function (k) { TOPIC_LABELS[k] = (TOPICS[k] || {}).label || k; });

  var TOPICS_PAGE = "content/topics/";   // site-root-relative URL of the topics page

  // Returns {icon, title, anchor} for an item's topic, or null.
  function topicInfo(item) {
    var t = item && item.topic && TOPICS[item.topic];
    if (!t) return null;
    return { icon: t.icon, title: t.label, anchor: item.topic };
  }

  // Link to the topics page section for an item's topic.
  function topicHref(item) {
    var a = (item && item.topic) || "";
    return SITE_BASE + TOPICS_PAGE + (a ? "#" + a : "");
  }

  // Site base derived from this script's own URL (works at any page depth and
  // under a /pr-preview/pr-N/ prefix).
  var SITE_BASE = (function () {
    var s = document.currentScript;
    if (!s) {
      var all = document.getElementsByTagName("script");
      for (var i = 0; i < all.length; i++) {
        if (/assets\/js\/catalog\.js/.test(all[i].src)) { s = all[i]; break; }
      }
    }
    return s && s.src ? s.src.replace(/assets\/js\/catalog\.js.*$/, "") : "";
  })();

  var _cache = null;
  function load() {
    if (_cache) return Promise.resolve(_cache);
    return fetch(SITE_BASE + "assets/data/algorithms.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (d) { _cache = Array.isArray(d) ? d : []; return _cache; });
  }

  function url(item) { return item && item.url ? SITE_BASE + item.url : "#"; }

  function name(item) {
    if (item && item.name) {
      if (typeof item.name === "string") return item.name;
      return item.name.es || item.name.en || item.id || "";
    }
    return (item && item.id) || "";
  }

  function passes(item, state) {
    if (item.wip && !(state && state.showWip)) return false;   // hidden by default
    if (state.types && !state.types.has(item.type)) return false;
    if (state.levels && !state.levels.has(item.level)) return false;
    if (state.topics && item.topic && !state.topics.has(item.topic)) return false;
    return true;
  }

  function makeFilters(mount, options, onChange) {
    options = options || {};
    var state = {
      types: new Set(options.lockedType ? [options.lockedType] : TYPES),
      levels: new Set(options.lockedLevel ? [options.lockedLevel] : LEVELS),
      topics: new Set(options.lockedTopic ? [options.lockedTopic] : TOPIC_IDS),
      showWip: false,   // "en construcción" items are hidden until toggled on
    };

    function group(title, keys, labels, set, classPrefix) {
      var wrap = document.createElement("div");
      wrap.className = "cat-fgroup";
      var t = document.createElement("span");
      t.className = "cat-fgroup__title";
      t.textContent = title;
      wrap.appendChild(t);

      var chips = [];
      keys.forEach(function (key) {
        var chip = document.createElement("button");
        chip.type = "button";
        chip.className = "cat-chip cat-chip--" + classPrefix + "-" + key +
          (set.has(key) ? " is-active" : "");
        chip.textContent = labels[key] || key;
        chip.setAttribute("aria-pressed", set.has(key) ? "true" : "false");
        chip.addEventListener("click", function () {
          if (set.has(key)) set.delete(key); else set.add(key);
          var on = set.has(key);
          chip.classList.toggle("is-active", on);
          chip.setAttribute("aria-pressed", on ? "true" : "false");
          onChange(state);
        });
        chips.push({ key: key, el: chip });
        wrap.appendChild(chip);
      });

      // "Select all" / "deselect all" for this group.
      function bulk(selectAll) {
        keys.forEach(function (key) { if (selectAll) set.add(key); else set.delete(key); });
        chips.forEach(function (c) {
          var on = set.has(c.key);
          c.el.classList.toggle("is-active", on);
          c.el.setAttribute("aria-pressed", on ? "true" : "false");
        });
        onChange(state);
      }
      function bulkBtn(text, tip, selectAll) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "cat-chip cat-chip--bulk";
        b.textContent = text; b.title = tip;
        b.addEventListener("click", function () { bulk(selectAll); });
        return b;
      }
      wrap.appendChild(bulkBtn("Todos", "Seleccionar todo", true));
      wrap.appendChild(bulkBtn("Ninguno", "Deseleccionar todo", false));

      return wrap;
    }

    // A group is shown unless it is locked (fixed to one value) or explicitly
    // hidden via options.show<Group> === false. A hidden-but-unlocked group
    // keeps its full set selected, so it simply doesn't filter anything.
    if (!options.lockedLevel && options.showLevel !== false) {
      mount.appendChild(group("Nivel", LEVELS, LEVEL_LABELS, state.levels, "level"));
    }
    if (!options.lockedType && options.showType !== false) {
      mount.appendChild(group("Tipo", TYPES, TYPE_LABELS, state.types, "type"));
    }
    if (!options.lockedTopic && options.showTopic !== false) {
      mount.appendChild(group("Tema", TOPIC_IDS, TOPIC_LABELS, state.topics, "topic"));
    }

    if (options.showState === false) return state;

    // "Show under-construction" toggle (off by default -> WIP items hidden).
    var eg = document.createElement("div");
    eg.className = "cat-fgroup";
    var et = document.createElement("span");
    et.className = "cat-fgroup__title"; et.textContent = "Estado";
    eg.appendChild(et);
    var wchip = document.createElement("button");
    wchip.type = "button"; wchip.className = "cat-chip cat-chip--wip";
    wchip.textContent = "🏗️ En construcción";
    wchip.title = "Mostrar también los elementos sin implementar";
    wchip.setAttribute("aria-pressed", "false");
    wchip.addEventListener("click", function () {
      state.showWip = !state.showWip;
      wchip.classList.toggle("is-active", state.showWip);
      wchip.setAttribute("aria-pressed", state.showWip ? "true" : "false");
      onChange(state);
    });
    eg.appendChild(wchip);
    mount.appendChild(eg);

    return state;
  }

  function langLabel(ext) { return LANG_LABELS[ext] || ext; }

  return {
    LEVELS: LEVELS, LEVEL_LABELS: LEVEL_LABELS, TYPES: TYPES, TYPE_LABELS: TYPE_LABELS,
    TOPICS: TOPICS, TOPIC_IDS: TOPIC_IDS, TOPIC_LABELS: TOPIC_LABELS, TOPICS_PAGE: TOPICS_PAGE,
    LANG_LABELS: LANG_LABELS, langLabel: langLabel,
    topicInfo: topicInfo, topicHref: topicHref,
    SITE_BASE: SITE_BASE, load: load, url: url, name: name,
    makeFilters: makeFilters, passes: passes,
  };
})();
