#structures/graphes/graphe_no.py

"""
Graphe non orienté pondéré

Choix d'implémentation : liste d'adjacence
-------------------------------------------
Un graphe est représenté par un dict[str, dict[str, Poids]] où :
- les clés du dict externe sont les sommets
- g[s1][s2] = poids de l'arête entre s1 et s2
  (absence de clé signifie absence d'arête)

Avantages :
- Espace mémoire O(n + m) avec m = nombre d'arêtes (efficace pour les graphes creux)
- Ajouter un sommet est O(1)
- Accès aux voisins en O(deg(s))

Inconvénients :
- Pas d'ordre naturel sur les sommets (ordre d'insertion des clés)
- index_sommet nécessite de convertir les clés en liste : O(n)

Alternative non retenue ici : matrice d'adjacence (list[list[Poids]])
  → accès au poids en O(1) via index, mais espace O(n²) même si le graphe est creux
"""

# from ..lineaires import file
from structures.lineaires import file

type Poids = int|float

type Graphe = dict[str, dict[str, Poids]]

type MatriceAdj =  list[list[Poids|None]]

# ! FONCTIONS DE CREATION ET D'ACCES AUX ELEMENTS DU GRAPHE

def creer() -> Graphe: # pragma: no coverage
    """Retourne un graphe vide (aucun sommet, aucune arête)"""
    return {}


def sommets(g: Graphe) -> list[str]:
    """Retourne la liste des sommets du graphe g.

    >>> g = {'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
    >>> sommets(g)
    ['A', 'B', 'C']
    """
    return g.keys()

def nb_sommets(g: Graphe) -> int:
    """renvoie le nombre de sommets de g

    >>> g = {'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
    >>> nb_sommets(g)
    3
    """
    return len(sommets(g))

def nb_arretes(g: Graphe) -> int:
    res = 0
    for s in g:
        for v in get_voisins(s, g):
            res += 1
    return res           

def poids(s1: str, s2: str, g: Graphe) -> Poids:
    """
    Retourne le poids de l'arête entre les sommets s1 et s2 dans le graphe g.

    >>> g = {'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
    >>> poids('A', 'B', g)
    2
    >>> poids('B', 'C', g)
    3
    """
    assert g[s1][s2], f"g[{s1}][{s2}] n'est pas accesible ou n'existe pas"
    return g[s1][s2]

def get_matrice_adjacence(g: Graphe) -> MatriceAdj:
    """Retourne la matrice d'adjacence du graphe g. None indique l'absence d'arête.

    >>> g = {'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
    >>> m = get_matrice_adjacence(g)
    >>> m
    [[None, 2, None], [2, None, 3], [None, 3, None]]
    """
    return [[g[sommet][other_sommet] if other_sommet in g[sommet] else None for other_sommet in g] for sommet in g]

def from_matrice_adjacence(s: list[str], m: MatriceAdj) -> Graphe:
    """Créé un graphe d'après sa liste de sommets insi que sa matrice d'adjacence.
    (liste des sommets, matrice) où None indique l'absence d'arête.

    >>> m = [[None, 2, None], [2, None, 3], [None, 3, None]]
    >>> from_matrice_adjacence(['A', 'B', 'C'], m)
    {'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
    """
    return {s[i]: {s[j]: m[i][j] for j in range(len(m)) if m[i][j]} for i in range(len(s))}
 

def ajouter_sommet(s: str, g: Graphe):
    """Ajoute le sommet s au graphe g (sans arête)

    >>> g = {'A': {'B': 1}, 'B': {'A': 1}}
    >>> ajouter_sommet('C', g)
    >>> sommets(g)
    ['A', 'B', 'C']
    >>> g['C']
    {}
    """
    g[s] = {}


def set_arete(s1: str, s2: str, g: Graphe, poids: Poids = 1):
    """Ajoute ou remplace l'arête s1-s2 dans le graphe g.
    Le poids vaut 1 par défaut

    >>> g = {}
    >>> set_arete('A', 'B', g, 3)
    >>> g
    {'A': {'B': 3}, 'B': {'A': 3}}
    >>> set_arete('B', 'C', g, 2)
    >>> g
    {'A': {'B': 3}, 'B': {'A': 3, 'C': 2}, 'C': {'B': 2}}
    """
    if s1 not in g.keys():
        g[s1] = {}
    if s2 not in g.keys():
        g[s2] = {}
    g[s1][s2] = poids
    g[s2][s1] = poids

