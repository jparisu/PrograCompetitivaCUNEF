/*
 * cheatsheet-builder.js — visual builder for the LaTeX cheatsheet.
 *
 * Vanilla JS, no dependencies. On load, if #cheatsheet-builder exists it loads
 * the catalogue via the shared Catalog.load() (which caches the fetch and works
 * under /pr-preview/... paths), reusing Catalog's levels/labels/name helpers.
 *
 * The page does NOT compile LaTeX (GitHub Pages is static). It lets the student
 * tick algorithms and pick a title, language, style, columns and stats toggle,
 * then builds the YAML config that tools/cheatsheet.py consumes. The YAML is
 * shown in a <pre> for copy/paste and offered as a download.
 *
 * The data file is written by tools/genoverview.py. If it is missing/unreadable
 * a message is shown in the container instead of throwing.
 */
(function () {
  "use strict";

  // Levels, labels and the display-name resolver come from the shared Catalog
  // (fed by window.Taxonomy); catalog.js is loaded before this file. No local
  // duplication of the taxonomy here.
  var container = null;
  var els = {}; // named controls

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") node.className = attrs[k];
        else if (k === "text") node.textContent = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function showMessage(msg) {
    container.innerHTML = "";
    container.appendChild(el("p", { class: "csb-message", text: msg }));
  }

  // ---- YAML generation ---------------------------------------------------
  function quoteYaml(s) {
    // Double-quote and escape backslash + quote so titles with ':' are safe.
    return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"';
  }

  function buildYaml(selectedIds) {
    var lines = [];
    lines.push("# Generado por el constructor visual del Chuletario.");
    lines.push("# Compílalo con:");
    lines.push("#   python tools/cheatsheet.py --config mi_chuleta.yaml --out build/chuleta --pdf");
    lines.push("");
    lines.push("title: " + quoteYaml(els.title.value || "Mi chuletario"));
    lines.push("language: " + els.language.value);
    lines.push("style: " + els.style.value);
    lines.push("include_stats: " + (els.stats.checked ? "true" : "false"));
    lines.push("columns: " + (parseInt(els.columns.value, 10) || 3));
    lines.push("algorithms:");
    if (selectedIds.length === 0) {
      lines.push("  []  # (ninguno seleccionado todavía)");
    } else {
      selectedIds.forEach(function (id) {
        lines.push("  - " + id);
      });
    }
    return lines.join("\n") + "\n";
  }

  function selectedIds() {
    var ids = [];
    var boxes = container.querySelectorAll('input.csb-algo[type="checkbox"]:checked');
    Array.prototype.forEach.call(boxes, function (b) { ids.push(b.value); });
    return ids;
  }

  function generate() {
    var yaml = buildYaml(selectedIds());
    els.output.textContent = yaml;
    els.output.hidden = false;

    // Offer a download via a Blob URL, refreshing the link each time.
    var blob = new Blob([yaml], { type: "text/yaml;charset=utf-8" });
    if (els.download.dataset.url) URL.revokeObjectURL(els.download.dataset.url);
    var url = URL.createObjectURL(blob);
    els.download.href = url;
    els.download.dataset.url = url;
    els.download.download = "cheatsheet.yaml";
    els.download.hidden = false;
    els.copy.hidden = false;
  }

  function copyYaml() {
    var text = els.output.textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        els.copy.textContent = "¡Copiado!";
        setTimeout(function () { els.copy.textContent = "Copiar"; }, 1500);
      });
    }
  }

  // ---- UI ----------------------------------------------------------------
  function labeledSelect(labelText, options) {
    var sel = el("select", { class: "csb-select" });
    options.forEach(function (o) {
      sel.appendChild(el("option", { value: o.value, text: o.label }));
    });
    var wrap = el("label", { class: "csb-field" }, [
      el("span", { class: "csb-field-label", text: labelText }),
      sel,
    ]);
    return { wrap: wrap, input: sel };
  }

  function buildControls() {
    var titleInput = el("input", {
      class: "csb-input", type: "text", value: "Mi chuletario",
    });
    var titleField = el("label", { class: "csb-field" }, [
      el("span", { class: "csb-field-label", text: "Título" }),
      titleInput,
    ]);

    var lang = labeledSelect("Lenguaje", [
      { value: "cpp", label: "C++" },
      { value: "py", label: "Python" },
    ]);
    var style = labeledSelect("Estilo", [
      { value: "contest", label: "contest" },
      { value: "clean", label: "clean" },
      { value: "full", label: "full" },
    ]);
    var columns = labeledSelect("Columnas", [
      { value: "1", label: "1" },
      { value: "2", label: "2" },
      { value: "3", label: "3" },
      { value: "4", label: "4" },
    ]);
    columns.input.value = "3";

    var statsBox = el("input", { class: "csb-check", type: "checkbox" });
    statsBox.checked = true;
    var statsField = el("label", { class: "csb-field csb-field--inline" }, [
      statsBox,
      el("span", { class: "csb-field-label", text: "Incluir complejidad / uso" }),
    ]);

    els.title = titleInput;
    els.language = lang.input;
    els.style = style.input;
    els.columns = columns.input;
    els.stats = statsBox;

    return el("div", { class: "csb-controls" }, [
      titleField, lang.wrap, style.wrap, columns.wrap, statsField,
    ]);
  }

  function buildAlgorithmList(data) {
    var groups = {};
    data.forEach(function (a) {
      var lv = a.level || "unknown";
      (groups[lv] = groups[lv] || []).push(a);
    });

    var wrap = el("div", { class: "csb-algos" });
    var levels = Catalog.LEVELS.filter(function (lv) { return groups[lv]; });
    Object.keys(groups).forEach(function (lv) {
      if (levels.indexOf(lv) === -1) levels.push(lv);
    });

    levels.forEach(function (lv) {
      var group = el("fieldset", { class: "csb-group" });
      group.appendChild(el("legend", {
        class: "csb-group-legend",
        text: Catalog.LEVEL_LABELS[lv] || lv,
      }));
      groups[lv]
        .sort(function (x, y) { return Catalog.name(x).localeCompare(Catalog.name(y), "es"); })
        .forEach(function (a) {
          var cb = el("input", {
            class: "csb-algo", type: "checkbox", value: a.id,
          });
          var row = el("label", { class: "csb-algo-row" }, [
            cb,
            el("span", { class: "csb-algo-name", text: Catalog.name(a) }),
            el("code", { class: "csb-algo-id", text: a.id }),
          ]);
          group.appendChild(row);
        });
      wrap.appendChild(group);
    });
    return wrap;
  }

  function buildActions() {
    var genBtn = el("button", { class: "csb-btn csb-btn--primary", type: "button", text: "Generar YAML" });
    genBtn.addEventListener("click", generate);

    var selectAll = el("button", { class: "csb-btn", type: "button", text: "Seleccionar todo" });
    selectAll.addEventListener("click", function () { toggleAll(true); });
    var clearAll = el("button", { class: "csb-btn", type: "button", text: "Limpiar" });
    clearAll.addEventListener("click", function () { toggleAll(false); });

    return el("div", { class: "csb-actions" }, [genBtn, selectAll, clearAll]);
  }

  function toggleAll(on) {
    var boxes = container.querySelectorAll('input.csb-algo[type="checkbox"]');
    Array.prototype.forEach.call(boxes, function (b) { b.checked = on; });
  }

  function buildOutput() {
    var download = el("a", { class: "csb-download", hidden: "hidden", text: "Descargar cheatsheet.yaml" });
    var copy = el("button", { class: "csb-btn csb-copy", type: "button", hidden: "hidden", text: "Copiar" });
    copy.addEventListener("click", copyYaml);
    var pre = el("pre", { class: "csb-output", hidden: "hidden" });

    els.download = download;
    els.copy = copy;
    els.output = pre;

    return el("div", { class: "csb-result" }, [
      el("div", { class: "csb-result-bar" }, [download, copy]),
      pre,
    ]);
  }

  function render(data) {
    container.innerHTML = "";
    container.appendChild(buildControls());
    container.appendChild(buildAlgorithmList(data));
    container.appendChild(buildActions());
    container.appendChild(buildOutput());
  }

  function init() {
    container = document.getElementById("cheatsheet-builder");
    if (!container) return;

    Catalog.load()
      .then(function (data) {
        if (!Array.isArray(data)) throw new Error("formato inesperado");
        render(data);
      })
      .catch(function (err) {
        showMessage(
          "No se pudo cargar la lista de algoritmos (algorithms.json). " +
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
