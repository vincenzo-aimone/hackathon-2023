import arcade
import pathlib

""" This is the main constant for the game """

# Game constants

# Window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Hackathon Arcade Game"

# Scaling constants
MAP_SCALING = 1.0

# Player constants
GRAVITY = 1.0
PLAYER_START_X = 65
PLAYER_START_Y = 256
PLAYER_MOVE_SPEED = 20
PLAYER_JUMP_SPEED = 25

# Viewport (horizontal/vertical scroll) margins
# How close do we have to be to scroll the viewport?
# Note the difference between LEFT_VIEWPORT_MARGIN and RIGHT_VIEWPORT_MARGIN.
# This allows the alien to get closer to the left edge than the right.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 150

# Number of lives the player can use to win the game
TOTAL_LIFE_COUNT = 5

# Assets path
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent.parent / "assets"


# Minimap config - Background color must include an alpha component
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color((239, 222, 205, 80))
MAP_WIDTH = {1: 3200, 2: 4800, 3: 6400, 4: 6400}
MAP_HEIGHT = {1: 1024, 2: 1280, 3: 2560, 4: 2560}
MINIMAP_WIDTH = {1: 192, 2: 288, 3: 384, 4: 384}
MINIMAP_HEIGHT = {1: 64, 2: 80, 3: 160, 4: 160}

IDLE_COMMAND_TIME = 5
IDLE_TEXT_DURATION = 3

# Speech bubble texts
WELCOME_TEXTS = [
    "Showtime, baby!",
    "Howdy folks!",
]
LADDER_TEXTS = [
    "This is exhausting! I need a vacation...",
    "Damn! I should go to the gym more often",
    "Aaargh....my back",
    "If this is a dream, I hate you my unconscious",
]
IDLE_TEXTS = [
    "What kinda planet has no pubs ANYWHERE...",
    "Kowabunga, let's get some pizza!",
    "I mean, what kinda name is Scrummy Bears anyway...",
    "If you wanna be listened to in life, you gotta speak up",
    "Stop mumbling, alien up!",
    "Argh, speak louder, and speak earlier!"
]
DYING_TEXTS = [
    "Ah, well done!",
    "Salvation... at last",
    "Well.. thanks for nothing",
]
ENEMY_KILLED_TEXTS = [
    "You don't mess with the Roz..an",
    "Was that meant to be challenging or something?",
    "This is getting boring now.."
]

ENEMY_STATIC_INFO = {
    "ladybug": {
        "default_state": arcade.FACE_LEFT,

    }
}

ENEMIES = {
    1: [
        # {
        #     "name": "ladybug",
        #     "center_x": 2200,
        #     "center_y": 640,
        #     "state": arcade.FACE_LEFT,
        #     "speed": 6,
        # }
    ],
    2: [],
    3: [],
    4: [],
}
