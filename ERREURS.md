# Erreurs et points à corriger

Relevé établi par lecture du code et par exécution (compilation, doctests, tests des routes Flask avec le client de test). Les jeux Pyxel, Flet et metagrid n'ont pas pu être lancés graphiquement.

Gravité : 🔴 bloquant · 🟠 comportement incorrect · 🟡 mineur

## Snake — `python/snake/main.py`

- 🔴 **Plantage au lancement** (ligne 117) : `json.dump(call_web_service(), "scores.json", indent=4)` s'exécute à l'import. `call_web_service()` est une coroutine jamais attendue et `"scores.json"` est une chaîne, pas un fichier. Résultat : `TypeError: Object of type coroutine is not JSON serializable`. → Supprimer ou commenter la ligne.
- 🔴 **Échap / Espace** (fonction `update`) : appelle `game_over()` alors que `game_over` est un booléen → `TypeError`. → Appeler `game_over_fc()`.
- 🟠 `STEP_FRAMES` n'est jamais utilisé : le serpent avance à chaque frame.
- 🟠 L'envoi du score (`requests.post`) est commenté, et l'URL `localhost:5500/...` n'a pas de `http://`.
- 🟡 Variable `timer` calculée dans `game_over_fc` mais inutilisée ; `sauvegarder_score` cherche toujours le nom `"serveur"` au lieu de `nom_joueur`.

## Serveur web — `python/snake/snakeWeb/`

- 🔴 **`/` renvoie 500 sous Linux** : `{% extends "base.J2" %}` mais le fichier est `base.j2` (la casse compte sous Linux, pas sous Windows/macOS).
- 🔴 **`/snake/` renvoie 500** : le template `snake.html` n'existe pas.
- 🟠 Le jeu appelle `/snake/scores`, route inexistante (la route est `/scores`).
- 🟠 `snakeHomeAfter.j2` n'est utilisé par aucune route.
- 🟡 `/snake/clear_scores` efface tous les scores par simple GET, sans protection.
- 🟡 `timer` est enregistré sous forme de chaîne (`request.args.get`) alors que `scores.json` contient un entier.
- 🟡 Les fichiers `scores.json` et `current_player.json` sont lus dans le dossier courant : le serveur et le jeu ne partagent pas le même fichier s'ils sont lancés depuis des dossiers différents.

## Pac-Man — `C/pacman/main.c`

Le jeu se compile et se lance correctement avec `grillePacman.txt`.

- 🟠 `nbLive` vaut 1 : le cahier des charges prévoit 3 vies.
- 🟠 Les super-gommes (`O`) n'ont aucun effet sur les fantômes (pas de mode vulnérable).
- 🟠 Pas de détection quand Pac-Man et un fantôme échangent leurs cases en se croisant.
- 🟡 `printf(message)` dans `finDePartie` sans format (avertissement `-Wformat-security`).
- 🟡 `main.exe` est un binaire Linux malgré son extension ; il peut devenir obsolète par rapport à `main.c`.

## Space Invaders — `python/space_invader/main.py`

- 🟠 Des listes sont modifiées pendant leur parcours (`remove` dans un `for`) : collisions ou suppressions de bonus parfois ratées.
- 🟠 Après un game over, `ennemies_level` est une liste partagée : les ennemis déjà tués ne reviennent pas à la nouvelle partie.
- 🟡 Seul le bonus « invisible » est implémenté (`auto-shot`, `super-shot`, `damage_multiplicateur` sont déclarés mais inactifs).
- 🟡 Pas d'écran de fin visible : en cas de victoire ou de défaite, seul un `print` est émis.

## Othello — `python/othello/main.py`

- 🔴 `jouer_coup` retourne tous les pions adverses alignés **même s'ils ne sont pas encadrés** par un pion du joueur (un coup illégal retourne quand même la ligne).
- 🟠 Le passage de tour n'est pas géré quand un joueur n'a aucun coup possible.
- 🟠 `partie2j` ne fait jamais `print(show(...))` : le plateau n'est pas affiché.
- 🟠 L'interface Flet est inachevée : le bouton ne joue aucun coup et `partie2j` n'est pas appelée depuis `main`.
- 🟡 `minimax()`, `poser_pion()` et `scorepoint` (4 lignes sur 8) sont des ébauches non utilisées.

## Démineur — `python/demineur/main.py`

- 🟠 Le message « WIN » s'affiche aussi en cas de défaite (condition `est_gagne() or game_over`).
- 🟡 La première case cliquée peut être une mine.

## Arbres binaires — `python/structures/hierarchiques/arbrebin.py`

- 🔴 `est_feuille` est utilisée mais jamais définie (`NameError`) : fait échouer un doctest (48 sur 49 passent) et fait planter `minimum` dès qu'il rencontre une feuille.
- 🔴 `recherche_abr` teste `cle(sag(a)) < e` : `AssertionError` dès que le sous-arbre gauche est vide. Il faut comparer `cle(a)` à `e`.
- 🔴 `insert_abr` crée le nœud avec `creer(a, ...)` au lieu de `creer(e, ...)` : l'arbre est inséré à la place de la valeur.
- 🟠 Le module importe `tkinter`, `geopandas` et `requests.models` sans les utiliser : il ne se charge pas si l'un d'eux est absent.
- 🟡 `egaux` compare les sous-arbres avec `==` au lieu de s'appeler récursivement.

## Graphes — `python/structures/graphes/`

- 🟠 `sommets()` renvoie `g.keys()` (un `dict_keys`) au lieu d'une liste : 2 doctests en échec sur 39 (`sommets`, `ajouter_sommet`). → `list(g.keys())`.
- 🟠 `nb_arretes` compte chaque arête deux fois (une par extrémité).
- 🟠 `get_voisins` lève une `AssertionError` pour un sommet sans voisin.
- 🟠 `shortest_path` / `distance` : `KeyError` si les deux sommets ne sont pas connectés.
- 🔴 `dessin.py` importe `graphe_oriente`, module absent du dossier, et appelle `graphe_no.matrice`, fonction qui n'existe pas (c'est `get_matrice_adjacence`).

## Structures linéaires — `python/structures/lineaires/`

Aucune erreur trouvée sur `pile.py` et `file.py` (tous les doctests passent) ni sur `file_de_pile.py`.

- 🟡 `liste_mutable.py` : l'attribut `__taille` est mis à jour mais jamais lu.
- 🟡 `file_de_pile.py` n'a ni docstrings ni doctests.
