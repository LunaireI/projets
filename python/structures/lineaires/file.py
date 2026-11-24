# from package import modules
from structures.lineaires import file, pile
from collections import deque

type File[T] = deque[T]

def creer[T]() -> File[T]:
    """
    Crée une nouvelle file vide.

    >>> f: File[int] = creer()
    >>> f
    deque([])
    """
    return deque()


def enfiler[T](e: T, f: File[T]):
    """
    Ajoute un élément à la file.

    >>> f: File[int] = creer()
    >>> enfiler(1, f)
    >>> enfiler(2, f)
    >>> f
    deque([2, 1])
    """
    f.appendleft(e)

def defiler[T](f: File[T]) -> T:
    """
    Retire et renvoie l'élément au début de la file.
    Lève unne exception si la file est vide.

    >>> f: File[int] = creer()
    >>> enfiler(1, f)
    >>> enfiler(2, f)
    >>> defiler(f)
    1
    >>> defiler(f)
    2
    >>> defiler(f)
    Traceback (most recent call last):
    AssertionError: La file est vide
    """
    assert len(f) != 0, "La file est vide"
    return f.pop()


def est_vide[T](f: File[T]) -> bool:
    """
    Vérifie si la file est vide.

    >>> f: File[int] = creer()
    >>> est_vide(f)
    True
    >>> enfiler(1, f)
    >>> est_vide(f)
    False
    """
    return len(f)==0

def file_exemple() -> file.File[str]:
    """
    Attention à bien enfiler dans le bon sens.
    """
    f: file.File[str] = file.creer()
    for c in ("jaune", "rouge", "jaune", "vert", "rouge"):
        file.enfiler(c, f)
    return f


def sortie[T](f: file.File[T]) -> T:
    """
    >>> f = file_exemple()
    >>> sortie(f)
    'jaune'
    """
    # On défile f, on obtient le résultat à retourner
    res = file.defiler(f)

    # On enfile cet élément ddans la file temporaire
    ftmp: file.File[T] = file.creer()
    file.enfiler(res, ftmp)

    # On transvase tout ce qu'il reste dans f dans la file temporaire
    while not file.est_vide(f):
        file.enfiler(file.defiler(f), ftmp)
    
    # On transvase la file temporaire dans f
    while not file.est_vide(ftmp):
        file.enfiler(file.defiler(ftmp), f)
    return res

def renverser[T](f: file.File[T]):
    """
    La fonction mystère "renverse" les éléments de la file.
    """
    p: pile.Pile[T] = pile.creer()
    # On transvase la file dans une pile
    while not file.est_vide(f):
        pile.empiler(file.defiler(f), p)
    # On transvase la pile dans f
    while not pile.est_vide(p):
        file.enfiler(pile.depiler(p), f)


def taille_file_nuke[T](f: file.File[T]) -> int:
    """
    Ici, on ne se contente pas de défiler, on effectue un calcul en même temps.
    Simplement accumuler 1 dans un compteur.

    >>> F = file_exemple()
    >>> taille_file_nuke(F)
    5
    >>> taille_file_nuke(F)
    0
    """
    cpt = 0
    while not file.est_vide(f):
        file.defiler(f)
        cpt += 1
    return cpt

def taille_file[T](f: file.File[T]) -> int:
    """
    Ici, on effectue l'accumulation en alimentant une file temporaire.
    on transvase ensuite la file temporaire dans la file d'entrée
    >>> F = file_exemple()
    >>> taille_file(F)
    5
    >>> F == file_exemple() #? La file est toujours égale à la file exemple
    True
    """
    cpt = 0
    ftmp: file.File[T] = file.creer()
    while not file.est_vide(f):
        file.enfiler(file.defiler(f), ftmp)
        cpt += 1
    while not file.est_vide(ftmp):
        file.enfiler(file.defiler(ftmp), f)
    return cpt

def nb_elements[T](e: T, f: file.File[T]) -> int:
    """
    La structure globale est la même que pour la fonction précédente,
    sauf qu'on ajoute une condition à l'accumulation.

    >>> F = file_exemple()
    >>> nb_elements("rouge", F)
    2
    >>> F == file_exemple() #? La file est toujours égale à la file exemple
    True
    >>> nb_elements("vert", F)
    1
    >>> nb_elements("violet", F)
    0
    """

    cpt = 0
    ftmp: file.File[T] = file.creer()
    while not file.est_vide(f):
        courant = file.defiler(f)
        file.enfiler(courant, ftmp)
        if courant == e:
            cpt += 1
    while not file.est_vide(ftmp):
        file.enfiler(file.defiler(ftmp), f)
    return cpt

if __name__ == "__main__":
    print("Début des tests")
    import doctest
    doctest.testmod()
    print("Fin des tests. Une absence d'erreur signifie que tous les tests sont bons")
