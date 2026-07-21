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

## 3. Escribe el código `full`

Solo la versión **`full`** (comentada, con doc-string de cabecera) en C++ y Python. Las
versiones `clean` y `contest` **no las escribes tú**: se generan.

## 4. Genera lo derivado

```bash
python tools/gen.py generate
```

Esto crea `*.clean.*`, `*.contest.*`, los ficheros `test/cases/*.in|*.out` y actualiza la
tabla resumen. Revisa las versiones `contest` (para C++ conviene repasarlas a mano).

## 5. Comprueba y previsualiza

```bash
python tools/gen.py status     # debe decir "up to date"
mkdocs serve                   # abre http://127.0.0.1:8000 y revisa tu página
```

## 6. Abre el Pull Request

Sigue [Git y GitHub](git-github.md). El robot te dará un enlace de vista previa.

!!! warning "Versionar sin romper"
    Si mejoras un algoritmo existente sin querer romper la versión anterior, crea una
    versión nueva: `<algo>.v2.full.cpp`, y actualiza `current_version: v2` en el
    `meta.yaml`. La `v1` sigue disponible.
