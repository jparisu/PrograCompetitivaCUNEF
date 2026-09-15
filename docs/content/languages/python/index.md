---
render_macros: true
---
# Python de cero a concurso

{{ metadata(complexity="") }}

Python es el lenguaje más rápido de **escribir** y el más lento de **ejecutar**. Para
empezar en programación competitiva es una elección excelente: la solución de un problema
fácil son dos líneas, y no tienes que pelearte con punteros ni con desbordamientos
mientras aprendes a resolver problemas.

Este capítulo va **desde cero** hasta los temas que hacen falta para competir.

Léelo con el intérprete abierto: escribe `python3` en una terminal y prueba ahí cada
expresión que veas. Python está hecho para eso, y comprobar una duda cuesta dos segundos.
Varios ejemplos te piden provocar un error a propósito: hazlo — distinguir un
`IndexError` de un `KeyError` de un `EOFError` de un golpe de vista es una habilidad
concreta y útil.

La orden del curso:

```bash
python3 solucion.py < 1.in > 1.out
diff 1.out 1.ans && echo "OK"
```

Si te falta el contexto de cómo funcionan los jueces, empieza por
[Introducción a la programación competitiva](../../fundamentals/introduction/index.md).
Y el otro camino es el capítulo de [C++](../cpp/index.md).

## Instalar y preparar el entorno

Necesitas Python 3.8 o superior, un editor y una terminal. No hace falta compilador ni
IDE pesado.

=== "Linux"
    Suele venir instalado. Si no: `sudo apt install python3`.
=== "macOS"
    El del sistema puede ser viejo: `brew install python`.
