# Space Invaders

Space Invaders avec [Pyxel](https://github.com/kitao/pyxel) (fenêtre 120×120, 60 fps).

## Fichiers
- `main.py` : le jeu.
- `2.pyxres` : ressources Pyxel (sprites), chargées au démarrage. Doit rester à côté de `main.py`.

## Lancer
```bash
pip install pyxel
cd python/space_invader
python main.py
```

## Commandes
← / → déplacer le vaisseau · Espace tirer

## Fonctionnement
- 7 niveaux d'ennemis : standard (1 PV), boosted (2 PV), boss (5 PV).
- Chaque ennemi tué rapporte son niveau en points ; 1 chance sur 10 de lâcher un bonus d'invisibilité (durée 600 frames).
- Les ennemis tirent toutes les 15 frames, avec une probabilité qui augmente avec le niveau.
- Défaite si un missile touche le vaisseau ; victoire après le dernier niveau.

## Points d'attention
- Plusieurs listes sont modifiées pendant qu'on les parcourt (`remove` dans un `for`) : possibles ratés de collision ou de suppression de bonus.
- Dans `Game.__init__`, `ennemies_level[level]` est la liste partagée : après un game over, les ennemis tués ne reviennent pas (la liste est réutilisée telle quelle).
- Seul le bonus « invisible » est implémenté (`auto-shot`, `super-shot`, `damage_multiplicateur` sont déclarés mais inactifs).
