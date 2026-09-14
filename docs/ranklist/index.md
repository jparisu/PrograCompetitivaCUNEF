# Ranking

Clasificación de la afiliación **CUNEF** en [Kattis](https://open.kattis.com/).
Aquí puedes ver quién va por delante, cuántos puntos lleva cada persona y cómo
han cambiado las posiciones a lo largo del tiempo. ¡Que empiece la sana competición!

!!! info "De dónde salen estos datos"
    Los datos provienen de la
    [página pública de la afiliación en Kattis](https://open.kattis.com/affiliations/cunef.edu)
    y se actualizan mediante una tarea programada (un *job* de GitHub Actions que
    ejecuta el *scraper* cada lunes). La tabla se carga al abrir la página desde
    la rama
    [`standing-data`](https://github.com/jparisu/PrograCompetitivaCUNEF/tree/standing-data)
    del repositorio, así que cada actualización se ve al instante, sin necesidad
    de volver a publicar el sitio. Eso sí: hace falta conexión: si la descarga
    falla, la página lo indica en lugar de mostrar datos antiguos.

Elige el **intervalo** que quieres mirar: un atajo (día, semana, mes, año) o un
rango de fechas a medida. Los cambios de posición y de puntos que aparecen a la
derecha son siempre los ocurridos dentro de ese intervalo. Pulsa cualquier
cabecera de la tabla para **ordenar** por esa columna.

<div class="ranklist-controls" markdown="0">
  <div class="ranklist-controls__group">
    <span class="ranklist-controls__label" id="ranklist-window-label">Comparar con:</span>
    <div class="ranklist-controls__buttons" role="group" aria-labelledby="ranklist-window-label">
      <button type="button" class="ranklist-btn" data-window="day">Día</button>
      <button type="button" class="ranklist-btn is-active" data-window="week">Semana</button>
      <button type="button" class="ranklist-btn" data-window="month">Mes</button>
      <button type="button" class="ranklist-btn" data-window="year">Año</button>
    </div>
  </div>
  <div class="ranklist-controls__group">
    <label class="ranklist-controls__label" for="ranklist-from">Desde</label>
    <input type="date" id="ranklist-from" class="ranklist-date">
    <label class="ranklist-controls__label" for="ranklist-to">Hasta</label>
    <input type="date" id="ranklist-to" class="ranklist-date">
    <button type="button" class="ranklist-reset" id="ranklist-reset">Limpiar</button>
  </div>
</div>

<div id="ranklist" class="ranklist" aria-live="polite">
  <p class="ranklist-loading">Cargando clasificación…</p>
</div>

!!! note "Privacidad"
    Estos datos proceden de la página **pública** de la afiliación de CUNEF en
    Kattis; cualquiera puede consultarlos allí. Aun así, el *scraper* admite una
    opción de anonimización (`--anonymize`) que sustituye los nombres por
    "Estudiante N" y los identificadores por un *hash* corto y estable. Si
    prefieres no aparecer con tu nombre real, escríbenos y publicaremos la versión
    anonimizada.
