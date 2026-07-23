# Condicionales en Python

[:octicons-arrow-left-24: Volver a Condicionales](index.md)

## `if` / `elif` / `else`

En Python la **indentación** (los espacios) marca el bloque; no hay llaves. La condición
suele ser una [comparación](../comparisons/index.md) (`a > b`, `x == y`…). Las ramas
se comprueban en orden: la primera condición verdadera ejecuta su bloque y **se salta
el resto**; un `elif` sólo se mira cuando todos los anteriores fallaron.

```python
if a > b:
    print("a es mayor")
elif a < b:          # sólo se comprueba si `a > b` fue falso
    print("b es mayor")
else:                # ni mayor ni menor => iguales
    print("son iguales")
```

<figure class="algo-figure">
  <img src="../media/if-else-flow.svg"
       alt="Diagrama de flujo del if/elif/else que decide el mayor de dos números">
  <figcaption>El flujo baja por las ramas "no" hasta que una se cumple.</figcaption>
</figure>

## Combinar condiciones

`and`, `or`, `not`. Se evalúan con **cortocircuito**: en `A and B`, si `A` es falso
`B` ni se mira; en `A or B`, si `A` es verdadero `B` tampoco. Sirve para proteger
comprobaciones peligrosas:

```python
if i < n and v[i] == x:    # no accede a v[i] si i está fuera de rango
    ...
```

Además, Python permite **encadenar comparaciones** de forma natural, tal como en
matemáticas:

```python
if 0 <= x < n:        # equivale a (0 <= x) and (x < n)
    ...
```

## Expresión condicional (ternario)

Elige entre dos **valores** en una sola línea (no dos bloques):

```python
mayor = a if a > b else b   # si a>b vale a, si no vale b
```

Útil dentro de una expresión (una asignación, un `print`, un argumento). Para lógica
más larga, un `if` normal se lee mejor.

## `match` — elegir según un patrón (Python 3.10+)

Compara un valor contra varios **patrones** de arriba abajo y ejecuta el primero que
encaje. `_` es el caso por defecto y `|` agrupa varios patrones:

```python
match comando:
    case "salir":
        print("adiós")
    case "hola" | "hey":    # varios patrones en un mismo case
        print("¡hola!")
    case _:                 # cualquier otro valor
        print("no entiendo")
```

Para dos o tres opciones simples, una cadena de `if` / `elif` es igual de clara.

## Veracidad de un valor

En una condición, muchos valores cuentan como **falsos** sin comparar nada:
`0`, `0.0`, `""`, `[]`, `{}`, `set()` y `None`. Cualquier otro valor es verdadero.
Así se comprueba "hay datos" de forma idiomática:

```python
if datos:            # verdadero si la lista NO está vacía
    ...
if not nombre:       # verdadero si la cadena está vacía
    ...
```

## Errores frecuentes

- **`=` vs `==`.** `=` asigna y `==` compara. Aquí Python te protege: `if x = 5:` es
  un **error de sintaxis**. Si de verdad quieres asignar dentro de la condición, usa
  el operador morsa: `if (n := len(datos)) > 0:`.
- **`is` vs `==`.** `==` compara **valores**; `is` compara **identidad** (si son el
  mismo objeto). Usa `==` para comparar datos y reserva `is` para `None`:
  `if x is None:`.
- **Comparar `float` con `==`.** El redondeo hace que `0.1 + 0.2 == 0.3` sea falso.
  Usa `math.isclose(a, b)`.
- **Indentación inconsistente.** Mezclar tabuladores y espacios lanza un
  `TabError`; usa siempre 4 espacios.

## Ejemplo completo

Muestra el mayor de dos números:

```python
--8<-- "content/fundamentals/conditionals/code/conditionals.v1.full.py"
```

| Entrada | Salida |
|---------|--------|
| `3 7` | `7` |
| `10 2` | `10` |
