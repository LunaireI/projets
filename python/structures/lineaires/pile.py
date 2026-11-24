# Python 3.13

type Pile[T] = list[T]

def creer[T]() -> Pile[T]:
    """
    Crée une pile vide.

    >>> p: Pile[int] = creer()
    >>> p
    []
    """
    return []

def est_vide[T](p: Pile[T]) -> bool:
    """
    Indique si la pile est vide.

    >>> p: Pile[str] = creer()
    >>> est_vide(p)  #? True pour une pile vide
    True
    >>> empiler("test", p)
    >>> est_vide(p)  #? False sinon
    False
    """
    return len(p) == 0

def empiler[T](e: T, p: Pile[T]):
    """
    Empile l'élément e au sommet de la pile p (modifie p sur place).

    >>> p = creer()
    >>> empiler(10, p)  #? pas de valeur de retour (None)
    >>> p
    [10]
    >>> empiler(5, p)
    >>> p
    [10, 5]
    """
    p.append(e)


def depiler[T](p: Pile[T]) -> T:
    """
    Dépile et retourne l'élément au sommet de la pile p.

    >>> p = creer()
    >>> empiler(1, p)
    >>> empiler(2, p)
    >>> depiler(p)
    2
    >>> p
    [1]

    Dépile sur pile vide -> AssertionError :

    >>> depiler(p)
    1
    >>> depiler(p)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AssertionError: La pile est vide
    """
    assert not est_vide(p), "La pile est vide"
    return p.pop()


if __name__ == "__main__":
    import doctest
    doctest.testmod()