def get_voisins(s: str, g: Graphe) -> list[str]:
    """renvoie la liste des voisins du sommet s

    >>> g = {'A': {'B': 2}, 'B': {'A': 2, 'C': 3}, 'C': {'B': 3}}
    >>> get_voisins('A', g)
    ['B']
    >>> get_voisins('B', g)
    ['A', 'C']
    >>> get_voisins('C', g)
    ['B']
    """
    assert g[s], f"g[{s}] n'est pas accesible ou n'existe pas"
    return [k for k in g[s].keys()]

def graphe_exemple() -> Graphe:
    """Retourne un arbre exemple"""
    g = {
    'E': {'F': 1, 'G': 1},
    'F': {'E': 1, 'G': 1},
    'G': {'E': 1, 'F': 1},
    
    'A': {'B': 1, 'C': 1, 'D': 1},
    'B': {'A': 1, 'C': 1, 'D': 1},
    'C': {'A': 1, 'B': 1, 'D': 1},
    'D': {'A': 1, 'B': 1, 'C': 1}
    }
    return g

def predecesseurs_bfs(g: Graphe, s1: str) -> dict[str, str]:
    """
    Retourne le dictionnaire des prédécesseurs d'un parcours en largeur (BFS) 
    depuis le sommet s1. La clé est le sommet visité, la valeur est son parent.
    La racine (s1) a pour parent une chaîne vide "".

    >>> g_ligne = {'A': {'B': 1}, 'B': {'A': 1, 'C': 1}, 'C': {'B': 1}}
    >>> predecesseurs_bfs(g_ligne, 'A')
    {'A': '', 'B': 'A', 'C': 'B'}

    >>> g_etoile = {'A': {'B': 1, 'C': 1}, 'B': {'A': 1}, 'C': {'A': 1}}
    >>> predecesseurs_bfs(g_etoile, 'A')
    {'A': '', 'B': 'A', 'C': 'A'}

    >>> g_isole = {'A': {'B': 1}, 'B': {'A': 1}, 'C': {'D': 1}, 'D': {'C': 1}}
    >>> predecesseurs_bfs(g_isole, 'A')
    {'A': '', 'B': 'A'}
    """
    f = file.creer()
    π = {s1: ""}
    file.enfiler(s1, f)
    while not file.est_vide(f):
        u = file.defiler(f)
        for v in get_voisins(u, g):
            if v not in π:
                π[v] = u 
                file.enfiler(v, f)
    return π

def shortest_path(g: Graphe, s1: str, s2: str) -> list[str]:
    """
    Reconstruit le plus court chemin de s1 à s2 sous forme de liste.

    >>> shortest_path(graphe_exemple(), 'A', 'D')
    ['A', 'D']

    >>> g_long = {'1': {'2': 1}, '2': {'1': 1, '3': 1}, '3': {'2': 1}}
    >>> shortest_path(g_long, '1', '3')
    ['1', '2', '3']

    >>> shortest_path(graphe_exemple(), 'A', 'A')
    ['A']
    """
    pred = predecesseurs_bfs(g, s1)
    path, temp = [], s2
    while temp != s1:
        path.append(temp)
        temp = pred[temp]
    path.append(s1)
    path.reverse()
    return path

def distance(g: Graphe, s1: str, s2: str) -> int:
    """
    Renvoie la longueur du plus court chemin (en nombre d'arêtes) 
    entre s1 et s2 dans le graphe g.

    >>> distance(graphe_exemple(), 'A', 'D')
    1

    >>> distance(graphe_exemple(), 'A', 'A')
    0

    >>> g_ligne = {
    ...     '1': {'2': 1}, 
    ...     '2': {'1': 1, '3': 1}, 
    ...     '3': {'2': 1, '4': 1}, 
    ...     '4': {'3': 1}
    ... }
    >>> distance(g_ligne, '1', '4')
    3
    """
    return len(shortest_path(g, s1, s2))-1

if __name__ == "__main__": # pragma: no coverage
    import doctest
    doctest.testmod()

    # import structures.graphes.dessin as dessin

    g = creer()
    set_arete("A", "B", g)
    set_arete("B", "C", g)
    set_arete("C", "D", g)
    set_arete("D", "E", g)
    set_arete("E", "F", g)
    set_arete("F", "A", g)
    set_arete("A", "C", g)
    set_arete("B", "D", g)
    set_arete("E", "C", g)

    get_matrice_adjacence(g)

    # dessin.genere_image(g)
