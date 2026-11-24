from structures.lineaires import file_de_pile as file
import random
import pyxel as px
import json
import time
# import requests
import asyncio

type Coord = tuple[int, int]   # Une coordonnée est un tuple constitué de deux ints
type Snake = file.File[Coord]  # Un snake est une file de coordonnées

# --- Constantes ---
W, H = 200, 200    # Largeur et Hauteur de la grille
STEP_FRAMES = 4     # Vitesse (Mise à jour toutes les 4 frames)
TAILLE_CASE = 10
TAILLE_BORDER = 12
SCORES_FILE = "scores.json"


# --- État global --- Déclaration de toutes les variables --- 
serpent: Snake                  # File de coordonnées
tete: Coord                     # Tete du serpent
queue_supprimee: Coord | None   # Dernière queue du serpent supprimée
direction: Coord                # vecteur de déplacement du serpent
pomme: Coord                    # coordonnée de la pomme
score: int                      # score de l'utilisateur
game_over: bool                 # indicateur de game over
frames: int                     # compteur de frames (augmente de 1 dès que update est appelé)
last_score: int
best_score: int
timer: int

# --- Initialisation ---
last_score = 0
best_score = 0

def reinit():
    """
    Initialisation de TOUTES les variables globales
    """
    global serpent, tete, direction, score, game_over, frames, queue_supprimee, last_score, best_score, timestamp
    serpent = file.creer()
    tete = (W//TAILLE_CASE//2, H//TAILLE_CASE//2)
    file.enfiler(tete, serpent)  # Initialiser le serpent avec sa tete
    direction = (1, 0)   # droite
    score = 0
    game_over = False
    frames = 0    # Ne vous souciez pas de ça pour le moment
    timestamp = time.time()
    # queue_supprimee = file.defiler(serpent)
    spawn_pomme()

def avancer():
    global serpent, tete, direction, score, game_over, frames, queue_supprimee, pomme, last_score, best_score, timestamp
    tete = (tete[0]+direction[0], tete[1]+direction[1])

    if file.contient(tete, serpent) or tete[0]*TAILLE_CASE == W or tete[0] == -1 or tete[1]*TAILLE_CASE == H or tete[1] == -1:
        game_over_fc()
        return

    file.enfiler(tete, serpent)

    if tete != pomme:
        file.defiler(serpent)
    else:
        spawn_pomme()
        score += 1

def get_current_player():
    try:
        with open("current_player.json", "r") as f:
            data = json.load(f)
            return data.get("pseudo", "Joueur")
    except FileNotFoundError:
        return "Joueur"

def game_over_fc():
    global serpent, tete, direction, score, game_over, frames, queue_supprimee, pomme, last_score, best_score, timestamp

    game_over = True
    last_score = score
    now = time.time() - timestamp
    timer = time.gmtime(now)

    # if score > int(get_player("serveur", SCORES_FILE)["score"]):
    #     sauvegarder_score("serveur", score, timer, SCORES_FILE)
    # ⚠️ Pseudo à récupérer depuis ton jeu ou ta page Flask
    pseudo = get_current_player()
    # Adresse du serveur Flask (modifie si besoin)
    url = "localhost:5500/snake/add_score"
    params = {
        "pseudo": pseudo,
        "score": score,
        "timer": int(now)
    }

    print(params)
    # requests.post(url, params=params)

        # response = requests.get(url, params=params)


        # if response.status_code == 200:
        #     print("✅ Score envoyé avec succès :", response.json())
        # else:
        #     print("❌ Erreur lors de l’envoi :", response.status_code)

    # except Exception as e:
    #     print("⚠️ Impossible d’envoyer le score :", e)
    

async def call_web_service():
    js = __import__("js")
    data = await js.fetchData("https://localhost:5500/snake/scores")
    print("Données reçues :", data)

json.dump(call_web_service(), "scores.json", indent=4)

def spawn_pomme():
    global pomme
    pomme = (random.randint(0, W//TAILLE_CASE-1), random.randint(0, H//TAILLE_CASE-1))
    if file.contient(pomme, serpent):
        spawn_pomme()

def sauvegarder_score(nom_joueur, score, timer, nom_fichier):
    try: 
        with open(nom_fichier, "r") as fichier: # Lire les scores existants s'ils existent
            scores: list[dict] = json.load(fichier)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = [] # Si le fichier n'existe pas ou est vide, on commence avec une liste vide

    joueur_find = next((item for item in scores if item.get("name") == "serveur"), None)

    if joueur_find:
        joueur_find["score"] = score
        joueur_find["timer"] = timer
    else:
        scores.append({
            "name": nom_joueur,
            "score": score,
            "timer": timer
        })

    # Réécrire tous les scores dans le fichier
    with open(nom_fichier, "w") as fichier:
        json.dump(scores, fichier, indent=4)

def get_player(nom_joueur, nom_fichier) -> dict:
    scores : list[dict]
    try:
        with open(nom_fichier, "r") as fichier:
            scores = json.load(fichier)
            for i in range(len(scores)):
                if scores[i]["name"] == nom_joueur:
                    return scores[i]
            return {"name": "noFind", "score": 0}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"name": "noFind", "score": 0}

    return

def update():
    global serpent, tete, direction, score, game_over, frames, queue_supprimee

    frames += 1
    # if frames%20 != 0:
    #     return

    if game_over:
        reinit()

    if px.btn(px.KEY_RIGHT) and direction != (-1, 0):
        direction = (1, 0)
    elif px.btn(px.KEY_LEFT) and direction != (1, 0):
        direction = (-1, 0)

    if px.btn(px.KEY_DOWN) and direction != (0, -1):
        direction = (0, 1)
    elif px.btn(px.KEY_UP) and direction != (0, 1):
        direction = (0, -1)

    if px.btn(px.KEY_ESCAPE) or px.btn(px.KEY_SPACE):
        game_over()

    avancer()
    
def draw():
    global serpent, tete, direction, score, game_over, frames, queue_supprimee, TAILLE_CASE, last_score, best_score

    px.cls(px.COLOR_LIME)

    px.rect(0, 0, W, TAILLE_BORDER, px.COLOR_ORANGE)

    # px.pset(pomme[0], pomme[1], px.COLOR_RED)
    px.rect(pomme[0]*TAILLE_CASE, pomme[1]*TAILLE_CASE+TAILLE_BORDER, TAILLE_CASE, TAILLE_CASE, px.COLOR_RED)
    px.text(2, 2, f"Score: {score} ; Dernier score: {last_score} ; Best score: {get_player("serveur", SCORES_FILE)["score"]}", px.COLOR_BROWN)
    f = file.creer()
    while not file.est_vide(serpent):
        coord = file.defiler(serpent)
        # px.pset(coord[0], coord[1], px.COLOR_BLACK)
        px.rect(coord[0]*TAILLE_CASE, coord[1]*TAILLE_CASE+TAILLE_BORDER, TAILLE_CASE, TAILLE_CASE, px.COLOR_BLACK)
        file.enfiler(coord, f)
        
    while not file.est_vide(f):
        file.enfiler(file.defiler(f), serpent)

def lancer_jeu():
    # Initialiser pyxel, le moteur graphique
    px.init(W, H+TAILLE_BORDER, title="Snake", fps=10)
    # Initialisaer l'état du jeu
    reinit()
    # lancer la boucle d'appels permanents à update puis draw
    px.run(update, draw)  


lancer_jeu()
