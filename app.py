# app.py
###############################################################################
#            Voici les imports des modules et librairies python               #
###############################################################################
import matplotlib.pyplot as plt
import datetime
from io import BytesIO
import base64
import json
from flask import Flask, render_template, request, redirect, url_for, session
from mastermind import Mastermind


###############################################################################
#    Initialisation des fonctions ne servant pas directement à l'interface    #
###############################################################################
def clear_fichier():
    """
    Cette fonction supprime toutes les lignes vides dans le fichier "data_parties".
    """
    result = ""
    with open("data_parties.data", "r+") as file:
        for line in file:
            if not line.isspace():
                result += line

        file.seek(0)
        file.write(result)


def save_games(id_partie, game_data):
    """
    Cette fonction sauvegarde les informations d'une partie de Mastermind :
    l'ID de la partie, la date, le code secret, les tentatives/propositions et les résultats.
    Ces informations sont ensuite stockées dans le fichier "data_parties".
    """
    clear_fichier()
    with open("data_parties.data", "a") as fichier:
        game_info = {
            "id": id_partie,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "secret_code": game_data["secret_code"],
            "guesses": game_data["guesses"],
            "results": game_data["results"]
        }
        fichier.write(json.dumps(game_info) + "\n")  # écrit une représentation JSON des infos de jeu dans le fichier.


def load_games():
    """
    Cette fonction charge toutes les parties de Mastermind stockées dans le fichier "data_parties" ;
    Enfin, les retourne sous forme d'une liste de dictionnaires.
    """
    games = []
    with open("data_parties.data", "r") as file:
        for line in file:
            # Si la ligne n'est pas une ligne vide, charge la partie en format JSON dans la variable game :
            if not line.isspace():
                game = json.loads(line)
                game["num_tries"] = len(game["guesses"])
                games.append(game)
    return games


def create_graph(games):
    """
    : games : Cette fonction prend une liste de parties de Mastermind en paramètre ;
    Puis, crée un graphique montrant l'évolution du nombre d'essais au cours du temps.
    """
    # S'il y a plus de 30 parties, ne considérer que les 30 dernières parties pour le graphique :
    games = games[-30:]

    # Crée un graphique à partir des données de parties précédentes :
    num_games = len(games)
    num_tries = [game["num_tries"] for game in games]

    fig, ax = plt.subplots()
    ax.plot(range(1, num_games+1), num_tries, marker='o', linestyle='-')
    ax.set(xlabel='Game Number (30 last games)', ylabel='Number of Tries',
           title='Evolution of Number of Tries Over Games Played')

    plt.xticks(range(1, num_games+1))
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')  # sauvegarde le graphique sous format png
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')  # retourne l'image sous forme d'une image encodée en base64


###############################################################################
#      Initialisation du menu (interface web) et des fonctions associées      #
###############################################################################

app = Flask(__name__)
app.secret_key = "jaimelescookiesalanoisette"


@app.route("/")
def home():
    """
    Affiche la page d'accueil et supprime la session de jeu/tutoriel en cours.
    """
    if "game" in session:
        session.pop("game", None)
    if "howtoplay" in session:
        session.pop("howtoplay", None)
    return render_template("home.html")


@app.route("/playing")
def index():
    """
    Affiche la page de jeu et permet au joueur de deviner la combinaison de couleurs (si cheat=true).
    Elle récupère les paramètres du formulaire POST et met à jour la session de jeu.
    Si le jeu est terminé, la fonction redirige vers la page de fin de jeu.
    """
    # La ligne récupère la valeur du paramètre "cheat" passé dans la requête HTTP :
    cheat_mode = request.args.get("cheat", "false").lower() == "true"

    # Les lignes vérifient si le jeu est présent dans la session et l'initialise si ce n'est pas le cas :
    if "game" not in session:
        session["game"] = Mastermind().to_dict()

    game = Mastermind.from_dict(session["game"])  # La ligne restaure l'état du jeu depuis la session.

    print(session["game"], game)  # Imprime l'état du jeu

    if game.is_game_over():
        return redirect(url_for("game_over"))  # Redirige vers la page "game_over" si le jeu est terminé.

    # La ligne renvoie la page "playing.html" avec les informations de jeu, le mode triche et l'objet zip :
    return render_template("playing.html", game=game, zip=zip, cheat_mode=cheat_mode)


