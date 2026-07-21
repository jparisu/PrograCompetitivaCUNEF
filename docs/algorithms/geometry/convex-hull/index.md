# Envolvente convexa

!!! info "Metadatos"
    **Nivel:** Experto · **Dificultad:** 5.5 · **Complejidad:** O(n log n)

La **envolvente convexa** de un conjunto de puntos es el menor polígono convexo que los
contiene a todos (imagina una goma elástica que se cierra alrededor de los puntos). El
algoritmo de **cadena monótona de Andrew** la calcula en O(n log n).

## Idea

Ordenamos los puntos por coordenada y construimos la envolvente en dos mitades (inferior
y superior). El **producto vectorial** nos dice si al añadir un punto giramos a la
izquierda (lo mantenemos) o a la derecha (descartamos el anterior).

## Código

=== "C++"
    ```cpp
    --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.full.cpp"
    ```
=== "Python"
    ```python
    --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.full.py"
    ```

## Complejidad

| Recurso | Coste |
|---------|-------|
| Tiempo | O(n log n) |
| Memoria | O(n) |

## Referencias

- [CP-Algorithms: Convex Hull (Andrew)](https://cp-algorithms.com/geometry/convex-hull.html)
