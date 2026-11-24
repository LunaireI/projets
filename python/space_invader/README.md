# Space Invaders

Défendez-vous contre des vagues d'envahisseurs de plus en plus résistantes. Jeu réalisé avec [Pyxel](https://github.com/kitao/pyxel).

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `main.py` | Le jeu |
| `2.pyxres` | Sprites du jeu (à garder à côté de `main.py`) |

## Lancer le jeu

```bash
pip install pyxel
cd python/space_invader
python main.py
```

## Commandes

| Touche | Action |
|---|---|
| ← / → | Déplacer le vaisseau |
| Espace | Tirer |

## Règles

- **7 niveaux** : on passe au suivant en détruisant tous les ennemis ; la partie est gagnée après le dernier.
- **Ennemis** :

  | Type | Points de vie | Points gagnés |
  |---|---|---|
  | Standard | 1 | 1 |
  | Boosted | 2 | 2 |
  | Boss | 5 | 3 |

  Une barre de vie s'affiche au-dessus de chaque ennemi.
- **Tirs ennemis** : plus fréquents à mesure que le niveau augmente. Un missile qui touche le vaisseau termine la partie.
- **Missiles** : un tir peut détruire un missile ennemi (sauf ceux des boss).
- **Bonus** : un ennemi détruit laisse tomber, une fois sur dix, un bonus d'invisibilité de 10 secondes environ ; ramassez-le pour absorber les tirs.
- Le score est affiché en haut à gauche.
