# Pac-Man

Version console de Pac-Man : traversez le labyrinthe, mangez toutes les gommes et évitez les quatre fantômes.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `main.c` | Code source du jeu |
| `grillePacman.txt` | Plan du labyrinthe (31 lignes × 28 colonnes) |
| `main.exe` | Exécutable Linux x86-64 déjà compilé |

## Lancer le jeu

Le programme lit `grillePacman.txt` dans le dossier courant : lancez-le depuis ce dossier.

```bash
cd C/pacman
gcc -o main main.c
./main
```

## Commandes

| Touche | Action |
|---|---|
| `z` | Haut |
| `s` | Bas |
| `q` | Gauche |
| `d` | Droite |

## Règles

- **Objectif** : manger toutes les gommes pour gagner. Toucher un fantôme fait perdre une vie.
- **Score** : gomme `.` = 10 points, super-gomme `O` = 50 points, cerise = 100 points.
- **Cerises** : une cerise apparaît au centre après 70 gommes mangées, puis une seconde après 170.
- **Fantômes** : Blinky (`B`) poursuit Pac-Man ; Inky (`I`), Pinky (`P`) et Clyde (`C`) sortent de leur maison et errent au hasard.
- **Tunnel** : les sorties sur les côtés de la ligne centrale relient la gauche et la droite du labyrinthe.

## Légende de l'écran

| Symbole | Élément |
|---|---|
| `G` | Pac-Man |
| `B` `I` `P` `C` | Fantômes |
| `#` | Mur |
| `-` | Porte de la maison des fantômes |
| `.` | Gomme |
| `O` | Super-gomme |
| `c` | Cerise |

## Modifier le labyrinthe

Éditez `grillePacman.txt` en conservant exactement 31 lignes de 28 caractères, avec les symboles de la légende.
