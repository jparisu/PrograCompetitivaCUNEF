# Entrada y salida

- [Entrada y salida](#entrada-y-salida)
  - [Advertencias](#advertencias)
  - [Imports](#imports)
  - [Entrada](#entrada)
    - [Split](#split)
    - [Leer números](#leer-números)
    - [Leer una lista de números](#leer-una-lista-de-números)
    - [El input se acaba sin avisar](#el-input-se-acaba-sin-avisar)
  - [Salida](#salida)
    - [Formatear strings](#formatear-strings)
    - [Argumentos de print](#argumentos-de-print)
  - [Ejemplo](#ejemplo)


En programación competitiva, la entrada y salida del programa viene dada de una forma muy concreta.
- El juez online pasa por la entrada estándar `stdin` un archivo de texto secreto de entrada
- El juez luego compara la salida `stdout` de tu programa con un archivo secreto de salida

Puedes emular esto copiando y pegando el sample in en la terminal, y viendo lo que saca tu programa en terminal.
En la terminal se verá la entrada y la salida mezclada, pero el juez las ve por separado.
Por esto, no hace falta procesar todos los casos de prueba del tirón y sacar toda la salida de todos los casos al final.

## Advertencias

- Cualquier print por pantalla se considera salida. Por lo tanto, cuidado con:
    - Los mensajes de esperar el input (*i.e. "dame un entero"*)
    - Los mensajes de depuración (*i.e. "el valor de x es 5"*)
- Normalmente el output esperado es exacto, así que mucho cuidado con el formato:
    - Espacios, tabuladores y saltos de línea antes, entre y detrás de los números
    - Números decimales (normalmente se establece el máximo de decimales)
    - Formato de las cadenas (espacios, mayúsculas, etc.)
- **NO** hace falta hacer comprobaciones de la entrada. Si el enunciado dice que la entrada viene dada de cierta forma, no hace falta comprobarla.


## Imports

Los imports en Python gastan tiempo y memoria, así que es mejor importar solo lo que se va a usar.


## Entrada

En Python se leen las líneas enteras con `input()` en formato `str`.

``` py
# LEER UNA LINEA
cadena = input() # leer una cadena
```

En muchos casos el input lo querremos en formato número o lista.
Estas funciones pueden ser muy útiles:

1. `split()` te divide la línea por espacios (o por el string que se pase por argumento)
2. `int()` y `float()` son funciones que convierten cadenas a enteros o números reales.
3. `map(f, lista)` aplica una función a cada elemento de la lista. Esta función puede ser, por ejemplo, un casting. El return de map es un iterador y no una lista, suele ser útil (aunque no siempre necesario) convertirlo a lista `list`.


### Split

``` py
# LEER UNA LINEA Y DIVIDIRLA
x, y = input().split() # Si conocemos de antemano el numero de elementos que hay
l = input().split() # Si no conocemos el numero de elementos que hay creamos una lista
```

### Leer números

``` py
# LEER NUMEROS
entero = int(input()) # leer un entero
decimal = float(input()) # leer un decimal
```

### Leer una lista de números

``` py
# LEER UNA LISTA DE NUMEROS
l = list(map(int, input().split())) # leer una lista de enteros
```

### El input se acaba sin avisar

Algunos problemas acaban cuando no quedan líneas que leer.

``` py
# EL INPUT SE ACABA SIN AVISAR
while True:
    try:
        x = input()
        # CODE HERE
    except EOFError:
        break
```

## Salida

La salida se hace con `print`.
Esta función añade por defecto un salto de línea al final.

### Formatear strings

Un string se formatea de forma muy sencilla con `f''`.
Esto permite meter variables directamente en el string.

``` py
x = 3
y = 5
print(f'{x} + {y} = {x+y}') # == "3 + 5 = 8"
```

### Argumentos de print

Print permite varios argumentos, los cuales se convertirán a string y se imprimirán separados por un espacio.
Si se quiere separar por otro string, se puede usar el argumento `sep`, que por defecto es un espacio.
Para determinar el final de la línea, se puede usar el argumento `end`, que por defecto es un salto de línea.

``` py
print(3, 5, 8) # == "3 5 8"
print(3, 5, 8, sep=' + ') # == "3 + 5 + 8"
print(3, 5, sep=' + ' , end=' = 8\n') # == "3 + 5 = 8"
```


## Ejemplo

Pongamos un problema cuyo input serán unas listas de números donde el primero de cada línea indica el número de elementos de esa línea.
El input acabará sin avisar.
La salida devolverá la suma de los elementos de cada línea.

``` txt
Input:
3 1 2 3
4 4 5 6 7
```

``` txt
Output:
6
22
```

``` py
while True:
    try:
        l = list(map(int, input().split()))
        n = l[0]
        print(sum(l[1:]))
    except EOFError:
        break
```
