---
render_macros: true
---
# Fenwick Tree (BIT)

{{ metadata(complexity="O(log n) por operación") }}

El **árbol de Fenwick** (o *Binary Indexed Tree*) mantiene las sumas de prefijos de un
array permitiendo **actualizaciones puntuales** y **consultas de rango**, ambas en
**O(log n)**. Es la estructura ideal cuando el array cambia y necesitamos sumas de rangos
muchas veces.

<figure class="algo-figure">
  <img src="media/fenwick-tree.svg" alt="Cada celda T[i] cubre un bloque cuyo tamaño es su bit menos significativo">
  <figcaption>Cada celda <code>T[i]</code> guarda la suma de un bloque que termina en la
  posición <code>i</code> y cuyo tamaño es el bit menos significativo de <code>i</code>.</figcaption>
</figure>

## Idea

Un array de sumas de prefijos responde consultas en O(1), pero cambiar un solo elemento
obliga a rehacer O(n) prefijos. El árbol de Fenwick reparte la información en **bloques de
distintos tamaños** para que tanto actualizar como consultar toquen solo O(log n) bloques.

Internamente los índices son **1-based** (la posición 0-based `p` del usuario se guarda en
la posición interna `p + 1`). La celda `T[i]` almacena la suma del rango medio-abierto
`(i − lowbit(i), i]`, donde `lowbit(i)` es el **bit menos significativo** de `i`:

- `lowbit(i) = i & -i`. En complemento a dos, `-i` invierte todos los bits y suma 1,
  así que `i & -i` deja solo el bit encendido más bajo. Ese valor es a la vez el
  **tamaño** del bloque que cubre `T[i]` y el **salto** al recorrer el árbol.
- Los índices impares (`lowbit = 1`) cubren un solo elemento; los que son potencia de dos
  cubren un bloque grande (`T[8]` cubre las 8 posiciones).

`update` y `query` recorren el árbol en **direcciones opuestas**:

- **`update(index, delta)`** sube: desde la posición, repite `index += index & -index`.
  Cada salto lleva a la siguiente celda cuyo bloque *contiene* esa posición, así que
  actualiza todos los bloques afectados (a lo sumo O(log n)).
- **`query(index)`** baja: repite `index -= index & -index`. Quitar el bit más bajo
  salta al bloque anterior; los bloques visitados son disjuntos y **embaldosan**
  exactamente `[0, index)`. Como cada paso apaga un bit, hay a lo sumo O(log n) pasos.

Las consultas son **medio-abiertas**: `query(index)` devuelve la suma de `[0, index)`.
La suma de un rango es la resta de dos prefijos: `query_range(l, r) = query(r) − query(l)`.

## Ejemplo

Partimos de un array de 5 ceros y aplicamos las operaciones del test:
`update(0, 3)` y luego `update(2, 5)`. El array lógico queda `a = [3, 0, 5, 0, 0]`.

Tras las dos actualizaciones, las celdas internas (1-based) valen:

| Celda | Cubre (posiciones 1-based) | Valor |
|-------|----------------------------|-------|
| `T[1]` | `{1}`       | `3` |
| `T[2]` | `{1, 2}`    | `3` |
| `T[3]` | `{3}`       | `5` |
| `T[4]` | `{1, 2, 3, 4}` | `8` |
| `T[5]` | `{5}`       | `0` |

Ahora `query(3)` (suma de `[0, 3)`) baja desde `index = 3`: suma `T[3] = 5`, salta a
`3 − 1 = 2`, suma `T[2] = 3` y salta a `0`. Total `5 + 3 = 8`. Fíjate en que los bloques
`(2, 3]` y `(0, 2]` cubren justo las tres primeras posiciones sin solaparse.

Del mismo modo `query(5)` suma `T[5] = 0` y `T[4] = 8`, dando `8`. Por tanto
`query_range(0, 3) = 8` y `query_range(0, 5) = 8`, la salida esperada del ejemplo.

## Código

{{ code_tabs() }}

## Complejidad

| Operación | Complejidad | Motivo |
|-----------|-------------|--------|
| Construcción | O(n) | reservar el vector de `n` ceros |
| `update` | O(log n) | sube saltando de bloque en bloque, uno por bit |
| `query` | O(log n) | baja sumando bloques disjuntos, uno por bit encendido |
| Memoria | O(n) | una celda por elemento |

## Cuándo usarlo

- **Array que cambia + muchas sumas de rango** → árbol de Fenwick. Es el caso donde brilla:
  ambas operaciones en O(log n) con muy poco código y una constante pequeña.

!!! tip "Truco"
    Para *actualizaciones de rango* con *consultas puntuales*, aplica el Fenwick sobre el
    **array de diferencias**: `update(l, +v)` y `update(r, −v)` suman `v` a todo `[l, r)`.

## Cuándo NO usarlo

- **Array estático** (nunca cambia) → un simple array de **sumas de prefijos** precalculado
  responde en O(1) y es más sencillo; no necesitas Fenwick.
- **Operaciones más generales** (máximo/mínimo de rango, asignaciones de rango,
  búsquedas tipo *lower bound*) → un **segment tree** es más flexible, a costa de más
  código. El Fenwick es su versión ligera para sumas.

## Errores comunes

- Confundir **0-based** (interfaz pública) con **1-based** (interior). El `index++` al
  inicio de `update` hace esa conversión; no lo dupliques.
- Olvidar que las consultas son **medio-abiertas**: `query_range(l, r)` no incluye `r`.
  Para la suma inclusiva de `[l, r]` usa `query_range(l, r + 1)`.
- Dimensionar mal el árbol: el bucle de `update` usa la condición `index <= n`, así que
  el vector debe tener sitio para las `n` posiciones 1-based.

## Ejercicios

| Nombre | Dificultad | Enlace |
|--------|------------|--------|
| fenwick | 4.0 | [Kattis](https://open.kattis.com/problems/fenwick) |
| supercomputer | 2.7 | [Kattis](https://open.kattis.com/problems/supercomputer) |

## Referencias

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
