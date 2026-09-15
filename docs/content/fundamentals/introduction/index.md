---
render_macros: true
---
# Introducción a la programación competitiva

{{ metadata(complexity="") }}

Este capítulo es el punto de partida. No supone que sepas programar competitivamente
nada: solo que puedes escribir un programa que sume dos números.

Al terminarlo sabrás qué es un algoritmo, cómo está escrito un problema de concurso,
cómo se lee la entrada y se escribe la salida, cómo enviar tu código a un juez online y
qué hacer con cada respuesta que te devuelva. Se lee en una tarde.

Todo gira alrededor de **un único problema**:
[A Shortcut to What?](https://open.kattis.com/problems/shortcuttowhat) de Kattis. Lee un
entero `n`, le suma cinco, triplica y resta diez —es decir, `3n + 5`—. Se resuelve en
tres líneas, y por eso sirve: podemos enviarlo, leer el veredicto y romperlo a propósito
de seis maneras sin que el algoritmo estorbe.

Solo necesitas una cuenta en [Kattis](https://open.kattis.com/) y un lenguaje instalado.
Si no tienes ninguno, los capítulos de [C++](../../languages/cpp/index.md) y
[Python](../../languages/python/index.md) empiezan por ahí.

## Índice

1. [¿Qué es la programación competitiva?](#que-es-la-programacion-competitiva)
2. [¿Qué es un algoritmo?](#que-es-un-algoritmo)
3. [Tu primer problema](#tu-primer-problema)
4. [La entrada y la salida](#la-entrada-y-la-salida)
5. [Enviar la solución](#enviar-la-solucion)
6. [Veredictos y errores](#veredictos-y-errores)
7. [Cómo es un concurso](#como-es-un-concurso)
8. [Siguientes pasos](#siguientes-pasos)

## ¿Qué es la programación competitiva?

**Resolver problemas escribiendo un programa, contra reloj, y que una máquina decida si
está bien.** Envías tu código a un servidor, lo ejecuta con datos que tú no ves, compara
la salida con la esperada y responde: correcto o incorrecto. Ese bucle —leer, pensar,
escribir, enviar, corregir— es todo lo que hay.

Tres cosas la diferencian de programar en clase o en el trabajo:

- **Solo importa el resultado.** Nadie lee tu código. Da igual si los nombres son de una
  letra o si no hay comentarios. (La trampa: un código ilegible es un código que tú no
  sabrás arreglar cuando falle.)
- **Hay que ser correcto *y* rápido.** Si tardas más de lo permitido, es tan malo como
  estar mal. Encontrar *una* solución suele ser fácil; encontrar una que entre en tiempo
  es el problema de verdad.
- **No hay interfaz.** Tu programa lee texto y escribe texto. Ese `Introduce un número:`
  que pondrías en un ejercicio de clase aquí es un error: se cuela en la salida.

Sirve para aprender a resolver problemas (el motivo principal), para las entrevistas
técnicas y para competir. Y no es programar rápido escribiendo, ni saberse algoritmos de
memoria: la mayoría de las soluciones tienen menos de treinta líneas.

### Los jueces que usaremos

- **[Kattis](https://open.kattis.com/)** — miles de problemas ordenados por dificultad.
  Es el del ICPC y el del curso.
- **[Codeforces](https://codeforces.com/)** — rondas en directo cada pocos días.

Hay más (AtCoder, CSES, SPOJ) y todos funcionan igual.

## ¿Qué es un algoritmo?

Una **secuencia finita de pasos precisos** que, partiendo de una entrada, produce la
salida correcta. Tres piezas: entrada, pasos, salida. Y tres propiedades:

| Propiedad | Si falla |
|-----------|----------|
| **Finito** — termina | tu programa se cuelga |
| **Preciso** — sin ambigüedad | dos personas obtienen resultados distintos |
| **Correcto** — para *toda* entrada válida | funciona con los ejemplos y falla en el juez |

Esa última fila es la que duele: «funciona con los ejemplos» y «es correcto» son cosas
distintas.

### El algoritmo existe antes que el código

Buscar una palabra en un diccionario de papel: abre por la mitad, mira la palabra de
arriba, y repite en la mitad izquierda o derecha. Nadie te lo enseñó como algoritmo,
pero lo es — y es exactamente la
[búsqueda binaria](../../search/binary-search-array/index.md).

El camino es siempre el mismo:

1. **Entender el problema**, límites incluidos.
2. **Escribir los pasos en español** (*pseudocódigo*).
3. **Traducirlos** al lenguaje.
4. **Comprobarlos** con los ejemplos.

```text
leer n
resultado = (n + 5) * 3 - 10
escribir resultado
```

=== "C++"
    ```cpp
    #include <iostream>
    using namespace std;

    int main() {
        int n;
        cin >> n;
        cout << (n + 5) * 3 - 10 << '\n';
    }
    ```
=== "Python"
    ```python
    n = int(input())
    print((n + 5) * 3 - 10)
    ```

Las mismas tres líneas que el pseudocódigo. Cuando eso no pasa, el paso 2 estaba
incompleto.

### Un problema, varios algoritmos

El enunciado dice «puedes simplificar la fórmula si eres capaz»: `(n+5)·3−10 = 3n+5`.
Aquí las dos versiones tardan lo mismo, así que da igual. Pero el hábito importa. Si en
vez de una fórmula te piden **sumar los números del 1 al N**:

| Algoritmo | Pasos | Con N = 10⁹ |
|-----------|-------|-------------|
| Bucle que suma uno a uno | N | ~10 s → **Time Limit Exceeded** |
| Fórmula `N·(N+1)/2` | 3 | instantáneo |

Los dos son correctos. Solo uno pasa.

### Cuánto tarda: contar operaciones, no segundos

No puedes decir «tarda 0,4 segundos»: depende de la máquina. Lo que sí puedes contar es
cuántas operaciones hace según el tamaño de la entrada. Un juez hace del orden de **10⁸
operaciones por segundo**, así que con 1 segundo de límite:

| Tamaño de n | Lo que te puedes permitir |
|-------------|---------------------------|
| n ≤ 10 | cualquier cosa, incluso probarlo todo |
| n ≤ 1 000 | O(n²) |
| n ≤ 100 000 | O(n log n) |
| n ≤ 10 000 000 | O(n) |

**Mira el límite del enunciado antes de elegir el algoritmo**: te está diciendo la
respuesta. Se formaliza en [Complejidad (Big-O)](../complexity/index.md).

## Tu primer problema

Regístrate en [open.kattis.com](https://open.kattis.com/). Si usas el correo de CUNEF
aparecerás en el [ranking del curso](../../../ranklist/index.md).

Abre **[A Shortcut to What?](https://open.kattis.com/problems/shortcuttowhat)**. Todas
las páginas de problema tienen la misma estructura:

- **Enunciado** — qué hay que calcular.
- **Input / Output** — el contrato con el juez. Aquí: leo *un* entero
  (−1000 ≤ n ≤ 1000), escribo *un* entero.
- **Límites** — 1 segundo de CPU, 1024 MB, dificultad 1.1.
- **Samples** — pares de entrada y salida.

| Entrada | Salida | | Entrada | Salida |
|---------|--------|-|---------|--------|
| `-4` | `-7` | | `2` | `11` |
| `0` | `5` | | `3` | `14` |
| `1` | `8` | | `12` | `41` |

Comprueba dos a mano antes de programar: `n = 0` → `15 − 10 = 5` ✅.
`n = -4` → `3 − 10 = −7` ✅. Que den bien confirma que has entendido el **orden** de las
operaciones; si restaras diez antes de triplicar, `n = 0` daría `−15`.

!!! tip "Los ejemplos no son las pruebas de verdad"
    Son una muestra amable. El juez guarda muchas más, e incluyen los casos raros que tú
    no has pensado. Pero fallar uno de los ejemplos garantiza fallar el envío, y
    comprobarlos cuesta diez segundos.

### Ejecutarlo en tu ordenador

=== "C++"
    ```bash
    g++ -std=c++17 -O2 -Wall solucion.cpp -o solucion
    echo 12 | ./solucion
    ```
=== "Python"
    ```bash
    echo 12 | python3 solucion.py
    ```

Debe responder `41`.

### Los tres ficheros que tendrás siempre

```text
shortcuttowhat/
├── solucion.cpp   (o .py)   el código
├── 1.in                     una entrada de ejemplo
└── 1.ans                    la salida esperada
```

Con eso pruebas sin teclear nada:

```bash
./solucion < 1.in > 1.out
diff 1.out 1.ans && echo "OK"
```

`diff` sin salida = ficheros idénticos = el juez también lo daría por bueno. En la
columna derecha del problema, *Downloads → Sample data files* te da los `.in` y `.ans`
ya hechos.

## La entrada y la salida

Tu programa vive en un tubo: **`stdin`** entra, **`stdout`** sale, y hay un tercer canal,
**`stderr`**, que el juez **ignora** — por eso es donde van los mensajes de depuración.

El juez no llama a tu función: **arranca tu programa entero**, le vuelca la entrada y
recoge lo que imprima. Y todo lo que va a `stdout` cuenta como respuesta: un
`print("estoy aquí")` olvidado convierte un Accepted en un Wrong Answer.

### Los formatos que cubren casi todo

| Formato | Cómo se reconoce |
|---------|------------------|
| Un número fijo de valores | *«one line containing one integer n»* |
| Primero `N`, luego `N` casos | *«The first line contains an integer N…»* |
| Hasta el final de la entrada (EOF) | no te dicen cuántas líneas hay |
| Una línea de texto completa | el dato puede contener espacios |
| Casos hasta un centinela | *«Input ends with a line containing 0»* |

=== "C++"
    ```cpp
    int n;   cin >> n;                    // un valor
    int a, b;   cin >> a >> b;            // varios (da igual cómo estén en líneas)
    while (cin >> n) { ... }              // hasta EOF
    string linea;   getline(cin, linea);  // la línea completa
    ```
=== "Python"
    ```python
    n = int(input())                          # un valor
    a, b = map(int, input().split())          # varios en la misma línea
    v = list(map(int, input().split()))       # una lista entera
    for linea in sys.stdin: ...               # hasta EOF
    ```

!!! warning "Lo que suele fallar"
    En **C++**, mezclar `cin >>` con `getline`: el primero deja el salto de línea sin
    consumir y el `getline` lee una cadena vacía. Pon un `cin.ignore()` entre medias.

    En **Python**, olvidar el `int(...)`: `input()` devuelve **texto** siempre.

### La salida

Escribe **solo** lo que pide el enunciado. Ni mensajes, ni etiquetas, ni unidades. Los
literales, copiados tal cual del enunciado (`YES` no es `Yes`). Y si piden decimales,
hay que decírselo al lenguaje:

=== "C++"
    ```cpp
    cout << fixed << setprecision(6) << x << '\n';   // 3.141593
    ```
=== "Python"
    ```python
    print(f"{x:.6f}")     # 3.141593
    ```

### Errores clásicos de formato

| Error | Veredicto |
|-------|-----------|
| Imprimir `"Introduce n: "` | Wrong Answer |
| Separar con `\n` lo que iba con espacio | Wrong Answer |
| `print` dentro del bucle en vez de fuera | Wrong Answer |
| Un `print` de depuración olvidado | Wrong Answer u Output Limit Exceeded |
| `5.0` donde se esperaba `5` (usar `/` en vez de `//`) | Wrong Answer |

Ninguno tiene que ver con tu algoritmo. Por eso, ante un Wrong Answer, **mira el formato
antes que la lógica**.

## Enviar la solución

Se envía **el código fuente**, un solo fichero, y hay que elegir bien el lenguaje del
desplegable (ojo: hay un «Python 2» en la lista que no es el que quieres). En la página
del problema, *Submit* → subes el fichero → *Submit*.

Lo que hace el juez:

1. **Compila** (o comprueba que arranca, en Python). Si falla: **Compile Error** y ni un
   caso ejecutado.
2. **Ejecuta** tu programa una vez por caso de prueba, en una máquina aislada: sin
   Internet, sin acceso a ficheros, con límite de tiempo y de memoria.
3. **Compara** tu `stdout` con la respuesta correcta, carácter a carácter (ignorando
   espacios al final de línea y líneas en blanco al final).
4. **Emite un veredicto**.

La pantalla muestra un cuadradito por caso. Si uno se pone rojo, **el juez se para ahí**:
no sigue probando, y nunca te enseña ese caso.

### Los casos ocultos

Quien los escribió pensó en lo que tú no vas a pensar: el mínimo y el máximo del rango,
el cero, los negativos, y la entrada más grande posible.

!!! tip "Pruébate los extremos"
    Antes de enviar, ejecuta con los límites del enunciado: `-1000` debe dar `-2995` y
    `1000` debe dar `3005`. Diez segundos, y caza la mitad de los Wrong Answer.

Fuera de concurso reenviar es **gratis**: aprovéchalo, el veredicto es información. En
concurso, cada intento fallido cuesta minutos. Y en los dos casos: quita la depuración
antes de pulsar Submit.

## Veredictos y errores

La solución correcta, para tenerla delante:

=== "C++"
    ```cpp
    int n;   cin >> n;
    cout << (n + 5) * 3 - 10 << '\n';
    ```
=== "Python"
    ```python
    n = int(input())
    print((n + 5) * 3 - 10)
    ```

### ✅ Accepted (AC)

Ha pasado todos los casos dentro del tiempo y la memoria. No significa que tu código sea
bueno ni que sea la solución prevista. Es suficiente: **Accepted es la única métrica**.

### ❌ Wrong Answer (WA)

El programa termina bien pero la salida no coincide. El clásico, olvidar los paréntesis:

```python
print(n + 5 * 3 - 10)      # la multiplicación va antes: calcula n + 5
```

| `n` | Esperado | Este programa | |
|-----|----------|---------------|-|
| `-4` | `-7` | `1` | ❌ |
| `0` | `5` | `5` | ✅ |
| `12` | `41` | `17` | ❌ |

**Acierta uno de los ejemplos del enunciado.** Si solo hubieras probado ese, habrías
enviado convencido.

Causas frecuentes, por síntoma: si falla desde el primer caso, es la lógica; si pasa
muchos y falla uno, es un caso límite (0, negativos, extremos); si falla solo con
números grandes, es un desbordamiento de enteros; si falla todo con el cálculo bien, es
el formato.

### ⏱️ Time Limit Exceeded (TLE)

No ha terminado dentro del límite. Un ejemplo real y muy común, leer mal el final de la
entrada:

```cpp
int n;
while (true) {      // el bucle no tiene salida
    cin >> n;       // al acabarse la entrada, cin FALLA y deja n como estaba
}
```

`cin >> n` no lanza ningún error al llegar al final: simplemente falla. La lectura tiene
que ir **en la condición**: `while (cin >> n)`.

Pero en un problema real el TLE casi nunca es un bucle infinito: es haber elegido un
algoritmo **demasiado lento**. Si tu solución es correcta pero lenta, no la parchees:
**cambia de algoritmo**.

### 💥 Run Time Error (RTE)

El programa se rompe: excepción, acceso ilegal, división entre cero.

=== "C++"
    ```cpp
    vector<int> tabla(1001);
    tabla.at(n) = 3 * n + 5;    // n puede ser -1000: índice negativo -> excepción
    ```
=== "Python"
    ```python
    n = int(input())
    m = int(input())     # EOFError: solo hay UNA línea en la entrada
    ```

Tres comportamientos que conviene conocer ante el mismo fallo:

- `vector::at` en C++ **lanza** → RTE claro.
- `vector[]` en C++ **no comprueba nada**: lee memoria ajena. A veces peta, a veces
  devuelve basura. Es el peor de los tres.
- En Python un índice negativo es **legal** (cuenta desde el final), así que no falla:
  te da un Wrong Answer silencioso.

Para reproducirlo en local, en Python lee el *traceback*; en C++:

```bash
g++ -std=c++17 -g -fsanitize=address,undefined solucion.cpp -o solucion
```

Eso convierte los accesos fuera de rango silenciosos en mensajes con línea exacta. Es la
herramienta que más tiempo ahorra de todo el curso.

### 🔧 Compile Error (CE)

No compila en la máquina del juez; no se ha ejecutado ni un caso. Un `;` o un `:` que
falta. Dos reglas al leer el mensaje: **mira el primer error**, no el último (uno genera
veinte en cascada), y ten en cuenta que **el número de línea suele apuntar a la
siguiente** al fallo real.

Si compila en tu máquina y no en el juez: versión del lenguaje distinta, una cabecera
que tu compilador incluye de propina, o el lenguaje mal elegido en el desplegable.
Compila en local antes de enviar y esto no pasa.

### 🧠 Memory Limit Exceeded (MLE)

Has pedido más memoria de la permitida. Con 1024 MB cabe mucho, pero una matriz
bidimensional se va enseguida: `int` de 10 000 × 10 000 son 400 MB. Si el enunciado dice
que n llega a 10⁵, una matriz n × n son 10¹⁰ celdas — y es la señal de que hacía falta
otro enfoque.

### 📄 Output Limit Exceeded (OLE)

Has escrito muchísimo más de lo esperado. Casi siempre es un `print` dentro de un bucle
que no termina, o una traza de depuración olvidada. Si ves OLE, busca `print`/`cout`
dentro de bucles: el fallo está ahí, no en tu algoritmo.

### Qué hacer con cada veredicto

```text
├── Accepted ──────────▶ Siguiente problema.
├── Compile Error ─────▶ Compila en local. Primer error, línea anterior.
├── Run Time Error ────▶ Ejecuta en local. Traceback, o -fsanitize.
├── Time Limit ────────▶ ¿Tu complejidad cabe en el límite de n? Si no, cambia
│                        de algoritmo; no lo optimices.
├── Memory Limit ──────▶ Suma el tamaño de tus estructuras.
├── Output Limit ──────▶ Busca prints dentro de bucles.
└── Wrong Answer ──────▶ 1. ¿El formato es exacto?
                         2. ¿Has probado 0, negativos y los extremos?
                         3. ¿Se desborda algún entero?
                         4. Relee el enunciado.
```

!!! tip "El veredicto es información, no una nota"
    Un Wrong Answer no es un suspenso: es un dato que no tenías hace un minuto. Léelo,
    forma una hipótesis, cámbiala, reenvía.

## Cómo es un concurso

El formato del curso es el del **ICPC**: equipos de 3, 5 horas, **un** ordenador para
los tres, 8–13 problemas etiquetados con letras y **no ordenados por dificultad**. Se
compite por fases: local → regional (SWERC) → final mundial. Codeforces, en cambio, es
individual y en rondas de dos horas.

### La penalización

Se ordena por **problemas resueltos**; a igualdad, por **menos penalización**:

- los **minutos** transcurridos hasta cada envío aceptado,
- más **20 minutos** por cada intento fallido, y solo en los problemas que acabas
  resolviendo.

| Problema | AC en el minuto | Fallos | Penalización |
|----------|-----------------|--------|--------------|
| A | 15 | 0 | 15 |
| C | 62 | 2 | 102 |
| E | 140 | 1 | 160 |
| | | | **277** |

Consecuencia práctica: fallar en un problema que no vas a sacar es gratis; enviar a
ciegas uno que sí vas a sacar es caro.

Se puede llevar **material impreso** (tu [chuletario](../../../cheatsheet/index.md)) y
nada electrónico. Cada problema resuelto te da un **globo** de su color en la mesa:
mirando la sala ves qué problemas son fáciles. En la última hora el marcador se
**congela**.

### Estrategia

- **Los primeros quince minutos, leed todos los enunciados**, repartidos. El objetivo es
  tener un mapa, no resolver nada.
- **Empezad por el más fácil.** Casi siempre hay un «leer y aplicar una fórmula» como el
  de este capítulo. Y mirad el marcador: si veinte equipos han resuelto el F, leedlo ya.
- **Que siempre haya alguien pensando en papel** mientras otro teclea. Programar dos
  personas sobre un teclado no funciona; pensar tres sobre el mismo problema, tampoco.
- **Abandona un problema atascado.** Lo más caro no es fallar un envío: es gastar dos
  horas en un problema que no ibas a sacar mientras había otro asequible sin tocar.
- **Con tres WA seguidos, vuelve al enunciado.** En concurso, casi todos los WA
  repetidos son un requisito mal leído.

Y el día antes: **prueba tu entorno**. Compila y envía un problema trivial con tu
plantilla. Si no compila en el juez, mejor descubrirlo entonces.

## Siguientes pasos

### Elegir lenguaje

| | C++ | Python |
|-|-----|--------|
| **Velocidad** | la referencia | 10–100 veces más lento |
| **Escribir** | más verboso | muy corto |
| **Curva de entrada** | más empinada | suave |
| **Enteros grandes** | se desbordan | precisión ilimitada |
| **En el ICPC** | la gran mayoría | se usa, con limitaciones |

**Empieza por el que ya conozcas**: el objetivo de los primeros meses es aprender a
resolver problemas, no pelearte con la sintaxis. Si no conoces ninguno, empieza por
[Python](../../languages/python/index.md) y prevé pasar a
[C++](../../languages/cpp/index.md) más adelante, porque a partir del nivel intermedio
hay problemas que en Python no entran en tiempo. Saber los dos es lo normal.

### Cómo usar este sitio

El contenido está en cinco niveles, de [Base](../../levels/base/index.md) a Experto, y
cada elemento declara sus prerrequisitos. El [mapa de contenidos](../../matrix.md) lo
muestra todo de un vistazo y el [grafo de dependencias](../../graph.md) dice qué
necesitas antes de cada cosa.

Un plan razonable para las primeras semanas:

1. **Entorno y primeros envíos.** Tres problemas de dificultad 1.x. Objetivo: que enviar
   deje de dar pereza.
2. **Lo básico del lenguaje.** [Tipos nativos](../native-types/index.md),
   [Condicionales](../conditionals/index.md), [Bucles](../loops/index.md),
   [Input/Output](../io/index.md), [Arrays](../../data-structures/lists/index.md).
3. **Los primeros algoritmos.** [Búsqueda lineal](../../search/linear-search/index.md),
   [Sum all](../sum-all/index.md), [Complejidad](../complexity/index.md) y
   [Desbordamiento](../overflow/index.md) — este último es la causa número uno de Wrong
   Answer inexplicables.

Un problema al día vale más que diez el domingo. La curva es lenta al principio y luego
se acelera de golpe; casi todo el mundo abandona justo antes de esa parte.

### Cuando te atasques

Prueba primero el árbol de decisión de los veredictos: resuelve la mayoría de los
atascos. Si preguntas, cuenta tres cosas en este orden: **qué problema es** (enlace),
**qué veredicto** te da, y **qué has probado ya**. Y enseña el código, no lo describas.

Sobre leer soluciones: piensa **30–45 minutos**; si no tienes ni idea de por dónde
empezar, busca una pista (el tema, el nombre del algoritmo) antes que la solución
completa. Y cuando leas una, **ciérrala y vuelve a escribirla tú**; si no puedes, no la
has entendido.

## Resumen

- Un problema = enunciado + formato de entrada/salida + límites + ejemplos.
- `stdin` entra, `stdout` sale, `stderr` lo ignora el juez: úsalo para depurar.
- Hay que ser correcto **y** rápido; el límite de n te dice qué complejidad buscar.
- Un envío = un veredicto. El juez se para en el primer fallo y no te lo enseña.
- Ante un **WA**, mira el formato antes que la lógica y prueba los extremos del rango.
- Ante un **TLE**, cambia de algoritmo en vez de optimizar el que tienes.
- Prueba en local con `diff` y quita la depuración antes de enviar. Siempre.
