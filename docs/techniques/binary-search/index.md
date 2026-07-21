# Búsqueda binaria

La **búsqueda binaria** encuentra un valor en un espacio **ordenado** dividiéndolo por la
mitad en cada paso, pasando de O(n) a **O(log n)**.

## Idea clave

En cada iteración descartamos la mitad del espacio de búsqueda porque sabemos hacia qué
lado está la respuesta. Funciona siempre que exista una propiedad **monótona**: algo que
sea "falso, falso, …, verdadero, verdadero".

## Dos usos habituales

1. **Buscar un elemento** en un array ordenado.
2. **Búsqueda binaria sobre la respuesta**: cuando la respuesta es un número y podemos
   comprobar rápido si un candidato es válido.

## Algoritmos que la usan

- [Búsqueda binaria en un array](../../algorithms/searching/binary-search-array/index.md)

!!! note "Más adelante"
    Añadiremos *búsqueda binaria sobre la respuesta* y su uso dentro de otros algoritmos
    (por ejemplo, la versión O(n log n) de la subsecuencia creciente más larga).
