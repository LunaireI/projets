# Pac-Man (console)

Pac-Man en C, affiché dans le terminal.

## Fichiers
- `main.c` : code source du jeu (grille 31 × 28).
- `main.exe` : exécutable Linux x86-64 déjà compilé (malgré l'extension `.exe`, ce n'est pas un programme Windows).

## Fichier requis : `grillePacman.txt`
Le jeu charge la grille depuis `grillePacman.txt`, **à placer dans le dossier d'où l'on lance le programme**. Ce fichier n'est pas présent dans ce dossier : sans lui, le jeu affiche « Erreur sur le fichier » puis une grille vide.

Format : 31 lignes de 28 caractères. `#` mur, `-` porte de la maison des fantômes, `.` gomme, `O` super-gomme, espace = case vide.

## Compiler et lancer
```bash
gcc -Wall -Wextra -o main main.c
./main
```
Nécessite un terminal POSIX (`termios`, `fcntl`, `clear`).

## Commandes
`z` haut · `s` bas · `q` gauche · `d` droite

## Fonctionnement
- Gommes : +10 points, super-gommes : +50 points, cerise : +100 points.
- Les cerises apparaissent après 70 puis 170 gommes mangées.
- Blinky poursuit Pac-Man ; Inky, Pinky et Clyde sortent de la maison et se déplacent au hasard.
- Les bords gauche/droite sont reliés (tunnel).
- Victoire quand toutes les gommes sont mangées, défaite quand les vies tombent à 0 (`nbLive`, 1 vie actuellement).

## Points d'attention
- `nbLive` est initialisé à 1 alors que le cahier des charges prévoit 3 vies.
- Les super-gommes n'ont aucun effet sur les fantômes (ils ne deviennent pas vulnérables).
- Il n'y a pas de vérification de collision quand Pac-Man et un fantôme se croisent (échange de cases).
- `finDePartie` appelle `printf(message)` sans format (avertissement de compilation).
