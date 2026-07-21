# Scripts del proyecto

Todos los scripts están en `tools/`, escritos en Python, y comparten la lógica común de
`tools/common.py`. Cada uno tiene ayuda detallada con `--help`.

Instala las dependencias una vez:

```bash
pip install -r tools/requirements.txt
```

## `gen.py` — orquestador

Ejecuta de una vez todas las generaciones (código, tests, resumen).

```bash
python tools/gen.py status                 # muestra qué se crearía/modificaría (no escribe)
python tools/gen.py generate               # crea/actualiza los ficheros derivados
python tools/gen.py generate --only code --algo fenwick-tree
```

`status` termina con error si algo está desactualizado — es lo que usa la CI para pedirte
que regeneres antes de fusionar.

## `gencode.py` — versiones del código

Genera las versiones `clean` (sin comentarios) y `contest` (nombres cortos) a partir de la
versión `full`.

```bash
python tools/gencode.py            # genera lo que falte
python tools/gencode.py --check    # dry-run
```

- Nunca sobrescribe un fichero escrito a mano (sin la marca `AUTO-GENERATED`).
- En Python, `contest` renombra variables locales de forma segura. En C++ es una versión
  compacta (sin comentarios): conviene repasar/reescribir a mano si quieres nombres cortos.

## `gentests.py` — fixtures de test

Crea los ficheros `test/cases/NN.in` y `NN.out` a partir del bloque `examples` del
`meta.yaml`. Así, los ejemplos de la documentación **son** los tests.

```bash
python tools/gentests.py
```

## `genoverview.py` — datos de la tabla resumen

Genera `docs/assets/data/algorithms.json`, que alimenta la [tabla dinámica](../overview/index.md).

```bash
python tools/genoverview.py
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
