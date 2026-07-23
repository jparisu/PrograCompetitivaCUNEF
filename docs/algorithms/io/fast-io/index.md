# E/S rápida

!!! info "Metadatos"
    **Tipo:** Técnica · **Nivel:** Principiante · **Dificultad:** 1.0

Cuando la entrada es grande, leerla de forma lenta provoca *Time Limit Exceeded*. La idea
es sencilla: **evita la entrada/salida carácter a carácter** y lee/escribe en bloque.

- **C++**: desengancha los flujos de C++ del `stdio` de C con `ios::sync_with_stdio(false)`
  y quita el "atado" entre `cin` y `cout` con `cin.tie(nullptr)`. Usa `"\n"` en lugar de
  `endl` (que además vacía el búfer).
- **Python**: `input()` en un bucle es lento; lee todo de golpe con `sys.stdin` y escribe
  con `sys.stdout.write`.

## Plantilla mínima

Esto es lo único que necesitas recordar (también está en el [chuletario](../../../cheatsheet/index.md)):

=== "C++"

    ```cpp
    --8<-- "algorithms/io/fast-io/code/io.cpp"
    ```

=== "Python"

    ```python
    --8<-- "algorithms/io/fast-io/code/io.py"
    ```

## Ejemplo completo

Un programa que lee `n` números y muestra su suma, ya con la E/S rápida aplicada.

=== "C++"

    ```cpp
    --8<-- "algorithms/io/fast-io/code/fast_io.v1.full.cpp"
    ```

=== "Python"

    ```python
    --8<-- "algorithms/io/fast-io/code/fast_io.v1.full.py"
    ```

| Entrada | Salida |
|---------|--------|
| `5` <br> `1 2 3 4 5` | `15` |
| `3` <br> `10 20 30` | `60` |
