import turtle as tur
import random, os.path
from Card import Card
from Board import Board
from GameData import GameData

# Turtle and Screen Globals
T = tur.Turtle(visible=False)
S = tur.Screen()


# starts the game
def start_up(data):
    """
    Function: start_up(data)
    Parameters:
        data: (dict) a dictionary of data from the game
    Returns:
        leaders: (dict) a dict of leaders and scores from leaders.txt
        data: (dict) the data dict updated with leaders and
        scores from leaders

    Starts up the game by reading leaders and scores from the
    leaders.txt file to be used in the Leadersboard
    Call try_file() on file name to see if it can be opened/accessed
    """

    # dict to store information for leaders.txt
    leaders = data["LEADERS"]
    num_line = 0
    nofile_l = None

    if try_file("leaders.txt", "r"):
        # test if file can be opened first before proceeding
        with open("leaders.txt", "r") as f:
            f.readline()
            for line in f:
                num_line += 1
                split_line = line.split()
                leaders[f"Player_{num_line}"] = []
                leaders[f"Player_{num_line}"].append(split_line[0])
                leaders[f"Player_{num_line}"].append(int(split_line[1]))
    # if error, let user know
    else:
        nofile_l = True

    data["nofile_l"] = nofile_l
    return leaders, data


def try_file(file_name, mode):
    """
    Function: try_file(file_name, mode)
    Parameters:
        file_name: (dict) a file name
        mode: (str) what to do with the file (w, r, or a)
    Returns:
        None

    Returns True if file can be opened and accessed, False and throws
    exception if it can not
    """

    try:
        file_open = open(file_name, mode)
        return True
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

    # if file is locked
    except PermissionError as e:
        print(f"Error: {e}")
        return False

    # if file does not exist
    except FileExistsError as e:
        print(f"Error: {e}")
        return False


def stamp_nofile(img):
    """
    Function: stamp_nofile(img)
    Parameters:
        img: (str) an file name/path
    Returns:
        nofile_id: (int) stamp id

    Stamps a warning message if a file is missing/can't be opened
    """

    # stamps error msg on main playing area
    S.addshape(img)
    T.shape(img)
    nofile_id = T.stamp()
    return nofile_id


def get_user_input(data):
    """
    Function: get_user_input(data)
    Parameters:
        data: (dict) a dictionary of data from the game
    Returns:
        game_cards: (dict) a dict of informatio on cards to be used in the
        current game
        data: (dict) the data dict updated with game_cards and user inputs

    Gets user input (name, game_mode and card) and creates/assigns cards
    to each position on the canvas
    Calls load_images() to get images from images.cfg
    """

    # name must be 15 letters or less (to fit on leaderboard), contain no spaces (for reading the file)
    good_name = False
    name = str(
        tur.textinput(
            "Name",
            "Name must be 15 letters or less and contain no spaces. Enter another name.",
        )
    )

    while good_name is False:
        if " " in name or len(name) >= 15:
            name = str(
                tur.textinput(
                    "Name",
                    "Name must be 15 letters or less and contain no spaces. Enter another name.",
                )
            )
            good_name = False
        else:
            good_name = True

    # if no name provided, use "Guest"
    if name == "":
        name = "Guest"

    data["NAME"] = name

    T.goto(-410, 290)
    T.write(
        f"Welcome to The Matching Game, {name.capitalize()}!",
        font=("Helvetica Neue", 16, "bold"),
    )

    # allowed inputs
    modes = ["C", "B", "Classis", "Bangtan", ""]

    # get user choice for game mode, classic (using images in game), or bangtan (get images from .cfg file)
    game_mode = tur.textinput(
        "Game Mode", "What game would you like to play? C/Classic or B/Bangtan."
    ).capitalize()

    while game_mode not in modes:
        game_mode = tur.textinput(
            "Game Mode", "Please choose a game? C/Classic or B/Bangtan."
        ).capitalize()

    # if not game mode is provide, play classic mode
    if game_mode == "":
        game_mode = "C"

    data["game_mode"] = game_mode

    cards = int(
        tur.numinput("Game Mode", "Chose number of cards to play (8, 10, or 12).")
    )

    allowed_cards = [8, 10, 12]

    while cards not in allowed_cards:
        cards = int(
            tur.numinput(
                "Game Mode",
                "Cards must be one of the following (8, 10, or 12). Please choose again.",
            )
        )

    game_cards = load_images(cards, data)
    game_cards["cards"] = cards

    return game_cards, data


