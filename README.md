# Projets

Recueil de petits jeux et de bibliothèques de structures de données, en Python et en C.

## Sommaire

| Projet | Langage | Description |
|---|---|---|
| [Pac-Man](C/pacman/) | C | Pac-Man jouable dans le terminal |
| [Snake](python/snake/) | Python | Snake avec tableau des scores en ligne (Flask) |
| [Space Invaders](python/space_invader/) | Python | Shoot'em up à niveaux avec ennemis et boss |
| [Othello](python/othello/) | Python | Jeu d'Othello 8×8 |
| [Démineur](python/demineur/) | Python | Démineur 10×10 |
| [Structures](python/structures/) | Python | Piles, files, listes, arbres binaires, graphes |

## Prérequis

- **C** : `gcc` et un terminal Linux/macOS.
- **Python** : version 3.12 ou plus récente.
- Bibliothèques Python selon le projet (précisées dans chaque README) : `pyxel`, `flask`, `flet`, `graphviz`.

## Organisation

```
projets/
├── C/
│   └── pacman/
└── python/
    ├── snake/ (+ snakeWeb/)
    ├── space_invader/
    ├── othello/
    ├── demineur/
    └── structures/ (lineaires, hierarchiques, graphes)
```

Chaque dossier contient son propre README avec les instructions de lancement.
Les problèmes connus sont listés dans [`ERREURS.md`](ERREURS.md).
