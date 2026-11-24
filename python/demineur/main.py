import metagrid
from metagrid import AbstractEngine
from random import randint

HAUTEUR  = 10
LARGEUR  = 10
NB_MINES = 10


#? STRUCTURE DE CELLULE

class Cellule:
    est_mine: bool
    nb_voisins: int
    revelee: bool
    drapeau: bool

    def __init__(self):
        self.est_mine   = False   # (1)
        self.nb_voisins = 0   # (1)
        self.revelee    = False   # (1)
        self.drapeau    = False   # (1)


#? ETAT DU JEU

grille: list[list[Cellule]]
game_over: bool
game: AbstractEngine


#? INITIALISATION

def init():
    global grille, game_over
    game_over = False
    grille = [[Cellule() for i in range(HAUTEUR)] for j in range(LARGEUR)]                # (2) grille vierge de HAUTEUR × LARGEUR Cellule()

    compteur = 0
    while compteur < NB_MINES:
        i = randint(0, HAUTEUR - 1)
        j = randint(0, LARGEUR - 1)
        if not grille[i][j].est_mine:                 # (3) la case n'est pas encore une mine
            grille[i][j].est_mine = True                 # (3) la marquer comme mine
            compteur += 1   

    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            grille[i][j].nb_voisins = get_mines_voisines(i, j)  # Pour l'instant


#? FONCTIONS UTILITAIRES

def get_mines_voisines(i: int, j: int) -> int:
    n = 0        # (4)
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if (di != 0 or dj != 0) and 0 <= i + di < HAUTEUR and 0 <= j + dj < LARGEUR:
                    if grille[i+di][j+dj].est_mine:
                        n += 1
    return n                         


def reveler_toutes_mines():
    for i in range(HAUTEUR):                      # (5)
        for j in range(LARGEUR):
            if grille[i][j].est_mine:
                grille[i][j].revelee = True

def est_gagne() -> bool:
    for i in range(HAUTEUR):                      # (6)
        for j in range(LARGEUR):
            if not grille[i][j].est_mine and not grille[i][j].revelee:
                return False
    return True

def decouvre(i: int, j: int):
    cell = grille[i][j]
    cell.revelee = True              # (7) révéler la case
    if cell.nb_voisins == 0:                         # (7) propager seulement si aucun voisin miné
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if (di, dj) != (0, 0) and 0 <= i + di < HAUTEUR and 0 <= j + dj < LARGEUR:     # (7) exclure le centre ET vérifier les bords
                    voisin = grille[i + di][j + dj]
                    if not voisin.revelee and not voisin.est_mine:         # (7) voisin non révélé ET pas une mine
                        decouvre(i+di, j+dj)   # (7) appel récursif


#? CALLBACKS

def click(i: int, j: int, button: str):
    global game_over
    if game_over:                     # (8) ignorer si partie terminée
        return
    case = grille[i][j]
    if button == "left" and not case.drapeau and not case.revelee:
        if case.est_mine:
            game_over = True
            reveler_toutes_mines()
            print("Game over !")
        else:
            decouvre(i, j)
            if est_gagne():
                print("Win")
                game_over = True             # (8) signaler la victoire
    elif button == "right" and not case.revelee:
        case.drapeau = not case.drapeau


def draw():
    if est_gagne() or game_over:
        game.set_cell_char(HAUTEUR//2, LARGEUR//2-1, "W", "#FFFFFF")
        game.set_cell_char(HAUTEUR//2, LARGEUR//2, "I", "#FFFFFF")
        game.set_cell_char(HAUTEUR//2, LARGEUR//2+1, "N", "#FFFFFF")
    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            case = grille[i][j]
            if case.drapeau:
                game.set_cell_color(i, j, "#555555")
                game.set_cell_char(i, j, "F", "#FF0000")
            elif case.est_mine and not case.revelee:           # (9) non révélée
                game.set_cell_color(i, j, "#000000")
                game.set_cell_char(i, j, "", "#000000")
            elif case.est_mine and case.revelee:           # (9) mine révélée
                game.set_cell_color(i, j, "#FF4444")
                game.set_cell_char(i, j, "X", "#FFFFFF")
            elif not case.est_mine and case.revelee:          # (9) case chiffrée
                game.set_cell_color(i, j, "#FFFFFF")
                game.set_cell_char(i, j, str(case.nb_voisins), "#3418D4")
            else:
                game.set_cell_color(i, j, "#FFFFFF")
                game.set_cell_char(i, j, "", "#000000")


if __name__ == "__main__":
    game = metagrid.create(HAUTEUR, LARGEUR, 50, 1)
    game.on_init(init)
    game.on_click(click)
    game.on_draw(draw)
    game.start()