# Añadir un algoritmo

Un algoritmo es **una carpeta** dentro de `docs/algorithms/<tema>/<algoritmo>/`. Sigue
estos pasos.

## 1. Crea la carpeta

```text
docs/algorithms/<tema>/<algoritmo>/
├── meta.yaml           # metadatos (fuente de la verdad)
├── es.md / index.md    # explicación en español
├── code/
│   ├── <algo>.v1.full.cpp
│   └── <algo>.v1.full.py
└── test/
    ├── driver.cpp      # (opcional, para ejecutar los tests)
    └── driver.py
```

Puedes copiar una carpeta existente (por ejemplo `data-structures/fenwick-tree/`) como
plantilla.

## 2. Escribe el `meta.yaml`

Es el corazón de todo: de aquí se generan la tabla resumen, el grafo, el chuletario y los
tests. Campos principales:

```yaml
id: segment-tree                 # identificador único, en kebab-case
topic: data-structures
name: { es: "Árbol de segmentos", en: "Segment tree" }
level: intermediate              # base | beginner | intermediate | advanced | expert
difficulty: 4.0
techniques: [divide-and-conquer]
tags: [range-query, point-update]
prerequisites: [fenwick-tree]    # ids de otros algoritmos (para el grafo)
current_version: v1
signature:                       # API pública (se conserva en la versión contest)
  type: SegmentTree
  methods: ["void update(int i, int x)", "int query(int l, int r)"]
stats:
  complexity: { build: "O(n)", update: "O(log n)", query: "O(log n)" }
  use_case: { es: "...", en: "..." }
references:
  - { title: "CP-Algorithms", url: "https://cp-algorithms.com/..." }
examples:                        # ¡esto son también los tests!
  - input: |
      ...
    expected_output: |
      ...
```

### Formato: `snippet` (por defecto) o `article`

Cada elemento tiene un **formato**, que decide qué esperan de él las herramientas:

- **`snippet`** (por defecto, no hace falta escribirlo): la página es *una implementación
  canónica*. **Debe** tener un fichero `*.full.*` y al menos un `examples:`. A partir de ahí
  se autogeneran las versiones `clean`/`contest`, los tests y su entrada en el chuletario.
  `python tools/gen.py status` **falla** si un `snippet` no-WIP no cumple esto.

- **`article`**: la página es *prosa con ejemplos libres* (por ejemplo, una técnica como
  bucles, recursión o complejidad). No tiene una implementación versionada, así que las
  herramientas de código, tests y chuletario **la ignoran**. Actívalo con:

  ```yaml
  format: article
  ```

Un `article` puede aun así aparecer en el chuletario si lo pides explícitamente con una
lista `cheatsheet:` (ficheros concretos a incluir tal cual):

```yaml
format: article
cheatsheet:
  - { file: code/ejemplo.cpp, title: "Lectura rápida", language: cpp }
```

Marca en su lugar `wip: true` si el elemento existe pero aún no está implementado: también
queda exento de la validación y aparece con el icono de "en construcción" 🏗️.

## 3. Escribe el código `full`

Puedes escribir solo la versión **`full`** (comentada, con doc-string de cabecera) en C++ y Python.
Las versiones `clean` y `contest` se autogenerarán a partir de esta.

Sin embargo, puedes escribir las otras versiones si quieres.
Esto puede ser útil para personalizar una de las versiones, o añadir una optimización del lenguaje.

## 4. Genera lo derivado

```bash
python tools/gen.py generate          # crea lo que falte (no toca lo que ya existe)
python tools/gen.py generate --force  # regenera también lo ya existente
```

Esto crea `*.clean.*`, `*.contest.*`, los ficheros `test/cases/*.in|*.out` y actualiza la
tabla resumen. Revisa las versiones `contest` (para C++ conviene repasarlas a mano).

Por defecto **no se sobrescribe** ningún fichero de código que ya exista, así que puedes
escribir tu propia versión `clean`/`contest`. Para controlarlo fichero a fichero tienes las
directivas `no-clean`, `no-contest` y `no-generate` (ver [Scripts](scripts.md#directivas-de-generacion-comentarios-ocultos)).

## 5. Comprueba y previsualiza

```bash
python tools/gen.py status     # debe decir "up to date"
mkdocs serve                   # abre http://127.0.0.1:8000 y revisa tu página
```

## Imágenes y gifs (opcional pero recomendado)

Una imagen o un gif ayuda muchísimo a entender un algoritmo. Guárdalos **dentro de la
carpeta del algoritmo**, en `media/`, y enlázalos de forma **relativa** desde la página:

```markdown
<figure class="algo-figure">
  <img src="media/mi-diagrama.svg" alt="Descripción para accesibilidad">
  <figcaption>Breve explicación de lo que muestra.</figcaption>
</figure>
```

Formatos:

- **SVG** dibujado a mano (como el de [Búsqueda binaria](../algorithms/searching/binary-search-array/index.md)):
  ligero, nítido y se adapta al modo claro/oscuro si usas `fill: currentColor` para el texto.
- **PNG/JPG** para capturas.
- **GIF** para animaciones (ideal para recorridos, ordenaciones, etc.).

### Usar imágenes de Wikipedia / Wikimedia Commons

Muchas figuras y gifs de [Wikimedia Commons](https://commons.wikimedia.org/) son de uso
libre. Para usarlas correctamente:

1. **Descarga** el archivo y guárdalo en `media/` (no enlaces directamente a Wikipedia:
   el enlace puede romperse y así la web funciona sin conexión).
2. Comprueba la **licencia** (CC BY, CC BY-SA, dominio público…).
3. Añade la **atribución** en el `figcaption`, por ejemplo:

```markdown
<figure class="algo-figure">
  <img src="media/binary-search.gif" alt="Búsqueda binaria animada">
  <figcaption>
    Animación: <a href="URL-DEL-ARCHIVO">Autor</a>,
    <a href="URL-LICENCIA">CC BY-SA 4.0</a>, vía Wikimedia Commons.
  </figcaption>
</figure>
```

También puedes registrar la imagen principal en `meta.yaml` con el campo `media:`.

## 6. Añádete a los autores

Añade tu fila (nombre, web y GitHub) a la página de [Autores](authors.md), en el mismo
Pull Request. Todo el que contribuye aparece ahí.

## 7. Abre el Pull Request

Sigue [Git y GitHub](git-github.md). El robot te dará un enlace de vista previa.

!!! warning "Versionar sin romper"
    Si mejoras un algoritmo existente sin querer romper la versión anterior, crea una
    versión nueva: `<algo>.v2.full.cpp`, y actualiza `current_version: v2` en el
    `meta.yaml`. La `v1` sigue disponible.
