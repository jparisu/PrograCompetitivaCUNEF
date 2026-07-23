/*
 * page-icon.js — shows the topic icon to the right of a content page's title.
 *
 * Data-driven: matches the current page URL against the catalogue and appends
 * the item's topic (or sub-topic) icon to the <h1>. No per-page editing needed.
 */
(function () {
  "use strict";

  function init() {
    if (!window.Catalog) return;
    var h1 = document.querySelector(".md-typeset h1") ||
             document.querySelector("article h1") ||
             document.querySelector("h1");
    if (!h1) return;

    Catalog.load().then(function (data) {
      var here = location.pathname.replace(/\/+$/, "");
      var best = null, bestLen = -1;
      data.forEach(function (it) {
        if (!it.url) return;
        var u = "/" + it.url.replace(/^\/+/, "").replace(/\/+$/, "");
        if (here.endsWith(u) && u.length > bestLen) { best = it; bestLen = u.length; }
      });
      if (!best) return;
      var ti = Catalog.topicInfo(best);
      if (!ti) return;
      var span = document.createElement("a");
      span.className = "topic-icon topic-icon--title topic-icon--link";
      span.textContent = ti.icon;
      span.title = ti.title;
      span.href = Catalog.topicHref(best);
      h1.appendChild(document.createTextNode(" "));
      h1.appendChild(span);
    }).catch(function () {});
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
