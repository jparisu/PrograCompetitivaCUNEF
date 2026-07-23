# Condicionales en C++

[:octicons-arrow-left-24: Volver a Condicionales](index.md)

## `if` / `else if` / `else`

La condición entre paréntesis se evalúa a un booleano, normalmente una
[comparación](../comparisons/index.md) (`a > b`, `x == y`…). Si es verdadera se ejecuta
su bloque y **se salta el resto**; sólo se comprueba el siguiente `else if` cuando
todas las condiciones anteriores han fallado. Por eso el orden importa: la primera
que se cumpla "gana".

```cpp
if (a > b) {
    cout << "a es mayor\n";
} else if (a < b) {          // sólo se comprueba si `a > b` fue falso
    cout << "b es mayor\n";
} else {                     // ni mayor ni menor => iguales
    cout << "son iguales\n";
}
```

<figure class="algo-figure">
  <img src="../media/if-else-flow.svg"
       alt="Diagrama de flujo del if/else if/else que decide el mayor de dos números">
  <figcaption>El flujo baja por las ramas "no" hasta que una se cumple.</figcaption>
</figure>

Con una sola instrucción puedes omitir las llaves, pero ponerlas siempre evita
errores al añadir líneas después.

## Combinar condiciones

`&&` (y), `||` (o), `!` (no). Se evalúan con **cortocircuito**: en `A && B`, si `A`
es falso `B` ni se mira; en `A || B`, si `A` es verdadero `B` tampoco. Esto sirve
para proteger comprobaciones peligrosas:

```cpp
if (i < n && v[i] == x) { ... }   // no accede a v[i] si i está fuera de rango
```

Para comprobar un rango hay que escribir **las dos comparaciones**:

```cpp
if (0 <= x && x < n) { ... }      // x está dentro de [0, n)
```

!!! warning "C++ no encadena comparaciones"
    `0 <= x < n` **compila pero no hace lo que crees**: evalúa `(0 <= x)`, que da
    `0` o `1`, y luego compara ese `0/1 < n`. Casi siempre es verdadero. Usa
    siempre `0 <= x && x < n`.

## Operador ternario

Elige entre dos **valores** en una sola expresión (no dos bloques de código):

```cpp
int mayor = (a > b) ? a : b;   // si a>b vale a, si no vale b
```

Útil dentro de una expresión (una asignación, un `cout`, un argumento). Para lógica
más larga, un `if` normal se lee mejor.

## `switch` — elegir según un valor

Compara **una** variable entera (o `char`/`enum`) contra varias constantes. Cada
`case` necesita `break`; si falta, la ejecución "cae" al siguiente `case`, lo que a
veces se aprovecha para agrupar casos:

```cpp
switch (opcion) {
    case 1:
        cout << "uno\n";
        break;              // sin break seguiría en el case 2
    case 2:
    case 3:                 // 2 y 3 comparten cuerpo (case 2 cae en el 3)
        cout << "dos o tres\n";
        break;
    default:                // ninguno de los anteriores
        cout << "otra\n";
}
```

No admite rangos, `float` ni `string`; para eso usa `if` / `else if`.

## Veracidad de un valor

En una condición, un número o puntero es **falso si vale `0`/`nullptr`** y verdadero
en cualquier otro caso. Así puedes escribir directamente:

```cpp
if (n) { ... }        // equivale a: if (n != 0)
if (!resto) { ... }   // se ejecuta cuando resto == 0
```

Los contenedores (`vector`, `string`, …) **no** se convierten a booleano: usa
`v.empty()` para saber si están vacíos.

## Errores frecuentes

- **`=` vs `==`.** `if (a = b)` **asigna** `b` a `a` y usa ese valor como condición;
  `if (a == b)` compara. Compila casi siempre, así que activa avisos (`-Wall`).
- **Comparar `double` con `==`.** El redondeo hace que `0.1 + 0.2 == 0.3` sea falso.
  Compara con una tolerancia: `if (abs(x - y) < 1e-9) { ... }`.
- **`else` colgante.** Sin llaves, un `else` se asocia al `if` **más cercano**, no al
  que la indentación sugiere:

    ```cpp
    if (a > 0)
        if (b > 0) cout << "ambos positivos\n";
    else cout << "??\n";      // este else pertenece al `if (b > 0)`
    ```

    Pon llaves y la ambigüedad desaparece.

## Ejemplo completo

Muestra el mayor de dos números:

```cpp
--8<-- "content/fundamentals/conditionals/code/conditionals.v1.full.cpp"
```

| Entrada | Salida |
|---------|--------|
| `3 7` | `7` |
| `10 2` | `10` |