def load_images(cards, data, f="images.cfg"):
    """
    Function: load_images(cards, data, f="file../images.cfg")
    Parameters:
        cards: (int) user card number input
        data: (dict) a dictionary of data from the game
        f: (file) file with card image names
    Returns:
        game_cards: (dict) a dict with game card information

    Loads images from image.cfg and calls add_images() to determine
    which cards to use for current game
    """

    images = []
    images_match = []
    game_mode = data["game_mode"]
    nofile_id = None

    if game_mode == "B" or game_mode == "Bangtan":
        if try_file(f, "r"):
            with open(f, "r") as img_file:
                for line in img_file:
                    split_line = line.split()
                    if "back" not in split_line[0]:
                        img_name = split_line[0]
                        beg_name = split_line[:-4]
                        img_match = f"{split_line[0][:-4]}_match.gif"
                        images.append(f"../cfg_images/{img_name}")
                        images_match.append(f"../cfg_images/{img_match}")
        # if error, let user know; playing default/classic game
        else:
            T.goto(-180, 110)
            nofile_id = stamp_nofile("../images/nofile.gif")

    game_cards = add_images(images, images_match, data, cards)
    game_cards["nofile_img"] = nofile_id

    return game_cards


def add_images(images, images_match, data, cards):
    """
    Function: add_images(images, immage_match, data, cards)
    Parameters:
        images: (list) card images
        images_match: (list) match for cards in images
        data: (dict) a dictionary of data from the game
        cards: (int) user card number input
    Returns:
        game_cards: (dict) a dict with game card information

    Determined with set of cards to use for the current game
    depending on game_mode and if a file with images was provided
    Call create_canvas() start creating playing board
    """

    # dict to store game_cards data (images, matches, etc)
    game_cards = {}

    # if bangtan version
    if (
            images
            and images_match
            and (data["game_mode"] == "B" or data["game_mode"] == "Bangtan")
    ):
        cards_images = images
        cards_images_match = images_match

        back = "../cfg_images/back.gif"
        game_cards["back"] = back
        game_cards["cards_images"] = cards_images
        game_cards["cards_images_match"] = cards_images_match
        S.bgpic("../cfg_images/bg.gif")

        create_canvas(cards, data)

    # if classic version
    else:
        cards_images = [
            "../images/king_of_diamonds.gif",
            "../images/2_of_clubs.gif",
            "../images/2_of_diamonds.gif",
            "../images/3_of_hearts.gif",
            "../images/ace_of_diamonds.gif",
            "../images/jack_of_spades.gif",
        ]

        cards_images_match = [
            "../images/king_of_diamonds_match.gif",
            "../images/2_of_clubs_match.gif",
            "../images/2_of_diamonds_match.gif",
            "../images/3_of_hearts_match.gif",
            "../images/ace_of_diamonds_match.gif",
            "../images/jack_of_spades_match.gif",
        ]

        back = "../images/back.gif"
        game_cards["back"] = back
        game_cards["cards_images"] = cards_images
        game_cards["cards_images_match"] = cards_images_match

        S.bgpic("../images/bg.gif")
        create_canvas(cards, data)
    return game_cards


def create_canvas(cards, data):
    """
    Function: create_cavas(cards, data)
    Parameters:
        cards: (int) user card number input
        data: (dict) a dictionary of data from the game
    Returns:
        None

    Create the canvas drawing board and creating turtle for each section.
    Calls draw_rect() to draw and get positions for each section
    """

    POSITIONS = data["POSITIONS"]

    T.goto(-430, 290)

    # change main board size depending on number of cards
    if cards == 8 or cards == 12:
        game_width = 500
    else:
        game_width = 620

    # draw each section on the board to get coordinates to use later
    draw_rect(game_width, 360, data, "main")
    T.goto(POSITIONS["main"]["topr_x"] + 15, POSITIONS["main"]["topr_y"])

    draw_rect(200, 210, data, "scores")
    T.goto(POSITIONS["scores"]["bottoml_x"], POSITIONS["scores"]["bottoml_y"] - 15)

    draw_rect(200, 60, data, "tracker")
    T.goto(POSITIONS["tracker"]["bottoml_x"], POSITIONS["tracker"]["bottoml_y"] - 15)

    draw_rect(200, 40, data, "quit")
    T.goto(POSITIONS["main"]["topl_x"] + 20, POSITIONS["main"]["topl_y"] - 20)


