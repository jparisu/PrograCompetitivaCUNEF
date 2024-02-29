# Bucles [Python]

```{contents}
:local:
:depth: 2
```


## While

El bucle `while` es un bucle que se ejecuta mientras una condición sea verdadera. La sintaxis es la siguiente:

```cpp
while (condicion) {
    // Codigo que se ejecuta mientras la condición sea verdadera
}
```

### Castings implícitos

Cuidado porque Pytohn realiza castings de cualquier tipo a bool, pero pueden no ser siempre intuitivos:

- **int** es **false** si es 0, y **true** en cualquier otro caso.
- **char** es **false** si es el carácter nulo `'\0'`, y **true** en cualquier otro caso.
- **float** es **false** si es 0.0, y **true** en cualquier otro caso.
- **punteros** son **false** si son `nullptr`, y **true** en cualquier otro caso.
- **string** es **false** si es está vacío, y **true** en cualquier otro caso.
- **container** (list, set, map) es **false** si está vacío, y **true** en cualquier otro caso.

```py
s = "False"
while s: # True
    print("Sí se ejecuta")
    break

list = []
while list: # False
    print("No se ejecuta")
```

## Bucle for

Un bucle for en Python siempre itera sobre una secuencia de elementos.

### range

Es el bucle más común. Itera sobre una secuencia de números generados por `range`, que permite mediante argumentos marcar el inicio, fin y paso de cada iteración.
Los argumentos son:

- **start**: número inicial (por defecto 0)
- **stop**: número final (**no incluido**)
- **step**: paso (por defecto 1)

En caso de solo tener un argumento, se considera como argumento **stop**.


```py
# Bucle for de 2 a 10 incluido de 2 en 2
for i in range(2, 11, 2):
    # SOME CODE WITH i (2, 4, 6, 8, 10)
```

### Container

Itera sobre los elementos de un contenedor (list, set, dict, etc).

#### list

```py
l = [1, 2, 3, 4, 5]
for i in l:
    # SOME CODE WITH i (1, 2, 3, 4, 5)
```

#### set

Cuidado, porque en este caso no se garantiza el orden de los elementos.

```py
s = {1, 2, 3, 4, 5}
for i in s:
    # SOME CODE WITH i (1, 2, 3, 4, 5)
```

#### dict

```py
d = {1: "uno", 2: "dos", 3: "tres"}

# Iterar sobre las claves
for k in d:
    # SOME CODE WITH k (1, 2, 3)

# Iterar sobre los valores
for v in d.values():
    # SOME CODE WITH v ("uno", "dos", "tres")

# Iterar sobre las claves y valores
for k, v in d.items():
    # SOME CODE WITH k, v (1, "uno"), (2, "dos"), (3, "tres")
```


### enumerate

La función `enumerate` devuelve un objeto que genera tuplas con el índice y el valor de cada elemento de un contenedor.

```py
l = ["a", "b", "c"]
for i, v in enumerate(l):
    # SOME CODE WITH i, v (0, "a"), (1, "b"), (2, "c")
```


## Palabras clave

### break

La palabra clave `break` se utiliza para salir de un bucle. Si se encuentra dentro de un bucle, el bucle se termina inmediatamente.
Cuidado, porque si se encuentra dentro de un bucle anidado, solo se sale del bucle más interno.

```py
while (True):
    if (condicion):
        break # salir del bucle
```

### continue

La palabra clave `continue` se utiliza para saltar a la iteración actual de un bucle.
El resto del código dentro del bucle no se ejecuta, y se pasa a la siguiente iteración.

```py
for i in range(10):
    if (condicion):
        continue # saltar a la siguiente iteracion (i++)
```

### return

La palabra clave `return` sale de la función y acaba cualquier bucle en el que se encuentre.

```py
while (True):
    if (condicion):
        return # salir del bucle y de la funcion
```


## Ejemplo

Pongamos un problema que recibe un entero `n` y suma los números impares menores o igual que `n`.

``` none
Input:
7
```

``` none
Output:
16
```

``` py
n = int(input())
suma = 0
for i in range(n+1):
    if i % 2 != 0:
        suma += i
print(suma)
```

``` py
n = int(input())
suma = 0
while True:
    if n == 0:
        break
    if n % 2 == 0:
        n -= 1
        continue
    else:
        suma += n
        n -= 1
print(suma)
```
