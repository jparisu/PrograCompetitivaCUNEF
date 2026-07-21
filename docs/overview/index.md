# Resumen

Esta tabla se genera automáticamente a partir de los `meta.yaml` de cada
algoritmo (mediante `tools/genoverview.py`, que escribe
`docs/assets/data/algorithms.json`). Puedes **buscar**, **filtrar por nivel o
técnica**, **ordenar** pulsando en las cabeceras y **mostrar u ocultar
columnas**.

<div class="ov-wrap" markdown="0">

  <div class="ov-controls" id="ov-controls">
    <input type="search" id="ov-filter" class="ov-input"
           placeholder="Buscar por nombre, tag o técnica…"
           aria-label="Buscar algoritmos" autocomplete="off">

    <label class="ov-field">
      <span>Nivel</span>
      <select id="ov-level" class="ov-select" aria-label="Filtrar por nivel">
        <option value="">Todos</option>
      </select>
    </label>

    <label class="ov-field">
      <span>Técnica</span>
      <select id="ov-technique" class="ov-select" aria-label="Filtrar por técnica">
        <option value="">Todas</option>
      </select>
    </label>

    <fieldset class="ov-columns" id="ov-columns" aria-label="Mostrar u ocultar columnas">
      <legend>Columnas</legend>
      <!-- checkboxes injected by overview-table.js -->
    </fieldset>
  </div>

  <div id="overview-table" class="ov-table-container">
    <p class="ov-loading">Cargando la tabla…</p>
  </div>

</div>
