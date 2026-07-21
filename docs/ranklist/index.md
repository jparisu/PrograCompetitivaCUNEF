# Ranking

Clasificación de la afiliación **CUNEF** en [Kattis](https://open.kattis.com/).
Aquí puedes ver quién va por delante, cuántos puntos lleva cada persona y cómo
han cambiado las posiciones a lo largo del tiempo. ¡Que empiece la sana competición!

!!! info "De dónde salen estos datos"
    Los datos provienen de la
    [página pública de la afiliación en Kattis](https://open.kattis.com/affiliations/cunef.edu)
    y se actualizan mediante una tarea programada (un *job* de GitHub Actions que
    ejecuta el *scraper* periódicamente). Si el sitio se abre sin conexión, se
    mostrarán datos de ejemplo.

<div class="ranklist-controls" markdown="0">
  <span class="ranklist-controls__label">Comparar con:</span>
  <div class="ranklist-controls__buttons" role="group" aria-label="Ventana de comparación">
    <button type="button" class="ranklist-btn" data-window="day">Día</button>
    <button type="button" class="ranklist-btn is-active" data-window="week">Semana</button>
    <button type="button" class="ranklist-btn" data-window="year">Año</button>
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
