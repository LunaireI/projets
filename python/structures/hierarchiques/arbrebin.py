# pyright: basic
# uv add geopandas requests

from structures.lineaires import file
from structures.lineaires import pile

from tkinter import Canvas, Tk
from requests.models import Response
import geopandas as gpd
from typing import Protocol, Self


class Comparable(Protocol):
    """
    Interface pour les types comparables.

    Les types comparables doivent implémenter le dunder __lt__. (lower than <)
    """
    def __lt__(self: Self, other: Self, /) -> bool: ...



# Un arbre est vide ou c'est un tuple constitué d'une clé et de 2 arbres, le sag et le sad.
type ArbreBin[T] = tuple[()]|tuple[T, ArbreBin[T], ArbreBin[T]]

ARBRE_VIDE = ()

def cle[T](a: ArbreBin[T]) -> T:
    """
    Retourne la clé (étiquette) de la racine de l'arbre.

    Précondition : l'arbre ne doit pas être vide.

    >>> a = creer_feuille(42)
    >>> cle(a)
    42
    >>> b = creer(10, creer_feuille(5), creer_feuille(15))
    >>> cle(b)
    10
    """
    assert len(a)==3, "L'arbre est vide"
    return a[0]


def sag[T](a: ArbreBin[T]) -> ArbreBin[T]:
    """
    Retourne le sous-arbre gauche de l'arbre.

    Précondition : l'arbre ne doit pas être vide.

    >>> a = creer(10, creer_feuille(5), creer_feuille(15))
    >>> cle(sag(a))
    5
    >>> est_vide(sag(creer_feuille(42)))
    True
    """
    assert len(a)==3, "L'arbre est vide"
    return a[1]


def sad[T](a: ArbreBin[T]) -> ArbreBin[T]:
    """
    Retourne le sous-arbre droit de l'arbre.

    Précondition : l'arbre ne doit pas être vide.

    >>> a = creer(10, creer_feuille(5), creer_feuille(15))
    >>> cle(sad(a))
    15
    >>> est_vide(sad(creer_feuille(42)))
    True
    """
    assert len(a)==3, "L'arbre est vide"
    return a[2]


def creer[T](e: T, gauche: ArbreBin[T], droite: ArbreBin[T]) -> ArbreBin[T]:
    """
    Crée un nouvel arbre avec la clé e, le sous-arbre gauche et le sous-arbre droit.

    >>> a = creer(10, ARBRE_VIDE, ARBRE_VIDE)
    >>> cle(a)
    10
    >>> est_vide(sag(a))
    True
    >>> b = creer(20, creer_feuille(15), creer_feuille(25))
    >>> cle(sag(b))
    15
    """
    return (e, gauche, droite)


def creer_feuille[T](e: T) -> ArbreBin[T]:
    """
    Crée une feuille (noeud sans enfants) avec la clé e.

    >>> f = creer_feuille(42)
    >>> cle(f)
    42
    >>> est_vide(sag(f))
    True
    >>> est_vide(sad(f))
    True
    >>> est_feuille(f)
    True
    """
    return (e, ARBRE_VIDE, ARBRE_VIDE)


def est_vide[T](a: ArbreBin[T]) -> bool:
    """
    Teste si l'arbre est vide.

    >>> est_vide(ARBRE_VIDE)
    True
    >>> est_vide(creer_feuille(1))
    False
    >>> est_vide(())
    True
    """
    return len(a) == 0


#! A partir de maintenant, nous n'utiliserons plus les tuples.

def exemple() -> ArbreBin[int]:
    """
    Crée un arbre binaire d'exemple pour les tests.

    Structure de l'arbre :
                    21
                   /  \\
                 14    28
                / \\   / \\
              11  18  25  32
             /   / \\
            9   15  19

    >>> a = exemple()
    >>> cle(a)
    21
    >>> taille(a)
    10
    >>> hauteur(a)
    4
    """
    a = creer(11, creer_feuille(9), ARBRE_VIDE)
    b = creer(18, creer_feuille(15), creer_feuille(19))
    f = creer(14, a, b)
    g = creer_feuille(25)
    h = creer_feuille(32)
    i = creer(28, g, h)
    return creer(21, f, i)

#?##########################
#! LES FONCTIONS EN LECTURE
#*##########################


def taille[T](a: ArbreBin[T]) -> int:
    """
    Retourne le nombre de noeuds de l'arbre.

    >>> taille(ARBRE_VIDE)
    0
    >>> taille(creer_feuille(1))
    1
    >>> taille(creer(10, creer_feuille(5), creer_feuille(15)))
    3
    >>> taille(exemple())
    10
    """
    if est_vide(a):
        return 0
    else:
        return 1+ taille(sag(a)) + taille(sad(a))

def taille_match[T](a: ArbreBin[T]) -> int:
    """
    Retourne le nombre de noeuds de l'arbre.
    On peut utiliser match/case, mais on match les tuples (on sort du coté hermétique de la définition des primitives).

    >>> taille(ARBRE_VIDE)
    0
    >>> taille(creer_feuille(1))
    1
    >>> taille(creer(10, creer_feuille(5), creer_feuille(15)))
    3
    >>> taille(exemple())
    10
    """
    match a:
        case ():
            return 0
        case (_, gauche, droit):
            return 1 + taille(gauche) + taille(droit)

