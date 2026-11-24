# Templates Jinja2

| Fichier | Rôle |
|---|---|
| `base.j2` | Gabarit de base (blocs `title` et `content`) |
| `snakeHome.j2.html` | Page d'accueil : saisie du pseudo |
| `snakeHomeAfter.j2` | Variante après connexion : affiche les scores via `fetch('/scores')` |

Les pages héritent de `base.J2` (avec un `J` majuscule) alors que le fichier est `base.j2` : à corriger pour Linux.
`snakeHome.j2.html` est le template effectivement utilisé par `appli.py` ; `snakeHomeAfter.j2` n'est référencé nulle part pour l'instant. Le template `snake.html`, demandé par la route `/snake/`, est absent.
