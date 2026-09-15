---
render_macros: true
---
# C++ de cero a concurso

{{ metadata(complexity="") }}

C++ es el lenguaje de la programación competitiva: rápido, con una librería estándar
enorme y el que usa la mayoría en el ICPC. Este capítulo va **desde cero** hasta los
temas que hacen falta para competir en serio.

Léelo con el editor abierto: cada bloque está pensado para copiarlo, compilarlo y
ejecutarlo. Y rompe las cosas a propósito — reconocer un mensaje de error en dos
segundos, en vez de en cinco minutos, es lo que separa un concurso bueno de uno malo.

Las dos órdenes del curso:

```bash
g++ -std=c++17 -O2 -Wall -Wextra solucion.cpp -o solucion        # normal
g++ -std=c++17 -g -fsanitize=address,undefined solucion.cpp -o solucion   # cuando algo falla
```

Si te falta el contexto de cómo funcionan los jueces, empieza por
[Introducción a la programación competitiva](../../fundamentals/introduction/index.md).
Y si dudas entre los dos lenguajes, el capítulo de
[Python](../python/index.md) es el otro camino.

## Instalar y preparar el entorno

Necesitas un compilador (`g++`, el mismo que usa Kattis), un editor y una terminal.

=== "Linux"
    ```bash
    sudo apt install build-essential     # Debian, Ubuntu
    sudo dnf install gcc-c++             # Fedora
    ```
=== "macOS"
    ```bash
    xcode-select --install
    ```
    Esto instala `clang` disfrazado de `g++`: funciona, pero **no es GCC** y no tendrás
    `bits/stdc++.h` ni `__int128`. Para el GCC real, `brew install gcc`.
=== "Windows"
    Lo mejor es **WSL**: instala Ubuntu desde la Microsoft Store y sigue las
    instrucciones de Linux. Es lo más parecido al juez. Alternativas: MSYS2
    (`pacman -S mingw-w64-ucrt-x86_64-gcc`) o MinGW-w64, añadiendo su `bin` al `PATH`.

Comprueba con `g++ --version`. En el editor (VS Code + extensión C/C++), activa
**Auto Save** —compilar una versión vieja del fichero es un clásico—, 4 espacios y
formateo al guardar.

Organiza una carpeta por problema, y nombra el fichero siempre igual (`solucion.cpp`):
así el comando de compilar es el mismo en todos.

## Tu primer programa

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hola\n";
}
```

```bash
g++ hola.cpp -o hola && ./hola
```

Las piezas:

- **`#include <iostream>`** — trae código que ya existe; `iostream` sabe leer y escribir.
  Los `include` van arriba del todo.
- **`using namespace std;`** — casi toda la librería estándar vive en el espacio de
  nombres `std`, y por eso habría que escribir `std::cout`. Esta línea te lo ahorra. En
  un proyecto grande está mal visto (`std` tiene cientos de nombres que pueden chocar con
  los tuyos); **en concurso se usa siempre**.
- **`int main()`** — el punto de entrada. Todo programa tiene exactamente uno.
- **`return 0;`** — «he terminado bien». En `main` se puede omitir, y se omite.
- **`{ }`** agrupan un bloque; **`;`** termina cada instrucción. La indentación no
  significa nada para el compilador; para ti sí.

### Escribir en la pantalla

```cpp
cout << "n vale " << 42 << " unidades\n";   // se encadena tantas veces como quieras
```

`endl` también escribe un salto de línea, pero además **vacía el búfer**, lo que cuesta
una llamada al sistema. Dentro de un bucle de 10⁵ líneas es una causa real de Time Limit
Exceeded. **Usa `'\n'` siempre.**

### Y leer

```cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;                              // lee un entero de la entrada
    cout << (n + 5) * 3 - 10 << '\n';      // escribe el resultado
}
```

