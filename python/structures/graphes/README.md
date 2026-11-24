# Graphes

| Fichier | Description |
|---|---|
| `graphe_no.py` | Graphe non orienté pondéré, en listes d'adjacence (`dict[str, dict[str, poids]]`) |
| `dessin.py` | Génère une image PNG d'un graphe avec Graphviz |

## `graphe_no.py`
Création et accès : `creer`, `sommets`, `nb_sommets`, `nb_arretes`, `poids`, `get_voisins`, `ajouter_sommet`, `set_arete`. Conversion avec matrice d'adjacence : `get_matrice_adjacence`, `from_matrice_adjacence`. Parcours : `predecesseurs_bfs`, `shortest_path`, `distance` (BFS, nombre d'arêtes).
```bash
cd python
python -m doctest structures/graphes/graphe_no.py
```
Résultat actuel : 37 doctests sur 39 passent.

## `dessin.py`
Nécessite `pip install graphviz` et le programme Graphviz installé sur le système.

## Points d'attention
- `sommets()` renvoie `g.keys()` (un `dict_keys`) au lieu d'une liste : c'est la cause des 2 doctests en échec (`sommets`, `ajouter_sommet`). Corriger avec `list(g.keys())`.
- `nb_arretes` compte chaque arête deux fois (une par extrémité) ; il faut diviser par 2.
- `get_voisins` plante avec une assertion sur un sommet isolé (dictionnaire de voisins vide).
- `shortest_path` boucle ou plante (`KeyError`) si `s2` n'est pas atteignable depuis `s1`.
- `dessin.py` importe `graphe_oriente`, module absent du dossier, et appelle `graphe_no.matrice`, fonction qui n'existe pas (c'est `get_matrice_adjacence`) : le dessin ne fonctionne pas en l'état.