def draw_rect(width, height, data, name):
    """
    Function: draw_rect(width, height, data, name)
    Parameters:
        width: (int) width of the section
        height: (int) height of the section
        data: (dict) a dictionary of data from the game
        cards: (int) user card number input
    Returns:
        None

    Draws a rectangle with provided width and height and saves
    the coordinate positions in data
    """

    pos = data["POSITIONS"][name]

    pos["topl_x"], pos["topl_y"] = round(T.xcor()), round(T.ycor())

    T.forward(width)
    pos["topr_x"], pos["topr_y"] = round(T.xcor()), round(T.ycor())
    T.right(90)

    T.forward(height)
    pos["bottomr_x"], pos["bottomr_y"] = round(T.xcor()), round(T.ycor())
    T.right(90)

    T.forward(width)
    pos["bottoml_x"], pos["bottoml_y"] = round(T.xcor()), round(T.ycor())
    T.right(90)

    T.forward(height)
    T.right(90)

    # create a turtle for each section on the board
    create_tur(pos, name)


def create_tur(pos, name):
    """
    Function: create_tur(pos, name)
    Parameters:
        pos: (dict) a dict of a section on the board
        name: (str) name of the section
    Returns:
        None

    Creates a turtle for a section on the board
    """

    pos["turtle"] = tur.Turtle(visible=False)
    pos["turtle"].speed("fastest")
    pos["turtle"].penup()


def place_cards(game_cards, data):
    """
    Function: place_cards_(game_cards, data)
    Parameters:
        game_cards: (dict) a dict with game card information
        data: (dict) a dictionary of data from the game
    Returns:
        game_cards: (dict) a dict with game card information
        data: (dict) a dictionary of data from the game

    Draws a rectangle for cards and saves coordinate positions in data
    """
    POSITIONS = data["POSITIONS"]
    cards = game_cards["cards"]

    # different number of rows depedning on number of cards
    if cards == 8 or cards == 10:
        if_two_rows(POSITIONS, cards)
    else:
        if_three_rows(POSITIONS, cards)
    return game_cards, data


def if_three_rows(POSITIONS, cards):
    """
    Function: if_three_rows(POSITIONS, cards)
    Parameters:
        cards: (int) number of cards in the game
        POSITIONS: (dict) a dictionary of data from the game
    Returns:
        None

    Draws a dict for cards if three rows are required, calls
    card_pos() to draw cards and save positions to POSITIONS
    """

    for i in range(int(cards / 3)):
        T.color("white")
        POSITIONS["images"][f"box_{i + 1}"] = {}
        card = POSITIONS["images"][f"box_{i + 1}"]

        # draws each card position on the board
        card_pos(card)

    T.goto(
        POSITIONS["images"]["box_1"]["bottoml_x"],
        POSITIONS["images"]["box_1"]["bottoml_y"] - 20,
    )

    for i in range(int(cards / 3), int(cards - cards / 3)):
        POSITIONS["images"][f"box_{i + 1}"] = {}
        card = POSITIONS["images"][f"box_{i + 1}"]

        # draws each card position on the board
        card_pos(card)

    T.goto(
        POSITIONS["images"]["box_5"]["bottoml_x"],
        POSITIONS["images"]["box_5"]["bottoml_y"] - 20,
    )

    for i in range(int(cards - cards / 3), cards):
        POSITIONS["images"][f"box_{i + 1}"] = {}
        card = POSITIONS["images"][f"box_{i + 1}"]

        # draws each card position on the board
        card_pos(card)


