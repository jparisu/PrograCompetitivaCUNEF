# Entrada y salida

- [Entrada y salida](#entrada-y-salida)
  - [While](#while)
    - [Castings implícitos](#castings-implícitos)
    - [Do while](#do-while)
  - [Bucle for](#bucle-for)
    - [Por índice](#por-índice)
    - [Por elemento](#por-elemento)
  - [Palabras clave](#palabras-clave)
    - [break](#break)
    - [continue](#continue)
    - [return](#return)
  - [Ejemplo](#ejemplo)

## While

El bucle `while` es un bucle que se ejecuta mientras una condición sea verdadera. La sintaxis es la siguiente:

```cpp
while (condicion) {
    // Codigo que se ejecuta mientras la condición sea verdadera
}
```

### Castings implícitos

Cuidado porque C++ realiza castings implícitos a bool, pero pueden no ser siempre intuitivos:

- **int** es **false** si es 0, y **true** en cualquier otro caso.
- **char** es **false** si es el carácter nulo `'\0'`, y **true** en cualquier otro caso.
- **float** es **false** si es 0.0, y **true** en cualquier otro caso.
- **punteros** son **false** si son `nullptr`, y **true** en cualquier otro caso.
- **string** no se castea implícitamente a **bool**.
- **vector** no se castea implícitamente a **bool**.

### Do while

El bucle `do while` es un bucle que se ejecuta al menos una vez, y después se ejecuta mientras una condición sea verdadera. La sintaxis es la siguiente:

```cpp
do {
    // Codigo que se ejecuta al menos una vez
} while (condicion);
```


## Bucle for

El bucle `for` es un bucle que se ejecuta un número determinado de veces.


### Por índice

Este bucle se utiliza para recorrer un rango de valores.
La sintaxis es la siguiente:

```cpp
for (inicialización; condición; actualización) {
    // Codigo que se ejecuta mientras la condicion sea verdadera
}
```

- La inicialización se ejecuta una sola vez al principio del bucle.
- La condición se evalúa antes de cada iteración. Si es falsa, el bucle termina. Si está vacía, se considera verdadera.
- La actualización se ejecuta al final de cada iteración.


### Por elemento

Otra forma común de hacer un bucle es recorrer los elementos de un container.
La sintaxis es la siguiente:

```cpp
for (tipo elemento : container) {
    // Codigo que se ejecuta para cada elemento del container
}
```

Esto permite recorrer un array, un vector, un string, un mapa, etc.
**Importante:** lo más eficiente es pasar cada elemento como referencia, aunque esto puede ser peligroso si no se quiere modificar el elemento.

```cpp
vector<string> v = {"hola", "adios"};
for (string &s : v) {
    // Codigo que se ejecuta para cada elemento del container
}
```




## Palabras clave

### break

La palabra clave `break` se utiliza para salir de un bucle. Si se encuentra dentro de un bucle, el bucle se termina inmediatamente.
Cuidado, porque si se encuentra dentro de un bucle anidado, solo se sale del bucle más interno.

```cpp
while (true) {
    if (condicion) {
        break; // salir del bucle
    }
}
```

### continue

La palabra clave `continue` se utiliza para saltar a la iteración actual de un bucle.
El resto del código dentro del bucle no se ejecuta, y se pasa a la siguiente iteración.

```cpp
for (int i = 0; i < 10; i++) {
    if (condicion) {
        continue; // saltar a la siguiente iteracion (i++)
    }
}
```

### return

La palabra clave `return` sale de la función y acaba cualquier bucle en el que se encuentre.

```cpp
while (true) {
    if (condicion) {
        return; // salir del bucle y de la funcion
    }
}
```


## Ejemplo

Pongamos un problema que recibe un entero `n` y suma los números impares menores o igual que `n`.

``` txt
Input:
7
```

``` txt
Output:
16
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    int suma = 0;
    // Empezar en 1 y saltar de 2 en 2 hasta 2n
    for (int i = 1; i <= n; i += 2) {
        suma += i;
    }

    cout << suma << endl;
    return 0;
}
```

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    int suma = 0;
    while (true){
        if (n == 0) {
            break;
        }

        if ( n % 2 == 0) {
            n--;
            continue;
        } else {
            suma += n;
            n--;
        }
    }

    cout << suma << endl;
    return 0;
}
```
