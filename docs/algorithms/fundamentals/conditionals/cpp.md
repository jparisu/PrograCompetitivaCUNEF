# Condicionales en C++

[:octicons-arrow-left-24: Volver a Condicionales](index.md)

## `if` / `else if` / `else`

```cpp
if (a > b) {
    cout << "a es mayor\n";
} else if (a < b) {
    cout << "b es mayor\n";
} else {
    cout << "son iguales\n";
}
```

Con una sola instrucción puedes omitir las llaves, pero ponerlas evita errores.

## Operador ternario

Para elegir entre dos valores en una línea:

```cpp
int mayor = (a > b) ? a : b;   // si a>b vale a, si no vale b
```

## Combinar condiciones

`&&` (y), `||` (o), `!` (no):

```cpp
if (0 <= x && x < n) { ... }   // x está dentro del rango
```

## Ejemplo completo

Muestra el mayor de dos números:

```cpp
--8<-- "algorithms/fundamentals/conditionals/code/conditionals.v1.full.cpp"
```

| Entrada | Salida |
|---------|--------|
| `3 7` | `7` |
| `10 2` | `10` |