def if_two_rows(POSITIONS, cards):
    """
    Function: if_two_rows(POSITIONS, cards)
    Parameters:
        cards: (int) number of cards in the game
        POSITIONS: (dict) a dictionary of data from the game
    Returns:
        None

    Draws a dict for cards if two rows are required, calls
    card_pos() to draw cards and save positions to POSITIONS
    """

    for i in range(int(cards / 2)):
        POSITIONS["images"][f"box_{i + 1}"] = {}
        card = POSITIONS["images"][f"box_{i + 1}"]

        # draws each card position on the board
        card_pos(card)

    T.goto(
        POSITIONS["images"]["box_1"]["bottoml_x"],
        POSITIONS["images"]["box_1"]["bottoml_y"] - 20,
    )

    for i in range(int(cards - cards / 2), cards):
        POSITIONS["images"][f"box_{i + 1}"] = {}
        card = POSITIONS["images"][f"box_{i + 1}"]

        # draws each card position on the board
        card_pos(card)


# draw each card pos on the board to save coordinates to use later
def card_pos(card):
    """
    Function: if_three_rows(POSITIONS, cards)
    Parameters:
        cards: (int) number of cards in the game
        POSITIONS: (dict) a dictionary of data from the game
    Returns:
        None

    Draws a rectangle for cards and saves coordinate positions in data
    """

    T.forward(100)
    card["topr_x"], card["topr_y"] = round(T.xcor()), round(T.ycor())

    T.right(90)
    T.forward(150)
    card["bottomr_x"], card["bottomr_y"] = round(T.xcor()), round(T.ycor())

    T.right(90)
    T.forward(100)
    card["bottoml_x"], card["bottoml_y"] = round(T.xcor()), round(T.ycor())

    T.right(90)
    T.forward(150)
    card["topl_x"], card["topl_y"] = round(T.xcor()), round(T.ycor())

    T.right(90)
    T.forward(120)


def sort_cards(game_cards):
    """
    Function: sort_cards(game_cards)
    Parameters:
        game_cards: (dict) a dict with game card information
    Returns:
        shuffled: (list) a list of shuffled cards for the current game

    Creates a shuffles list of cards for the current game

    """

    cards = game_cards["cards"]
    cards_images = game_cards["cards_images"]
    cards_images_match = game_cards["cards_images_match"]
    pairs = cards / 2
    indices = []
    raw_pairs_list = []

    for i in range(int(pairs)):
        img = random.choice(cards_images)
        ind = cards_images.index(img)
        raw_pairs_list.append(img)
        indices.append(ind)
        cards_images.remove(img)

    for i in indices:
        img = cards_images_match[i]
        raw_pairs_list.append(img)
        cards_images_match.remove(img)

    # shuffled list of cards, both matches
    shuffled = random.sample(raw_pairs_list, len(raw_pairs_list))

    return shuffled


def create_board_objects(data):
    """
    Function: create_board_objects(data)
    Parameters:
        data: (dict) a dictionary of data from the game
    Returns:
        None

    Creates Board class instances of each section in data and saves it
    to Board class

    """

    # save each board section in a class, x, y, turtle and name variables
    boards = ["main", "scores", "tracker", "quit"]
    for a, b in data["POSITIONS"].items():
        if a in boards:
            name = a
            tur = b["turtle"]
            x = b["topl_x"]
            y = b["topl_y"]
            box = Board(name, tur, x, y)


# create an object to save game data needed to run the game
def create_game_data_objects(data):
    """
    Function: create_data_objects(data)
    Parameters:
        data: (dict) a dictionary of data from the game
    Returns:
        None

    Creates GameData instances of data in data and saves it
    to GameData class

    """
    name = data["NAME"]
    leaders = data["LEADERS"]
    guesses = 0
    matches = 0
    clicked_cards = []

    obj = GameData(name, leaders, matches, guesses, clicked_cards)


