---
render_macros: true
---
# E/S rápida

{{ metadata() }}

En muchos problemas la entrada es enorme (cientos de miles de números). Leerla o escribirla
de forma lenta hace que el programa supere el límite de tiempo (*Time Limit Exceeded*) **aunque
el algoritmo sea correcto**. La solución no cambia tu algoritmo: solo cambia *cómo* lees y
escribes. La idea es una: **no proceses la E/S carácter a carácter; trabájala en bloque**.

## ¿Por qué es lento por defecto?

- **C++** — Por compatibilidad, `cin`/`cout` están **sincronizados** con el `scanf`/`printf` de
  C y, además, `cin` está **atado** a `cout` (antes de cada lectura se vacía la salida). Eso
  cuesta tiempo en cada operación. Se desactiva con dos líneas al principio de `main()`:

    ```cpp
    ios::sync_with_stdio(false);   // desliga cin/cout del stdio de C
    cin.tie(nullptr);              // no vaciar cout antes de cada cin
    ```

    Además, **usa `'\n'` en lugar de `endl`**: `endl` imprime un salto de línea *y vacía el
    búfer* cada vez; dentro de un bucle eso es carísimo.

    !!! warning "Al desactivar la sincronización"
        No mezcles `cin`/`cout` con `scanf`/`printf` en el mismo programa: al perder la
        sincronización, el orden de la salida puede desordenarse.

- **Python** — La función `input()` es cómoda pero lenta si la llamas miles de veces. Lo
  básico es **reemplazarla** por el lector con búfer `sys.stdin.readline`; y si hay muchísimos
  números, leer **todo de una vez** con `sys.stdin.read().split()`. Para imprimir mucho, junta
  todo y escríbelo de golpe (`"\n".join(...)`) en lugar de un `print` por línea.

## Plantilla mínima

Esto es lo único que necesitas recordar (también está en el [chuletario](../../../cheatsheet/index.md)):

=== "C++"

    ```cpp
    --8<-- "content/fundamentals/fast-io/code/io.cpp"
    ```

=== "Python"

    ```python
    --8<-- "content/fundamentals/fast-io/code/io.py"
    ```

## Ejemplo completo

Un programa que lee `n` números y muestra su suma, ya con la E/S rápida aplicada. Fíjate en
que el algoritmo (sumar) es trivial: lo único "especial" es la preparación de la E/S.

=== "C++"

    ```cpp
    --8<-- "content/fundamentals/fast-io/code/fast_io.v1.full.cpp"
    ```

=== "Python"

    ```python
    --8<-- "content/fundamentals/fast-io/code/fast_io.v1.full.py"
    ```

| Entrada | Salida |
|---------|--------|
| `5` <br> `1 2 3 4 5` | `15` |
| `3` <br> `10 20 30` | `60` |

!!! tip "¿Cuándo hace falta?"
    Si el enunciado maneja entradas grandes (≈10⁵ valores o más) o tienes un TLE que no
    explicas por complejidad, aplica esta plantilla. En entradas pequeñas no cambia nada, así
    que puedes ponerla siempre por costumbre.
