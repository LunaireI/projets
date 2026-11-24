# Snake

Snake réalisé avec [Pyxel](https://github.com/kitao/pyxel), avec un petit serveur Flask pour partager les scores.

## Fichiers
- `main.py` : le jeu (flèches pour se diriger). Utilise la file de `structures/lineaires/file_de_pile.py` pour stocker le serpent.
- `scores.json` : scores enregistrés (`name`, `score`, `timer`).
- `snakeWeb/` : application web Flask (voir son README).

## Lancer
```bash
pip install pyxel flask
cd python
PYTHONPATH=. python snake/main.py
```

## Points d'attention (le jeu ne démarre pas en l'état)
- `main.py` ligne 117 : `json.dump(call_web_service(), "scores.json", indent=4)` s'exécute à l'import. `call_web_service()` est une coroutine jamais attendue et `"scores.json"` est un nom, pas un fichier ouvert : `TypeError: Object of type coroutine is not JSON serializable`. Cette ligne doit être supprimée ou commentée.
- `update()` appelle `game_over()` (Échap / Espace) alors que `game_over` est un booléen : `TypeError`. La fonction à appeler est `game_over_fc()`.
- `STEP_FRAMES` n'est pas utilisé : le serpent avance à chaque frame (10 fps).
- L'envoi du score au serveur (`requests.post`) est commenté ; l'URL est sans `http://`.