# place face-down cards at each card pos
def facedown_cards(game_cards, data):
    """
    Function: facedown_cards(game_cards, data)
    Parameters:
        game_cards: (dict) a dict with game card information
        data: (dict) a dictionary of data from the game
    Returns:
        None

    Places facedown cards at each card positon on the game board,
    assigns a card image to each card and saves information to data
    """

    T.speed("fast")
    POSITIONS = data["POSITIONS"]

    cards = game_cards["cards"]
    back = game_cards["back"]

    shuffled = sort_cards(game_cards)
    game_cards["shuffled"] = shuffled

    # clear error message if any
    if game_cards["nofile_img"]:
        T.clearstamp(game_cards["nofile_img"])
    # add back to shapes
    S.addshape(back)
    T.shape(back)

    # place facedown cards and then randomly assign a card at each card pos
    for i in range(cards):
        card = POSITIONS["images"][f"box_{i + 1}"]
        T.goto((card["topl_x"]) + 50, (card["topl_y"]) - 75)
        stamp = T.stamp()
        card["back_stamp"] = stamp
        card["name"] = f"box_{i + 1}"
        card["card"] = shuffled[i]
        card["clicked"] = False

    T.speed("fastest")


def create_card_objects(data):
    """
    Function: create_card_objects(data)
    Parameters:
        data: (dict) a dictionary of data from the game
    Returns:
        None

    Creates Card instances of each card in data["images"] and saves it
    to the Card class
    """
    # save each card as an object in the Card class
    for b in data["POSITIONS"]["images"]:
        name = data["POSITIONS"]["images"][b]["name"]
        image = data["POSITIONS"]["images"][b]["card"]
        x = data["POSITIONS"]["images"][b]["topl_x"]
        y = data["POSITIONS"]["images"][b]["topl_y"]
        back_stamp = data["POSITIONS"]["images"][b]["back_stamp"]

        box = Card(name, image, x, y, back_stamp)


def set_tracking(data):
    """
    Function: set_tracking()
    Parameters:
        data: (dict) a dictionary of data from the game
    Returns:
        None

    Keeps track of leaderboard, matches and guesses for each game
    and updates with they're updated
    """

    for a in Board.instances:
        if a.name == "scores":
            sco = a.tur
            x = a.x
            y = a.y

    # write leaderboard titles
    sco.goto(x + 100, y - 30)
    sco.write(f"LEADERBOARD", align="center", font=("Arial", 16, "bold"))
    sco.goto(x + 20, y - 50)
    sco.write(f"Name\t\tScore", align="left", font=("Arial", 14, "bold"))

    if data["nofile_l"] is True:
        T.goto(x + 100, y - 150)
        stamp_nofile("../images/leaderboard_error.gif")
    else:
        scores()

    # write tracking title
    tracker()


def scores():
    """
    Function: scores()
    Parameters:
        None
    Returns:
        None

    Write leaderboard information on game board at beginning of
    each game using information in GameData class
    Call find_duplicates() to deal with duplicate names;
    remove_duplicates() to pick only lowest score data
    """

    for a in Board.instances:
        if a.name == "scores":
            sco = a.tur
            x = a.x
            y = a.y

    sco.goto(x + 20, y - 80)

    # fine duplicate name and choose the one with the lowest score
    leader_names, new_leaders = find_duplicates()
    new_leaders = remove_duplicates(new_leaders)

    # sort leaders from lowest score to highest
    new_leaders.sort(key=lambda x: x[1][1])

    for tup in new_leaders[0:8]:
        leader_names.append(tup[0])
        sco.color("white")
        sco.write(
            f"{tup[1][0][:7]}\t\t    {tup[1][1]}",
            align="left",
            font=("Arial", 14, "bold"),
        )

        current_x, current_y = sco.xcor(), sco.ycor()

        # move to next line
        sco.goto(current_x, current_y - 20)


def find_duplicates():
    """
    Function: find_duplicates()
    Parameters:
        None
    Returns:
        None

    Finds duplicate names in leaders dict from GameData
    Calls id_duplicates() to determine names that show up more than once
    """

    # get leaders dict from GameData
    for o in GameData.obj:
        leaders = o.leaders

    leader_names = []
    new_leaders = []

    for t in leaders.items():
        leader_names.append(t[1][0])
    for n in leader_names:
        if leader_names.count(n) > 1:
            id_duplicates(n, leaders, new_leaders)
        else:
            for t in leaders.items():
                if t[1][0] == n:
                    new_leaders.append(t)

    return leader_names, new_leaders