=== "Windows"
    Instalador de [python.org](https://www.python.org/downloads/).

    !!! warning "Marca «Add python.exe to PATH»"
        Es una casilla en la primera pantalla y es fácil pasarla por alto. Sin ella,
        `python` no funciona desde la terminal.

Comprueba con `python3 --version`. En Linux y macOS el bueno es `python3` (`python` a
veces es Python 2, muerto desde 2020); en Windows, `python`. Averigua cuál funciona en tu
sistema y usa siempre ese.

### El editor

VS Code + extensión Python, y estos ajustes **no son opcionales** porque en Python la
indentación *es* el lenguaje: **Tab Size 4**, **Insert Spaces** activado, y
*Render Whitespace* en `boundary` para ver la indentación real.

!!! warning "Nunca mezcles tabuladores y espacios"
    Python lanza `TabError` y el fichero **parece** perfectamente correcto en pantalla.
    Es el error más frustrante de los primeros días y se evita con esos dos ajustes.

!!! warning "No llames a tu fichero como un módulo estándar"
    Si creas `random.py`, `math.py`, `string.py`, `queue.py` o `collections.py`, Python
    importará **el tuyo** en vez del de la librería estándar, con errores
    incomprensibles. Y borra `__pycache__` después de renombrar.

Los entornos virtuales no hacen falta para competir: no vas a instalar nada.

## Tu primer programa

```python
print("Hola")
```

```bash
python3 hola.py
```

Una línea. Sin `main`, sin includes, sin punto y coma, sin llaves. Esa brevedad es la
razón principal para empezar por Python.

Lo que hay que saber del fichero:

- **No hay `main`.** Python ejecuta de arriba abajo; la primera línea es lo primero que
  pasa. (El `if __name__ == "__main__":` que verás por ahí sirve para distinguir «me
  ejecutan» de «me importan»; en concurso es innecesario.)
- **La indentación define los bloques**, con 4 espacios, y todo lo que abre bloque
  termina en `:`.
- **Comentarios** con `#`.

### Escribir y leer

```python
print("a", "b")            # 'a b'  ← separa con espacio y añade salto de línea
print("a", "b", sep="-")   # 'a-b'
print("a", end="")         # sin salto
print(*[1, 2, 3])          # 1 2 3  ← el * desempaqueta; lo usarás constantemente

n = 42
print(f"n vale {n}")       # f-string: la f delante de las comillas es obligatoria
print(f"{2/3:.3f}")        # 0.667
```

Y ya podemos resolver
[A Shortcut to What?](https://open.kattis.com/problems/shortcuttowhat):

```python
n = int(input())          # lee una línea y la convierte a entero
print((n + 5) * 3 - 10)   # escribe el resultado
```

`echo 12 | python3 solucion.py` debe responder `41`.

!!! warning "`input()` devuelve **texto**"
    Es la trampa número uno al empezar:
    ```python
    n = input()
    print(n + 1)      # TypeError: can only concatenate str (not "int") to str
    ```
    Convertir es cosa tuya: `int(input())`.

### Interpretado, no compilado

No hay una fase que revise todo el fichero antes de empezar. Python lee y ejecuta línea a
línea:

```python
print("empiezo")
print(variable_que_no_existe)    # el error salta AQUÍ, no antes
```

El programa imprime `empiezo` y **después** falla. En C++ eso no habría compilado. Por
eso en Python hay que **probar el código**, no solo leerlo.

### Los errores de la primera vez

| Error | Causa |
|-------|-------|
| `IndentationError` | falta (o sobra) indentación |
| `TabError` | tabuladores mezclados con espacios |
| `SyntaxError: expected ':'` | faltan los dos puntos |
| `NameError` | variable que no existe (casi siempre una errata) |
| `ValueError` | `int("hola")`, o `int("")` al leer una línea de más |

## Ejecutar un programa

```bash
python3 solucion.py            # escribes la entrada a mano; Ctrl+D para acabar
python3 solucion.py < 1.in     # la entrada sale de un fichero
python3 solucion.py < 1.in > 1.out
diff 1.out 1.ans && echo "OK"  # el mismo criterio que usa el juez
echo 12 | python3 solucion.py  # un caso suelto
```

Esa pareja `< 1.in` + `diff` es tu comprobación antes de cada envío. Para competir usa la
terminal, no el botón ▶ del editor: es más rápido y es lo que vas a tener en un concurso.

### El intérprete interactivo

```bash
python3
```

```text
>>> -7 // 2
-4
>>> "abc"[::-1]
'cba'
>>> help(sorted)
>>> dir(str)          # todos los métodos de las cadenas
```

Para comprobar una duda en dos segundos sin crear un fichero. Y `help()` + `dir()` son
documentación **sin Internet**: en un concurso presencial, es la que tienes.

### Leer un *traceback*

```text
Traceback (most recent call last):
  File "solucion.py", line 8, in <module>
    total += v[i]
IndexError: list index out of range
```

Se lee **de abajo arriba**: la última línea dice **qué** ha pasado, la de encima **dónde**.
Si hay varias entradas, la de más abajo es donde reventó.

Todos estos errores, en el juez, son un **Run Time Error**, y el *traceback* solo lo ves
en local: reproduce el fallo en tu máquina antes de intentar adivinar.

`Ctrl+C` para parar un programa colgado. Si redirigiste la entrada con `<` y sigue
colgado, es un bucle infinito.

## Sintaxis e indentación

```python
if n > 0:
    print("dentro")
print("fuera")
```

4 espacios por nivel, nunca tabuladores, y `:` en todo lo que abre bloque. Un bloque no
puede estar vacío: si lo necesitas, `pass`.

Sin punto y coma (existe y no se usa), una sentencia por línea, y para partir una línea
larga basta con estar dentro de paréntesis, corchetes o llaves.

```python
x = 5                 # asignar es crear: no se declara nada, no hay tipo escrito
x = "hola"            # el tipo lo tiene el VALOR, no la variable
a, b = 1, 2
a, b = b, a           # intercambio, sin variable auxiliar
a, b = map(int, input().split())    # el patrón de lectura más común
MOD = 10**9 + 7       # Python no tiene constantes: el convenio es MAYÚSCULAS
x = None              # el valor "nada"; compáralo con `is None`
```

!!! warning "No uses nombres de funciones estándar"
    ```python
    list = [1, 2, 3]     # ahora list() ya no funciona
    sum = 0              # ahora sum() ya no funciona
    ```
    No es un error de sintaxis: has tapado la función, y el fallo aparece cincuenta
    líneas más abajo. Evita `list`, `dict`, `set`, `str`, `int`, `sum`, `max`, `min`,
    `input`, `id`, `type`, `next`.

Nota a favor de Python: `if x = 5:` es un **SyntaxError**, no un fallo silencioso como en
C++. Si de verdad quieres asignar en una condición, el operador morsa:
`if (n := len(datos)) > 0:`.

## Tipos nativos y variables

Ficha corta: [Tipos nativos](../../fundamentals/native-types/index.md).

### Enteros: precisión ilimitada

La mejor característica de Python para concursos:

```python
print(2 ** 1000)      # un número de 302 cifras, exacto
```

**No hay desbordamiento.** En C++ eso es la causa número uno de Wrong Answer; aquí
sencillamente no existe. El precio es la velocidad: un `int` de Python es un objeto, no
un número en un registro.

### La división

```python
7 / 2      # 3.5   ← SIEMPRE devuelve float
7 // 2     # 3     ← división entera
7 % 2      # 1
7 ** 2     # 49
divmod(7, 2)   # (3, 1)
pow(2, 10**6, MOD)   # exponenciación MODULAR rápida, ya implementada
```

!!! warning "`/` devuelve `float` aunque divida exacto"
    `10 / 2` es `5.0`, no `5`. Imprimir `5.0` donde se esperaba `5` es un Wrong Answer, y
    es **el error más frecuente de todos** en Python competitivo. Con enteros, usa `//`.

Y con negativos, Python es distinto de C++ — para bien:

```python
-7 // 2    # -4   (C++ da -3: redondea hacia cero; Python, hacia abajo)
-7 % 3     #  2   (C++ da -1: aquí el resto es siempre >= 0)
```

Así que en aritmética modular no hace falta normalizar.

### Decimales, booleanos, cadenas

Los `float` son doble precisión, como el `double` de C++: **sí** tienen el problema de
siempre, aunque los `int` no.

```python
0.1 + 0.2 == 0.3          # False
math.isclose(a, b)        # así
```

!!! tip "Evita los decimales si puedes"
    Comparar `a/b < c/d` puede fallar por redondeo; comparar `a*d < c*b` con enteros es
    exacto. Y como los `int` no se desbordan, multiplicar en cruz es gratis. Ver
    [Coma flotante](../../arithmetics/float-treatment/index.md).

`bool` es un `int` (`sum(x > 0 for x in v)` cuenta los positivos), y son **falsos** `0`,
`0.0`, `""`, `[]`, `{}`, `set()`, `None` y `False`. De ahí la forma idiomática
`if datos:` en vez de `if len(datos) > 0:`.

Las cadenas son **inmutables**: `s[0] = "H"` es un `TypeError`.

### Conversiones

```python
n = int(input())                         # un entero
a, b = map(int, input().split())         # dos en la misma línea
v = list(map(int, input().split()))      # una lista entera
int("3.5")        # ValueError: hay que pasar por float
int(3.9)          # 3: trunca hacia cero, no redondea
```

## Operadores y expresiones

```python
+ - * / // % **       += -= *= //= %=      :=
== != < <= > >=       and or not           in  not in   is
& | ^ ~ << >>
```

### Las comparaciones **sí** se encadenan

```python
if 0 <= x < n:       # equivale a (0 <= x) and (x < n), y x se evalúa una vez
if a < b < c:
```

Al contrario que en C++. Es una de las cosas que hacen Python cómodo.

### `==` frente a `is`

`==` compara **valores**, `is` compara **identidad** (si son el mismo objeto).

```python
a = 100;  b = 100;   a is b     # True
a = 1000; b = 1000;  a is b     # False (normalmente)
```

Python precrea los enteros de −5 a 256, así que `is` parece funcionar con números
pequeños y falla con grandes. **Usa `is` solo con `None`, `True` y `False`.**

### `and` / `or` devuelven un valor

```python
0 or "por defecto"      # 'por defecto'
nombre = entrada or "anónimo"     # si entrada está vacía, "anónimo"
```

Y cortocircuitan: `if i < len(v) and v[i] == x:` no evalúa `v[i]` si `i` está fuera de
rango.

### `in`

```python
3 in [1, 2, 3]      # True, pero O(n)
3 in {1, 2, 3}      # True, y O(1)
"ol" in "hola"      # True (subcadena)
"k" in {"k": 1}     # True (busca en las CLAVES)
```

!!! tip "`in` sobre una lista es O(n)"
    Dentro de un bucle es un O(n²) silencioso y un Time Limit Exceeded. Si vas a
    consultar muchas veces, convierte la lista en `set` primero.

### Secuencias y rebanadas

```python
[1, 2] + [3]        # concatenar
[0] * 5             # repetir
v[1:3]   v[:3]   v[2:]   v[::2]   v[-1]
v[::-1]             # al revés  ← la forma corta de dar la vuelta
```

!!! warning "`[[0] * m] * n` no crea una matriz"
    ```python
    m = [[0] * 3] * 2
    m[0][0] = 1
    print(m)      # [[1, 0, 0], [1, 0, 0]]  ← ¡las dos filas!
    ```
    El `*` externo copia **la misma referencia**. La forma correcta es una comprensión:
    ```python
    m = [[0] * 3 for _ in range(2)]
    ```

Y una nota de precedencia: `-2 ** 2` es `-4`, porque `**` va antes que el menos unario.

## Entrada y salida

Fichas: [Input/Output](../../fundamentals/io/index.md) y
[E/S rápida](../../fundamentals/fast-io/index.md).

```python
n = int(input())
a, b = map(int, input().split())
v = list(map(int, input().split()))
s = input().strip()                  # quita espacios y saltos
```

Esa segunda línea es la más escrita de todo Python competitivo. De dentro afuera:
`input()` da `'3 7'`, `.split()` da `['3','7']`, `map(int, ...)` convierte, y la
asignación desempaqueta.

### Los patrones

```python
n = int(input())
v = [int(input()) for _ in range(n)]              # N líneas anunciadas

import sys
for linea in sys.stdin:                            # hasta el final de la entrada
    n = int(linea)

datos = sys.stdin.read().split()                   # todo de golpe: lo más rápido
```

!!! warning "No uses `input()` en un bucle hasta EOF"
    ```python
    while True:
        n = int(input())     # EOFError al acabarse la entrada → Run Time Error
    ```
    `for linea in sys.stdin:` es más corto, más rápido y no lanza nada.

### Leer rápido

```python
import sys
input = sys.stdin.readline
```

Con esa línea, todo tu código sigue igual pero lee ~5 veces más rápido. `input()` hace
comprobaciones extra y decodifica línea a línea; con 10⁶ líneas es la diferencia entre
Accepted y Time Limit Exceeded.

!!! warning "`readline` **no** quita el salto de línea"
    A diferencia de `input()`. Con números da igual (`int()` lo ignora), pero con texto
    hace falta `.strip()`.

| Forma | Relativo |
|-------|----------|
| `input()` | 1× |
| `sys.stdin.readline` | ~5× |
| `sys.stdin.read().split()` | ~10× |

### Escribir rápido

Cada `print` es una llamada al sistema. Con muchas líneas, **acumula y escribe una vez**:

```python
salida = []
for x in v:
    salida.append(str(x))
print("\n".join(salida))
```

Y para decimales, la f-string:

```python
print(f"{x:.6f}")
```

!!! warning "`round` no redondea como crees"
    `round(0.5)` es `0`, `round(1.5)` es `2` y `round(2.5)` es `2`: es redondeo bancario,
    los empates van al par. Si quieres el de toda la vida, `math.floor(x + 0.5)`.

Para depurar sin ensuciar la salida: `print("n vale", n, file=sys.stderr)`.

## Condicionales

Ficha corta: [Condicionales en Python](../../fundamentals/conditionals/python.md).

```python
if a > b:
    ...
elif a < b:              # una sola palabra: no existe `else if`
    ...
else:
    ...
```

Las ramas se evalúan **en orden**: con condiciones solapadas, ordena de la más
restrictiva a la más general (`if nota >= 5 ... elif nota >= 9` nunca llega al segundo).

```python
if 0 <= x < n and v[x] > 0: ...          # encadenar + cortocircuito
mayor = a if a > b else b                # ternario: valor if cond else valor
v = [x if x > 0 else 0 for x in v]       # útil dentro de otra expresión
```

`match` (Python 3.10+) compara contra **patrones** con `case`, `|` para agrupar y `_`
como defecto. Comprueba la versión del juez antes de usarlo; y para dos o tres opciones,
una cadena de `elif` es igual de clara.

!!! warning "Cuidado con el 0 que sí importa"
    `if valor:` es falso también cuando `valor == 0`. Si el cero es un dato legítimo,
    escribe `if valor is not None:`.

Un `elif` que debería ser `if`: si las dos condiciones son independientes, son dos `if`
separados.

## Bucles

Ficha corta: [Bucles en Python](../../fundamentals/loops/python.md).

En Python el `for` **recorre una secuencia**, no cuenta. No hay `for (i = 0; ...)`.

```python
for x in v: ...
for c in "hola": ...
for clave in diccionario: ...

for i in range(n): ...              # 0 .. n-1   (el final NUNCA se incluye)
for i in range(1, n + 1): ...       # 1 .. n
for i in range(n - 1, -1, -1): ...  # al revés
for i, x in enumerate(v): ...              # índice y valor
for nombre, nota in zip(nombres, notas): ...   # dos secuencias a la vez
```

`enumerate` en vez de `for i in range(len(v))`, y `zip(*matriz)` transpone una matriz.
`range` no crea la lista: `range(10**9)` no ocupa memoria.

No hay `do ... while`, y el `else` de un bucle significa **«si no hubo `break`»**, que es
útil para búsquedas aunque la palabra elegida sea desafortunada.

Para salir de dos bucles, lo más limpio es sacar el código a una función y usar `return`.

### Saca el trabajo del bucle

En Python, un bucle escrito a mano es lento porque cada vuelta pasa por el intérprete.
Las funciones integradas hacen el bucle en C:

```python
total = 0
for x in v:            # lento
    total += x

total = sum(v)         # varias veces más rápido
```

Lo mismo con `max`, `min`, `len`, `any`, `all`, `sorted`, `"".join`. **Es la optimización
más rentable de Python competitivo.**

### Errores

```python
for x in v:
    if x < 0:
        v.remove(x)          # salta elementos, o peta
v = [x for x in v if x >= 0] # así

for i in range(3): pass
print(i)                     # 2  ← la variable SOBREVIVE: el for no crea ámbito
```

Y recuerda que los bucles anidados **multiplican** el coste. Ver
[Complejidad](../../fundamentals/complexity/index.md).

## Cadenas de texto

```python
s = "competitiva"
s[0]        # 'c'
s[-1]       # 'a'
s[2:5]      # 'mpe'
s[::-1]     # al revés
len(s)
```

### Son inmutables, y eso importa

```python
s = ""
for i in range(100000):
    s += "a"              # O(n²): cada += crea una cadena NUEVA

s = "".join(partes)       # O(n)
```

**Nunca construyas una cadena concatenando en un bucle.** Acumula en una lista y haz
`join` al final. Es una causa habitual de Time Limit Exceeded.

### Los métodos que salen siempre

```python
"a b c".split()          # ['a','b','c']  (por espacios, ignora los repetidos)
"a,b,c".split(",")
" ".join(["a","b"])      # 'a b'    ← necesita cadenas: map(str, v) con números
"  hola  ".strip()       # imprescindible al leer con readline
"Hola".upper()   .lower()
"hola".find("z")         # -1 si no está
"ol" in "hola"           # más cómodo para comprobar
"hola".replace("o","0")  .count("o")  .startswith("ho")
"123".isdigit()          # validar antes de un int()
```

### Caracteres

```python
ord('a')    # 97
chr(97)     # 'a'

cuenta = [0] * 26
for c in s:
    cuenta[ord(c) - ord('a')] += 1     # el truco del índice alfabético

import string
string.ascii_lowercase                  # 'abc...z'
```

Aunque en Python suele ser más cómodo `Counter(s)`.

### Comparar y ordenar

```python
"abc" < "abd"                    # orden lexicográfico
sorted(v, key=len)
"".join(sorted("hola"))          # 'ahlo'
sorted(a) == sorted(b)           # ¿son anagramas? en una línea
```

## Listas y tuplas

Ficha corta: [Arrays](../../data-structures/lists/index.md).

Una lista de Python es un **array dinámico**: es el `vector` de C++.

```python
v = []
v = [0] * 5
v = list(range(5))

v[0]   v[-1]   v[1:3]   len(v)
v.append(x)      # O(1)
v.pop()          # O(1)
v.pop(0)         # O(n)  ← usa deque si necesitas esto
v.insert(0, x)   # O(n)
v.remove(x)      # O(n)
v.index(x)   v.count(x)   v.reverse()   v.clear()
```

### `sort` frente a `sorted`

```python
v.sort()             # modifica v y devuelve None
w = sorted(v)        # NO modifica v, devuelve una lista nueva
v.sort(reverse=True)
v.sort(key=lambda p: (p[1], p[0]))
```

!!! warning "`v = v.sort()` deja `v` a `None`"
    Es el error más común con listas: `sort()` no devuelve nada.

### Matrices

```python
m = [[0] * columnas for _ in range(filas)]     # ✔
m = [[0] * columnas] * filas                    # ✗ todas las filas son la MISMA
```

Memoriza la primera. Es de los errores que más caros salen porque el programa funciona
en el ejemplo pequeño.

### Tuplas

Como una lista pero **inmutable**, y por eso pueden ser clave de un diccionario:

```python
t = (1, 2, 3)
t = 1, 2, 3                       # los paréntesis son opcionales
t1 = (1,)                         # una sola: OJO con la coma
primero, *resto = [1, 2, 3, 4]    # desempaquetado con estrella
n, *v = map(int, input().split()) # el primero es n, el resto la lista

visitado[(3, 5)] = True           # coordenadas como clave
(1, 2) < (1, 3)                   # se comparan LEXICOGRÁFICAMENTE
```

Eso último las hace perfectas para ordenar por varios criterios: un
`v.sort()` sobre tuplas `(peso, nombre)` ordena por peso y, a igualdad, por nombre.

### Pilas y colas

```python
pila = []
pila.append(x);  x = pila.pop()          # LIFO: la lista ya es una pila

from collections import deque
cola = deque()
cola.append(x);  x = cola.popleft()      # FIFO, las dos en O(1)
```

**No uses una lista como cola**: `pop(0)` es O(n) porque desplaza todo. Ver
[Stack & queue](../../data-structures/stack-queue/index.md).

## Diccionarios y conjuntos

Ficha corta: [Dictionaries / maps](../../data-structures/dictionaries/index.md).

```python
d = {"a": 1}
d["b"] = 2
d["a"] += 1
if "a" in d: ...        # comprueba las CLAVES, O(1)
del d["a"]
for clave, valor in d.items(): ...
```

Las claves deben ser **inmutables** (números, cadenas, tuplas; no listas). Y los
diccionarios mantienen el **orden de inserción** desde Python 3.7 — que no es orden
alfabético: si lo quieres, `sorted(d)`.

!!! warning "`d[clave]` lanza `KeyError`"
    A diferencia de C++, consultar **no** crea la entrada: revienta.
    ```python
    d["z"]            # KeyError
    d.get("z", 0)     # 0   ← valor por defecto
    ```

### Las variantes útiles

```python
from collections import defaultdict, Counter

cuenta = defaultdict(int)      # las claves nuevas valen 0
cuenta[x] += 1                 # sin comprobar si existe

g = defaultdict(list)          # las claves nuevas son []
g[a].append(b)                 # la forma estándar de construir un grafo

c = Counter("abracadabra")
c["a"]                         # 5
c.most_common(2)               # [('a', 5), ('b', 2)]
Counter(a) == Counter(b)       # ¿son permutación uno del otro?
```

(`OrderedDict` ya no hace falta: el `dict` normal mantiene el orden.)

### Conjuntos

```python
s = set()             # OJO: {} es un DICCIONARIO vacío
s = {1, 2, 3}
s.add(4);  s.discard(4);  4 in s      # todo O(1)

a | b     # unión
a & b     # intersección
a - b     # diferencia
a <= b    # ¿subconjunto?

v = sorted(set(v))    # quitar duplicados, ordenado, en una línea
```

### El coste

| Operación | Medio |
|-----------|-------|
| `d[k]`, `k in d`, `x in s` | O(1) |
| **`x in lista`** | **O(n)** |

Esa última fila es la que cuesta Time Limit Exceeded. Y si las claves son **enteros
pequeños y acotados**, una lista indexada (`cuenta = [0] * 1000001`) es más rápida que
cualquier diccionario.

## Comprensiones

Construir una lista a partir de otra, en una línea. Es la construcción más
característica de Python.

```python
cuadrados = [x * x for x in range(10)]
pares = [x for x in v if x % 2 == 0]          # el if del FINAL filtra
signos = [1 if x > 0 else -1 for x in v]      # el condicional del principio transforma
pares = [(i, j) for i in range(3) for j in range(3)]   # anidado, en el mismo orden
```

Dos posiciones distintas para dos cosas distintas:

```python
[x for x in v if cond]           # FILTRAR: se queda con algunos
[a if cond else b for x in v]    # TRANSFORMAR: los mantiene todos
```

Son más cortas y un 30–50 % más rápidas que el `for` + `append`, porque el bucle se
ejecuta en C. Pero si no se leen de un vistazo, escribe el bucle — y nunca las uses solo
por el efecto secundario (`[print(x) for x in v]` construye una lista de `None` para
nada).

```python
cuadrados = {x: x*x for x in range(5)}        # de diccionario
inverso = {v: k for k, v in d.items()}        # invertir un diccionario
unicos = {x % 10 for x in v}                  # de conjunto
```

### Expresiones generadoras

Con paréntesis en vez de corchetes, **no construyen la lista**:

```python
sum([x*x for x in range(10**7)])    # ~400 MB
sum(x*x for x in range(10**7))      # memoria constante
```

Cuando el resultado se consume una vez —dentro de `sum`, `max`, `any`, `all`, `join`—
quita los corchetes. Además `any`/`all` **cortocircuitan**.

### Los patrones de lectura

```python
n, m = map(int, input().split())
matriz = [list(map(int, input().split())) for _ in range(n)]   # una matriz entera
rejilla = [input().strip() for _ in range(n)]                   # una rejilla de caracteres
plana = [x for fila in matriz for x in fila]                    # aplanar
```

## Funciones

```python
def suma(a, b):
    return a + b
```

Sin `return` devuelve `None`. Devolver varios valores es devolver una **tupla**:
`return min(v), max(v)`.

```python
def potencia(base, exp=2): ...      # valor por defecto, al final de la lista
potencia(3)        # 9
potencia(base=3, exp=4)             # por nombre

def total(*numeros): return sum(numeros)     # recoge los posicionales en una tupla
total(*[1, 2, 3])                            # el * también desempaqueta al llamar
```

!!! warning "Nunca uses un mutable como valor por defecto"
    ```python
    def añadir(x, lista=[]):        # MAL
        lista.append(x)
        return lista

    añadir(1)      # [1]
    añadir(2)      # [1, 2]   ← ¡la misma lista!
    ```
    El valor por defecto se evalúa **una sola vez**, al definir la función. La forma
    correcta es `lista=None` y `if lista is None: lista = []`.

### Las funciones son objetos

```python
f = doble                       # sin paréntesis: guardas la función
list(map(doble, [1, 2, 3]))     # la pasas a otra función
sorted(v, key=len)
```

### Funciones dentro de funciones

La interna **ve** las variables de la externa (una *clausura*), y eso hace muy cómoda la
recursión anidada:

```python
def main():
    g = leer_grafo()
    vis = [False] * n

    def dfs(u):
        vis[u] = True          # MODIFICAR el contenido: funciona sin más
        for v in g[u]:
            if not vis[v]:
                dfs(v)         # ve g y vis sin recibirlos

    dfs(0)

main()
```

!!! tip "Mete la solución en `main()`"
    No es cosmética: acceder a una variable **local** es más rápido que a una global en
    Python, y en un bucle grande se nota. Es gratis.

## Ámbito y mutabilidad

Estas dos cosas causan más errores de Python que ninguna otra.

### La regla LEGB

Python busca un nombre en la función **L**ocal, en la **E**nvolvente, en la **G**lobal y
en las integradas (**B**uilt-in), y se para en la primera. Por eso `list = [1,2,3]` rompe
`list()`.

**Leer** una global funciona. **Asignarla** crea una local nueva:

```python
n = 10
def f():
    print(n)      # UnboundLocalError
    n = 20        # esta línea hace n local en TODA la función
```

Python decide si un nombre es local **al compilar la función**, no al ejecutarla: basta
una asignación en cualquier punto. Para asignar de verdad, `global n` o `nonlocal n`.

### Mutable frente a inmutable

| Inmutables | Mutables |
|------------|----------|
| `int`, `float`, `bool`, `str`, `tuple`, `frozenset` | `list`, `dict`, `set`, tus objetos |

Y la regla que resume cómo se pasan los argumentos:

> **Modificar el contenido** de un mutable se ve fuera.
> **Reasignar el nombre** nunca se ve fuera.

```python
def f(v): v.append(4)      # modifica la lista de fuera
def g(v): v = [9, 9]       # solo reapunta el nombre local: fuera, nada
```

Por eso `vis[u] = True` dentro de una función anidada funciona sin `nonlocal`, y
`vis = []` no.

### Copias

```python
b = a              # NO copia: dos nombres, UNA lista  ← aliasing
b = a[:]           # copia el primer nivel
import copy
b = copy.deepcopy(a)   # copia todo, y es LENTA
```

La copia superficial no basta con listas de listas: las filas siguen compartidas. En
concurso casi siempre sale más barato reconstruir la estructura que copiarla con
`deepcopy`.

## Clases y objetos

Para poco. Un problema de concurso se resuelve con listas, diccionarios y funciones; una
**tupla** o un **diccionario** bastan casi siempre y son más rápidos. Las clases
aparecen en una estructura de datos propia (un *segment tree*, un *union-find*) o cuando
necesitas objetos ordenables.

```python
class Punto:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def norma2(self):
        return self.x**2 + self.y**2

p = Punto(3, 4)
print(p.norma2())     # 25
```

`self` es el primer parámetro de todos los métodos (no lo pasas al llamar), y dentro hay
que escribir `self.x`: sin el `self`, `x` sería local.

### Los métodos que merecen la pena

```python
def __repr__(self):  return f"Punto({self.x}, {self.y})"     # imprimir: para DEPURAR
def __eq__(self, o): return (self.x, self.y) == (o.x, o.y)
def __hash__(self):  return hash((self.x, self.y))           # va en pareja con __eq__
def __lt__(self, o): return (self.x, self.y) < (o.x, o.y)    # ordenar y heapq
```

Sin `__repr__` verías `<__main__.Punto object at 0x7f...>`. Y si defines `__eq__` sin
`__hash__`, el objeto deja de poder ir en un `set`.

### Las alternativas cortas

```python
from collections import namedtuple
Punto = namedtuple("Punto", ["x", "y"])     # inmutable, comparable, ordenable, hashable

from dataclasses import dataclass
@dataclass
class Punto:                                 # genera __init__, __repr__ y __eq__
    x: int = 0
    y: int = 0
```

`namedtuple` si solo agrupas datos; `dataclass` si además los modificas. `__slots__`
ahorra memoria si vas a crear millones de objetos. Herencia: existe y no la necesitas.

## Módulos e importaciones

Un módulo es **un fichero `.py`**. La librería estándar son cientos de ellos, y es lo
único que vas a tener en el juez.

```python
import sys
from collections import deque, defaultdict
from math import gcd, isqrt, inf
import numpy as np        # ← esto NO está en el juez
```

En concurso se usa mucho la forma `from ... import ...`: escribes `deque(...)` en vez de
`collections.deque(...)`.

!!! warning "Nunca `from modulo import *`"
    Trae cientos de nombres y puede tapar los tuyos:
    ```python
    from math import *
    pow(2, 10, 1000)     # TypeError: math.pow solo acepta 2 argumentos
    ```
    El `pow` integrado, que sí acepta el módulo, ha quedado tapado.

Python busca primero en la carpeta del fichero que ejecutas: de ahí que llamar a tu
fichero `random.py` rompa `import random`.

El juez acepta **un fichero**, así que si tienes una biblioteca personal, la pegas dentro
antes de enviar. Y `if __name__ == "__main__":` no hace falta: el juez ejecuta tu
fichero, nunca lo importa.

## Módulos imprescindibles

Todo esto está en el juez y ya está optimizado.

```python
import sys
input = sys.stdin.readline          # lectura rápida
sys.setrecursionlimit(300000)
print("traza", file=sys.stderr)
```

```python
import math
math.isqrt(17)     # 4   raíz entera EXACTA (mejor que int(sqrt(n)))
math.gcd(12, 18)   math.lcm(4, 6)
math.comb(10, 3)   math.perm(10, 3)      # combinaciones y permutaciones
math.factorial(20)   math.inf   math.isclose(a, b)   math.log2(1024)
```

!!! tip "`isqrt` en vez de `int(sqrt(n))`"
    `math.sqrt` devuelve un `float`, y con números grandes el redondeo da el valor
    equivocado. `isqrt` es exacta.

`math.comb` hace innecesario implementar el binomio de Newton para números pequeños. Ver
[Combinatoria](../../combinatorics/combinatory/index.md).

```python
from collections import deque, Counter, defaultdict      # ver secciones anteriores

import heapq                                  # cola de prioridad DE MÍNIMOS
heapq.heappush(h, 3);  h[0];  heapq.heappop(h)
heapq.heapify(v)                              # O(n)
heapq.heappush(h, -x); -heapq.heappop(h)      # montículo de MÁXIMOS: niega
heapq.heappush(h, (distancia, nodo))          # con prioridad y dato: base de Dijkstra

import bisect                                 # búsqueda binaria, sobre lista ORDENADA
bisect.bisect_left(v, x)    # primer índice donde insertar (y cuántos son < x)
bisect.bisect_right(v, x)
bisect.bisect_right(v,x) - bisect.bisect_left(v,x)    # cuántas veces aparece x

from itertools import permutations, combinations, product, accumulate
list(product([0,1], repeat=3))       # sustituye 3 bucles anidados
list(accumulate([1,2,3,4]))          # [1,3,6,10]  sumas prefijas

from functools import cache, reduce, cmp_to_key
```

Ver [Priority queue](../../data-structures/priority-queue/index.md),
[Binary search](../../search/binary-search-array/index.md) y
[sumas prefijas](../../data-structures/prefix-sums/index.md).

`string.ascii_lowercase` y `re` para texto, y `random` para **generar casos de prueba**
(no para resolver).

## Lambdas y funciones de orden superior

Ficha corta: [Lambda](../../fundamentals/lambda/index.md).

```python
sorted(v, key=lambda p: p[1])
```

`lambda parametros: expresion` — una **sola expresión**, sin `return`. Nada de `if` en
bloque, bucles ni asignaciones: si necesitas eso, es un `def`. Y no le pongas nombre a
una lambda (`doble = lambda x: x*2`): para eso está `def`.

### Ordenar, que es el uso principal

```python
sorted(v, key=len)                              # por longitud
sorted(v, key=lambda s: s.lower())              # ignorando mayúsculas
sorted(v, reverse=True)
sorted(alumnos, key=lambda a: (-a[1], a[0]))    # nota desc., nombre asc.
```

`key` recibe una función que dice **con qué se compara** cada elemento, y se llama una
vez por elemento (no en cada comparación). Para varios criterios, devuelve una **tupla**.

El truco del `-` solo vale con números. Con cadenas, aprovecha que la ordenación es
**estable** y ordena en dos pasadas:

```python
v.sort(key=lambda a: a[0])                     # primero el criterio secundario
v.sort(key=lambda a: a[1], reverse=True)       # después el principal
```

```python
max(v, key=len)                        # el más largo
max(alumnos, key=lambda a: a[1])       # el de mayor nota
max(range(n), key=lambda i: v[i])      # el ÍNDICE del máximo
```

### `map`, `filter` y decoradores

```python
list(map(int, input().split()))    # map con una función EXISTENTE: limpio
[x * 2 for x in v]                 # con una expresión: comprensión, no map+lambda
```

`map` y `filter` devuelven **iteradores**. Y el decorador que de verdad usarás:

```python
from functools import cache

@cache
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)
```

`cmp_to_key` existe para comparadores al estilo C++ (devuelven negativo/cero/positivo).
Es más lento que `key`: úsalo solo cuando el criterio no se pueda expresar como clave.

## Iteradores y generadores

Ficha corta: [Iteradores](../../fundamentals/iterators/index.md).

Un **iterable** se puede recorrer; un **iterador** va devolviendo los elementos y **se
agota**.

```python
it = iter([1, 2, 3])
next(it)      # 1
next(it)      # 2
```

Un `for` hace exactamente eso: `iter(...)`, `next(...)` repetido, y para cuando salta
`StopIteration`.

### `yield`

```python
def fibonacci():
    a, b = 0, 1
    while True:            # infinito, y no pasa nada
        yield a
        a, b = b, a + b
```

`yield` **devuelve un valor y congela la función** donde está; en el siguiente `next`
continúa justo después, con las variables intactas. Un generador infinito es útil porque
**solo se calcula lo que consumes**. Y `yield from` delega en otro iterable.

### Evaluación perezosa

`range`, `map`, `filter`, `zip`, `enumerate` y `d.items()` devuelven iteradores, no
listas. Eso ahorra memoria, pero:

!!! warning "Un iterador se agota"
    ```python
    m = map(int, ["1", "2", "3"])
    list(m)     # [1, 2, 3]
    list(m)     # []   ← ya se consumió
    ```
    Si vas a recorrerlo dos veces, guárdalo con `list(...)`. Es la causa de resultados
    vacíos inexplicables.

Y `print(map(int, v))` imprime `<map object at 0x...>`, no la lista.

```python
from itertools import count, cycle, islice
list(islice(count(1), 10))       # los 10 primeros de un infinito
```

Para hacer iterable una clase propia, un generador en `__iter__` es mucho más corto que
`__iter__` + `__next__`.

## Recursión y su límite

Ficha corta: [Recursión](../../fundamentals/recursion/index.md).

```python
def factorial(n):
    if n <= 1:          # caso base
        return 1
    return n * factorial(n - 1)    # caso recursivo, MÁS PEQUEÑO
```

### El límite

```python
def f(n): return 0 if n == 0 else f(n - 1)
f(2000)      # RecursionError: maximum recursion depth exceeded
```

Python pone un tope artificial de **1000 llamadas**, que es bajísimo para concursos:
cualquier DFS sobre un grafo de más de mil nodos lo supera.

```python
import sys
sys.setrecursionlimit(300000)
```

Ponlo en la plantilla y olvídate.

!!! warning "Subirlo no siempre basta"
    `setrecursionlimit` levanta el tope **de Python**, pero la pila del sistema sigue
    siendo finita (~8 MB). Si te pasas de verdad, el programa se cierra sin *traceback*
    (`Segmentation fault`), que el juez reporta como Run Time Error. Y ponerlo a mil
    millones solo cambia cómo se cae.

Si n puede llegar a 10⁶ y el grafo puede ser un camino, escribe la versión **iterativa**
desde el principio:

```python
def dfs(inicio):
    pila = [inicio]
    vis[inicio] = True
    while pila:
        u = pila.pop()
        for v in g[u]:
            if not vis[v]:
                vis[v] = True
                pila.append(v)
```

Es la misma idea: lo que guardaba la pila de llamadas lo guardas tú en una lista.

### Memoización

```python
def fib(n):                                   # O(2^n): fib(35) tarda segundos
    return n if n <= 1 else fib(n-1) + fib(n-2)

from functools import cache
@cache
def fib(n):                                   # O(n): fib(200) instantáneo
    return n if n <= 1 else fib(n-1) + fib(n-2)
```

**Una línea.** Es lo mejor que tiene Python para
[programación dinámica](../../dynamic-programming/dynamic-programming/index.md). (En
Python < 3.9, `@lru_cache(maxsize=None)`.) Requisito: los argumentos deben ser
**hashables** — tuplas, no listas.

### Vuelta atrás

```python
def permutar(v, k):
    if k == len(v):
        print(*v)
        return
    for i in range(k, len(v)):
        v[k], v[i] = v[i], v[k]      # probar
        permutar(v, k + 1)           # seguir
        v[k], v[i] = v[i], v[k]      # DESHACER  ← la esencia del backtracking
```

Si no restauras el estado, las siguientes ramas parten de datos corruptos: Wrong Answer
difícil de encontrar. Ver [Backtracking](../../search/backtracking/index.md) y
[DFS](../../graphs/dfs/index.md).

## Rincones del lenguaje

### Desempaquetado y rebanadas

```python
a, *resto = [1, 2, 3, 4]
n, *v = map(int, input().split())     # entradas de longitud variable
c = [*a, *b]                          # concatenar
d = {**d1, **d2}                      # fusionar diccionarios

v[1:3] = [9]          # asignar a una rebanada cambia el tamaño
v[:] = [7, 8]         # sustituye el CONTENIDO sin cambiar el objeto
del v[1:3]
```

Ese `v[:] = ...` es el truco para modificar una lista desde dentro de una función y que
se vea fuera.

### Excepciones

```python
try:
    n = int(input())
except ValueError:
    n = 0
except EOFError:
    break
finally:
    ...
```

Captura **lo que esperas**: un `except:` desnudo atrapa todo, incluido `Ctrl+C`, esconde
errores de programación y te deja depurando a ciegas.

`with open(...)` cierra el fichero solo — pero en concurso no abrirás ficheros, así que
apenas aparece.

### Lo que hay que saber que existe

```python
enumerate(v, start=1)         zip(*matriz)          divmod(17, 5)
min(v, default=0)             max(v, default=0)     # evita ValueError con lista vacía
str.zfill(5)                  int("1010", 2)        bin(10)  hex(10)
math.prod(v)                  n.bit_length()        n.bit_count()   # 3.10+
isinstance(x, (int, float))
```

Y un aviso de estilo: `print(" ".join(map(str, sorted(set(map(int, input().split()))))))`
funciona, impresiona y no se lee. Pártela.

## Rendimiento en concurso

### Cuánto más lento

Entre **10 y 100 veces** más lento que C++: es interpretado, todo es un objeto y el
tipado es dinámico. Donde C++ hace 10⁸ operaciones por segundo, Python hace
**10⁶–10⁷**.

| n | C++ | Python |
|---|-----|--------|
| 10⁵ | cualquier cosa razonable | bien |
| 10⁶ | bien | justo: hay que cuidar el bucle |
| 10⁷ | bien | solo con funciones integradas |
| 10⁸ | O(n) cabe | no |

Esto **no** significa que Python no sirva: significa que la complejidad tiene que estar
bien y que los bucles internos hay que sacarlos del intérprete. Ver
[Complejidad (Big-O)](../../fundamentals/complexity/index.md).

### Lo que se aplica siempre

```python
import sys
input = sys.stdin.readline        # ~5x
print("\n".join(salida))          # ~10x frente a un print por línea
```

Con 10⁵ líneas, esas dos cosas solas pueden ser la diferencia entre TLE y Accepted.

### Lo que más se gana después

1. **Sacar el trabajo del bucle**: `sum`, `max`, `any`, `all`, `join`, comprensiones.
2. **`set` en vez de `in` sobre listas.** La que más veces convierte un TLE en Accepted.
3. **No concatenar cadenas en un bucle**: `"".join(...)`.
4. **Meter la solución en `main()`**: las variables locales son más rápidas.
5. **Memoizar** con `@cache` y **precalcular** (sumas prefijas, cribas, factoriales).

### Cuándo Python no llega

Si tu complejidad es la correcta, la has comprobado, y aun así da TLE:

- **PyPy**, si el juez lo ofrece como lenguaje aparte: el mismo código, varias veces más
  rápido. Codeforces lo tiene.
- **Reescribir en [C++](../cpp/index.md).** Para los problemas más exigentes es la única
  salida, y no es un fracaso: lo normal es pensar en Python y pasar a C++ lo que va justo.

`numpy` no está en el juez, y aunque estuviera ayuda menos de lo que parece: los
algoritmos de concurso (grafos, DP con dependencias, búsquedas) no se vectorizan.

### Medir

```python
import time
t0 = time.perf_counter()
...
print(f"{time.perf_counter()-t0:.3f}s", file=sys.stderr)
```

Con la entrada **más grande posible**, no con el ejemplo del enunciado. Y arregla la
complejidad antes que las constantes: si es O(n²) con n = 10⁵, ninguna cantidad de `join`
lo salva.

## Qué se puede usar en un concurso

La regla es corta: **un fichero fuente, la librería estándar y nada más**. El juez
ejecuta tu programa en una máquina aislada con la entrada por `stdin`. Todo lo que se
salga de ahí —un paquete que hay que instalar, un fichero del disco, una conexión a
Internet— o no está o está prohibido.

### Sí

**Toda la librería estándar**, que para concursos es muchísimo: `sys`, `math`,
`collections`, `heapq`, `bisect`, `itertools`, `functools`, `decimal`, `fractions`,
`string`, `re`, `random`. Más tu propio código, pegado en el fichero que envías. Y
`sys.setrecursionlimit`, que está permitido y a menudo hace falta.

### No

- **Paquetes externos.** `numpy`, `pandas`, `scipy`, `networkx`, `sympy`, `requests`: no
  están. Tu envío falla nada más arrancar con un `ModuleNotFoundError`. Es la diferencia
  más chocante si vienes de análisis de datos: aquí `numpy` no existe y las listas
  normales son tu única estructura.
- **Ficheros, sistema operativo y red.** Nada de `open("datos.txt")`, `os.system`,
  `subprocess`, `socket` ni `urllib`.
- **Hilos y paralelismo.** `threading` y `multiprocessing` no sirven para ganar tiempo:
  el juez mide el tiempo de CPU total y normalmente da un solo núcleo.
- **Trampas.** Intentar leer los casos de prueba, detectar en qué caso estás para
  responder a mano, escribir en `stderr` para esquivar la comparación: detectado, es
  descalificación.

!!! tip "La regla práctica"
    Si has tenido que hacer `pip install` alguna vez para usarlo, **no está en el juez**.
    Si viene con Python recién instalado, sí.

!!! warning "El truco de redirigir `stdin` en el código"
    Es cómodo probar en local con `sys.stdin = open("entrada.txt")`. **Bórralo antes de
    enviar**: en el juez ese fichero no existe. Redirige desde la terminal
    (`python3 solucion.py < entrada.txt`) y no toques el código.

### En un concurso presencial (ICPC)

**Sin Internet** salvo el juez, **sin comunicación** fuera del equipo, **un solo
ordenador** para los tres, y **material impreso sí**, con el límite de páginas que fije
la organización — es tu [chuletario](../../../cheatsheet/index.md).

### Compruébalo antes de competir

Mira la página de lenguajes del juez (en Kattis, *Help → Languages*) y apunta **qué
versión de Python** usa y **si ofrece PyPy**. Pero la prueba definitiva es más simple:
**envía un problema trivial con tu plantilla** antes del concurso. Si pasa, tu plantilla
es válida.

## Errores frecuentes

### Que no arrancan

`IndentationError` / `TabError` (4 espacios, nunca tabuladores); `SyntaxError` por los
dos puntos o un paréntesis —que puede señalar la línea **siguiente**—; `NameError` por
una errata; y un fichero llamado como un módulo estándar.

### Que dan Wrong Answer

```python
10 / 2                          # 5.0 en vez de 5  ← el error #1
-7 // 2                         # -4  (C++ da -3)
round(2.5)                      # 2   (redondeo bancario)
b = a                           # NO copia: b = a[:]
[[0]*3]*2                       # las dos filas son la MISMA
v = v.sort()                    # v pasa a valer None
def f(lista=[])                 # compartida entre todas las llamadas
list(m); list(m)                # la segunda vez el iterador está agotado
print(x, end=" ")               # deja un espacio final: print(*v)
```

!!! warning "Los índices negativos NO dan error"
    `v[-1]` es el último elemento. Si calculas un índice y sale `-1` por error, obtienes
    un valor equivocado **sin ninguna excepción**: es un Wrong Answer, no un RTE, y es
    mucho más difícil de encontrar que en C++.

### Que dan Run Time Error

`IndexError`; `KeyError` (usa `d.get(k, 0)`); `ValueError` (`int("")`, `int("3.5")`);
`EOFError` al leer de más; `ZeroDivisionError`; `RecursionError`; `TypeError` (`"1" + 1`);
`ModuleNotFoundError`.

### Que dan Time Limit Exceeded

`input()` en vez de `sys.stdin.readline` (la causa número uno); un `print` por línea;
`+=` sobre cadenas en un bucle; `in` sobre una lista dentro de un bucle; `lista.pop(0)`;
bucles anidados que sobran; recursión sin memoizar.

### Que dan Memory Limit Exceeded

Construir una lista enorme donde bastaba un generador, y guardar toda la entrada sin
necesitarla. Una lista de 10⁶ enteros ocupa ~40 MB, diez veces más que en C++.

### Checklist antes de enviar

```text
□ Pasa TODOS los ejemplos del enunciado
□ Probado con los extremos del rango (mínimo, máximo, 0, negativos)
□ ¿Hay algún / que debería ser //?
□ Sin prints de depuración, sin sys.stdin = open(...)
□ Sin imports de paquetes que no están (numpy, etc.)
□ input = sys.stdin.readline si la entrada es grande
□ La salida es un solo print con join si hay muchas líneas
□ sys.setrecursionlimit si hay recursión
□ La complejidad cabe en el límite del enunciado
□ El formato de salida es EXACTAMENTE el del enunciado
```

## Plantilla de concurso

La mínima:

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    # resolver
    print(resultado)

main()
```

La ampliada:

```python
import sys
from collections import deque, defaultdict, Counter
from functools import cache
from heapq import heappush, heappop
from math import gcd, isqrt, inf
from bisect import bisect_left, bisect_right

input = sys.stdin.readline
sys.setrecursionlimit(300000)

MOD = 10**9 + 7

def leer_int():   return int(input())
def leer_ints():  return list(map(int, input().split()))

def main():
    n = leer_int()
    v = leer_ints()

    # resolver

    print(resultado)

main()
```

### Para entradas enormes

```python
def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    def leer():
        nonlocal pos
        pos += 1
        return int(datos[pos - 1])

    n = leer()
    v = [leer() for _ in range(n)]
```

`sys.stdin.buffer` lee bytes sin decodificar: es lo más rápido que hay.

### Para varios casos de prueba

```python
def resolver():
    n = int(input())
    return 3 * n + 5

def main():
    salida = []
    T = int(input())
    for _ in range(T):
        salida.append(str(resolver()))
    print("\n".join(salida))
```

Sacar el caso a una función permite `return` sin tocar el bucle, y se acumula la salida
para un solo `print`.

!!! warning "Reinicializa el estado entre casos"
    Si usas globales o memoización, límpialas al empezar cada caso (`f.cache_clear()`).
    Arrastrar el estado del anterior es un Wrong Answer que **solo aparece con varios
    casos**.

### Cómo usarla

Guárdala como *snippet* del editor, haz **una copia por problema**, y adáptala: si nunca
usas `heapq`, quita el import. Lo importante es **entender cada línea**: una plantilla
con cosas que no sabes qué hacen es una fuente de errores, no una ayuda.

Y para el papel del ICPC: la plantilla, las estructuras que no quieres reescribir
(*union-find*, *segment tree*), los algoritmos largos (Dijkstra, flujo máximo, KMP,
criba) y las fórmulas. El [Chuletario](../../../cheatsheet/index.md) del curso te deja
elegir qué entra. Imprímelo **con semanas de antelación** y **úsalo en un
entrenamiento**.

## Siguiente paso

Ya tienes Python. Lo que falta es resolver problemas: vuelve a
[Contenidos](../../index.md) y empieza por el nivel
[Base](../../levels/base/index.md).
