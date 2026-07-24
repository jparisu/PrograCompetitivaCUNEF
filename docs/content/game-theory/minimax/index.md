---
render_macros: true
---
# MiniMax

{{ metadata() }}

Minimax es un algoritmo de búsqueda recursivo usado en **juegos de dos jugadores** de **suma cero** con **información perfecta** para minimizar la posible pérdida máxima.
Se basa en la idea de que un jugador intenta maximizar su puntuación mientras el otro intenta minimizarla.

## Idea

Este algoritmo asume que ambos jugadores juegan de manera óptima.
Se construye un **árbol de juego** donde cada nodo representa un estado del juego y cada arista un posible movimiento.
El algoritmo sigue una estrategia de **backtracking** para explorar todos los posibles movimientos y sus consecuencias, evaluando los estados terminales del juego para determinar el mejor movimiento inicial.

## Código

{{ code_tabs() }}

## Cómo funciona

El algoritmo recorre el árbol de juego en profundidad (*backtracking*):

1. Si el estado es **terminal** (no hay movimientos posibles), devuelve su
   puntuación con `score_funct`: es el valor real de esa hoja.
2. Si no, genera los estados hijos con `possible_moves_funct` y llama a `minimax`
   sobre cada uno, **alternando** el jugador (`-maximizing_player`).
3. El jugador que **maximiza** se queda con el hijo de mayor valor; el que
   **minimiza**, con el de menor valor. Ese valor "sube" al nodo padre.

Así, el valor de cada nodo interno resume *lo mejor que puede conseguir quien
mueve ahí si ambos juegan de forma óptima*. La llamada raíz devuelve el valor
óptimo y, además, el **índice del mejor movimiento** (`best_move`).

La función es **genérica**: no sabe nada del juego concreto. Todo lo específico
—cómo se representan los estados, qué movimientos hay y cómo se puntúa una
posición final— vive en las dos funciones que le pasas (mira el driver del juego
de las monedas en `test/driver.py`).

## Complejidad

Minimax visita **cada nodo del árbol de juego una sola vez**, así que su coste es
proporcional al número de estados que explora. Con un factor de ramificación `b`
(movimientos por turno) y una profundidad `d` (jugadas hasta el final), el árbol
tiene hasta `bᵈ` nodos:

| Recurso | Coste |
|---------|-------|
| Tiempo | O(bᵈ) — es decir, O(n) en el número de nodos `n` |
| Memoria | O(d) — la pila de recursión |

Es **exponencial** en la profundidad: por eso, en juegos grandes (ajedrez, Go) no
se explora el árbol completo. Se limita la profundidad y se evalúan las posiciones
intermedias con una **heurística**, y se recorta el árbol con **poda alfa-beta**
(ver [Variantes](#variantes)). Si un mismo estado se alcanza por varios caminos,
**memoizar** su valor evita recalcular subárboles.

## Ejemplos

Supongamos que estamos jugando al juego de las monedas, donde dos jugadores alternan turnos para tomar monedas de una pila.
Cada jugador puede tomar una o dos monedas en su turno, y el objetivo es maximizar la cantidad de monedas que uno puede recoger.
Dependiendo de la pila inicial, determina el máximo valor esperado y el mejor movimiento para el jugador que comienza asumiendo que el rival juega de manera óptima.

| Pila inicial | Mejor resultado | Mejor movimiento |
|-------|--------|-----------|
| `2 3 5 8` | 10 | `0` (Tomar 1 moneda) |

## Variantes

### Minimax heurístico

!!! warning "Trabajo en curso"
    Esta página todavía no tiene contenido. ¿Te animas a escribirla? Sigue
    [Cómo contribuir](../../../contributing/index.md) y añade el código, la explicación y
    los ejemplos.

### Minimax con poda alfa-beta

!!! warning "Trabajo en curso"
    Esta página todavía no tiene contenido. ¿Te animas a escribirla? Sigue
    [Cómo contribuir](../../../contributing/index.md) y añade el código, la explicación y
    los ejemplos.

## Cuándo usarlo

- **Juegos de dos jugadores** de **suma cero** con **información perfecta** con un número limitado de estados (Tic-Tac-Toe, Coins, etc.).

## Cuándo NO usarlo

!!! warning
    Muchos juegos que se presentan como problema cuentan con una heurística o estrategia óptima que no requiere una exploración exhaustiva, por ejemplo: NIM.
    En esos casos, usar minimax no es la opción correcta.

- **Árboles de juego enormes** sin poda ni límite de profundidad: el coste O(bᵈ)
  se dispara (ajedrez, Go). Usa poda alfa-beta, límite de profundidad y una
  heurística de evaluación.
- **Juegos con azar** (dados) o **información imperfecta** (cartas ocultas):
  minimax asume determinismo e información perfecta. Para el azar se usa
  *expectimax*, con nodos de valor esperado.
- **Más de dos jugadores** o juegos que **no son de suma cero**: la dicotomía
  maximizar/minimizar deja de valer; hacen falta variantes como *maxⁿ*.
- **Juegos con estrategia óptima conocida**: si hay una fórmula o estrategia que garantiza la victoria, no hace falta explorar el árbol de juego.


## Errores comunes

- **No alternar el jugador** en la llamada recursiva: hay que pasar
  `-maximizing_player`, no el mismo valor.
- **Inicializar mal el mejor valor**: `-∞` para quien maximiza y `+∞` para quien
  minimiza (si los intercambias, ningún movimiento supera el valor inicial).
- **Puntuar nodos internos** en vez de solo los terminales: `score_funct` únicamente
  tiene sentido en estados finales; el valor de un nodo interno sale de sus hijos.
- **Confundir el movimiento con el estado**: `best_move` es el *índice* del
  movimiento elegido, no el estado resultante.
- **Juegos que pueden entrar en ciclos**: sin estados terminales garantizados (o un límite de profundidad), la recursión no termina.

## Referencias

- [Minimax — Wikipedia](https://en.wikipedia.org/wiki/Minimax)
- [Poda alfa-beta — Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
