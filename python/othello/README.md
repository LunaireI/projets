# Othello

Jeu d'Othello (Reversi) sur plateau 8 × 8 pour deux joueurs.

## Lancer

```bash
pip install flet
cd python/othello
python main.py
```

## Règles

- Chaque joueur pose à tour de rôle un pion de sa couleur (● blanc, ○ noir).
- Un pion doit encadrer, en ligne droite (horizontale, verticale ou diagonale), un ou plusieurs pions adverses : ceux-ci sont retournés.
- Les cases jouables sont repérées par un `.` sur le plateau.
- La partie s'arrête quand aucun joueur ne peut plus jouer ; celui qui a le plus de pions gagne.

## Saisie d'un coup

Un coup s'écrit sous la forme `xy` : numéro de ligne puis numéro de colonne, de 0 à 7. Exemple : `42` désigne la ligne 4, colonne 2.

## Organisation du code

| Fonction | Rôle |
|---|---|
| `creer_grille()` | Plateau de départ |
| `peut_jouer(coup, joueur, grille)` | Teste si un coup est légal |
| `coups_possibles(joueur, grille)` | Liste des coups légaux |
| `jouer_coup(coup, joueur, grille)` | Pose un pion et retourne les pions capturés |
| `get_score(grille)` | Nombre de pions de chaque couleur |
| `is_game_over(grille)` | Détecte la fin de partie |
| `show(joueur, grille)` | Représentation texte du plateau |
| `partie2j()` | Partie à deux joueurs en console |
