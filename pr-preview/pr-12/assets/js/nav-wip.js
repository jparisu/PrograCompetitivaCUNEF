/*
 * nav-wip.js — gray out not-yet-implemented (WIP) elements in the left sidebar.
 *
 * Data-driven, same approach as page-icon.js: match each primary-nav link
 * against the catalogue and add `.md-nav__link--wip` to the ones whose target
 * page is flagged `wip: true`. The class is styled (dimmed) in theme.css.
 * No per-page editing and no hard-coded list — it follows algorithms.json.
 */
(function () {
  "use strict";

  function norm(p) {
    return "/" + String(p).replace(/^\/+/, "").replace(/\/+$/, "");
  }

  function apply(wipUrls) {
    var links = document.querySelectorAll(".md-nav--primary a.md-nav__link[href]");
    links.forEach(function (a) {
      var path;
      try { path = norm(new URL(a.href, location.href).pathname); }
      catch (e) { return; }
      for (var i = 0; i < wipUrls.length; i++) {
        // wipUrls[i] starts with "/", so this only matches on a full segment
        // boundary (".../a-star" won't match ".../a-star-extended").
        if (path === wipUrls[i] || path.endsWith(wipUrls[i])) {
          a.classList.add("md-nav__link--wip");
          break;
        }
      }
    });
  }

  function init() {
    if (!window.Catalog) return;
    Catalog.load().then(function (data) {
      var wip = data
        .filter(function (it) { return it.wip && it.url; })
        .map(function (it) { return norm(it.url); });
      if (wip.length) apply(wip);
    }).catch(function () {});
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
