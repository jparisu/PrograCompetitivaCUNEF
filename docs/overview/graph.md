# Grafo de dependencias

Relación de prerrequisitos entre temas: sigue las flechas para saber qué aprender antes.
En la siguiente fase este grafo se generará automáticamente desde el campo `prereq` de
cada `meta.yaml`.

```mermaid
graph LR
  loops["Bucles<br/>(Base)"]
  bsearch["Búsqueda binaria<br/>(Principiante)"]
  fenwick["Árbol de Fenwick<br/>(Intermedio)"]
  tsp["DP con máscaras / TSP<br/>(Avanzado)"]
  hull["Envolvente convexa<br/>(Experto)"]

  loops --> bsearch
  bsearch --> fenwick
  fenwick --> tsp
  bsearch --> hull

  classDef base fill:#e8f5e9,stroke:#43a047;
  classDef beginner fill:#e3f2fd,stroke:#1e88e5;
  classDef intermediate fill:#fff8e1,stroke:#fbc02d;
  classDef advanced fill:#fce4ec,stroke:#e91e63;
  classDef expert fill:#ede7f6,stroke:#673ab7;
  class loops base;
  class bsearch beginner;
  class fenwick intermediate;
  class tsp advanced;
  class hull expert;
```