def hauteur[T](a: ArbreBin[T]) -> int:
    """
    Retourne la hauteur de l'arbre (nombre de niveaux).

    La hauteur de l'arbre vide est 0.
    La hauteur d'une feuille est 1.

    >>> hauteur(ARBRE_VIDE)
    0
    >>> hauteur(creer_feuille(1))
    1
    >>> hauteur(creer(10, creer_feuille(5), ARBRE_VIDE))
    2
    >>> hauteur(exemple())
    4
    """
    if est_vide(a):
        return 0
    else:
        return 1 + max(hauteur(sag(a)), hauteur(sad(a)))

def egaux[T](a1: ArbreBin[T], a2: ArbreBin[T]) -> bool:
    if est_vide(a1) and est_vide(a2):
        return True
    if est_vide(a1) or est_vide(a2):
        return False
    return cle(a1) == cle(a2) and sag(a1) == sag(a2) and sad(a1) == sad(a2)

def recherche_abr[T: Comparable](e: T, a: ArbreBin):
    if est_vide(a):
        return False
    if cle(a) == e:
        return True
    if cle(sag(a)) < e:
        return recherche_abr(e, sad(a))
    return recherche_abr(e, sag(a))

def insert_abr[T: Comparable](e: T, a: ArbreBin) -> ArbreBin:
    if est_vide(a):
        return creer(a, ARBRE_VIDE, ARBRE_VIDE)
    if cle(a) > e:
        return creer(cle(a), insert_abr(e, sag(a)), sad(a))
    return creer(cle(a), sag(a), insert_abr(e, sad(a)))

# def parcours_largeur[T](a: ArbreBin[T]) -> list[T]:
#     """
#     Prend en paramètre un arbre et renvoie la liste de c'est élément sous forme d'une liste et respectant le parcour en largeur
    
#     >>> exemple()
#     [21, 14, 28, 11, 18, 25, 32, 9, 15, 19]
    
#     """
#     f: file.File[T] = file.creer()
#     lst = []
#     file.enfiler(a, f)
#     while not file.est_vide(f):
#         n = file.defiler(f)
#         print(cle(n))
#         lst.append(cle(n))
#         file.enfiler(sag(n), f)
#         file.enfiler(sad(n), f)
#     return lst

# def parcours_largeur2[T](a: ArbreBin[T]) -> list[T]:
#     f: pile.Pile[T] = pile.creer()
#     lst = []
#     pile.empiler(a, f)
#     while not pile.est_vide(f):
#         n = pile.depiler(f)
#         print(cle(n))
#         lst.append(cle(n))
#         pile.empiler(sag(n), f)
#         pile.empiler(sad(n), f)
#     return lst

# print(parcours_largeur2(exemple()))

def min_abr[T](a: ArbreBin[T]) -> T:
    if est_vide(sag(a)):
        return cle(a)
    return min_abr(sag(a))

def max_abr[T](a: ArbreBin[T]) -> T:
    if est_vide(sad(a)):
        return cle(a)
    return max_abr(sad(a))

def parcours_infixe[T](a: ArbreBin[T]) -> list[T]:
    if est_vide(a):
        return []
    return parcours_infixe(sag(a)) + [cle(a)] + parcours_infixe(sad(a))


def est_equilibre[T](a: ArbreBin[T]) -> bool:
    """
    >>> est_equilibre(ARBRE_VIDE)
    True
    >>> est_equilibre(creer_feuille(1))
    True
    >>> est_equilibre(creer(10, creer_feuille(5), creer_feuille(15)))
    True
    >>> # Arbre déséquilibré : chaîne à gauche
    >>> desequilibre = creer(3, creer(2, creer_feuille(1), ARBRE_VIDE), ARBRE_VIDE)
    >>> est_equilibre(desequilibre)
    False
    """
    if est_vide(a):
        return True
    return abs(hauteur(sag(a)) - hauteur(sad(a))) < 2 and est_equilibre(sad(a)) and est_equilibre(sag(a)) 

def sont_miroirs[T](a: ArbreBin[T], b: ArbreBin[T]) -> bool:
    """
    >>> a = creer(1, creer_feuille(2), creer_feuille(3))
    >>> b = creer(1, creer_feuille(3), creer_feuille(2))
    >>> sont_miroirs(a, b)
    True
    >>> sont_miroirs(a, a)
    False
    >>> sont_miroirs(ARBRE_VIDE, ARBRE_VIDE)
    True
    """
    if est_vide(a) and est_vide(b):
        return True
    if est_vide(a) or est_vide(b):
        return False
    return cle(a) == cle(b) and sont_miroirs(sag(a), sad(b)) and sont_miroirs(sad(a), sag(b))

def est_symetrique[T](a: ArbreBin[T]) -> bool:
    return sont_miroirs(a, a)

# def minimum[T: Comparable](a: ArbreBin[T]) -> T:
#     if est_vide(a):
#         return 0
#     return min([cle(a)].extend([minimum(sag(a))]).extend([minimum(sad)]))

def minimum[T: Comparable](a: ArbreBin[T]) -> T:
    if est_vide(a):
        raise ValueError("L'arbre est vide")
    elif est_feuille(a):
        return cle(a)
    elif est_vide(sag(a)):
        min_d = minimum(sad(a))
        return cle(a) if cle(a) < min_d else min_d
    elif est_vide(sad(a)):
        min_g = minimum(sag(a))
        return cle(a) if cle(a) < min_g else min_g
    else:
        min_g = minimum(sag(a))
        min_d = minimum(sad(a))
        m = min_g if min_g < min_d else min_d
        return cle(a) if cle(a) < m else m