# Bucles en Python

[:octicons-arrow-left-24: Volver a Bucles](index.md)

## `for` — recorrer un rango o un iterable

```python
for i in range(n):        # i = 0, 1, ..., n-1
    ...

for x in [10, 20, 30]:    # recorre directamente los elementos
    ...
```

`range(a, b)` va de `a` a `b-1`; `range(a, b, paso)` permite saltos (incluso negativos).

## `while` — hasta que se cumpla una condición

```python
while condicion:
    # se repite mientras `condicion` sea verdadera
    ...
```

!!! tip "Python no tiene `do…while`"
    Se imita con un bucle infinito y una salida explícita:
    ```python
    while True:
        ...
        if not condicion:
            break
    ```

## Ejemplo completo

Lee `n` números y muestra su suma:

```python
--8<-- "algorithms/fundamentals/loops/code/loops.v1.full.py"
```

| Entrada | Salida |
|---------|--------|
| `3` <br> `10 20 30` | `60` |
