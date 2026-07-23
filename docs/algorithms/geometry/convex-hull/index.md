# Convex hull

!!! info "Metadatos"
    **Tipo:** Algoritmo · **Nivel:** Experto · **Dificultad:** 5.5 · **Complejidad:** O(n log n)

!!! warning "Pendiente de revisión"
    Esta página y su implementación **están pendientes de revisar**. Comprueba con cuidado
    el código, los casos límite (puntos colineales, duplicados) y los ejemplos antes de
    usarla en un concurso.

La **envolvente convexa** de un conjunto de puntos es el menor polígono convexo que los
contiene a todos (imagina una goma elástica que se cierra alrededor de los puntos). El
algoritmo de **cadena monótona de Andrew** la calcula en O(n log n).

<figure class="algo-figure">
  <img src="media/convex-hull.svg" alt="Puntos y su envolvente convexa">
  <figcaption>Los puntos naranjas forman la envolvente; los grises quedan dentro.</figcaption>
</figure>

## Idea

Ordenamos los puntos por coordenada y construimos la envolvente en dos mitades (inferior
y superior). El **producto vectorial** nos dice si al añadir un punto giramos a la
izquierda (lo mantenemos) o a la derecha (descartamos el anterior).

## Código

=== "C++"

    === "full"

        ```cpp
        --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.full.cpp"
        ```

    === "clean"

        ```cpp
        --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.clean.cpp"
        ```

    === "contest"

        ```cpp
        --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.contest.cpp"
        ```

=== "Python"

    === "full"

        ```python
        --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.full.py"
        ```

    === "clean"

        ```python
        --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.clean.py"
        ```

    === "contest"

        ```python
        --8<-- "algorithms/geometry/convex-hull/code/convex_hull.v1.contest.py"
        ```


## Complejidad

| Recurso | Coste |
|---------|-------|
| Tiempo | O(n log n) |
| Memoria | O(n) |

## Referencias

- [CP-Algorithms: Convex Hull (Andrew)](https://cp-algorithms.com/geometry/convex-hull.html)
