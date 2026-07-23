# Scripts del proyecto

Todos los scripts están en `tools/`, escritos en Python, y comparten la lógica común de
`tools/common.py`. Cada uno tiene ayuda detallada con `--help`.

Instala las dependencias una vez:

```bash
pip install -r tools/requirements.txt
```

## `gen.py` — orquestador

Ejecuta de una vez todas las generaciones: **código** (`gencode`), **tests** (`gentests`),
**datos del resumen** (`genoverview` → `algorithms.json`), **taxonomía del front-end**
(`gentaxonomy` → `taxonomy.js`) y **navegación** (`gennav` → el `nav` de `mkdocs.yml`).

```bash
python tools/gen.py status                 # muestra qué se crearía/modificaría (no escribe)
python tools/gen.py generate               # crea SOLO los ficheros derivados que falten
python tools/gen.py generate --force       # regenera también los que ya existen
python tools/gen.py generate --only code --algo fenwick-tree
```

`status` termina con error si falta algún fichero derivado (o si la navegación/taxonomía
están desactualizadas), y también valida que cada `topic` sea uno conocido — es lo que usa
la CI para pedirte que regeneres antes de fusionar. El chuletario **ya no** forma parte de
este orquestador: lo reconstruye su propio workflow (ver `cheatsheet.py`).

## `gencode.py` — versiones del código

Genera las versiones `clean` (sin comentarios) y `contest` (nombres cortos) a partir de la
versión `full`.

```bash
python tools/gencode.py            # crea SOLO las versiones que falten
python tools/gencode.py --force    # regenera también las que ya existen
python tools/gencode.py --check    # dry-run
```

- **Por defecto no sobrescribe ficheros existentes**: solo crea los que faltan. Así puedes
  escribir tu propia `clean`/`contest` y conservarla. Usa `--force` para regenerarlos.
- En Python, `contest` renombra variables locales de forma segura. En C++ es una versión
  compacta (sin comentarios): conviene repasar/reescribir a mano si quieres nombres cortos.

### Directivas de generación (comentarios ocultos)

Dentro de un comentario **oculto** (`//!` en C++, `#!` en Python) puedes escribir directivas
que afinan la generación fichero a fichero:

| Directiva | Dónde | Efecto |
|-----------|-------|--------|
| `no-clean`    | en el `full` | no genera su versión `clean` |
| `no-contest`  | en el `full` | no genera su versión `contest` |
| `no-generate` | en cualquier fichero | nunca lo sobrescribe, ni con `--force` |

Ejemplo — una `contest` escrita a mano que no debe tocarse:

```cpp
//! no-generate
// (tu versión optimizada a mano)
```

## `gentests.py` — fixtures de test

Crea los ficheros `test/cases/NN.in` y `NN.out` a partir del bloque `examples` del
`meta.yaml`. Así, los ejemplos de la documentación **son** los tests.

```bash
python tools/gentests.py
```

## `runtests.py` — ejecuta los tests

Compila y ejecuta cada variante de código `(lenguaje × versión × estilo)` contra los casos
generados por `gentests.py` y compara la salida. La CI lo ejecuta en cada Pull Request.

```bash
python tools/runtests.py                       # todo
python tools/runtests.py --algo fenwick-tree   # un solo elemento
```

## `genoverview.py` — datos de la tabla resumen

Genera `docs/assets/data/algorithms.json`, que alimenta la [tabla de algoritmos](../content/index.md).

```bash
python tools/genoverview.py
```

## `gentaxonomy.py` — taxonomía del front-end

Genera `docs/assets/js/taxonomy.js` (niveles, tipos, temas, etiquetas de lenguaje) a partir
de `tools/common.py`, que es la **fuente única** de la taxonomía. El JavaScript la lee como
`window.Taxonomy`, así que no hay que duplicar esas listas en los `.js`.

```bash
python tools/gentaxonomy.py
```

## `gennav.py` — navegación del sitio

Genera el bloque `nav:` de `mkdocs.yml` a partir de los `meta.yaml`, **agrupado por nivel**.
Por eso añadir un elemento no requiere editar el menú a mano.

```bash
python tools/gennav.py
```

## `scrape_kattis.py` — ranking de Kattis

Descarga la clasificación de la afiliación de CUNEF en Kattis y guarda el histórico.

```bash
python tools/scrape_kattis.py                # actualiza docs/assets/data/standings.json
python tools/scrape_kattis.py --dry-run -v   # solo muestra lo que ha leído
python tools/scrape_kattis.py --anonymize    # oculta nombres (privacidad)
```

## `cheatsheet.py` — chuletario en LaTeX/PDF

Genera un chuletario a partir de un YAML de configuración.

```bash
python tools/cheatsheet.py --config templates/cheatsheet.example.yaml --out build/chuleta --pdf
python tools/cheatsheet.py --all --language cpp --style contest --out build/todo
```

Consulta la página [Chuletario](../cheatsheet/index.md) para el formato del YAML y el
constructor visual.
