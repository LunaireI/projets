# Snake

Le jeu classique du serpent, réalisé avec [Pyxel](https://github.com/kitao/pyxel). Un serveur web Flask (dossier `snakeWeb/`) permet de consulter et d'enregistrer les scores.

## Contenu du dossier

| Élément | Rôle |
|---|---|
| `main.py` | Le jeu |
| `scores.json` | Scores enregistrés (nom, score, durée) |
| [`snakeWeb/`](snakeWeb/) | Serveur web des scores |

## Lancer le jeu

```bash
pip install pyxel
cd python
PYTHONPATH=. python snake/main.py
```

## Commandes

| Touche | Action |
|---|---|
| ← ↑ ↓ → | Diriger le serpent |
| Échap / Espace | Terminer la partie |

## Règles

- Le serpent grandit d'une case à chaque pomme rouge mangée (+1 point).
- La partie se termine si le serpent touche un mur ou son propre corps, puis une nouvelle partie démarre.
- La barre du haut affiche le score en cours, le dernier score et le meilleur score.
- Fenêtre de 200 × 200 pixels, grille de cases de 10 pixels.

## Scores

Le pseudo du joueur est lu dans `current_player.json` (créé par le serveur web). Les scores sont stockés dans `scores.json` au format :

```json
[{ "name": "serveur", "score": 31, "timer": 0 }]
```
