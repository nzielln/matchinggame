"""
    CS5001
    Fall 2020
    Project: Matching Game
    Ellah Nzikoba
"""

from match_functions import *


def main():
    # Dictionary to store most of the game data(mostly positions and turtles)
    DATA = {
        "NAME": "",
        "POSITIONS": {
            "main": {},
            "images": {},
            "scores": {},
            "tracker": {},
            "quit": {},
        },
        "TRACKER": {"Guesses": 0, "Matches": 0},
        "LEADERS": {},
        "CLICKED_CARDS": [],
    }

    T.penup()

    # Set initial settings
    T.speed("fastest")
    T.color("white")

    # Adjust screen size
    S.screensize(900, 700)
    S.setup(900, 700)

    # start game
    leaders, DATA = start_up(DATA)

    # set number of cards and card images, other parameters for the game
    game_cards, DATA = get_user_input(DATA)

    # place cards and assign image to each position
    game_cards, DATA = place_cards(game_cards, DATA)  # get POSITIONS

    # create board objects to store as data n Board class
    create_board_objects(DATA)

    # create game_data object to store as data in GameData class
    create_game_data_objects(DATA)

    # place face down cards on board
    facedown_cards(game_cards, DATA)

    # create objects for each card in DATA and save to Card class
    create_card_objects(DATA)

    # start tracking matches, guesses and display leader board
    set_tracking(DATA)

    # add quit button
    add_quit()

    # on_click function to handle user clicks
    tur.onscreenclick(on_click, 1)

    tur.done()


main()
