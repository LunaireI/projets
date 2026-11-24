# Structures linéaires

| Module | Structure | Fonctions |
|---|---|---|
| `pile.py` | Pile (liste Python) | `creer`, `est_vide`, `empiler`, `depiler` |
| `file.py` | File (`collections.deque`) | `creer`, `enfiler`, `defiler`, `est_vide`, `taille_file`, `nb_elements`, `renverser`, `sortie` |
| `file_de_pile.py` | File construite avec deux piles | `creer`, `enfiler`, `defiler`, `est_vide`, `contient` |
| `liste_mutable.py` | Liste chaînée avec sentinelle | `Liste.add_tete`, `Liste.est_vide`, `Liste.longueur` |

## Exemple

```python
from structures.lineaires import file

f = file.creer()
file.enfiler("a", f)
file.enfiler("b", f)
file.defiler(f)        # 'a' : premier arrivé, premier sorti
```

`defiler` sur une structure vide lève une `AssertionError`. La file de `file_de_pile.py` est celle utilisée par le [Snake](../../snake/) pour stocker le serpent.
