# Binary search

!!! info "Metadatos"
    **Tipo:** Algoritmo · **Nivel:** Principiante · **Dificultad:** 1.5 · **Complejidad:** O(log n)

Busca un valor en un array **ordenado** dividiendo el espacio de búsqueda por la mitad en
cada paso. Devuelve la posición del valor, o `-1` si no está.

<figure class="algo-figure">
  <img src="media/binary-search.svg" alt="En cada paso se compara con el elemento central y se descarta la mitad del rango">
  <figcaption>En cada paso se compara con el elemento central y se descarta la mitad del rango.</figcaption>
</figure>

## Código

=== "C++"

    === "full"

        ```cpp
        --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.full.cpp"
        ```

    === "clean"

        ```cpp
        --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.clean.cpp"
        ```

    === "contest"

        ```cpp
        --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.contest.cpp"
        ```

=== "Python"

    === "full"

        ```python
        --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.full.py"
        ```

    === "clean"

        ```python
        --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.clean.py"
        ```

    === "contest"

        ```python
        --8<-- "algorithms/searching/binary-search-array/code/binary_search.v1.contest.py"
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
