# Bucles en Python

[:octicons-arrow-left-24: Volver a Bucles](index.md)

## `for` — recorrer un rango o un iterable

```python
for i in range(n):        # i = 0, 1, ..., n-1
    ...

for x in [10, 20, 30]:    # recorre directamente los elementos
    ...
```

`range(a, b)` va de `a` a `b-1` (el extremo derecho **no** se incluye). `range(a, b, paso)`
permite saltos, incluso negativos:

```python
for i in range(0, 10, 2):     # 0, 2, 4, 6, 8  (de dos en dos)
    ...

for i in range(n - 1, -1, -1):  # n-1, n-2, ..., 0  (al revés)
    ...
```

<!-- TODO (trabajo futuro): enlazar con "Iteradores" (../iterators/index.md) cuando esa
     página tenga contenido — `for x in v`, range/enumerate/reversed son iteradores. -->

Para recorrer al revés también sirve `reversed(v)`, y si necesitas el índice **y** el
valor a la vez, usa `enumerate`:

```python
for i, x in enumerate(v):     # i = posición, x = valor en esa posición
    print(i, x)
```

## `while` — hasta que se cumpla una condición

```python
while condicion:
    # se repite mientras `condicion` sea verdadera
    ...
```

Úsalo cuando **no sabes de antemano** cuántas vueltas darás. La
[condición](../conditionals/index.md) es la misma que la de un `if`. Algo dentro del
cuerpo debe acercarla a volverse falsa, o el bucle nunca terminará.

!!! tip "Python no tiene `do…while`"
    Se imita con un bucle infinito y una salida explícita:
    ```python
    while True:
        ...
        if not condicion:
            break
    ```

## `break` y `continue`

Dos formas de alterar el flujo desde dentro del cuerpo:

```python
for x in v:
    if x == objetivo:
        break         # encontrado: salir del bucle YA
    if x < 0:
        continue      # ignorar negativos: saltar a la vuelta siguiente
    suma += x
```

- **`break`** abandona el bucle inmediatamente.
- **`continue`** salta el resto del cuerpo y pasa a la siguiente iteración.

En bucles anidados, ambos afectan **solo al bucle más interno** que los contiene.

## Bucles anidados y su coste

Un bucle dentro de otro multiplica el número de vueltas. Con dos bucles de tamaño `n` el
cuerpo interior se ejecuta `n · n = n²` veces:

```python
for i in range(n):
    for j in range(n):
        # este cuerpo se ejecuta n² veces  ->  O(n²)
        print(i, j)
```

<figure class="algo-figure">
  <img src="media/nested-loops.svg" alt="Rejilla de n por n celdas; cada celda es una
    ejecución del cuerpo interior">
  <figcaption>Cada celda es una ejecución del cuerpo interior: dos bucles de tamaño
    <code>n</code> dan <code>n²</code> repeticiones.</figcaption>
</figure>

Esto importa mucho en competitiva: si `n = 10⁵`, un algoritmo `O(n²)` haría 10¹⁰
operaciones y se pasaría del tiempo límite. Y en Python, ya de por sí más lento que C++,
conviene evitar los bucles anidados innecesarios.

## Patrón acumulador

Una variable *fuera* del bucle que se actualiza en cada vuelta (suma, máximo, contador…):

```python
suma = 0                    # acumulador de suma
maximo = float("-inf")      # "peor caso" inicial para un máximo
pares = 0                   # contador

for x in v:
    suma += x
    maximo = max(maximo, x)
    if x % 2 == 0:
        pares += 1
```

La clave es **inicializar bien** el acumulador: `0` para sumas, `1` para productos y
`float("-inf")` para un máximo.

!!! tip "Muchas veces no necesitas el bucle"
    Python trae atajos: `sum(v)`, `max(v)`, `min(v)`, `len(v)`. Escribe el bucle a mano
    solo cuando la operación no encaje en uno de ellos.

## Leer un número desconocido de datos (hasta EOF)

<!-- TODO: add this to std I/O when exists -->

A veces la entrada no dice cuántos números hay: hay que leer **hasta el final** (EOF). Lo
más cómodo es leerlo todo de golpe y trocearlo:

```python
import sys

datos = sys.stdin.read().split()   # todos los tokens de la entrada, como texto
suma = 0
for token in datos:
    suma += int(token)             # convertir cada token a entero antes de sumar
print(suma)
```

## Ejemplo completo

Lee `n` números y muestra su suma:

```python
--8<-- "content/fundamentals/loops/code/loops.v1.full.py"
```

| Entrada | Salida |
|---------|--------|
| `3` <br> `10 20 30` | `60` |

## Complejidad

| Estructura | Coste |
|------------|-------|
| Un bucle de `n` vueltas | O(n) |
| Dos bucles anidados de `n` | O(n²) |
| `k` bucles anidados de `n` | O(nᵏ) |

Regla rápida: multiplica las vueltas de cada nivel de anidamiento.

## Errores comunes

- **Confundir el rango**: `range(n)` llega hasta `n-1`, no hasta `n`.
- **Bucle infinito**: olvidar actualizar la variable de un `while`.
- **Indentación**: en Python los espacios definen el cuerpo del bucle; mezclarlos rompe
  el programa.
- **Anidar sin pensar en el coste**: `O(n²)` con `n` grande se sale del tiempo límite.

## Referencias

- [Python docs: `for`](https://docs.python.org/3/tutorial/controlflow.html#for-statements)
- [Python docs: `range`](https://docs.python.org/3/library/stdtypes.html#range)
