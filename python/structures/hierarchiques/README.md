# Arbres binaires

`arbrebin.py` : arbre binaire représenté par un tuple `(clé, sag, sad)`, l'arbre vide étant `()`.

## Fonctions
- Primitives : `cle`, `sag`, `sad`, `creer`, `creer_feuille`, `est_vide`, `exemple`.
- Lecture : `taille`, `hauteur`, `egaux`, `est_equilibre`, `sont_miroirs`, `est_symetrique`, `minimum`, `parcours_infixe`.
- Arbres binaires de recherche : `recherche_abr`, `insert_abr`, `min_abr`, `max_abr`.

## Tests
```bash
cd python
python -m doctest structures/hierarchiques/arbrebin.py
```
Le module importe `tkinter`, `geopandas` et `requests` en tête de fichier alors qu'ils ne sont pas utilisés ; ils doivent être installés (ou ces imports retirés) pour que le module se charge. Avec ces imports neutralisés : 48 doctests sur 49 passent.

## Points d'attention
- `est_feuille` est utilisée (doctest de `creer_feuille` et `minimum`) mais n'est pas définie : `NameError`. C'est l'unique doctest en échec, et `minimum` plante sur toute feuille.
- `recherche_abr` teste `cle(sag(a)) < e` : lève une `AssertionError` dès que le sous-arbre gauche est vide. La comparaison doit se faire avec `cle(a)`.
- `insert_abr` crée la feuille avec `creer(a, ...)` au lieu de `creer(e, ...)` : le nœud inséré contient l'arbre vide au lieu de la valeur.
- `egaux` compare `sag(a1) == sag(a2)` avec l'opérateur Python au lieu de s'appeler récursivement (fonctionne car ce sont des tuples).
- `est_symetrique(exemple())` renvoie `False` : normal, l'arbre exemple n'est pas symétrique.
- Les parcours en largeur sont commentés.
