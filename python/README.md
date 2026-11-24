# Projets en Python

Python 3.12+ requis (syntaxe `type X = ...` et génériques `def f[T]()`).

| Dossier | Description | Dépendances |
|---|---|---|
| [`snake/`](snake/) | Snake (Pyxel) + serveur web Flask pour les scores | `pyxel`, `flask` |
| [`space_invader/`](space_invader/) | Space Invaders (Pyxel) | `pyxel` |
| [`othello/`](othello/) | Othello (logique de jeu + interface Flet en cours) | `flet` |
| [`demineur/`](demineur/) | Démineur 10×10 | `metagrid` (bibliothèque de cours) |
| [`structures/`](structures/) | Piles, files, listes, arbres binaires, graphes | selon le module |

## Important : lancer depuis ce dossier
Plusieurs modules font `from structures.lineaires import ...`. Il faut donc que `python/` soit dans le chemin d'import, par exemple :
```bash
cd python
PYTHONPATH=. python snake/main.py
python -m doctest -v structures/lineaires/pile.py
```
