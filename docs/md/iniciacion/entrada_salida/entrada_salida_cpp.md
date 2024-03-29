# Entrada y salida [C++]

```{contents}
:local:
:depth: 2
```

## Fichero de código fuente

Casi todos los ficheros soluciones tendrán la misma estructura de includes y main.

En C++ las librerías deben añadirse al principio del programa.
La librería `iostream` es necesaria para la entrada/salida y se va a usar en prácticamente cualquier programa.
En varios casos se deberán incluir más librerías, pero es mejor solo incluirlas cuando sean necesarias.

Aconsejamos usar el namespace `std` para no tener que escribir `std::` delante de cada función de la librería estándar.

Por último, el programa debe tener una función `main` que es donde se ejecutará el programa.
Por si acaso, intentad que siempre devuelva 0.


``` c++
// Program init for every file
#include <iostream> // librería para entrada/salida
using namespace std;

#include <string> // librería para cadenas de texto
#include <vector> // librería para vectores
#include <algorithm> // librería para algoritmos
#include <cmath> // librería para funciones matemáticas

int main() {
    // CODE HERE
    return 0;
}
```


## Entrada

En c++ leemos cada valor hasta el siguiente espacio.
Las cadenas se convertirán en el tipo de dato donde guardemos el valor (si lo guardamos en un `int`, esperará leer un número).

``` c++
// LEER CADENAS DE TEXTO
string cadena; // inicializar variable de tipo string

cin >> cadena; // leer una cadena de texto hasta el siguiente espacio
cadena = cin.getline(); // leer una cadena hasta el final de la linea
```

``` c++
// LEER NUMEROS
int entero; // inicializar variable de tipo entero
float decimal; // inicializar variable de tipo decimal

cin >> entero; // leer un numero entero hasta el siguiente espacio (no acepta decimales)
cin >> entero; // leer un numero decimal hasta el siguiente espacio
```

En muchos casos hay que leer diferentes casos de prueba.
El input puede venir dado generalmente de 3 formas:

1. El input contiene el número de casos de prueba y luego los casos de prueba
1. El input tiene casos de prueba hasta que se lee un 0 (o algún string de cierre)
1. El input acaba sin avisar

### N casos

``` c++
// LEER UN NUMERO N Y LUEGO UNA LISTA DE N NUMEROS
int n;
vector<int> lista(n); // inicializar un vector con espacio para n enteros

cin >> n; // leer un numero entero hasta el siguiente espacio
for(int i=0; i<n; i++) {
    cin >> lista[i]; // leer n numeros enteros hasta el siguiente espacio
}
```

### Casos hasta un 0

``` c++
// LEER CASOS DE PRUEBA HASTA QUE SE LEE UN 0
string input_value;

while (cin >> input_value && input_value != "0") {
    // CODE HERE
}
```

### Acaba sin avisar

``` c++
// LEER CASOS DE PRUEBA HASTA QUE SE ACABA EL INPUT
string input_value;

while (cin >> input_value) {
    // CODE HERE
}
```

## Salida

La salida se hace con `cout`.
Para un salto de línea se puede usar `endl` o `"\n"`.
`endl` además hace flush del buffer.

``` c++
// IMPRIMIR UN VALOR
int entero = 5;
float decimal = 3.14;
string cadena = "hola";

cout << cadena << endl; // imprimir un string y saltar de linea
cout << decimal << " " << cadena; // imprimir 2 numeros separados por espacio
cout << endl; // saltar de linea y vaciar el buffer
```

## Ejemplo

Pongamos un problema cuyo input serán unas listas de números donde el primero de cada línea indica el número de elementos de esa línea.
El input acabará sin avisar.
La salida devolverá la suma de los elementos de cada línea.

``` none
Input:
3 1 2 3
4 4 5 6 7
```

``` none
Output:
6
22
```

``` c++
#include <iostream>
#include <vector>
using namespace std;

int main() {

    int n; // numero de elementos de cada lista
    int v; // auxiliar para leer los valores de la lista

    while (cin >> n) {
        vector<int> lista;
        for(int i=0; i<n; i++) {
            cin >> v;
            lista.push_back(v);
        }

        int suma = 0;
        for(int i=0; i<n; i++) {
            suma += lista[i];
        }

        cout << suma << endl;
    }

    return 0;
}
```
