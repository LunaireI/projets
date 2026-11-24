# Démineur

Démineur sur une grille de 10 × 10 contenant 10 mines.

## Lancer

```bash
cd python/demineur
python main.py
```

Le jeu utilise la bibliothèque `metagrid` pour l'affichage de la grille.

## Commandes

| Action | Effet |
|---|---|
| Clic gauche | Révéler une case |
| Clic droit | Poser ou retirer un drapeau (`F`) |

## Règles

- Un chiffre indique combien de mines se trouvent dans les 8 cases voisines.
- Une case sans mine voisine révèle automatiquement ses voisines.
- Cliquer sur une mine termine la partie et dévoile toutes les mines.
- Vous gagnez en révélant toutes les cases qui ne contiennent pas de mine.

## Réglages

Dans `main.py` : `HAUTEUR`, `LARGEUR` (taille de la grille) et `NB_MINES`.
