# Fenwick Tree (BIT)

!!! info "Metadatos"
    **Tipo:** Estructura · **Nivel:** Intermedio · **Dificultad:** 3.0 · **Complejidad:** O(log n) por operación

El **árbol de Fenwick** (o *Binary Indexed Tree*) mantiene las sumas de prefijos de un
array permitiendo **actualizaciones puntuales** y **consultas de rango**, ambas en
**O(log n)**. Es la estructura ideal cuando el array cambia y necesitamos sumas de rangos
muchas veces.

## Código

=== "C++"

    === "full"

        ```cpp
        --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.full.cpp"
        ```

    === "clean"

        ```cpp
        --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.clean.cpp"
        ```

    === "contest"

        ```cpp
        --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.contest.cpp"
        ```

=== "Python"

    === "full"

        ```python
        --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.full.py"
        ```

    === "clean"

        ```python
        --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.clean.py"
        ```

    === "contest"

        ```python
        --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.contest.py"
        ```


## Complejidad

| Operación | Complejidad |
|-----------|-------------|
| Construcción | O(n) |
| `update` | O(log n) |
| `query` | O(log n) |
| Memoria | O(n) |

## Ejercicios

| Nombre | Dificultad | Enlace |
|--------|------------|--------|
| fenwick | 4.0 | [Kattis](https://open.kattis.com/problems/fenwick) |
| supercomputer | 2.7 | [Kattis](https://open.kattis.com/problems/supercomputer) |

## Referencias

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
