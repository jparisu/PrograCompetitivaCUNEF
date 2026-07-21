# Búsqueda binaria en un array

!!! info "Metadatos"
    **Nivel:** Principiante · **Dificultad:** 1.5 · **Complejidad:** O(log n)
    · **Técnica:** [Búsqueda binaria](../../../techniques/binary-search/index.md)

Busca un valor en un array **ordenado** dividiendo el espacio de búsqueda por la mitad en
cada paso. Devuelve la posición del valor, o `-1` si no está.

## Código

=== "C++"
    ```cpp
    --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.full.cpp"
    ```
=== "Python"
    ```python
    --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.full.py"
    ```

!!! warning "Precondición"
    El array debe estar **ordenado**. Si no lo está, ordénalo primero (O(n log n)).

## Complejidad

| Operación | Complejidad |
|-----------|-------------|
| Búsqueda | O(log n) |
| Memoria | O(1) |

## Ejemplos

| Array | Buscar | Resultado |
|-------|--------|-----------|
| `1 3 5 7 9 11` | `7` | `3` (posición) |
| `1 3 5 7 9 11` | `4` | `-1` (no está) |

## Referencias

- [CP-Algorithms: Binary search](https://cp-algorithms.com/num_methods/binary_search.html)
