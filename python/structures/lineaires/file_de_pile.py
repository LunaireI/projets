from . import pile

type File[T] = tuple[pile.Pile[T], pile.Pile[T]]

def creer[T]() -> File:
    return (pile.creer(), pile.creer())

def est_vide(f: File) -> bool:
    return pile.est_vide(f[0]) and pile.est_vide(f[1])

def enfiler[T](e: T, f: File):
    pile.empiler(e, f[0])


def defiler(f: File):

    assert not est_vide(f), "La file est vide"  

    if not pile.est_vide(f[1]):
        return pile.depiler(f[1])
    while not pile.est_vide(f[0]):
        pile.empiler(pile.depiler(f[0]), f[1])
    return pile.depiler(f[1])

def contient[T](e: T, f: File[T]) -> bool:
    new_f = creer()
    res = False
    while not est_vide(f):
        temp = defiler(f)
        enfiler(temp, new_f)
        if temp == e:
            res = True
    while not est_vide(new_f):
        enfiler(defiler(new_f), f)
    return res