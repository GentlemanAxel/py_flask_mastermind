# mastermind.py
###############################################################################
#            Voici les imports des modules et librairies python               #
###############################################################################

import random

###############################################################################
#      Voici la class Mastermind contenant les fonctions à importer           #
###############################################################################


class Mastermind:
    def __init__(self):
        """
        Initialise un nouvel objet Mastermind avec un code secret aléatoire,
        une liste de propositions vides et une liste de résultats vides.
        """
        self.secret_code = self.generate_code()  # Crée un code secret
        self.guesses = []  # Initialise une liste de tentatives pour deviner le code
        self.results = []  # Initialise une liste des résultats de ces tentatives

    def to_dict(self):
        """
        Retourne un dictionnaire contenant les attributs de l'objet Mastermind :
        le code secret, les propositions et les résultats.
        """
        return {
            # Ces lignes définissent les clés d'un dictionnaire contenant les attributs :
            # Secret_code, guesses et results de l'objet self.
            "secret_code": self.secret_code,
            "guesses": self.guesses,
            "results": self.results
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée et renvoie un nouvel objet Mastermind à partir d'un dictionnaire qui contient les attributs de l'objet.
        """
        instance = cls()  # Crée une instance de la classe,

        # attribue les valeurs de "secret_code", "guesses" et "results" aux attributs correspondants de l'instance :
        instance.secret_code = data["secret_code"]
        instance.guesses = data["guesses"]
        instance.results = data["results"]

        return instance  # Retourne l'instance.

    @staticmethod
    def generate_code():
        """
        Génère et retourne un code secret aléatoire composé de 4 chiffres compris entre 1 et 4.
        """
        return [random.randint(1, 4) for _ in range(4)]

    def make_guess(self, guess):
        """
        Vérifie si le nombre de propositions est inférieur à 8.
        Si c'est le cas, ajoute la proposition à la liste de propositions et renvoie le résultat de cette dernière.
        Si le nombre de propositions est supérieur ou égal à 8,
        retourne False sans ajouter la proposition à la liste de propositions.
        """
        # Si le nombre d'essais est supérieur ou égal à 8, la méthode retourne False,
        if len(self.guesses) >= 8:
            return False

        # Sinon, elle ajoute le guess à la liste, vérifie le guess, ajoute le résultat à la liste et le retourne :
        self.guesses.append(guess)
        result = self.check_guess(guess)
        self.results.append(result)
        return result

    def check_guess(self, guess):
        """
        Compare la proposition à la combinaison secrète et retourne un dictionnaire avec :
        le nombre de languettes rouges et blanches correspondant à la proposition.
        """
        # Copie les codes secrets et les propositions :
        secret_code_copy = self.secret_code.copy()
        guess_copy = guess.copy()

        # Calcule le nombre de jetons rouges et blancs :
        # Trouvé bien placé :
        red_pins = sum(a == b for a, b in zip(secret_code_copy, guess_copy))
        # Trouvé mal placé :
        white_pins = sum(min(secret_code_copy.count(col), guess_copy.count(col)) for col in range(1, 5)) - red_pins

        # Renvoie un dictionnaire contenant ces valeurs.
        return {"red_pins": red_pins, "white_pins": white_pins}

    def is_game_over(self):
        """
        Vérifie si le nombre de propositions est supérieur ou égal à 8 ou,
        si l'un des résultats des propositions a un nombre de broches rouges égal à 4.
        Retourne True si le jeu est terminé, False sinon.
        """
        return len(self.guesses) >= 8 or any(result["red_pins"] == 4 for result in self.results)
