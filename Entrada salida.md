# Entrada y salida

En programación competitiva, la entrada y salida del programa viene dada de una forma muy concreta.
- El juez online pasa por la entrada estándar un archivo secreto de entrada
- El juez luego compara la salida de tu programa con un archivo secreto de salida.

Puedes emular esto copiando y pegando el sample in en la terminal, y viendo lo que saca tu programa en terminal. En la terminal se verá la entrada y la salida mezclada, pero el juez las ve por separado. Por esto, no hace falta procesar todos los casos de prueba del tirón y sacar toda la salida de todos los casos al final.

**NO** hay que hacer couts superfluos tipo "dame un entero". También, si el enunciado dice que la entrada viene dada de cierta forma, **NO** hay que comprobar que la entrada esté bien formada.

### Entrada y salida básica

En python, ``input()`` devuelve la siguiente línea de la entrada en formato cadena. Puedes usar algunas de las siguientes funciones:
- ``split()`` te divide la línea por espacios
- ``int()`` y ``float()`` son funciones que convierten cadenas a enteros o números reales.
- ``map(int, lista)`` aplica el casting a entero a cada elemento de la lista

Algunos ejemplos:

```python 
cadena1=input() # leer una cadena
cadena1,cadena2=input().split() # divide la línea en dos (asume que hay exactamente un espacio en la línea)

entero1=int(input()) # cuando lees un entero de una línea
entero1, entero2= map(int,input().split()) # Para leer una línea con dos enteros

lista_cadenas=input().split() # leer muchas cadenas en la misma línea, separadas por espacios

lista_enteros=list(map(int,input().split())) # leer muchos enteros en la misma línea
```

En c++ el paradigma es totalmente distinto. En vez de leer línea a línea, leemos hasta el siguiente espacio. El compilador mágicamente convierte las cadenas en el tipo qu sea sin pedirlo nosotros. Pero no podemos leer del tirón una lista como en python.

```c++
string cadena; cin>>cadena; //lee una cadena terminando en el espacio
cadena= cin.getline(); // esto es cuando quieres leer hasta final de línea

int entero1, entero2;
cin>>entero1>>entero2; // leer varios enteros se hace así.

// para leer una lista de enteros tienes que saber cuántos hay primero. Casi siempre te lo da el enunciado.
int numero_enteros; cin>>numero_enteros;
vector<int> lista_enteros(numero_enteros);
for(int i=0; i<numero_enteros; i++) cin>>lista_enteros[i];
```

### La entrada comienza con una linea con el número $n$ de casos de prueba...
```c++
int main() {
  int num_casos; cin>>num_casos;

  for(int caso=1; caso<=num_casos; caso++) {
    //lee y procesa el caso de prueba
    //...
    
    cout<<"Case #"<<caso<<": "<<solucion<<endl; // A veces el enunciado te pide dar el caso de prueba. Otras no.
  }
  return 0;
}
```

```python
num_casos=int(input())
for caso in range(1, num_casos+1):
  # Lee y procesa el caso de prueba
  # ...

  print("Case #{}: {}".format(caso,solución))
```

### La entrada termina con una línea con uno/varios ceros que no debe procesarse...

```c++
// tipicamente esto es cuando la primera línea del caso de prueba es n, o m>0
int n,m;
cin>>n>>m;
while(n!=0 || m!=0) {
  // lee el resto del caso de prueba y procesalo
  // ...
  cin>>n>>m;
}
```
```python
n,m=map(int,input().split());
while n!=0 or m!=0:
  # lee el resto del caso de prueba y procesalo
  # ...
  n,m=map(int,input().split())
```

### La entrada termina sin avisar porque los problemsetters son mala gente

```c++
int n,m;
while(cin>>n>>m) { // lees la primera línea del caso de prueba
  // lee el resto del caso de prueba y procesalo
  // ...
}
```
```python
while True:
  try:
    n,m=map(int,input().split())
    # lee el resto del caso de prueba y procesalo
    # ...
  except:
    break
```