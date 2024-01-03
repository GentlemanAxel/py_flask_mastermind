# py_flask_mastermind

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

A complex mastermind project in python with a custom library.

##### Project's language (functions, variables, comments): FRENCH.

---

## Overview

"py_flask_mastermind" is a Flask-based web application for playing the Mastermind game. It includes functionalities to play the game, view game history, and learn how to play. The game's state, including secret codes, guesses, and results, is stored and managed using the Mastermind class (custom library). The application also features a graphical representation of the evolution of the number of tries over multiple games.

---

## Main Features

- Mastermind Game: Play the classic Mastermind game, attempting to guess the secret code based on feedback after each guess.

- Game History: View a list of previous Mastermind games along with associated information, including a graphical representation of the number of tries over games played.
     -> Graphical Representation: Utilizes Matplotlib to create a graph showing the evolution of the number of tries over the last 30 games.

- How to Play: Access a guide on how to play the Mastermind game, with interactive examples.

- Cheat mode : Activate & desactivate a cheating mode 🔒

Data Persistence: Saves game information, including ID, date, secret code, guesses, and results, to a file (data_parties.data) for future reference.

---

## Usage

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/GentlemanAxel/py_flask_mastermind.git
    ```

2. Navigate to the project directory:

    ```bash
    cd py_flask_mastermind
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
### Run the Application

```bash
python app.py
```
Access the application in your web browser at http://127.0.0.1:5000/.

---


### Example Usage
1. Open the web browser and go to http://127.0.0.1:5000/.
2. Learn how to play Mastermind by visiting the "How to Play" section.
3. Play the Mastermind game by following the on-screen instructions.
4. Explore game history and view the graphical representation of the number of tries over the last 30 games.

### Credits

<a href='https://github.com/GentlemanAxel' target="_blank"><img alt='GitHub' src='https://img.shields.io/badge/GentlemanAxel-100000?style=for-the-badge&logo=GitHub&logoColor=white&labelColor=black&color=CA2C2C'/></a>
