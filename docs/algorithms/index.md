# Contenidos

Todo el contenido en una tabla: **técnicas**, **algoritmos** y **estructuras**. Puedes
**buscar**, **filtrar por nivel, tipo, tema o estado** (incluir los elementos *en
construcción*), **ordenar** pulsando en las cabeceras y **mostrar u ocultar columnas**.
Usa el menú lateral para navegar por nivel.

!!! note
    La tabla se genera automáticamente a partir de los `meta.yaml` de cada elemento
    (mediante `tools/genoverview.py`, que escribe `docs/assets/data/algorithms.json`).

<div class="ov-wrap" markdown="0">

  <div class="ov-controls" id="ov-controls">
    <input type="search" id="ov-filter" class="ov-input"
           placeholder="Buscar por nombre, tag o técnica…"
           aria-label="Buscar algoritmos" autocomplete="off">



    <fieldset class="ov-columns" id="ov-columns" aria-label="Mostrar u ocultar columnas">
      <legend>Columnas</legend>
      <!-- checkboxes injected by overview-table.js -->
    </fieldset>
  </div>

  <div id="overview-table" class="ov-table-container">
    <p class="ov-loading">Cargando la tabla…</p>
  </div>

</div>
