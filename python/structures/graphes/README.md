# Graphes

| Module | Rôle |
|---|---|
| `graphe_no.py` | Graphe non orienté pondéré |
| `dessin.py` | Export d'un graphe en image PNG |

## Représentation

Un graphe est un dictionnaire de listes d'adjacence : `g[s1][s2]` est le poids de l'arête entre `s1` et `s2`.

```python
{'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
```

## Fonctions de `graphe_no.py`

| Catégorie | Fonctions |
|---|---|
| Construction | `creer`, `ajouter_sommet`, `set_arete`, `graphe_exemple` |
| Consultation | `sommets`, `nb_sommets`, `nb_arretes`, `poids`, `get_voisins` |
| Matrice d'adjacence | `get_matrice_adjacence`, `from_matrice_adjacence` |
| Parcours | `predecesseurs_bfs`, `shortest_path`, `distance` |

## Exemple

```python
from structures.graphes import graphe_no as gr

g = gr.creer()
gr.set_arete("A", "B", g)
gr.set_arete("B", "C", g)
gr.shortest_path(g, "A", "C")   # ['A', 'B', 'C']
gr.distance(g, "A", "C")        # 2
```

## Dessiner un graphe

`dessin.py` utilise [Graphviz](https://graphviz.org) : installez le programme sur votre système puis `pip install graphviz`.
