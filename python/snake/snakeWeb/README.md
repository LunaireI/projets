# snakeWeb — serveur web des scores

Application Flask (`appli.py`) qui sert une page d'accueil et gère `scores.json`.

## Lancer
```bash
pip install flask
cd python/snake/snakeWeb
python appli.py        # http://localhost:5500
```
Les fichiers `scores.json` et `current_player.json` sont lus/écrits dans le dossier courant : lancer depuis un dossier contenant `scores.json` (copier celui de `snake/`).

## Routes
| Route | Rôle |
|---|---|
| `/` | page d'accueil (`snakeHome.j2.html`) |
| `/snake/?pseudo=X` | page du joueur (mémorise le pseudo dans `current_player.json`) |
| `/scores` | liste des scores en JSON |
| `/scores/download_scores` | téléchargement de `scores.json` |
| `/snake/add_score?pseudo=X&score=N&timer=T` | ajoute ou met à jour un score |
| `/snake/clear_scores` | vide tous les scores |

## Points d'attention (testés avec le client de test Flask)
- `/` renvoie une erreur 500 sous Linux : les templates font `{% extends "base.J2" %}` mais le fichier s'appelle `base.j2` (majuscule/minuscule). Ça passe sous Windows/macOS, pas sous Linux.
- `/snake/` renvoie une erreur 500 : le template `snake.html` n'existe pas dans `templates/`.
- Le jeu pointe vers `/snake/scores`, route qui n'existe pas (la route est `/scores`).
- `/snake/clear_scores` efface les scores via un simple GET, sans protection.
