import flet as ft

VIDE = 0
BLANC = 1   # joueur 1
NOIR = 2    # joueur 2

type grille = list[list[int]]
type coup = tuple[int, int]

def autre(joueur: int) -> int:
    """
    Retourne l'autre joueur
    """
    assert joueur in (1,2), "Seuls les joueurs 1 et 2 sont possibles"
    return 3-joueur

def peut_jouer(c: coup, joueur: int, g: grille) -> bool:
    """Cette fonction a besoin d'exister pour l'affichage.
    Vous l'écrirez en chemin """
    i,j = c
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di != 0 or dj != 0:
                ci, cj = i + di, j +dj
                test = False
                while ci >= 0 and ci <= 7 and cj >= 0 and cj <= 7 and g[ci][cj] == autre(joueur):
                    ci += di 
                    cj += dj
                    test = True
                if test and ci >= 0 and ci <= 7 and cj >= 0 and cj <= 7 and g[ci][cj] == joueur:
                    return True
    
    return False

def coups_possibles(joueur: int, g: grille) -> list[coup]:
    coups: list[coup] = []
    for i in range(8):
        for j in range(8):
            if peut_jouer((i, j), joueur, g):
                new_coup: tuple[int, int] = (i, j)
                coups.append(new_coup)
    return coups

def get_score(g: grille) -> tuple[int, int]:
    score_blanc, score_noir = 0, 0
    for i in range(8):
        for j in range(8):
            if g[i][j] == BLANC:
                score_blanc += 1
            if g[i][j] == NOIR:
                score_noir += 1
    return (score_blanc, score_noir)

def jouer_coup(c: coup, joueur: int, g: grille) -> grille:
    newG = g
    i,j = c
    g[i][j] = joueur
    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di != 0 or dj != 0:
                ci, cj = i + di, j +dj
                while ci >= 0 and ci <= 7 and cj >= 0 and cj <= 7 and g[ci][cj] == autre(joueur):
                    newG[ci][cj] = joueur
                    ci += di
                    cj += dj
    return newG

def is_game_over(g: grille) -> bool:
    return len(coups_possibles(BLANC, g)) == 0 and len(coups_possibles(NOIR, g)) == 0

def partie2j():
    g = creer_grille()
    current_joueur = BLANC
    show(current_joueur, g)
    while not is_game_over(g):
        coup = askCoup()
        while not peut_jouer(coup, current_joueur, g):
            coup = askCoup()
        jouer_coup(coup, current_joueur, g)
        current_joueur = autre(current_joueur)
        show(current_joueur, g)

def minimax():
    pass

scorepoint = [
    [8, -1, 4, 4, 4, 4, -1, 8],
    [-1, 0, 2, 2, 2, 2, 0, -1],

    [-1, 0, 2, 2, 2, 2, 0, -1],
    [8, -1, 4, 4, 4, 4, -1, 8]
]

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True

def askCoup() -> tuple[int, int]:
    c = input("Coup à joueur : ")
    if len(c) != 2 or not represents_int(c):
        print("Entrez un coup possible. \nFormat suivant: xy\nExemple : 42")
        return (-1, -1)
    return (int(c[0]), int(c[1]))

def show(joueur: int, g: grille) -> str:
    """
    Affiche la grille g, le joueur allant jouer étant donné
    """
    msg = ""
    msg += "".join(f"   {j}" for j in range(8)) + "\n"
    msg += " ┌───" + 7*"┬───" + "┐\n"

    for i in range(8):
        msg += f"{i}│"
        for j in range(8):
            if g[i][j] == NOIR:
                msg += " ○ │"
            elif g[i][j] == BLANC:
                msg += " ● │"
            elif peut_jouer((i, j), joueur, g):
                msg += " . │"
            else:
                msg += "   │"
        msg += "\n"
        if i == 7:
            msg += " └───" + 7*"┴───" + "┘\n"
        else:
            msg += " ├───" + 7*"┼───" + "┤\n"

    msg += f"C'est le tour du joueur {joueur}"

    return msg

def poser_pion(c: coup, joueur: int, g: grille):
    g[c[0]][c[1]] = 2

def creer_grille() -> grille:
    g = [[0 for i in range(8)] for i in range(8)]
    g[3][3], g[4][4] = 1, 1
    g[4][3], g[3][4] = 2, 2
    return g

def main(page: ft.Page):
    def coup_button(e):
        page.add(ft.Checkbox(label=coup_txt.value))
        coup_txt.value = ""
        coup_txt.focus()
        coup_txt.update()

    def button_clicked(e):
        page.add(ft.Text("Coup jouer !"))

    page.title = "Othello"

    g = creer_grille()
    t = ft.Text(value=f"{show(BLANC, g)}", color="green")
    cj = ft.Text(value="Coup a jouer : ", color="green")
    
    page.add(t)
    page.add(cj)


    coup_txt = ft.TextField(hint_text="Exemple : 42", width=300)
    page.add(ft.Row([coup_txt, ft.ElevatedButton("Add", on_click=button_clicked)]))

    page.update()



ft.app(main)


