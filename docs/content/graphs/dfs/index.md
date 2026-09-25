---
render_macros: true
---
# Depth-first search (DFS)

{{ metadata() }}

El algoritmo de **Depth First Search** ó **DFS** (en español Búsqueda en Profundidad) es un algoritmo sencillo de recorrido de grafos. Este algoritmo busca explorar el grafo tan profundo como sea posible a lo largo de cada rama, retrocediendo (**backtracking**) cuando se topa con un callejón sin salida.

## Idea

Para implementar este algoritmo usaremos una estructura **LIFO** (last in, first out), que podemos implementar con una **pila** o utilizando **recursividad**.

Durante la ejecución del algoritmo podemos dividir los nodos en tres posibles estados:
- `No visitado`: Nodos por los que aún no ha pasado nuestro algoritmo.
- `En proceso`: Nodos que hemos visitado, pero no sus nodos vecinos.
- `Procesado`: Nodos que hemos visitado, incluyendo sus nodos vecinos.

El algoritmo parte de un nodo **no visitado** cualquiera, lo marca como **en proceso**, y avanza hasta uno de sus nodos vecinos, en caso de que dicho nodo sea un nodo **no visitado**. Una vez hemos visitado todos los vecinos de un nodo, exceptuando el vecino de origen, lo marcamos como **procesado** y retrocedemos al vecino de origen. Repetiremos este proceso hasta haber **procesado** todo el grafo.

Este algoritmo es especialmente útil ya que sirve como base para el desarrollo de otros algoritmos más complejos como **Toposort** o **Detección de ciclos**.

## Código

{code_tabs()}

## Complejidad

| Recurso | Coste |
|---------|-------|
| Tiempo | O(n + m) |
| Memoria | O(n) |

Siendo **n** el número de vértices del grafo y **m** el número de aristas. Como recorremos el grafo en su totalidad, pasaremos por todos los vértices y aristas, de ahí el coste (`O(n + m)`).

## Casos límite y errores comunes
- **Grafos disconexos**: Al no ser posible recorrer el grafo en su totalidad con una sola pasada de **DFS**, se pueden usar varias.
- **Ciclos infinitos**: Un error común es marcar erróneamente las aristas, resultando en ciclos infinitos y en un **TLE**.
- **Memory Limit**: En su versión recursiva, si clonamos el grafo en cada paso de la recursión, acabaremos con un problema de límite de memoria (**MLE**) o simplemente **TLE**.