# DP con máscaras de bits — TSP

!!! info "Metadatos"
    **Nivel:** Avanzado · **Dificultad:** 6.0 · **Complejidad:** O(2ⁿ·n²)
    · **Técnica:** [Programación dinámica](../../../techniques/dynamic-programming/index.md)

El **problema del viajante** (TSP) busca el ciclo de coste mínimo que visita todos los
nodos exactamente una vez. Con **DP sobre máscaras de bits** (Held-Karp) lo resolvemos en
O(2ⁿ·n²), práctico para `n` pequeño (hasta ~20).

## Idea

Una **máscara de bits** representa el conjunto de nodos ya visitados. El estado
`dp[mask][u]` es el coste mínimo de un camino que empezó en 0, visitó exactamente los
nodos de `mask` y termina en `u`.

## Código

=== "C++"
    ```cpp
    --8<-- "algorithms/dynamic-programming/bitmask-tsp/code/tsp.v1.full.cpp"
    ```
=== "Python"
    ```python
    --8<-- "algorithms/dynamic-programming/bitmask-tsp/code/tsp.v1.full.py"
    ```

## Complejidad

| Recurso | Coste |
|---------|-------|
| Tiempo | O(2ⁿ·n²) |
| Memoria | O(2ⁿ·n) |

## Referencias

- [CP-Algorithms: Bitmask DP](https://cp-algorithms.com/dynamic_programming/profile-dynamics.html)
