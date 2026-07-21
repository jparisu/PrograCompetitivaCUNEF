# Chuletario

El **chuletario** (o *cheatsheet*) es una hoja de referencia compacta al estilo
[KACTL](https://github.com/kactl/kactl): varias columnas con los algoritmos del
repositorio impresos uno tras otro, pensada para imprimir y llevar a un
concurso ICPC. Se genera a partir de los mismos ficheros de código que ves en
cada algoritmo, así que **lo que llevas al concurso es exactamente el código
probado por el CI**.

Puedes usar el chuletario de tres maneras:

1. **Descargar el chuletario completo** que construye el CI (todos los algoritmos).
2. **Construir el tuyo a medida** con un fichero YAML y `tools/cheatsheet.py`.
3. **Usar el constructor visual** de esta página para generar ese YAML sin
   escribirlo a mano.

## Descargas

<!-- Estos ficheros los produce el CI dentro de docs/cheatsheet/. Hasta que el
     CI se ejecute por primera vez darán 404: es normal. -->

- [:material-file-pdf-box: Chuletario completo (PDF)](cheatsheet.pdf)
- [:material-file-code: Fuente LaTeX (.tex)](cheatsheet.tex)

!!! note "¿Enlaces rotos (404)?"
    Los ficheros `cheatsheet.pdf` y `cheatsheet.tex` los genera el CI y los
    publica en esta misma carpeta. Si acabas de crear la página puede que aún
    no existan: aparecerán en cuanto se ejecute el workflow del chuletario.

## Formato del YAML

La configuración elige **qué** algoritmos entran y **cómo** se renderizan.
Estos son los campos:

| Campo | Valores | Descripción |
|---|---|---|
| `title` | texto | Título impreso en la hoja. |
| `language` | `cpp` \| `py` | Lenguaje por defecto del código. |
| `style` | `full` \| `clean` \| `contest` | Estilo de código por defecto. |
| `include_stats` | `true` \| `false` | Imprimir complejidad / caso de uso bajo cada fragmento. |
| `columns` | entero | Número de columnas. |
| `algorithms` | lista | Qué incluir, **en orden**. Cada elemento es un `id` suelto o un mapa que sobreescribe los valores globales (`id`, `version`, `style`, `language`). |

Ejemplo completo (`templates/cheatsheet.example.yaml`):

```yaml
title: "Chuletario ICPC CUNEF"
language: cpp
style: contest
include_stats: true
columns: 3

algorithms:
  - loops
  - binary-search-array
  - fenwick-tree
  # Un elemento puede sobreescribir los valores globales:
  - id: bitmask-tsp
    version: v1        # por defecto: current_version del meta.yaml
    style: clean       # por defecto: el style global
    language: cpp      # por defecto: el language global
  - convex-hull
```

## Generar el tuyo

Guarda tu configuración (por ejemplo `mi_chuleta.yaml`) y ejecuta:

```bash
python tools/cheatsheet.py --config mi_chuleta.yaml --out build/chuleta --pdf
```

Esto escribe `build/chuleta.tex` y, si tienes `pdflatex` instalado,
`build/chuleta.pdf`. Sin `pdflatex` obtienes solo el `.tex` (puedes compilarlo
en [Overleaf](https://www.overleaf.com/) u otro editor LaTeX).

Opciones útiles: `--all` (incluir todos los algoritmos), `--language {cpp,py}`
y `--style {full,clean,contest}` (forzar lenguaje/estilo globales), `-v`
(detallado). Consulta `python tools/cheatsheet.py --help`.

## Constructor visual

Marca los algoritmos que quieras, elige lenguaje y estilo y pulsa **Generar
YAML**. La página **no compila LaTeX** (es estática): produce el YAML que luego
pasas por el comando de arriba.

<div id="cheatsheet-builder" markdown="0">
  <p class="csb-message">Cargando la lista de algoritmos… Si este mensaje no
  desaparece, necesitas JavaScript activado y el fichero
  <code>assets/data/algorithms.json</code> (lo genera <code>tools/genoverview.py</code>).</p>
</div>
