# Démineur

Démineur 10×10 avec 10 mines, affiché grâce à la bibliothèque `metagrid` (bibliothèque fournie en cours, non incluse ici).

## Lancer
```bash
cd python/demineur
python main.py
```

## Commandes
Clic gauche : révéler une case · Clic droit : poser/retirer un drapeau.

## Fonctionnement
- Placement aléatoire des mines, calcul du nombre de voisins miné pour chaque case.
- Une case à 0 voisin révèle récursivement ses voisines.
- Défaite : toutes les mines sont révélées. Victoire : toutes les cases sans mine sont révélées.

## Points d'attention
- Le message « WIN » s'affiche aussi en cas de défaite (condition `est_gagne() or game_over`).
- La première case cliquée peut être une mine.
