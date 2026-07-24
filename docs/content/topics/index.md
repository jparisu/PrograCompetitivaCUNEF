# Temas

Cada elemento del catálogo pertenece a un **tema**, y lleva su icono en todas partes
(título, tablas, matriz y grafo). Ese icono enlaza a la sección correspondiente de esta
página.

La tabla resume los temas: el nombre enlaza a su explicación, la columna *Descripción* da
una idea rápida, y las tres últimas columnas listan sus elementos por tipo, **coloreados
según la dificultad**.

<div id="topics-table"><p>Cargando la tabla…</p></div>

## 🧱 Fundamentos {#fundamentals}

Todo lo imprescindible para empezar a competir. Incluye la **entrada/salida** (leerla y
escribirla, y hacerlo *rápido* para no exceder el tiempo límite), las **estructuras de
control** (condicionales y bucles) y la capacidad de **estimar el coste** de una solución
con la notación Big-O. Son los cimientos: sin ellos ningún algoritmo más avanzado se
sostiene, y muchos problemas sencillos se resuelven únicamente con esto.

## 🔤 Strings {#strings}

Procesamiento de **texto**: manipular cadenas, compararlas y **buscar patrones** de forma
eficiente. Abarca desde operaciones básicas (recorrer, contar, transformar) hasta técnicas
como el *hashing* de cadenas, la búsqueda de subcadenas (KMP, algoritmo Z) o estructuras
como los *tries*. Aparece en problemas de coincidencia de patrones, palíndromos,
anagramas y análisis de secuencias.

## 🔎 Ordenación y búsqueda {#search}

**Ordenar** datos y **localizarlos** rápidamente. La búsqueda binaria reduce a la mitad un
espacio ordenado en cada paso (O(log n)), y su variante *búsqueda sobre la respuesta*
resuelve muchos problemas de optimización ("¿cuál es el mínimo valor que cumple…?").
Ordenar es, además, el primer paso que habilita técnicas como dos punteros o algoritmos
voraces.

## 🗃️ Estructuras de datos {#data-structures}

Formas de **guardar y organizar** los datos para consultarlos y modificarlos de forma
eficiente: listas y vectores, pilas, colas, conjuntos y mapas, y estructuras más potentes
como el **árbol de Fenwick** o el *segment tree* para consultas de rango con
actualizaciones. Elegir la estructura adecuada suele marcar la diferencia entre una
solución O(n²) que no entra en tiempo y otra O(n log n) que sí.

## 🕸️ Grafos {#graphs}

Modelan **relaciones** entre elementos mediante **nodos y aristas**. Es uno de los temas
más amplios: recorridos (BFS, DFS), **caminos más cortos** (Dijkstra, Bellman-Ford, A\*),
árboles de expansión mínima, componentes conexas, orden topológico y flujos en redes.
Muchísimos problemas —rutas, dependencias, redes sociales, mapas— se reducen a plantear el
grafo correcto.

## 🧩 Programación dinámica {#dynamic-programming}

Resuelve un problema **combinando las soluciones de sus subproblemas** y guardándolas para
no recalcularlas (memoización). Se aplica cuando hay *subestructura óptima* y
*subproblemas solapados*: mochila, cambio de monedas, subsecuencias, DP sobre máscaras de
bits o sobre árboles. Es una de las técnicas más potentes —y de las más temidas— de los
concursos: la dificultad está en **encontrar el estado y la transición** correctos.

## 🪙 Voraz (greedy) {#greedy}

Construye la solución tomando en cada paso la **mejor opción local**, con la esperanza de
alcanzar el óptimo global. Es rápida y sencilla de programar, pero **solo es correcta
cuando el problema tiene la "propiedad voraz"**, así que hay que demostrarla (o encontrar
un contraejemplo antes de fiarse). Típico en planificación de intervalos, selección de
actividades y problemas de intercambio.

## ➗ Aritmética {#arithmetics}

Trabajar con enteros grandes y **bajo módulo**: aritmética modular, exponenciación rápida,
inverso modular, máximo común divisor y números primos (criba de Eratóstenes). Es la base
de casi toda la parte matemática de los concursos y lo que permite operar con resultados
enormes usando módulos como `1e9 + 7` sin desbordarse.

## 🎲 Combinatoria {#combinatorics}

**Contar** de cuántas formas puede ocurrir algo: combinaciones, permutaciones, coeficientes
binomiales y el principio de inclusión-exclusión, casi siempre bajo módulo. Aparece en
problemas de probabilidad, conteo de caminos en rejillas y de configuraciones válidas, y
se apoya mucho en la [aritmética](#arithmetics) modular.

## 📐 Geometría {#geometry}

Problemas con **puntos, rectas, segmentos y polígonos** en el plano: producto vectorial y
orientación, intersecciones, cálculo de áreas y algoritmos como la **envolvente convexa**.
Exige especial cuidado con la **precisión numérica** y con los casos degenerados (puntos
colineales o coincidentes, divisiones por cero).

## ♟️ Teoría de juegos {#game-theory}

Problemas de búsqueda donde se añade incertidumbre debido a la **interacción con un adversario**.
El objetivo será maximizar la puntuación propia, teniendo en cuenta que el rival intentará maximizar su propia puntuación.
Los problemas más comunes suponen **juegos de dos jugadores** de **suma cero** con **información perfecta**, como el ajedrez, el tres en raya o el NIM.
Incluye algoritmos como **Minimax** y sus variantes.
