# Cómo contribuir

¡Gracias por querer aportar! Este proyecto crece con las contribuciones de estudiantes y
profesores. Aquí encontrarás todo lo necesario, **desde cero**.

## La idea en una frase

> Cada algoritmo es **una carpeta**. Escribes el código `full` (comentado) en C++ y
> Python, rellenas un `meta.yaml`, y **el resto se genera solo**: las versiones `clean` y
> `contest`, los tests, la tabla resumen, el grafo de dependencias y el chuletario.

## Ruta recomendada

1. [Git y GitHub](git-github.md) — si nunca los has usado, empieza aquí.
2. [Añadir un algoritmo](add-algorithm.md) — el paso a paso completo.
3. [Scripts del proyecto](scripts.md) — qué hace cada script y cómo ejecutarlo.

## Requisitos

- Python 3.11 o superior.
- Un compilador de C++ (`g++`) si vas a probar el código C++.
- Las dependencias de las herramientas:

```bash
pip install -r tools/requirements.txt
```

Y, si quieres previsualizar la web en local:

```bash
pip install -r requirements.txt
mkdocs serve
```

!!! tip "Antes de abrir tu Pull Request"
    Ejecuta la generación y comprueba que todo está al día:
    ```bash
    python tools/gen.py generate   # crea/actualiza los ficheros derivados
    python tools/gen.py status     # debe decir "up to date"
    ```
    Si no lo haces, la comprobación automática (CI) fallará y te lo recordará.
