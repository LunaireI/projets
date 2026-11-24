# Arbres binaires

`arbrebin.py` représente un arbre binaire par un tuple `(clé, sous-arbre gauche, sous-arbre droit)` ; l'arbre vide est `()`.

## Fonctions

| Catégorie | Fonctions |
|---|---|
| Construction | `creer`, `creer_feuille`, `exemple`, constante `ARBRE_VIDE` |
| Accès | `cle`, `sag`, `sad`, `est_vide` |
| Mesures | `taille`, `hauteur`, `minimum` |
| Comparaison | `egaux`, `sont_miroirs`, `est_symetrique`, `est_equilibre` |
| Arbre binaire de recherche | `recherche_abr`, `insert_abr`, `min_abr`, `max_abr`, `parcours_infixe` |

## Exemple

```python
from structures.hierarchiques import arbrebin as ab

a = ab.exemple()
ab.taille(a)       # 10
ab.hauteur(a)      # 4
ab.parcours_infixe(a)
```

`exemple()` construit l'arbre suivant :

```
            21
          /    \
        14      28
       /  \    /  \
     11   18  25   32
    /    /  \
   9   15   19
```
