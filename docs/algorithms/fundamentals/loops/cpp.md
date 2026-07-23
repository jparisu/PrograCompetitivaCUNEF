# Bucles en C++

[:octicons-arrow-left-24: Volver a Bucles](index.md)

## `for` — número conocido de repeticiones

```cpp
for (int i = 0; i < n; i++) {
    // se ejecuta n veces, con i = 0, 1, ..., n-1
}
```

Las tres partes son: **inicialización** (`int i = 0`), **condición** (`i < n`, se comprueba
antes de cada vuelta) y **actualización** (`i++`, al final de cada vuelta).

## `while` — hasta que se cumpla una condición

```cpp
while (condicion) {
    // se repite mientras `condicion` sea verdadera
}
```

## `do … while` — al menos una vez

```cpp
do {
    // se ejecuta y LUEGO se comprueba: siempre corre al menos una vez
} while (condicion);
```

## Ejemplo completo

Lee `n` números y muestra su suma:

```cpp
--8<-- "algorithms/fundamentals/loops/code/loops.v1.full.cpp"
```

| Entrada | Salida |
|---------|--------|
| `3` <br> `10 20 30` | `60` |
