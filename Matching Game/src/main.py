"""
    CS5001
    Fall 2020
    Project: Matching Game
    Ellah Nzikoba
"""

from match_functions import *


def main():
    # Dictionary to store most of the game data(mostly positions and turtles)
    data = {
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
    leaders, data = start_up(data)

    # set number of cards and card images, other parameters for the game
    game_cards, data = get_user_input(data)

    # place cards and assign image to each position
    game_cards, data = place_cards(game_cards, data)  # get POSITIONS

    # create board objects to store as data n Board class
    create_board_objects(data)

    # create game_data object to store as data in GameData class
    create_game_data_objects(data)

    # place face down cards on board
    facedown_cards(game_cards, data)

    # create objects for each card in data and save to Card class
    create_card_objects(data)

    # start tracking matches, guesses and display leader board
    set_tracking(data)

    # add quit button
    add_quit()

    # on_click function to handle user clicks
    tur.onscreenclick(on_click, 1)

    tur.done()


main()