def id_duplicates(n, leaders, new_leaders):
    """
    Function: id_duplicates(n, leaders, new_leaders)
    Parameters:
        n: (str) names that show up more than once
        leaders: (dict) leaders and scores from GameData class
        new_leaders: (list) itmes with names that show up only once
    Returns:
        None

    Identifies duplicates and determines the lowest score; appends lowest
    score item to new_leaders
    """

    scores = []
    score_num = None

    for t in leaders.items():
        if t[1][0] == n:
            scores.append(t[1][1])

    score_num = min(scores)

    for t in leaders.items():
        if t[1][0] == n and t[1][1] == score_num:
            new_leaders.append(t)


def remove_duplicates(new_leaders):
    """
    Function: remove_duplicates(new_leaders)
    Parameters:
        new_leaders: (list) itmes with names that show up only once
    Returns:
        new_leaders: (list) itmes with names that show up only once

    Identifies duplicates items in new_leaders() and returns new list
    """

    for t in new_leaders:
        if new_leaders.count(t) > 1:
            new_leaders.remove(t)

    return new_leaders


def tracker():
    """
    Function: tracker()
    Parameters:
        None
    Returns:
        None

    Updates guesses and matches for current game by reading
    data from GameData
    """

    for a in Board.instances:
        if a.name == "tracker":
            tr = a.tur
            x = a.x
            y = a.y

    for o in GameData.obj:
        guesses = o.guesses
        matches = o.matches

    # clear tracker and re_write them on update
    tr.clear()

    tr.color("black")
    tr.goto(x + 100, y - 40)
    tr.write(f"Status: ", move=True, align="center", font=("Arial", 14, "bold"))
    tr.forward(20)

    tr.color("white")
    tr.goto(x + 20, y - 60)
    tr.write(
        f"Guesses: {guesses}   Matches: {matches}",
        move=True,
        align="left",
        font=("Arial", 14, "normal"),
    )
    tr.forward(20)


def add_quit():
    """
    Function: add_quit()
    Parameters:
        None
    Returns:
        None

    Adds quit button to the game board
    """

    for a in Board.instances:
        if a.name == "quit":
            q = a.tur
            x = a.x
            y = a.y

    q.goto(x + 100, y - 20)
    S.addshape("../images/quit_button.gif")
    q.shape("../images/quit_button.gif")
    a.stamp = q.stamp()


def on_click(x, y):
    """
    Function: on_click(x, y)
    Parameters:
        x: (int) x coordinate of the turtle
        y: (int) y coordinate of the turtle
    Returns:
        None

    Determines what to do when user clicks on game board
    """

    for q in Board.instances:
        if q.name == "quit":
            q = q

    for o in GameData.obj:
        clicked_cards = o.clicked_cards

    # function to handle different click positions
    if_click_conditions(q, clicked_cards, x, y)


def if_click_conditions(q, clicked_cards, x, y):
    """
    Function: if_click_conditions(q, clicked_cards, x, y)
    Parameters:
        q: (object) quit section object from Board class
        clicked_cards: (list) clicked_cards list from GameData class
        x: (int) x coordinate of the turtle
        y: (int) y coordinate of the turtle
    Returns:
        None

    Handled difference conditions based on where the user clicked
    """

    # if game is won, close turtle
    if T.shape() == "../images/won.gif":
        S.bye()

    # if no cards in instance list in Card, game is won
    elif len(Card.instances) == 0:
        won_game()

    # if user quits, close turtle
    elif T.shape() == "../images/quit.gif":
        S.bye()

    # if user clicks quit button
    elif x in range(q.x + 75, q.x + 150) or y in range(q.y - 20, q.y - 80):
        quit_game()

    # handle other types of click (ie. clicked on card)
    else:

        # if not two cards yet, allow clicks
        if len(clicked_cards) < 2:
            two_clicks(x, y)

        # if two cards clicked, compare them on next click
        else:
            match_cards()
            tracker()


