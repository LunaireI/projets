class Maillon:
    
    def __init__(self, data: int, next: 'Maillon'):
        """
        Initialse un moyen
        """
        self.data = data
        self.next = next
    
    def __repr__(self) -> str:
        return f"{self.data} | "

class Liste(Maillon):
    """
    Construit une liste
    """
    def __init__(self):
        super().__init__(0, self)
        self.__taille = 0
    """
    Ajoute un element a notre liste
    """
    def add_tete(self, e: int):
        m = Maillon(e, self.next)
        self.next = m
        self.__taille += 1

    def est_vide(self) -> bool:
        """
        Renvoie True si la liste est vide, False sinon.
        """
        return self.next is self
    
    def longueur(self) -> int:
        """
        Renvoie la taille calculée de la liste.
        """
        acc = 0
        courant = self.next
        while courant is not self:
            acc += 1
            courant = courant.next
        return acc

    def __repr__(self) -> str:
        return super().__repr__() 
    
if __name__ == "__main__":
    l = Liste()
    l.add_tete(4)
    print(l)