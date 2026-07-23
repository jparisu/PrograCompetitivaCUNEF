# Contributing

Thanks for helping improve **Programación Competitiva CUNEF**! Contributions from
students and faculty are very welcome — code, fixes, explanations, or just ideas.

📖 **Full step-by-step guide (Spanish):**
<https://jparisu.github.io/PrograCompetitivaCUNEF/contributing/>

## Quick links

- 🐛 Report a bug or typo → [new issue](https://github.com/jparisu/PrograCompetitivaCUNEF/issues/new/choose)
- 💡 Suggest or discuss an idea → [Discussions](https://github.com/jparisu/PrograCompetitivaCUNEF/discussions)
- 🔀 Open a pull request → [compare](https://github.com/jparisu/PrograCompetitivaCUNEF/compare)

## In short

- Each algorithm is **one folder** under `docs/algorithms/<topic>/<algorithm>/`.
- Write the hand-written `full` code (C++ **and** Python) and fill `meta.yaml`; the
  `clean`/`contest` versions, tests, tables and graph are generated.
- Before opening a PR:

  ```bash
  pip install -r tools/requirements.txt
  python tools/gen.py generate   # create/update derived files
  python tools/gen.py status     # must say "up to date"
  ```

See the online guide for the complete walkthrough (Git basics, adding an algorithm,
images/gifs, and the project scripts).
