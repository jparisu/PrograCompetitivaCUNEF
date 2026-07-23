# Empezar aquí

Guía rápida para dar tus primeros pasos en programación competitiva en CUNEF.

## 1. Elige un lenguaje

- **C++** es el más usado en concursos: rápido y con la STL.
- **Python** es más sencillo de escribir; suficiente para muchos problemas.

En este sitio tienes **ambos** en cada algoritmo, así que puedes empezar por el que prefieras.

## 2. Prepara tu entorno

- Un editor (VS Code recomendado) y un compilador (`g++`) o Python 3.
- Regístrate en un juez online: [Kattis](https://open.kattis.com/) y
  [Codeforces](https://codeforces.com/) son los que usaremos.

## 3. Plantilla de entrada/salida rápida

Leer y escribir rápido evita muchos *Time Limit Exceeded*:

=== "C++"
    ```cpp
    #include <iostream>
    using namespace std;

    int main() {
        int input, output;
        cin >> input;
        // tu solución aquí
        cout << output << endl;
        return 0;
    }
    ```
=== "Python"
    ```python
    input_value = int(input())
    # tu solución aquí
    print(output_value)
    ```

## 4. Sigue la escalera

Empieza por el nivel **Base** y ve subiendo. Consulta el
[grafo de dependencias](../content/graph.md) para ver qué necesitas antes de cada tema.
