# Git y GitHub (desde cero)

Si nunca has usado Git ni GitHub, esta página te lleva paso a paso. Git guarda el
historial de cambios; GitHub aloja el repositorio en la nube y coordina las
contribuciones mediante *Pull Requests* (PR).

## 1. Instala Git

- **Windows:** descarga [git-scm.com](https://git-scm.com/) e instala con las opciones por defecto.
- **macOS:** `brew install git` (o instala Xcode Command Line Tools).
- **Linux:** `sudo apt install git`.

Comprueba: `git --version`.

## 2. Crea una cuenta en GitHub

Regístrate en [github.com](https://github.com/) y configura tu nombre y correo en Git:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@cunef.edu"
```

## 3. Haz un *fork* y clónalo

1. En la página del repositorio, pulsa **Fork** (crea tu copia).
2. Clona tu copia en tu ordenador:

```bash
git clone https://github.com/TU-USUARIO/PrograCompetitivaCUNEF.git
cd PrograCompetitivaCUNEF
```

## 4. Crea una rama

Nunca trabajes directamente en `main`. Crea una rama con un nombre descriptivo:

```bash
git checkout -b anade-segment-tree
```

## 5. Haz tus cambios y guárdalos

Edita los archivos, y luego:

```bash
git add .
git commit -m "Añade Segment Tree con explicación y tests"
```

## 6. Súbelos y abre el Pull Request

```bash
git push -u origin anade-segment-tree
```

GitHub te mostrará un botón para **abrir un Pull Request** hacia `main`. Rellena la
plantilla que aparece.

!!! success "Previsualización automática"
    Al abrir el PR, un robot publicará un comentario con un **enlace a una vista previa**
    de la web con tus cambios (`.../pr-preview/pr-N/`), para que puedas verlos antes de
    que se fusionen.

## 7. Revisión

Alguien revisará tu PR y quizá te pida cambios. Para incorporarlos, repite el paso 5 y
vuelve a hacer `git push`: el PR se actualiza solo.

---

¿Listo? Continúa con [Añadir un algoritmo](add-algorithm.md).
