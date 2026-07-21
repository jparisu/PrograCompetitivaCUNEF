# Programación dinámica

La **programación dinámica** (DP) resuelve un problema combinando las soluciones de sus
**subproblemas**, guardando cada resultado para no recalcularlo (*memoización*).

## Cuándo aplicarla

Buscamos DP cuando el problema tiene:

- **Subestructura óptima**: la solución óptima se construye a partir de óptimas de
  subproblemas.
- **Subproblemas solapados**: los mismos subproblemas aparecen muchas veces.

## Pasos para diseñar una DP

1. Define el **estado** (qué describe un subproblema).
2. Escribe la **transición** (cómo se combina con estados menores).
3. Fija los **casos base**.
4. Elige el **orden** de cálculo (o usa recursión con memoización).

## Algoritmos que la usan

- [DP con máscaras de bits — TSP](../../algorithms/dynamic-programming/bitmask-tsp/index.md)

!!! note "Más adelante"
    Añadiremos mochila, cambio de monedas, DP en árboles y DP con máscaras adicionales.
