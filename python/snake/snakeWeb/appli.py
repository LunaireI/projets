import json
import flask
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)

@app.route('/')
def accueil_controller():
    return render_template("snakeHome.j2.html")

@app.route('/snake/')
def snakeGame():
    pseudo = request.args.get("pseudo", "Joueur")

    # 🔹 Valeurs par défaut si le joueur n'existe pas
    joueur_score = 0
    joueur_timer = 0

    try:
        with open("scores.json", "r") as f:
            scores = json.load(f)
            for joueur in scores:
                if joueur.get("name") == pseudo:
                    joueur_score = joueur.get("score", 0)
                    joueur_timer = joueur.get("timer", 0)
                    break
    except (FileNotFoundError, json.JSONDecodeError):
        # Aucun score pour le joueur
        pass

    # Facultatif : enregistrer le pseudo dans current_player.json
    with open("current_player.json", "w") as f:
        json.dump({"pseudo": pseudo}, f)

    # 🔹 Renvoyer les données du joueur à la page HTML
    return render_template("snake.html", pseudo=pseudo, score=joueur_score, timer=joueur_timer)

@app.route("/scores")
def afficher_scores():
    try:
        with open("scores.json", "r") as f:
            data = json.load(f)
        return flask.jsonify(data)  # 🔹 renvoie du JSON proprement formaté
    except FileNotFoundError:
        return flask.jsonify({"error": "scores.json introuvable"}), 404
    
@app.route("/scores/download_scores")
def download_scores():
    try:
        return send_file(
            "scores.json",
            as_attachment=True,          # 🔹 force le téléchargement
            download_name="scores.json", # 🔹 nom du fichier à enregistrer
            mimetype="application/json"  # 🔹 type MIME correct
        )
    except FileNotFoundError:
        return "Le fichier scores.json est introuvable", 404

@app.route('/snake/clear_scores')
def clear_scores():
    with open("scores.json", "w") as fichier:
        json.dump([], fichier)
    return "Scores réinitialisés ✅"

@app.route('/snake/add_score', methods=["GET", "POST"])
def add_score():
    """
    Route pour enregistrer un score dans scores.json
    URL : /snake/add_score?pseudo=Nom&score=10&timer=123
    """
    pseudo = request.args.get("pseudo", "Joueur")
    score = int(request.args.get("score", 0))
    timer = request.args.get("timer", 0)
    
    sauvegarder_score(pseudo, score, timer, "scores.json")

    # Lecture et renvoi du fichier complet
    try:
        with open("scores.json", "r") as fichier:
            scores: list[dict] = json.load(fichier)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    # On renvoie la liste des scores au format JSON
    return jsonify(scores)

#  --- Fonction utilitaire pour enregistrer un score ---

def sauvegarder_score(nom_joueur: str, score: int, timer: object, nom_fichier: str):
    """
    Modifie le score du joueur, ou crée son score s’il n’existait pas encore.
    """
    try:
        with open(nom_fichier, "r") as fichier:
            scores: list[dict] = json.load(fichier)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    joueur_find = next((item for item in scores if item.get("name") == nom_joueur), None)

    if joueur_find:
        joueur_find["score"] = score
        joueur_find["timer"] = timer
    else:
        scores.append({
            "name": nom_joueur,
            "score": score,
            "timer": timer
        })

    with open(nom_fichier, "w") as fichier:
        json.dump(scores, fichier, indent=4)

if __name__ == "__main__":
    app.run(port=5500, debug=True)
