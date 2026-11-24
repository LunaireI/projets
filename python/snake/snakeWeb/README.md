# snakeWeb — serveur de scores

Petite application web Flask pour saisir un pseudo, consulter le tableau des scores et enregistrer de nouveaux scores du Snake.

## Lancer le serveur

```bash
pip install flask
cd python/snake/snakeWeb
cp ../scores.json .      # le serveur lit scores.json dans le dossier courant
python appli.py
```

Le site est alors disponible sur <http://localhost:5500>.

## Pages et routes

| Route | Description |
|---|---|
| `/` | Page d'accueil (saisie du pseudo) |
| `/snake/?pseudo=Nom` | Page du joueur ; mémorise le pseudo dans `current_player.json` |
| `/scores` | Tous les scores au format JSON |
| `/scores/download_scores` | Téléchargement de `scores.json` |
| `/snake/add_score?pseudo=Nom&score=10&timer=123` | Ajoute ou met à jour le score d'un joueur |
| `/snake/clear_scores` | Supprime tous les scores |

## Fichiers

- `appli.py` : application Flask.
- [`templates/`](templates/) : pages HTML (Jinja2).
