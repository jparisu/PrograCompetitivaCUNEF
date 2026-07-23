/*
 * Header navigation dropdowns.
 *
 * TODO(nav-dropdown): the click-to-open behaviour is PARKED because the menu
 * would not reveal reliably in the browser (works in the built HTML/CSS, fails
 * live — likely a Material/stacking interaction still to be understood).
 *
 * For now the top-level tabs simply NAVIGATE to their section index page (the
 * plain <a href> is left untouched here — we intentionally do NOT preventDefault
 * so the button is useful). The submenu is still available on HOVER via CSS
 * (assets/css/theme.css), as a best effort.
 *
 * When revisiting: re-enable a click toggle on `.cunef-has-menu > .md-tabs__link`
 * (add/remove `.cunef-open`) and on `.cunef-menu__label` (`.cunef-subopen`),
 * plus close-on-outside-click / Escape. See git history for the previous
 * implementation.
 */
(function () {
  "use strict";
  // Intentionally a no-op for top-level clicks so navigation works.
  // (Hover reveal is handled entirely in CSS.)
})();
