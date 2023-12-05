import arcade
import pathlib

""" This is the main constant for the game """

# Game constants

NEW_SCALING = 1

# Colours for darkening sky
FRESH_AIR = (166, 231, 255)
FRESH_AIR_90 = (154,215,237)
FRESH_AIR_80 = (148,206,227)
FRESH_AIR_70 = (138,192,212)
FRESH_AIR_60 = (133,185,204)
FRESH_AIR_50 = (126,176,194)
FRESH_AIR_40 = (106,148,163)
FRESH_AIR_30 = (101,141,156)
FRESH_AIR_20 = (88,123,135)
FRESH_AIR_10 = (75,104,115)
FRESH_AIR_0 = (53,74,82)

# Window dimensions
SCREEN_WIDTH = int(1000 * NEW_SCALING)
SCREEN_HEIGHT = int(650 * NEW_SCALING)
SCREEN_TITLE = "Hackathon Arcade Game"

# Scaling constants
MAP_SCALING = 1

# Player constants
GRAVITY = 1.0
PLAYER_START_X = 65 * NEW_SCALING
PLAYER_START_Y = 256 * NEW_SCALING
PLAYER_MOVE_SPEED = 6
PLAYER_JUMP_SPEED = 25

# Viewport (horizontal/vertical scroll) margins
# How close do we have to be to scroll the viewport?
# Note the difference between LEFT_VIEWPORT_MARGIN and RIGHT_VIEWPORT_MARGIN.
# This allows the alien to get closer to the left edge than the right.
LEFT_VIEWPORT_MARGIN = int(50 * NEW_SCALING)
RIGHT_VIEWPORT_MARGIN = int(850 * NEW_SCALING)
TOP_VIEWPORT_MARGIN = int(300 * NEW_SCALING)
BOTTOM_VIEWPORT_MARGIN = int(150 * NEW_SCALING)

# Number of lives the player can use to win the game
TOTAL_LIFE_COUNT = 5

# Assets path
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent.parent / "assets"


# Minimap config - Background color must include an alpha component
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color((239, 222, 205, 150))
MAP_WIDTH = {1: 4800, 2: 4800, 3: 6400, 4: 6400}
MAP_HEIGHT = {1: 1024, 2: 1280, 3: 2560, 4: 2560}
MINIMAP_WIDTH = {1: 288, 2: 288, 3: 384, 4: 384}
MINIMAP_HEIGHT = {1: 64, 2: 80, 3: 160, 4: 160}

IDLE_COMMAND_TIME = 5
IDLE_TEXT_DURATION = 3

# Speech bubble texts
WELCOME_TEXTS = [
    "Showtime, baby!",
    "Howdy folks!",
]
BOSS_FIGHT_TEXTS = [
    "Everything seems to get slower...",
    "I'm feeling... weird...",
    "What's happening to me?",
    "Someone said IE was not a real browser...I'm starting to believe them...",
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
IE_KILLED_TEXTS = [
    "I'm not sure what I expected",
    "What just happened?",
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
