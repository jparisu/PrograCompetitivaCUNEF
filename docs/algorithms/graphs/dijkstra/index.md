# Dijkstra

!!! info "Metadatos"
    **Tipo:** Algoritmo · **Nivel:** Intermedio · **Dificultad:** 3.5 · **Complejidad:** O((V+E) log V)
    · **Técnica:** Recorridos de grafos

**Dijkstra** calcula el **camino más corto** desde un nodo origen a todos los demás en un
grafo con **pesos no negativos**, expandiendo siempre el nodo más cercano aún no fijado
con ayuda de una cola de prioridad.

## Código

=== "C++"

    === "full"

        ```cpp
        --8<-- "algorithms/graphs/dijkstra/code/dijkstra.v1.full.cpp"
        ```

    === "clean"

        ```cpp
        --8<-- "algorithms/graphs/dijkstra/code/dijkstra.v1.clean.cpp"
        ```

    === "contest"

        ```cpp
        --8<-- "algorithms/graphs/dijkstra/code/dijkstra.v1.contest.cpp"
        ```

=== "Python"

    === "full"

        ```python
        --8<-- "algorithms/graphs/dijkstra/code/dijkstra.v1.full.py"
        ```

    === "clean"

        ```python
        --8<-- "algorithms/graphs/dijkstra/code/dijkstra.v1.clean.py"
        ```

    === "contest"

        ```python
        --8<-- "algorithms/graphs/dijkstra/code/dijkstra.v1.contest.py"
        ```

!!! warning "Pesos no negativos"
    Dijkstra **no funciona con aristas de peso negativo**. En ese caso usa Bellman-Ford.

## Complejidad

| Recurso | Coste |
|---------|-------|
| Tiempo | O((V+E) log V) |
| Memoria | O(V+E) |

## Referencias

- [CP-Algorithms: Dijkstra](https://cp-algorithms.com/graph/dijkstra.html)
