# Añadir un elemento

Un elemento (algoritmo, técnica o estructura) es **una carpeta** dentro de
`docs/content/<tema>/<id>/`. Añadir esa carpeta es lo único que tienes que hacer: la
**navegación, las tablas, el grafo y el chuletario se generan solos** a partir de tu
`meta.yaml`. No tienes que editar `mkdocs.yml` ni ningún índice a mano.

## 1. Crea la carpeta

```text
docs/content/<tema>/<id>/
├── <id>.meta.yaml      # metadatos (fuente de la verdad) — nombrado con el id
├── index.md            # explicación en español (+ index.en.md opcional para inglés)
├── code/
│   ├── <id>.v1.full.cpp
│   └── <id>.v1.full.py
└── test/               # opcional
    ├── driver.cpp
    └── driver.py
```

!!! tip "Nombra los ficheros con el `id`"
    El `meta.yaml` se llama `<id>.meta.yaml` (por ejemplo `bogosort.meta.yaml`), igual que
    el nombre de la carpeta y que los ficheros de `code/`. Así es fácil localizarlo al
    buscar. La página se llama `index.md` (así la URL queda limpia: `.../<id>/`).

`<tema>` es uno de los **temas** existentes (mira la carpeta `docs/content/`): `fundamentals`,
`strings`, `search`, `data-structures`, `graphs`, `dynamic-programming`, `greedy`,
`arithmetics`, `combinatorics`, `geometry`, `game-theory`. La lista canónica vive en
`docs/content/topics/topics.json`; si necesitas un tema nuevo, mira
[Añadir un tema](#add-topic).

Lo más rápido es **copiar una carpeta ya hecha** como plantilla, por ejemplo
`docs/content/data-structures/fenwick-tree/`.

## 2. Escribe el `<id>.meta.yaml`

Es el corazón de todo: de aquí se generan la navegación, la tabla resumen, el grafo, el
chuletario y los tests. Campos principales:

```yaml
id: segment-tree                 # identificador único, en kebab-case (= nombre de la carpeta)
type: structure                  # algorithm | technique | structure
topic: data-structures           # uno de los temas de tools/common.py (TOPICS)
name: { es: "Árbol de segmentos", en: "Segment tree" }
level: intermediate              # base | beginner | intermediate | advanced | expert
difficulty: 4.0
techniques: [divide-and-conquer]
tags: [range-query, point-update]
prerequisites: [fenwick-tree]    # ids de otros elementos (para el grafo)
current_version: v1
signature:                       # API pública (se conserva en la versión contest)
  type: SegmentTree
  methods: ["void update(int i, int x)", "int query(int l, int r)"]
stats:
  complexity: { time: "O(log n)", space: "O(n)" }
  use_case: { es: "...", en: "..." }
references:
  - { title: "CP-Algorithms", url: "https://cp-algorithms.com/..." }
examples:                        # ¡esto son también los tests!
  - input: |
      ...
    expected_output: |
      ...
```

`type`, `topic` y `level` deciden **dónde aparece** el elemento (la navegación se agrupa por
nivel y etiqueta cada entrada con su tipo; el tema aporta el icono). `python tools/gen.py
status` **falla** si el `topic` no es uno de los conocidos.

### Formato: `snippet` (por defecto) o `article`

- **`snippet`** (por defecto): la página es *una implementación canónica*. **Debe** tener un
  fichero `*.full.*` y al menos un `examples:`. A partir de ahí se autogeneran las versiones
  `clean`/`contest`, los tests y su entrada en el chuletario.
- **`article`**: la página es *prosa con ejemplos libres* (una técnica como bucles o
  recursión). No tiene implementación versionada, así que las herramientas de código, tests
  y chuletario **la ignoran**. Actívalo con `format: article`.

Marca `wip: true` si el elemento existe pero aún no está implementado: queda exento de la
validación y aparece atenuado en la navegación con el icono 🏗️.

## 3. Escribe la página `index.md`

La página lleva **solo la explicación**. Los metadatos y el bloque de código se generan
desde el `meta.yaml` con dos *macros* (activa las macros con `render_macros: true` en la
cabecera):

````markdown
---
render_macros: true
---
# Árbol de segmentos

{{ metadata() }}

Aquí va tu explicación clara del algoritmo…

## Código

{{ code_tabs() }}

## Complejidad

| Recurso | Coste |
|---------|-------|
| ...     | ...   |
````

- `{{ metadata() }}` → la caja *Metadatos* (tipo · nivel · dificultad · complejidad) desde
  `meta.yaml`. Acepta `metadata(complexity="O(log n) por operación")` si quieres matizar la
  complejidad, y `metadata(extra="**Técnica:** ...")` para añadir una nota.
- `{{ code_tabs() }}` → las pestañas C++/Python × full/clean/contest con el código de
  `code/` (solo las que existan), ya sin los comentarios ocultos.

(Las macros están en `main.py`. Una página `article` sin código puede omitir `code_tabs()`.)

## 4. Escribe el código `full`

Escribe solo la versión **`full`** (comentada) en C++ y Python. Las versiones `clean` y
`contest` se autogeneran a partir de ella. Puedes escribir tú mismo una `clean`/`contest` si
quieres personalizarla; contrólalo con las directivas `no-clean`, `no-contest`, `no-generate`
(ver [Scripts](scripts.md#directivas-de-generacion-comentarios-ocultos)).

## 5. Genera lo derivado

```bash
python tools/gen.py generate          # crea lo que falte (no toca lo que ya existe)
python tools/gen.py generate --force  # regenera también lo ya existente
```

Esto crea `*.clean.*`, `*.contest.*`, los `test/cases/*.in|*.out`, actualiza
`algorithms.json` y `taxonomy.js`, y **regenera la navegación (`mkdocs.yml`)**. Por eso
**no editas el menú a mano**: aparece solo.

## 6. Comprueba y previsualiza

```bash
python tools/gen.py status     # debe decir "up to date" (lo que comprueba la CI)
python tools/runtests.py       # tus examples deben pasar como tests
mkdocs serve                   # abre http://127.0.0.1:8000 y revisa tu página
```

## Imágenes y gifs (opcional pero recomendado)

Guárdalos **dentro de la carpeta del elemento**, en `media/`, y enlázalos de forma
**relativa** desde la página:

```markdown
<figure class="algo-figure">
  <img src="media/mi-diagrama.svg" alt="Descripción para accesibilidad">
  <figcaption>Breve explicación de lo que muestra.</figcaption>
</figure>
```

Formatos: **SVG** dibujado a mano (como el de
[Búsqueda binaria](../content/search/binary-search-array/index.md)), **PNG/JPG** para
capturas, **GIF** para animaciones. Si usas imágenes de Wikimedia Commons, **descárgalas** a
`media/`, comprueba la **licencia** y añade la **atribución** en el `figcaption`.

## 7. Añádete a los autores

Añade tu fila a la página de [Autores](authors.md), en el mismo Pull Request.

## 8. Abre el Pull Request

Sigue [Git y GitHub](git-github.md). El robot te dará un enlace de vista previa.

!!! warning "Versionar sin romper"
    Si mejoras un elemento existente sin querer romper la versión anterior, crea una
    versión nueva: `<id>.v2.full.cpp`, y actualiza `current_version: v2` en el `meta.yaml`.
    La `v1` sigue disponible.

## Añadir un tema (topic) {#add-topic}

Los **temas** son una taxonomía plana y son lo único que no vive dentro de la carpeta de un
elemento. Añade un tema nuevo **solo** si ninguno de los existentes encaja. Son **dos
ficheros**, ambos en `docs/content/topics/`:

**1. Regístralo** en `docs/content/topics/topics.json` — la **fuente de la verdad** (la leen
las herramientas de Python y, de ahí, el front-end). Añade una entrada `id → {label, icon,
desc}`, con el `id` en kebab-case. El **orden** de las claves es el orden en que el tema
aparece en todas partes (filtro de *Temas*, tabla, iconos):

```json
"game-theory": { "label": "Teoría de juegos", "icon": "♟️", "desc": "Juegos de dos jugadores de suma cero." }
```

**2. Descríbelo** en `docs/content/topics/index.md`: añade una sección cuyo **ancla sea el
`id`** del tema y cuyo emoji coincida con el `icon`. Es obligatorio: los iconos de tema de
todo el sitio enlazan a `#<id>` de esta página, así que sin la sección el enlace se rompe.

```markdown
## ♟️ Teoría de juegos {#game-theory}

Un párrafo explicando el tema…
```

**3. Regenera** lo derivado (nunca lo edites a mano):

```bash
python tools/gen.py generate   # actualiza taxonomy.js, algorithms.json y el nav
python tools/gen.py status     # debe decir "up to date"
```

`taxonomy.js` (para el front-end) y la tabla de *Temas* se generan a partir del JSON, así que
no tocas nada más. `python tools/gen.py status` **falla** si un elemento declara un `topic`
que no está en `topics.json`.
