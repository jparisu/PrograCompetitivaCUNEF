# Condicionales en Python

[:octicons-arrow-left-24: Volver a Condicionales](index.md)

## `if` / `elif` / `else`

En Python la indentación (los espacios) marca el bloque; no hay llaves:

```python
if a > b:
    print("a es mayor")
elif a < b:
    print("b es mayor")
else:
    print("son iguales")
```

## Expresión condicional (ternario)

Para elegir entre dos valores en una línea:

```python
mayor = a if a > b else b   # si a>b vale a, si no vale b
```

## Combinar condiciones

`and`, `or`, `not`:

```python
if 0 <= x < n:      # Python permite encadenar comparaciones
    ...
```

## Ejemplo completo

Muestra el mayor de dos números:

```python
--8<-- "algorithms/fundamentals/conditionals/code/conditionals.v1.full.py"
```

| Entrada | Salida |
|---------|--------|
| `3 7` | `7` |
| `10 2` | `10` |