@app.route("/game_history")
def game_history():
    """
    Affiche une liste de parties précédentes et les informations qui leur sont liées.
    Affiche également un graphique montrant le nombre de coups nécessaires au joueur pour gagner chaque partie.
    """
    games = load_games()  # Initialise les informations des parties jouées.
    img = create_graph(games)  # Initialise un graphique à partir de ces informations.

    # La ligne renvoie la page "game_history.html" avec les informations des précèdentes parties ;
    # (ainsi que le graphique en paramètres) :
    return render_template("game_history.html", games=games, img=img)


@app.route("/howtoplay")
def howtoplay_func():
    """
    Affiche une page expliquant à l'utilisateur comment jouer au jeu.
    """
    # Si "howtoplay" est dans la session, le supprimer, sinon créer un nouveau jeu et le stocker dans la session :
    if "howtoplay" in session:
        session.pop("howtoplay", None)

    if "howtoplay" not in session:
        session["howtoplay"] = Mastermind().to_dict()

    howtoplay_var = Mastermind.from_dict(session["howtoplay"])

    #  Afficher un modèle qui montre comment jouer en utilisant la variable de jeu créée.
    return render_template("how_to_play.html", howtoplay=howtoplay_var, zip=zip)


@app.route('/guess', methods=['POST'])
def guess():
    """
    Permet au joueur de deviner la combinaison de couleurs.
    Elle utilise la méthode POST pour récupérer les couleurs choisies par le joueur ;
    Puis, elle met à jour la session de jeu et redirige vers la page de jeu.
    """
    game = Mastermind.from_dict(session["game"])  # Crée un objet "game" à partir d'un dictionnaire de session.

    # Récupère les données envoyées via un formulaire :
    user_guess = [int(request.form[f"color_{i}"]) for i in range(1, 5)]

    # Met à jour la session avec les nouvelles données du jeu et la prédiction de l'utilisateur :
    game.make_guess(user_guess)
    session["game"] = game.to_dict()

    # Détermine si le mode triche est activé,
    # puis redirige l'utilisateur vers la page d'index en transmettant l'information du mode triche :
    cheat_mode = request.form.get("cheat", "false").lower() == "true"
    return redirect(url_for("index", cheat=cheat_mode))


@app.route("/game_over")
def game_over():
    """
    Affiche la page de fin de jeu avec le nombre de coups nécessaires pour gagner & sauvegarde la partie dans un fichier
    Si le jeu n'est pas terminé, la fonction redirige vers la page de jeu.
    """
    # Charge la partie en cours à partir de la session utilisateur :
    game = Mastermind.from_dict(session["game"])
    # Vérifie si elle n'est pas terminée :
    if not game.is_game_over():
        return redirect(url_for("index"))

    # Récupère le nombre de tentatives et le code secret de la partie.
    num_tries = len(game.guesses)
    secret_code = game.secret_code

    # Check if the game is won
    if any(result["red_pins"] == 4 for result in game.results):
        result = "won"
    elif num_tries >= 8:
        result = "lost"
    else:
        result = "won"

    # Sauvegarde les données de la partie dans un fichier :
    game_id = str(len(open("data_parties.data").readlines()) + 1)
    save_games(game_id, game.to_dict())

    session.pop("game", None)  # Met fin à la partie.

    # Affiche la page "game_over" avec les données de la partie :
    return render_template("game_over.html", game=game, result=result, num_tries=num_tries, secret_code=secret_code)


if __name__ == "__main__":
    app.run(debug=True)