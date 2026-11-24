# Structures de données

| Dossier | Contenu |
|---|---|
| [`lineaires/`](lineaires/) | Pile, file, file à deux piles, liste chaînée |
| [`hierarchiques/`](hierarchiques/) | Arbres binaires |
| [`graphes/`](graphes/) | Graphes non orientés pondérés + dessin |

Les modules s'importent comme `from structures.lineaires import pile` : travailler depuis le dossier `python/` (ou ajouter `python/` au `PYTHONPATH`). Les fonctions sont documentées avec des doctests :
```bash
cd python
python -m doctest -v structures/lineaires/pile.py
```