Eso resuelve
[A Shortcut to What?](https://open.kattis.com/problems/shortcuttowhat). Pruébalo con
`echo 12 | ./solucion`: debe responder `41`.

### Los tres errores de la primera vez

| Código | Mensaje |
|--------|---------|
| Falta un `;` | `error: expected initializer before 'cin'` — y señala la línea **siguiente** |
| Falta un `#include` | `error: 'cout' is not a member of 'std'` |
| `void main()` | `error: '::main' must return 'int'` |

Provócalos una vez a propósito. Los vas a ver mucho.

## Compilar y ejecutar

Compilar traduce tu `.cpp` a instrucciones de la CPU **una sola vez**, antes de
ejecutar; de ahí que C++ sea rápido. Hay tres fases, y saber cuál falla ahorra tiempo:

| Mensaje | Fase | Causa |
|---------|------|-------|
| `'cout' is not a member of 'std'` | preprocesador | falta un `#include` |
| `expected ';'` | compilador | error de sintaxis |
| `undefined reference to ...` | enlazador | declarado y no definido |

### Las opciones que importan

| Opción | Para qué |
|--------|----------|
| `-std=c++17` | fija la versión del lenguaje; sin esto cada `g++` usa otra por defecto |
| `-O2` | optimiza. **Es lo que usa el juez**: medir sin esto es medir otra cosa |
| `-Wall -Wextra` | avisos. Cada aviso es un Wrong Answer que te acabas de ahorrar |
| `-g -fsanitize=address,undefined` | convierte los fallos silenciosos en mensajes con línea exacta |

Ese último es la herramienta más valiosa de la página. Si te sales de un `vector`, en vez
de devolver basura te dice:

```text
ERROR: AddressSanitizer: heap-buffer-overflow
    #0 0x... in main solucion.cpp:12
```

El programa va unas tres veces más lento, así que úsalo para depurar, no para medir.

### Pasarle la entrada

```bash
./solucion < 1.in            # la entrada sale de un fichero
./solucion < 1.in > 1.out    # y la salida va a otro
diff 1.out 1.ans             # ¿coinciden?
echo 12 | ./solucion         # un caso suelto
```

Y al leer errores: **arregla el primero**. Un `;` que falta genera veinte en cascada, y
al arreglar el primero desaparecen todos (`-fmax-errors=1` si quieres verlo solo).

## Sintaxis básica

Cada instrucción termina en `;`. Las llaves `{ }` crean un bloque **y un ámbito**: una
variable declarada dentro solo existe ahí. (En Python un `if` no crea ámbito; en C++ sí.)

```cpp
int n;              // declarada SIN inicializar: contiene BASURA
int m = 5;          // así
auto x = 5;         // el compilador deduce el tipo (int)
const int LIMITE = 1000;
constexpr int MOD = 1e9 + 7;      // además, se calcula al compilar
```

!!! warning "Variables sin inicializar"
    `int n;` no vale cero: vale lo que hubiera en esa memoria. Leerla antes de asignarle
    nada produce Wrong Answer que **cambian de una ejecución a otra**. Inicializa
    siempre.

`auto` úsalo cuando el tipo sea evidente o inmanejable (`auto it = v.begin();`), no para
esconder qué estás haciendo.

### La estructura de un programa de concurso

```cpp
#include <bits/stdc++.h>          // 1. incluir
using namespace std;

int main() {
    ios::sync_with_stdio(false);  // 2. E/S rápida
    cin.tie(nullptr);

    int n;   cin >> n;            // 3. leer
    int r = 3 * n + 5;            // 4. calcular
    cout << r << '\n';            // 5. escribir
}
```

Cinco bloques en ese orden. Cuando un programa tuyo no siga esta forma, pregúntate por
qué.

### Tres errores que no dan error

```cpp
if (n = 0) { ... }                // ASIGNA 0; la condición es falsa. -Wall avisa
for (int i = 0; i < n; i++);      // el ; cierra el for: el cuerpo está vacío
if (x > 0);                       // lo mismo: el if no hace nada
    cout << "positivo\n";         // y esto se ejecuta siempre
```

Los dos últimos no dan **ningún** aviso y producen un Wrong Answer perfectamente
silencioso.

## Tipos nativos y variables

Ficha corta: [Tipos nativos](../../fundamentals/native-types/index.md).

### Enteros

| Tipo | Rango |
|------|-------|
| `int` | ±2,1 · 10⁹ |
| `long long` | ±9,2 · 10¹⁸ |
| `unsigned long long` | 0 … 1,8 · 10¹⁹ |

`long` es ambiguo (64 bits en Linux, 32 en Windows): **no lo uses**. Memoriza dos
números —`int` aguanta 2·10⁹ y `long long` aguanta 9·10¹⁸— y una regla: **`int` para
índices y contadores, `long long` para resultados**.

Cuando el resultado no cabe, C++ **no avisa**: da la vuelta.

```cpp
int n = 100000;
long long mal = n * n;              // -1794967296: la multiplicación es de int
long long bien = (long long)n * n;  // 10000000000
```

La multiplicación se hace **entre `int`**, se desborda, y solo después se guarda el
resultado roto. Hay que forzar el tipo **antes**.

!!! warning "La causa número uno de Wrong Answer"
    Un desbordamiento no rompe nada: el programa sigue con un número equivocado. Falla
    solo con las entradas grandes, así que pasa los ejemplos y falla en el juez. Ficha:
    [Desbordamiento](../../fundamentals/overflow/index.md).

### Decimales

Usa siempre `double` (`float` tiene tan poca precisión que da problemas). Y recuerda que
`0.1 + 0.2 == 0.3` es **falso**: compara con tolerancia.

```cpp
if (abs(a - b) < 1e-9) { ... }
cout << fixed << setprecision(6) << x << '\n';   // sin `fixed`, cuenta significativas
```

!!! tip "Evita los decimales si puedes"
    Comparar fracciones multiplicando en cruz (`a*d < c*b`) es exacto; dividir y
    comparar, no. Ver [Coma flotante](../../arithmetics/float-treatment/index.md).

### Caracteres, booleanos y cadenas

```cpp
char c = 'a';
int pos = 'e' - 'a';        // 4: posición en el alfabeto. Aparece constantemente
bool mayor = (a > b);       // imprime 1 o 0, no true/false
string s = "hola";  s += " mundo";
```

`'a'` es un **carácter** y `"a"` una **cadena**: no son intercambiables.

### Conversiones y división

```cpp
int a = 3.9;              // 3: TRUNCA, no redondea
double b = 7 / 2;         // 3.0: la división ya se hizo entre enteros
double c = 7.0 / 2;       // 3.5: basta con que uno sea double
cout << -7 / 2;           // -3: trunca hacia cero
cout << -7 % 2;           // -1: el resto puede ser NEGATIVO
```

!!! warning "El resto negativo"
    En C++ `-7 % 3` da `-1`; en Python da `2`. Con aritmética modular, normaliza:
    `((a % MOD) + MOD) % MOD`.

Para un «infinito», `const int INF = 1e9;` — cabe en `int` y `INF + INF` no se desborda.
No uses `INT_MAX`: `INT_MAX + 1` sí, y esa suma aparece sola dentro de un Dijkstra.

## Operadores y expresiones

```cpp
+ - * / %        ++ --        += -= *= /= %=
== != < <= > >=  && || !      & | ^ ~ << >>       ?:
```

### Cortocircuito

En `A && B`, si `A` es falso **`B` ni se evalúa**. Eso protege los accesos peligrosos:

```cpp
if (i < v.size() && v[i] == x) { ... }   // al revés, se sale del vector
```

### C++ no encadena comparaciones

`0 <= x < n` **compila** y hace otra cosa: evalúa `(0 <= x)`, que da `0` o `1`, y compara
ese `0/1` con `n`. Casi siempre es verdadero. Escribe `0 <= x && x < n`.

### Bits

```cpp
n & 1            // ¿impar?
n >> 1           // dividir entre 2
1 << k           // 2 elevado a k   (¡1LL << k si k es grande!)
n & (1 << k)     // ¿está encendido el bit k?
n | (1 << k)     // encenderlo
n & (n - 1)      // apagar el bit encendido más bajo
__builtin_popcount(n)   // cuántos bits a 1 (GCC)
```

`1` es un `int`: `1 << 40` se desborda. Usa `1LL << 40`.

### Precedencia

Tres trampas que cuestan Wrong Answer de verdad:

```cpp
n + 5 * 3 - 10        // es n + 15 - 10
if (a & 1 == 0)       // es a & (1 == 0), es decir a & 0, siempre 0
cout << i++ << i++;   // el orden de evaluación NO está garantizado
```

**Ante la duda, paréntesis.** No cuestan nada. Y no modifiques una variable y la uses en
la misma expresión.

## Entrada y salida

Fichas: [Input/Output](../../fundamentals/io/index.md) y
[E/S rápida](../../fundamentals/fast-io/index.md).

`cin >> x` se salta todos los espacios en blanco (espacios, tabuladores, saltos de
línea), lee lo que encaje con el tipo, y **devuelve algo que vale `false` si la lectura
falla**. Por eso le da igual cómo esté repartida la entrada en líneas, y por eso funciona
el bucle hasta EOF.

```cpp
int n;      cin >> n;                 // un valor
int a, b;   cin >> a >> b;            // varios
while (cin >> n) { ... }              // hasta el final de la entrada
string linea;  getline(cin, linea);   // la línea completa, espacios incluidos

int N;  cin >> N;                     // N casos anunciados
for (int i = 0; i < N; i++) { ... }

while (cin >> n && n != 0) { ... }    // hasta un centinela
```

!!! warning "Los dos errores de la E/S en C++"
    **El bucle infinito.** `while (true) { cin >> n; }` gira para siempre al acabarse la
    entrada, porque `cin >> n` falla pero no lanza nada. La lectura va **en la
    condición**.

    **El salto de línea pendiente.** `cin >> n` deja el `'\n'` sin consumir, así que el
    `getline` siguiente lee una cadena vacía. Pon un `cin.ignore()` entre medias.

### La salida

```cpp
cout << x << '\n';                                // nunca endl
cout << fixed << setprecision(10) << x << '\n';   // decimales (persistente)
for (int i = 0; i < n; i++)
    cout << v[i] << (i + 1 < n ? ' ' : '\n');     // separados por espacios
```

### E/S rápida

Por compatibilidad con C, `cin`/`cout` se sincronizan con `scanf`/`printf` en cada
operación. Se desactiva así:

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

Leer 10⁶ enteros pasa de ~1 s a ~0,1 s. Como no cuesta nada, va siempre en la plantilla.
El precio: después de esto **no mezcles** `cin`/`cout` con `scanf`/`printf`.

### Depurar

```cpp
cerr << "n vale " << n << '\n';     // el juez ignora la salida de error
```

Mejor todavía, una macro que se apaga sola:

```cpp
#ifdef LOCAL
  #define debug(x) cerr << #x << " = " << (x) << '\n'
#else
  #define debug(x)
#endif
```

Compila en local con `-DLOCAL` y los mensajes aparecen; el juez compila sin él y
desaparecen. Así es imposible dejarse una traza puesta.

## Condicionales

Ficha corta: [Condicionales en C++](../../fundamentals/conditionals/cpp.md).

```cpp
if (a > b) {
    ...
} else if (a < b) {      // solo se comprueba si el anterior falló
    ...
} else {
    ...
}
```

Las ramas se evalúan **en orden** y gana la primera que se cumple: con condiciones
solapadas, ordena de la más restrictiva a la más general.

**Pon las llaves siempre**, aunque el bloque tenga una línea. Sin ellas, añadir una
segunda línea después no la mete en el bloque (y la indentación miente), y un `else`
suelto se asocia al `if` más cercano, no al que sugiere la sangría.

```cpp
int mayor = (a > b) ? a : b;                  // ternario: elige entre dos VALORES
cout << (encontrado ? "SI" : "NO") << '\n';
```

`switch` compara **una** variable entera contra constantes, cada `case` necesita su
`break`, y no admite `double`, `string` ni rangos. En concurso se usa poco: una cadena de
`if`/`else if` es igual de rápida y más flexible.

### Veracidad

```cpp
if (n) { ... }           // equivale a n != 0
if (!v.empty()) { ... }  // los CONTENEDORES no se convierten a bool
```

### Errores

`=` en lugar de `==` (compila; `-Wall` avisa), comparar `double` con `==`, y comparar un
`char` con una cadena (`s[0] == "a"` en vez de `'a'`).

## Bucles

Ficha corta: [Bucles en C++](../../fundamentals/loops/cpp.md).

```cpp
for (int i = 0; i < n; i++)          // de 0 a n-1  ← el 95% de los casos
for (int i = n - 1; i >= 0; i--)     // al revés
for (int i = 1; i * i <= n; i++)     // hasta la raíz (divisores, primalidad)
for (int i = 0, j = n - 1; i < j; i++, j--)   // dos contadores

while (cond) { ... }                 // cuando no sabes las vueltas
```

### `for` sobre un rango

```cpp
for (int x : v)          cout << x;    // copia cada elemento
for (int& x : v)         x *= 2;       // referencia: MODIFICA el vector
for (const auto& x : v)  cout << x;    // sin copiar y sin poder modificar
```

| Forma | Cuándo |
|-------|--------|
| `for (int x : v)` | tipos pequeños, solo lectura |
| `for (auto& x : v)` | quieres **modificar** |
| `for (const auto& x : v)` | tipos grandes (`string`, `vector`), solo lectura |

!!! warning "El `&` olvidado"
    `for (auto x : v) x *= 2;` no hace **nada**: `x` es una copia. Compila sin avisos.

No sirve cuando necesitas el índice: para eso, el `for` clásico.

### Salir de dos bucles

No hay `break 2`. Lo más limpio es sacar el código a una función y usar `return`. Las
alternativas son una bandera o un `goto` a una etiqueta después de los bucles.

### Errores

- **Off-by-one**: con índices desde 0 es `i < n`; desde 1, `i <= n`.
- **Modificar el contenedor mientras lo recorres**: puede reubicarlo en memoria.
- **`v.size()` no tiene signo**: `v.size() - 1` con el vector vacío es un número
  **enorme**, y ahí tienes un bucle de 4 000 millones de vueltas. Guarda el tamaño en un
  `int`.

Y recuerda que los bucles anidados **multiplican** el coste: dos sobre 10⁵ elementos son
10¹⁰ operaciones. Ver [Complejidad](../../fundamentals/complexity/index.md).

## Arrays, vector y string

### `vector`, no arrays crudos

```cpp
vector<int> v;                 // vacío
vector<int> w(n);              // n ceros
vector<int> x(n, -1);          // n veces -1
vector<int> y = {3, 1, 4};

v.push_back(7);   v.pop_back();
v.size();  v.empty();  v.clear();
v[i];              // sin comprobar
v.at(i);           // con comprobación: lanza excepción si te sales
```

El array crudo tiene tamaño fijo, no sabe su tamaño, no se copia bien, y si es local va
en la **pila** (1–8 MB): un `int v[1000000]` dentro de `main` son 4 MB y puede petar con
un Run Time Error. Los arrays grandes van **globales** (y entonces se inicializan a cero)
o en un `vector`, que reserva en el montón.

C++ **no comprueba los índices**: `v[10]` en un vector de 5 escribe donde no debe. A
veces peta, a veces corrompe otra variable, a veces funciona por casualidad. Compila con
`-fsanitize=address` y te lo dice.

El fragmento que aparece en la mitad de los problemas:

```cpp
int n;  cin >> n;
vector<int> v(n);
for (int i = 0; i < n; i++) cin >> v[i];
```

### Matrices

```cpp
vector<vector<int>> m(filas, vector<int>(columnas, 0));
```

Se lee de dentro afuera: «un vector de `filas` elementos, cada uno un vector de
`columnas` ceros». Si el enunciado da un máximo, un array global `int m[MAXN][MAXN]`
suele ser más rápido — pero cuidado: `10000 x 10000` enteros son 400 MB.

### `string`

```cpp
string s = "hola";
s += "!";                            // concatenar
s.size();  s[0];  s.substr(1, 3);
if (s == t) { ... }                  // compara CONTENIDO
if (s < t) { ... }                   // orden lexicográfico
int n = stoi("42");   string t = to_string(42);

int cuenta[26] = {};
for (char c : s) cuenta[c - 'a']++;  // contar letras
```

`s.find("ola")` devuelve `string::npos` si no está, **no** `-1`: compáralo con `npos`.

### Copiar cuesta

Asignar un `vector` o un `string` copia todos los elementos, y pasarlo a una función por
valor también. Esa diferencia puede ser Accepted o Time Limit Exceeded — es el tema de la
sección siguiente.

## Funciones

```cpp
int suma(int a, int b) {
    return a + b;
}
```

C++ lee de arriba abajo: una función debe estar **antes** de usarla. Si prefieres `main`
arriba, declara el prototipo (`int suma(int a, int b);`) y define después. Declarar y no
definir da el error de enlazado `undefined reference to 'suma(int, int)'`.

`void` = no devuelve nada. Y los parámetros son **copias**: modificarlos no afecta a
fuera.

### Devolver varios valores

```cpp
pair<int,int> min_max(const vector<int>& v) { ...; return {mn, mx}; }
auto [mn, mx] = min_max(v);          // structured bindings (C++17)
```

Con más de dos valores, o cuando `first`/`second` no dicen nada, un `struct`.

### Globales

Fuera de concurso están mal vistas. **Dentro son habituales**: en un DFS recursivo,
pasar el grafo y el vector de visitados por todas las llamadas es ruido (y copiarlos sin
darte cuenta, un TLE). Además se inicializan a cero solas.

## Valor, referencia y const

Esta sección decide si tu programa va rápido o lento sin cambiar una línea de algoritmo.

```cpp
void f(vector<int> v);          // COPIA el vector en cada llamada
void f(vector<int>& v);         // referencia: puede modificarlo
void f(const vector<int>& v);   // no copia y no puede modificarlo  ← lo normal
```

Con un vector de un millón de elementos, la primera copia 4 MB **por llamada**. Dentro de
un bucle o de una recursión, es un Time Limit Exceeded garantizado — y no da ningún
aviso.

| Tipo del parámetro | Cómo pasarlo |
|--------------------|--------------|
| `int`, `double`, `char`, `bool` | por valor |
| `vector`, `string`, `map`, `struct` grande | `const T&` si solo lees |
| Cualquiera que debas modificar | `T&` |

Memoriza `const vector<int>&`. Lo vas a escribir mil veces.

Lo mismo en los bucles y al recorrer un `map`:

```cpp
for (const auto& [clave, valor] : m) { ... }   // sin copiar la clave ni el valor
```

**Usa referencias, no punteros**, para pasar argumentos: no pueden ser nulas, no hay que
inicializarlas y la sintaxis es la normal.

Dos cosas que **no** son problema: devolver un contenedor **por valor** (desde C++11 el
compilador lo mueve o lo construye en su destino, sin coste), y `std::move`, que existe y
que en concurso casi nunca hace falta. El problema son los parámetros, no los retornos.

Y nunca devuelvas una referencia a una variable local: muere al salir.

## struct y class

```cpp
struct Punto {
    int x = 0, y = 0;                        // valores por defecto: gratis y evitan errores

    int norma2() const {                     // const: no modifica el objeto
        return x * x + y * y;
    }
};

Punto p{3, 4};
cout << p.norma2();      // 25

vector<Punto> v;
v.push_back({1, 2});
v.emplace_back(3, 4);    // construye en el sitio
```

`class` es idéntico salvo que su contenido es **privado** por defecto. En concurso, usa
`struct` con todo público: tus programas son de treinta líneas y no hay a quién proteger.
La excepción es una estructura reutilizable de tu chuletario, donde la interfaz pública
es corta y el estado interno no debe tocarse.

### Ordenar objetos propios

```cpp
struct Punto {
    int x = 0, y = 0;
    bool operator<(const Punto& o) const {
        if (x != o.x) return x < o.x;    // primero por x
        return y < o.y;                   // a igualdad, por y
    }
};

sort(v.begin(), v.end());                              // usa tu operator<
sort(v.begin(), v.end(), [](const Punto& a, const Punto& b) {
    return a.y < b.y;                                  // o un criterio puntual
});
```

Con `operator<` definido, el tipo sirve también como clave de un `set` o un `map`.

!!! warning "Tiene que ser un orden estricto"
    `sort` exige que nunca sea `a < a`. Si te equivocas (por ejemplo usando `<=`), el
    programa puede **petar dentro de `sort`**, no dar un resultado mal.

Añade `operator<<` (fuera del struct) si quieres poder hacer `cout << p` al depurar.
Herencia y métodos virtuales existen y **no se usan en concurso**.

## Organizar el código

El juez acepta **un fichero**, y va en este orden: includes → alias y constantes →
globales → structs y funciones → `main`.

```cpp
using ll = long long;
using pii = pair<int,int>;
#define all(v) (v).begin(), (v).end()
const int INF = 1e9;
const int MOD = 1e9 + 7;
```

Los `using` están en toda plantilla de concurso (mejor que `typedef`, misma cosa con peor
sintaxis). Para constantes, `const`/`constexpr` en vez de `#define`: tienen tipo y
respetan el ámbito.

Si alguna vez separas en varios ficheros: la cabecera `.h` dice **qué** existe, el `.cpp`
**cómo** funciona, `#pragma once` al principio de cada cabecera, y se compila
`g++ main.cpp otro.cpp -o programa`. Olvidar un `.cpp` en esa orden da el
`undefined reference` de siempre.

### Macros

```cpp
#define CUADRADO(x) ((x) * (x))     // los paréntesis de sobra NO son opcionales
```

`#define MAL(x) x * x` con `MAL(1 + 2)` se expande a `1 + 2 * 1 + 2 = 5`. Y aun con
paréntesis, el argumento se evalúa dos veces: `CUADRADO(i++)` es comportamiento
indefinido. Úsalas si te sientes cómodo, pero sabiendo qué hacen: una macro mal escrita
produce errores imposibles de leer.

## Contenedores (STL)

La **STL** tiene tres piezas: contenedores (guardan datos), iteradores (los recorren) y
algoritmos (operan sobre rangos). Está probada y es rápida, y es la razón principal de
que C++ domine en concursos. **No reimplementes nada de lo que hay aquí.**

### Secuencias y adaptadores

```cpp
vector<int> v;       // tu contenedor por defecto
deque<int> d;        // crecer por los DOS extremos en O(1): BFS, ventana deslizante
array<int,3> a;      // tamaño fijo, coste cero, copiable

stack<int> s;    s.push(x);  s.top();  s.pop();
queue<int> q;    q.push(x);  q.front(); q.pop();
priority_queue<int> pq;                                   // máximo arriba
priority_queue<int, vector<int>, greater<int>> pqmin;     // mínimo arriba
```

!!! warning "`top()` y `pop()` están separados"
    `pop()` no devuelve el elemento: hay que leerlo antes con `top()`/`front()`.

`list` existe y casi nunca gana a `vector`. Ver
[Stack & queue](../../data-structures/stack-queue/index.md) y
[Priority queue](../../data-structures/priority-queue/index.md).

### Conjuntos y diccionarios

```cpp
set<int> s;              // ORDENADO, sin repetidos, todo O(log n)
multiset<int> ms;        // admite repetidos
map<string,int> m;       // diccionario ordenado
unordered_map<string,int> um;   // hash: O(1) medio, SIN orden

s.insert(3);  s.count(3);  s.erase(3);
auto it = s.lower_bound(x);     // el menor elemento >= x
m["hola"]++;
```

!!! warning "Dos trampas caras"
    **`m[clave]` crea la entrada.** Consultar con `[]` una clave que no existe la
    **inserta** con valor cero. Para solo comprobar, `m.count(k)` o `m.find(k)`.

    **En `set`/`map`, usa el método.** `s.lower_bound(x)` es O(log n);
    `lower_bound(s.begin(), s.end(), x)` es **O(n)**, porque sus iteradores no son de
    acceso aleatorio. Un TLE silencioso.

`ms.erase(3)` borra **todas** las copias; para una sola, `ms.erase(ms.find(3))`.

### `pair` y `tuple`

```cpp
pair<int,int> p = {1, 2};       // p.first, p.second
auto [a, b] = p;
tuple<int,int,string> t;
```

Se comparan **lexicográficamente**, lo que los hace perfectos para ordenar por varios
criterios: `sort` sobre un `vector<pair<int,int>>` ordena por el primero y, a igualdad,
por el segundo. Y sirven como clave de un `map` (no de un `unordered_map`, que no sabe
calcular su hash).

### Qué contenedor para qué

| Necesito | Contenedor | Coste |
|----------|-----------|-------|
| Acceso por índice | `vector` | O(1) |
| Los dos extremos | `deque` | O(1) |
| Sacar siempre el mínimo/máximo | `priority_queue` | O(log n) |
| «El siguiente mayor que x» | `set` | O(log n) |
| Diccionario ordenado | `map` | O(log n) |
| Diccionario rápido sin orden | `unordered_map` | O(1) medio |
| **Claves enteras pequeñas y acotadas** | **`vector` indexado** | **O(1)** |

Esa última fila importa y se olvida: si las claves son enteros de 0 a 10⁶, un
`vector<int>` de un millón de posiciones gana a cualquier diccionario.

## Iteradores

Ficha corta: [Iteradores](../../fundamentals/iterators/index.md).

Un iterador **señala a una posición** y sabe avanzar. Es la pieza que permite que `sort`
funcione igual con un `vector` que con un array.

```text
   v:   [ 3 ][ 1 ][ 4 ]
          ▲            ▲
        begin()      end()
```

`end()` señala **uno más allá** del último. Eso hace que un rango vacío sea
`begin() == end()` y que el tamaño sea `last - first`, sin restar uno en ningún sitio.
Desreferenciarlo es comportamiento indefinido.

```cpp
for (auto it = v.begin(); it != v.end(); ++it) cout << *it;
for (auto it = m.begin(); it != m.end(); ++it) cout << it->first;
```

El tipo real es larguísimo: usa `auto`. Y si solo vas a recorrer, el `for` por rango es
más claro — los iteradores hacen falta cuando **necesitas la posición**: borrar,
insertar, o pasar un rango a un algoritmo.

No todos pueden lo mismo: `vector`/`deque`/`string` son de **acceso aleatorio**
(`it + 5`, `it2 - it1`), `set`/`map`/`list` son **bidireccionales** (solo `++`/`--`, y
para moverse `next`/`prev`/`advance`). De ahí la trampa del `lower_bound` de la sección
anterior.

### Borrar

```cpp
for (auto it = v.begin(); it != v.end(); ) {
    if (*it < 0) it = v.erase(it);     // erase devuelve el siguiente válido
    else ++it;                          // el ++ NO va en el for
}

v.erase(remove(all(v), 0), v.end());    // borrar TODOS los ceros, en O(n)
sort(v.rbegin(), v.rend());             // ordenar descendente
```

`remove` no borra: **compacta** y devuelve el nuevo final; `erase` borra la cola. Por eso
hacen falta los dos. (En C++20, `std::erase(v, 0)` hace lo mismo en una llamada.)

Y ojo: modificar un contenedor **invalida** iteradores. En un `vector`, un `push_back`
que lo haga crecer invalida todos.

## `<algorithm>`

Todo esto está escrito, probado y optimizado. Reimplementarlo cuesta tiempo y añade
errores.

```cpp
#define all(v) (v).begin(), (v).end()
```

### Ordenar y buscar

```cpp
sort(all(v));                                  // O(n log n)
sort(all(v), greater<int>());                  // descendente
sort(v.rbegin(), v.rend());                    // descendente, más corto
stable_sort(all(v), cmp);                      // mantiene los empates
nth_element(v.begin(), v.begin()+k, v.end());  // el k-ésimo, en O(n)

find(all(v), x);                 // O(n)
count(all(v), x);                // O(n)
binary_search(all(v), x);        // O(log n), rango ORDENADO
lower_bound(all(v), x);          // primer elemento >= x
upper_bound(all(v), x);          // primer elemento >  x
upper_bound(all(v), x) - lower_bound(all(v), x);   // cuántos x hay
```

Sobre un rango sin ordenar, `lower_bound` no da error: da un resultado **mal**. Ficha:
[Binary search](../../search/binary-search-array/index.md).

### El resto

```cpp
max({a, b, c});                  min(a, b);
*max_element(all(v));            max_element(all(v)) - v.begin();   // valor / índice
accumulate(all(v), 0LL);         // suma — el 0LL decide el TIPO
reverse(all(v));                 iota(all(v), 0);      // 0, 1, 2, ...
sort(all(v)); v.erase(unique(all(v)), v.end());        // quitar duplicados

sort(all(v));
do { ... } while (next_permutation(all(v)));           // las n! permutaciones
```

!!! warning "`accumulate(all(v), 0)` se desborda"
    El tercer argumento decide el tipo del acumulador. Con `0`, acumula en un `int`
    aunque guardes el resultado en un `long long`. Escribe `0LL`.

`unique` solo elimina duplicados **consecutivos** — de ahí el `sort` previo — y, como
`remove`, no borra: compacta. Esas dos líneas juntas son el idioma estándar.

Y antes de escribir un bucle, comprueba si ya existe la función.

## Otras utilidades

```cpp
#include <bits/stdc++.h>     // TODA la librería estándar de golpe
```

No es estándar: es una extensión de GCC. En Kattis y Codeforces funciona; en macOS con
`clang` o en Visual Studio, no.

### Matemáticas

```cpp
abs(-5);   sqrt(16.0);   ceil(3.2);   floor(3.8);   round(3.5);
hypot(3.0, 4.0);                      // sqrt(x²+y²) sin desbordar
const double PI = acos(-1.0);
gcd(a, b);   lcm(a, b);               // <numeric>, C++17
```

!!! warning "`pow` y `sqrt` trabajan con `double`"
    `int x = pow(10, 2);` puede dar **99**, porque `10²` sale como `99.999...` y al
    convertir a `int` trunca. Para potencias enteras escribe un bucle (o
    [exponenciación binaria](../../arithmetics/binary-exponentiation/index.md)); para
    raíces, ajusta con `while (r*r > n) r--;`.

`__int128` (extensión de GCC) da enteros de 128 bits, útiles para comprobar si una
multiplicación se desborda. No se imprime con `cout` directamente.

### Texto, azar, tiempo y bits

```cpp
stringstream ss(linea);
while (ss >> x) { ... }               // partir una línea en trozos de longitud variable

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
uniform_int_distribution<int> dist(1, 100);   // dist(rng)

auto t0 = chrono::steady_clock::now();
cerr << chrono::duration_cast<chrono::milliseconds>(
        chrono::steady_clock::now() - t0).count() << " ms\n";

bitset<100000> b;   b.set(7);   b.count();   b1 &= b2;
```

`mt19937` (evita `rand()`) sirve sobre todo para **generar casos de prueba** y compararlos
contra una solución lenta pero segura. Y `bitset` ocupa un bit por elemento y opera 64 a
la vez: convierte un O(n²) en un O(n²/64), que a veces es justo lo que falta. Su tamaño
tiene que ser constante en tiempo de compilación.

## Punteros y memoria

En concurso apenas escribirás punteros —`vector` y las referencias cubren casi todo—,
pero explican por qué fallan algunas cosas.

### El modelo de memoria

| Zona | Qué guarda | Tamaño |
|------|-----------|--------|
| **Pila** | locales y llamadas a función; se libera sola | 1–8 MB |
| **Montón** | `vector`, `string`, `new` | casi toda la RAM |
| **Estática** | globales, inicializadas a 0 | |

De ahí dos cosas que ya hemos visto: un `int v[1000000]` **local** peta, y una recursión
de 10⁶ niveles también (`Segmentation fault`, que el juez reporta como Run Time Error).

### Punteros

```cpp
int x = 42;
int* p = &x;      // &x: la DIRECCIÓN de x
cout << *p;       // *p: el CONTENIDO de esa dirección  → 42
*p = 100;         // modifica x
int* q = nullptr; // no apunta a nada; comprueba antes de usar: if (q) ...
```

Dos operadores y no más. El nombre de un array es la dirección de su primer elemento, y
`v[i]` **es** `*(v + i)`: eso es toda la magia de la indexación, y explica por qué C++ no
comprueba los límites — `v[1000]` es una dirección perfectamente calculable.

Con structs, `p->campo` es azúcar para `(*p).campo`. Y una estructura que se apunta a sí
misma es la idea detrás de listas enlazadas y árboles:

```cpp
struct Nodo { int valor; Nodo* siguiente = nullptr; };
for (Nodo* n = &a; n != nullptr; n = n->siguiente) cout << n->valor;
```

(En concurso los árboles se representan con índices en un `vector`: más rápido y no hay
que liberar nada.)

### `new` y `delete`

Existen, y en concurso **no los uses**: `vector` hace el mismo `new` por dentro, libera
solo, sabe su tamaño y se copia bien. Los punteros inteligentes (`unique_ptr`,
`shared_ptr`) son la forma correcta fuera de concurso.

Los tres errores clásicos —desreferenciar `nullptr`, un puntero colgante a una variable
que ya murió, y salirse de un array— se detectan todos con
`-fsanitize=address,undefined`. Si alguna vez ves un `Segmentation fault` sin más
información, esa es la orden.

## Lambdas y objetos función

Ficha corta: [Lambda](../../fundamentals/lambda/index.md).

`sort` sabe ordenar pero no sabe **según qué criterio**. Una lambda es ese criterio
escrito ahí mismo:

```cpp
sort(all(v), [](const Punto& a, const Punto& b) { return a.y < b.y; });
```

La sintaxis es `[captura](parámetros) { cuerpo }`, y se guarda con `auto` porque su tipo
es único e inescribible:

```cpp
auto es_par = [](int x) { return x % 2 == 0; };
count_if(all(v), es_par);
```

### Capturas

Una lambda no ve las variables de fuera salvo que las capture: `[x]` por valor (copia,
y es `const` dentro), `[&x]` por referencia, `[=]` y `[&]` todo lo que use. **En concurso
`[&]` es lo habitual**: captura lo que haga falta y no copia nada.

!!! warning "No captures por referencia algo que muere"
    Si la lambda va a sobrevivir al ámbito actual, captura **por valor**.

### Los usos

```cpp
sort(all(v), [](const Alumno& a, const Alumno& b) {
    if (a.nota != b.nota) return a.nota > b.nota;   // nota descendente
    return a.nombre < b.nombre;                      // empate: nombre
});

vector<int> peso = {5, 2, 9}, idx = {0, 1, 2};
sort(all(idx), [&](int a, int b) { return peso[a] < peso[b]; });   // ordenar ÍNDICES
```

Ese último patrón —ordenar índices por un criterio externo— aparece constantemente.

Para `priority_queue` y `set` el comparador es parte del **tipo**, así que hay que
declararlo antes: `priority_queue<T, vector<T>, decltype(cmp)> pq(cmp);`. Con `set`,
muchas veces sale más fácil definir `operator<`.

### Lambdas recursivas

Una lambda no puede llamarse por su nombre (`auto` aún no ha deducido el tipo). Dos
salidas:

```cpp
function<int(int)> fact = [&](int n) { return n <= 1 ? 1 : n * fact(n-1); };  // cómoda, lenta
auto f = [](auto&& self, int n) -> int { return n <= 1 ? 1 : n*self(self,n-1); };  // rápida, fea
```

`std::function` añade una llamada indirecta por nivel; en un DFS pesado se nota.

La STL trae los comparadores más comunes ya hechos: `greater<int>()` para orden
descendente y para montículos de mínimos.

## Plantillas (templates)

Escribir `maximo` para `int`, `double` y `string` son tres funciones idénticas. Una
plantilla escribe esa familia de una vez:

```cpp
template <typename T>
T maximo(T a, T b) { return a > b ? a : b; }

maximo(3, 7);            // T = int
maximo<double>(3, 7.1);  // forzando T, porque no puede deducirlo de tipos distintos
```

Y lo mismo con clases, que es el uso real en concurso: una estructura de datos que
funcione con `int` y con `long long`.

```cpp
template <typename T>
struct Pila {
    vector<T> datos;
    void push(const T& x) { datos.push_back(x); }
    T pop() { T x = datos.back(); datos.pop_back(); return x; }
};

Pila<int> p;      // al usarla hay que decir el tipo
```

Una plantilla **no es código**: es una receta. El compilador genera una copia por cada
tipo con el que la uses, así que **no hay coste en tiempo de ejecución** — es como si las
hubieras escrito a mano. A cambio, los errores no aparecen hasta que la instancias, y
producen un muro de texto. Dos reglas para leerlo: busca la línea
`in instantiation of ... [with T = ...]`, que dice desde dónde llamaste, y el **primer**
`error:`.

**Úsalas para las estructuras reutilizables de tu chuletario.** Para la solución de un
problema concreto, si solo vas a usar `int`, escribe `int`: es más corto, compila antes y
los errores se leen.

## Recursión y pila de llamadas

Ficha corta: [Recursión](../../fundamentals/recursion/index.md).

```cpp
long long factorial(int n) {
    if (n <= 1) return 1;            // caso base
    return n * factorial(n - 1);     // caso recursivo, con un problema MÁS PEQUEÑO
}
```

Las dos partes son obligatorias, y el caso recursivo tiene que **encoger**. Cada llamada
activa ocupa un marco de pila, así que con 10⁵–10⁶ niveles se agota y obtienes un
`Segmentation fault` → Run Time Error.

### Cuándo compensa

El bucle, salvo que la recursión sea claramente más natural. **La recursión gana cuando
el problema se ramifica**: árboles, grafos, backtracking. Ahí el bucle equivalente
necesita una pila explícita y se lee mucho peor.

```cpp
void dfs(int u) {                        // seis líneas
    visitado[u] = true;
    for (int v : g[u]) if (!visitado[v]) dfs(v);
}

void permutar(vector<int>& v, int k) {   // vuelta atrás
    if (k == (int)v.size()) { imprimir(v); return; }
    for (int i = k; i < (int)v.size(); i++) {
        swap(v[k], v[i]);        // probar
        permutar(v, k + 1);      // seguir
        swap(v[k], v[i]);        // DESHACER  ← la esencia del backtracking
    }
}
```

Ver [DFS](../../graphs/dfs/index.md) y
[Backtracking](../../search/backtracking/index.md).

### Memoización

```cpp
long long fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);       // O(2^n): fib(40) son 300 millones de llamadas
}

vector<long long> memo;               // inicializado a -1
long long fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib(n-1) + fib(n-2);    // O(n)
}
```

De exponencial a lineal con tres líneas. Esto **es**
[programación dinámica](../../dynamic-programming/dynamic-programming/index.md), y
[Fibonacci](../../dynamic-programming/fibonacci/index.md) su ejemplo canónico.

### Los errores

Sin caso base; un caso base que nunca se alcanza (usa `if (n <= 0)` si el paso no es de
uno en uno); no marcar los visitados, que en un ciclo no termina nunca; y sobre todo
**pasar los contenedores por valor**, que copia el grafo entero en cada llamada.

## Rendimiento en concurso

### La regla de bolsillo

Un juez hace ~**10⁸ operaciones por segundo**. Con 1 segundo:

| n máximo | Complejidad que cabe | Ejemplo |
|----------|----------------------|---------|
| 10 | O(n!) | permutaciones |
| 20 | O(2ⁿ) | subconjuntos, DP de máscaras |
| 500 | O(n³) | Floyd-Warshall |
| 5 000 | O(n²) | DP sobre dos índices |
| 10⁶ | O(n log n) | ordenar, búsqueda binaria |
| 10⁸ | O(n) | un solo recorrido |

**Mira el límite del enunciado antes de elegir el algoritmo**: te está diciendo la
respuesta. Ver [Complejidad (Big-O)](../../fundamentals/complexity/index.md).

### Lo que se aplica siempre

1. `ios::sync_with_stdio(false); cin.tie(nullptr);`
2. `'\n'` en vez de `endl`.
3. `const vector<int>&` en los parámetros y `const auto&` en los bucles por rango.
4. Compilar con `-O2`, porque es lo que usa el juez.

### Lo que se aplica a veces

- **Elegir bien la estructura**: `vector` antes que `list`, `unordered_map` antes que
  `map`, y un `vector` indexado antes que cualquier diccionario si las claves son enteros
  acotados.
- `reserve(n)` si sabes cuántos elementos vas a meter.
- **Salir pronto** de los bucles, y **precalcular** si vas a responder muchas consultas
  (ver [sumas prefijas](../../data-structures/prefix-sums/index.md)).
- **Enteros en vez de decimales**: más rápidos y más exactos.
- `bitset` para conjuntos grandes.
- Acumular la salida en un `string` y escribirla de una vez, a partir de ~10⁶ líneas.

`#pragma GCC optimize("O3")` está permitido, pero **no arregla una complejidad mala**.

### Medir

```bash
./generador > grande.in       # el peor caso que permita el enunciado
time ./solucion < grande.in > /dev/null
```

Medir con el ejemplo del enunciado no dice nada. Y tres cosas que no hay que hacer:
microoptimizar antes de arreglar la complejidad, confiar en que «el juez es rápido» (suele
ser más lento que tu portátil) y optimizar sin medir.

## Qué se puede usar en un concurso

La regla es corta: **un fichero fuente, la librería estándar y nada más**. El juez
compila tu código en una máquina aislada y lo ejecuta con la entrada por `stdin`. Todo lo
que se salga de ahí —una librería que hay que instalar, un fichero del disco, una
conexión a Internet— o no está o está prohibido.

### Sí

- **Toda la librería estándar de C++.** Es la que se espera que uses.
- **`#include <bits/stdc++.h>`** y las **extensiones de GCC** (`__int128`,
  `__builtin_popcount`). Funcionan en Kattis y Codeforces, no en `clang` ni en Visual
  Studio.
- **`#pragma GCC optimize("O2")`** y similares.
- **Tu propio código**: plantillas y estructuras que hayas escrito antes, pegadas en el
  fichero que envías.

### No

- **Librerías de terceros.** Boost, Eigen, GMP, OpenCV: no están. Si tu código las
  incluye, **Compile Error**. Si necesitas enteros grandes o una estructura rara, la
  escribes tú.
- **Ficheros, sistema operativo y red.** Nada de `fopen`, `ifstream` sobre un fichero
  tuyo, `system()`, `getenv` ni sockets. El sandbox lo bloquea.
- **Hilos y paralelismo.** `<thread>` y OpenMP no sirven para ganar tiempo: el juez mide
  el tiempo de CPU total y normalmente da un solo núcleo.
- **Trampas.** Intentar leer los casos de prueba, detectar en qué caso estás para
  responder a mano, escribir en `stderr` para esquivar la comparación: detectado, es
  descalificación.

!!! warning "El `freopen` de depurar"
    Es cómodo probar en local con `freopen("entrada.txt", "r", stdin);`. **Bórralo antes
    de enviar**: en el juez ese fichero no existe y tu programa se queda sin entrada.

### En un concurso presencial (ICPC)

Se añaden las reglas de la sala: **sin Internet** salvo el juez, **sin comunicación**
fuera del equipo, **un solo ordenador** para los tres, y **material impreso sí**, con el
límite de páginas que fije la organización — es tu
[chuletario](../../../cheatsheet/index.md).

### Compruébalo antes de competir

Los detalles cambian de un juez a otro. Mira la página de lenguajes (en Kattis,
*Help → Languages*) y apunta **qué versión del compilador** usa y **con qué opciones**
compila. Pero la prueba definitiva es más simple: **envía un problema trivial con tu
plantilla** antes del concurso. Si pasa, tu plantilla es válida.

## Errores frecuentes

### Que no compilan

| Mensaje | Causa |
|---------|-------|
| `expected initializer before ...` | falta un `;` en la línea **anterior** |
| `expected '}' at end of input` | una llave sin cerrar |
| `'cout' is not a member of 'std'` | falta un `#include` |
| `undefined reference to 'f()'` | declarada y no definida |
| `undefined reference to 'main'` | no hay `main`, o está mal escrito |

Y si compila en local y no en el juez: `-std=c++17`, una cabecera de propina, o
`bits/stdc++.h` en un compilador que no es GCC.

### Que dan Wrong Answer

```cpp
long long x = n * n;              // se desborda: (long long)n * n
double m = suma / n;              // división entera: (double)suma / n
if (a == b)                       // con double: abs(a-b) < 1e-9
(-7) % 3                          // -1 en C++, 2 en Python
n + 5 * 3 - 10                    // precedencia: paréntesis
if (0 <= x < n)                   // 0 <= x && x < n
for (auto x : v) x *= 2;          // no hace nada: auto&
int suma;                         // sin inicializar: contiene basura
cout << "El resultado es: " << x; // el juez compara texto
```

Y los casos límite que casi siempre fallan: `n = 0` o entrada vacía, un único elemento,
todos iguales, los extremos del rango, negativos y el cero.

### Que dan Run Time Error

Índice fuera de rango; `v.size() - 1` con el vector **vacío** (es sin signo, así que da
un número enorme); dividir entre cero; recursión demasiado profunda; un array grande en
la pila; un puntero nulo.

### Que dan Time Limit Exceeded

Complejidad demasiado alta (lo primero que hay que mirar, siempre); pasar un contenedor
**por valor**, especialmente en recursión; `endl` en un bucle; no poner la E/S rápida; un
bucle que no termina; `lower_bound` libre sobre un `set`.

### Checklist antes de enviar

```text
□ Compila con -std=c++17 -O2 -Wall -Wextra, sin avisos
□ Pasa TODOS los ejemplos del enunciado
□ Probado con los extremos del rango (mínimo, máximo, 0, negativos)
□ Sin cout de depuración, sin freopen
□ ¿Puede desbordarse algún int? → long long
□ ¿La complejidad cabe en el límite del enunciado?
□ ios::sync_with_stdio(false) si la entrada es grande
□ El formato de salida es EXACTAMENTE el del enunciado
```

Treinta segundos que ahorran veinte minutos de penalización.

## Plantilla de concurso

La mínima, que es la que deberías usar si no vas a usar más:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // leer / resolver / escribir
}
```

La ampliada:

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll  = long long;
using pii = pair<int, int>;
using vi  = vector<int>;

#define all(v) (v).begin(), (v).end()

const int INF = 1e9;
const ll  INFLL = 4e18;
const int MOD = 1e9 + 7;

#ifdef LOCAL
  #define debug(x) cerr << #x << " = " << (x) << '\n'
#else
  #define debug(x)
#endif

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;   cin >> n;
    vi v(n);
    for (int& x : v) cin >> x;

    // resolver
}
```