def two_clicks(x, y):
    """
    Function: two_clicks(x, y)
    Parameters:
        x: (int) x coordinate of the turtle
        y: (int) y coordinate of the turtle
    Returns:
        None

    Adds clicks to cliked_cards list if user clicks on cards
    """

    for o in GameData.obj:
        clicked_cards = o.clicked_cards

    # get card objects from Card class
    for box in Card.instances:
        box_x = box.x
        box_y = box.y

        # check in click is in range of any card pos
        if (
                x in range(box_x, box_x + 100)
                and y in range(box_y - 150, box_y)
                and box.clicked is not True
        ):
            # get card img, pos and flip card
            card_img = box.image
            x_pos = box.x
            y_pos = box.y

            S.addshape(card_img)
            T.shape(card_img)
            T.goto(x_pos + 50, y_pos - 75)
            box.card_stamp = T.stamp()
            box.clicked = True

            # add to clicked_list (will only take up to 2 cards)
            clicked_cards.append(box)


def match_cards():
    """
    Function: match_Cards()
    Parameters:
        None
    Returns:
        None

    Determines if the two cards in clicked_card match or not
    """

    # get clickec_card list and compare items
    for o in GameData.obj:
        clicked_cards = o.clicked_cards

    # use __eq__() to compare cards
    a, b = clicked_cards[0], clicked_cards[1]

    if a == b:

        # what to do if they match
        cards_match(a, b)
    else:

        # what to do if they don't match
        cards_no_match(a, b)


def cards_match(a, b):
    """
    Function: cards_match(a, b)
    Parameters:
        a: (object) first Card object in clicked_cards list
        b: (object) second Card object in clicked_cards list
    Returns:
        None

    Updates GameData and clears approriate stamps and lists if the two objects match
    """

    # update tracker information and clear stamps if cards match
    for o in GameData.obj:
        o.matches += 1
        o.guesses += 1
        clicked_cards = o.clicked_cards

    tracker()
    T.clearstamp(a.card_stamp)
    T.clearstamp(a.back_stamp)
    T.clearstamp(b.card_stamp)
    T.clearstamp(b.back_stamp)

    # remove cards objects from Card class
    Card.instances.remove(a)
    Card.instances.remove(b)

    # cleard clicked_Card list in GameData class
    clicked_cards.clear()


def cards_no_match(a, b):
    """
    Function: cards_no_match(a, b)
    Parameters:
        a: (object) first Card object in clicked_cards list
        b: (object) second Card object in clicked_cards list
    Returns:
        None

    Updates GameData and clears appropriate stamps and lists if the two objects match
    """

    # updater GameData and reset everything else
    for o in GameData.obj:
        o.guesses += 1
        clicked_cards = o.clicked_cards

    T.clearstamp(a.card_stamp)
    T.clearstamp(b.card_stamp)

    a.clicked = False
    b.clicked = False

    clicked_cards.clear()


def won_game():
    """
    Function: won_game()
    Parameters:
        None
    Returns:
        None

    Let's user know they've won if board is cleared
    """

    for a in Board.instances:
        if a.name == "main":
            m_x = a.x
            m_y = a.y

    for o in GameData.obj:
        name = o.name
        guesses = o.guesses

    # update leaders file by adding to the end of file; if file doesn't exist, create it
    if try_file("leaders.txt", "r"):
        with open("leaders.txt", "a") as f:
            name = name
            score = guesses
            f.write(f"\n{name.capitalize()} {score}")
            f.close()

    # how to handle if file doesnt exist, create new one
    else:
        with open("leaders.txt", "a") as f:
            name = name
            score = guesses
            f.write("Name Scores")
            f.write(f"\n{name.capitalize()} {score}")
            f.close()

    # stamo win msg
    T.goto(m_x + 250, m_y - 180)
    S.addshape("../images/won.gif")
    T.shape("../images/won.gif")
    T.stamp()


def quit_game():
    """
    Function: quit_game()
    Parameters:
        None
    Returns:
        None

    Shows message when quit_button is clicked
    """

    # stamp quit msg if user clicks quit button
    for a in Board.instances:
        if a.name == "main":
            m_x = a.x
            m_y = a.y

    S.addshape("../images/quit.gif")
    T.shape("../images/quit.gif")
    T.goto(m_x + 250, m_y - 180)
    T.stamp()
