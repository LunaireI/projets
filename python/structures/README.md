# Structures de données

Bibliothèque de structures de données en Python.

| Dossier | Contenu |
|---|---|
| [`lineaires/`](lineaires/) | Pile, file, file à deux piles, liste chaînée |
| [`hierarchiques/`](hierarchiques/) | Arbres binaires et arbres binaires de recherche |
| [`graphes/`](graphes/) | Graphes non orientés pondérés, parcours en largeur, dessin |

## Utilisation

Importez les modules depuis le dossier `python/` :

```python
from structures.lineaires import pile
from structures.graphes import graphe_no

p = pile.creer()
pile.empiler(1, p)
```

Chaque module est écrit en style fonctionnel : les fonctions prennent la structure en paramètre (`pile.empiler(e, p)`). Les exemples des docstrings peuvent être exécutés :

```bash
cd python
python -m doctest -v structures/lineaires/pile.py
```
