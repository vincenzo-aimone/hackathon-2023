"""
Blueface November 2023 - Hackathon Arcade Game
"""
import os
from dotenv import load_dotenv

import arcade  # This is the main library our arcade game is built with

from arcade_game.arcade_platformer.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from arcade_game.arcade_platformer.player.player import Player
from arcade_game.arcade_platformer.view import welcome_view
from log.config_log import logger

if __name__ == "__main__":

    logger.info("Game started")

    # Load environment variables
    load_dotenv()
    
    # 1st let's check the speech venv variables were properly set, if not let's throw an error with instructions
    if not os.environ.get('SPEECH_API_KEY') and not os.environ.get('SPEECH_REGION'):
        raise Exception("You need to set the speech key and speech region. Read readme file for instructions.")

    window = arcade.Window(
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE
    )

    global_player: Player = Player()

    welcome_view = welcome_view.WelcomeView(global_player)
    window.show_view(welcome_view)

    arcade.run()

    # Closes the speech processor when the game is closed
    if welcome_view.game_view and welcome_view.game_view.recognize_proc:
        welcome_view.game_view.recognize_proc.terminate()

    logger.info("Game closed")
