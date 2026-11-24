# Othello

Logique complète d'un jeu d'Othello 8×8 (`BLANC = 1`, `NOIR = 2`) et début d'une interface graphique avec [Flet](https://flet.dev).

## Lancer
```bash
pip install flet
cd python/othello
python main.py
```
L'interface Flet affiche pour l'instant seulement le plateau en texte et un champ de saisie sans action réelle. La partie jouable à deux est la fonction `partie2j()` (saisie `xy` au clavier), qui n'est pas appelée depuis `main`.

## Fonctions principales
`creer_grille`, `peut_jouer`, `coups_possibles`, `jouer_coup`, `get_score`, `is_game_over`, `show`, `partie2j`.

## Points d'attention
- `jouer_coup` retourne tous les pions adverses alignés, même quand ils ne sont pas encadrés par un pion du joueur (testé : un coup illégal retourne quand même la ligne). Il faut ne retourner que si la ligne se termine par un pion du joueur.
- `show` renvoie une chaîne mais `partie2j` ne l'affiche pas (il manque un `print`).
- Le passage de tour quand un joueur n'a aucun coup n'est pas géré.
- `minimax()`, `poser_pion()` et `scorepoint` (tableau incomplet, 4 lignes sur 8) sont des ébauches.
