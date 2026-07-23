# PrograCompetitivaCUNEF

Repositorio con código, explicaciones, chuletarios y ejercicios de la Universidad CUNEF
para programación competitiva (C++ y Python), orientado a concursos tipo ICPC.

La documentación se construye con **MkDocs (Material)** y se publica en **GitHub Pages**.

## Documentación online

<https://jparisu.github.io/PrograCompetitivaCUNEF/>


## Ver la documentación en local (sin hacer push)

Puedes previsualizar toda la web en tu ordenador. Necesitas Python 3.11+.

```bash
# 1. Crea y activa un entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instala las dependencias
pip install -r requirements.txt          # web (MkDocs Material, i18n)
pip install -r tools/requirements.txt    # scripts (opcional)

# 3. Arranca el servidor de desarrollo
mkdocs serve
```

Abre <http://127.0.0.1:8000> en el navegador. La página **se recarga sola** cada vez que
guardas un cambio en `docs/`.

Para comprobar que la web se construye igual que en CI (falla si hay enlaces rotos):

```bash
mkdocs build --strict
```

## Regenerar los ficheros derivados

Las versiones `clean`/`contest` del código, los tests y la tabla resumen se generan
automáticamente desde los `meta.yaml`:

```bash
python tools/gen.py generate     # crea/actualiza lo derivado
python tools/gen.py status       # comprueba que está al día (lo usa la CI)
```

Consulta la sección **Contribuir** de la documentación para el detalle de cada script.