Compila en local con `-DLOCAL` y las trazas salen; el juez compila sin él y desaparecen.
Así es imposible dejarte una puesta.

### Con varios casos de prueba

```cpp
void resolver() {
    int n;  cin >> n;
    cout << 3 * n + 5 << '\n';
}

int main() {
    ios::sync_with_stdio(false);  cin.tie(nullptr);
    int T;  cin >> T;
    while (T--) resolver();
}
```

Sacar el caso a una función es lo que hace esto cómodo: `return` te saca del caso actual
sin tocar el bucle.

!!! warning "Reinicializa las globales entre casos"
    Arrastrar el estado del caso anterior es un Wrong Answer que **solo aparece con
    varios casos**.

### Cómo usarla

Guárdala como *snippet* del editor, haz **una copia por problema** (nunca trabajes sobre
la original), y adáptala: si nunca usas `pii`, quítalo. Lo importante es que **entiendas
cada línea**. Una plantilla copiada de Internet con veinte macros que no sabes qué hacen
es una fuente de errores, no una ayuda.

Y para el papel del ICPC: la plantilla, las estructuras que no quieres reescribir
(*union-find*, *segment tree*, Fenwick), los algoritmos largos (Dijkstra, flujo máximo,
KMP, criba) y las fórmulas. El [Chuletario](../../../cheatsheet/index.md) del curso te
deja elegir qué entra. Imprímelo **con semanas de antelación** y **úsalo en un
entrenamiento**: un chuletario que nunca has consultado no lo vas a saber consultar bajo
presión.

## Siguiente paso

Ya tienes C++. Lo que falta es resolver problemas: vuelve a
[Contenidos](../../index.md) y empieza por el nivel
[Base](../../levels/base/index.md).
