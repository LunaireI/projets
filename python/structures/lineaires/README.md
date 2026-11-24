# Structures linéaires

| Fichier | Description |
|---|---|
| `pile.py` | Pile (`list`) : `creer`, `est_vide`, `empiler`, `depiler` |
| `file.py` | File (`collections.deque`) : `creer`, `enfiler`, `defiler`, `est_vide`, plus des exercices (`sortie`, `renverser`, `taille_file`, `nb_elements`) |
| `file_de_pile.py` | File implémentée avec deux piles (`creer`, `enfiler`, `defiler`, `est_vide`, `contient`). Utilisée par le Snake |
| `liste_mutable.py` | Liste chaînée circulaire avec sentinelle (`add_tete`, `est_vide`, `longueur`) |

## Tests
`pile.py` et `file.py` ont des doctests, qui passent tous (18 et 29 exemples) :
```bash
cd python
python -m doctest structures/lineaires/pile.py
python -m doctest structures/lineaires/file.py
```

## Points d'attention
- `file.py` : `enfiler` ajoute à gauche et `defiler` retire à droite ; la file affichée dans les doctests est donc dans l'ordre inverse de l'arrivée.
- `liste_mutable.py` : le paramètre `__taille` est mis à jour mais jamais utilisé, `longueur()` recalcule la taille. `Liste` hérite de `Maillon` pour jouer le rôle de sentinelle.
- `file_de_pile.py` : pas de doctests ; ses fonctions n'ont pas de documentation.
