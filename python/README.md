# Projets Python

Nécessite Python 3.12 ou plus récent.

| Dossier | Description | Bibliothèques |
|---|---|---|
| [`snake/`](snake/) | Snake et serveur de scores | `pyxel`, `flask` |
| [`space_invader/`](space_invader/) | Space Invaders | `pyxel` |
| [`othello/`](othello/) | Othello | `flet` |
| [`demineur/`](demineur/) | Démineur | `metagrid` |
| [`structures/`](structures/) | Structures de données | `graphviz` (dessin de graphes) |

## Installation

```bash
pip install pyxel flask flet graphviz
```

## Lancement

Certains modules importent le paquet `structures`. Pour qu'il soit trouvé, lancez les commandes depuis ce dossier `python/` avec `PYTHONPATH=.` :

```bash
cd python
PYTHONPATH=. python snake/main.py
```
