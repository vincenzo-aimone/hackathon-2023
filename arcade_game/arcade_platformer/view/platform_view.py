import logging
from time import sleep
from timeit import default_timer
from multiprocessing import Process, Queue
import os
import arcade

from speech.speech_recognition import speech_to_text_continuous
from arcade_game.arcade_platformer.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, TOTAL_LIFE_COUNT, ASSETS_PATH, \
    MAP_SCALING, PLAYER_START_X, PLAYER_START_Y, GRAVITY, LEFT_VIEWPORT_MARGIN, RIGHT_VIEWPORT_MARGIN, \
    TOP_VIEWPORT_MARGIN, BOTTOM_VIEWPORT_MARGIN, PLAYER_MOVE_SPEED, PLAYER_JUMP_SPEED
from arcade_game.arcade_platformer.player.player import Player
from . import game_over_view, winner_view


class PlatformerView(arcade.View):
    """
    Displays the platform game view, where you can interact with the player
    """
    def __init__(self, player: Player) -> None:
        """The init method runs only once when the game starts"""
        super().__init__()

        self.game_player = player

        # These lists will hold different sets of sprites
        self.coins = None
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.traps = None

        # Avoids leaving the mouse pointer in the middle
        self.window.set_mouse_visible(False)

        # One sprite for the player, no more is needed
        self.player = self.game_player.player

        # We need a physics engine as well
        self.physics_engine = None

        # Someplace to keep score
        self.score = 0

        # Life count init
        self.life_count = TOTAL_LIFE_COUNT

        # Start the timer
        self.time_start = default_timer()  # integer, expressing the time in seconds

        # Which level are we on?
        self.level = 1

        # Instantiate some variables that we will initialise in the setup function
        self.map_width = 0
        self.view_left = 0
        self.view_bottom = 0

        # Load up our sound effects here
        self.ready_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "ready.wav")
        )
        self.go_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "go.wav")
        )
        self.coin_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "coin.wav")
        )
        self.jump_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "jump.wav")
        )
        self.level_victory_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "level_victory.wav")
        )
        self.death_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "death.wav")
        )

        # Init object for the process
        self.recognize_proc = None
        self.message_queue = None
        self.current_command = None

        # Play the game start sound animation
        # There is a lag with the 1st sound played so to avoid having a lag during the game
        # when we take the 1st coin we play a sound for the start of the game
        arcade.play_sound(self.ready_sound)
        sleep(1)
        arcade.play_sound(self.go_sound)

    def setup(self):
        """Sets up the game for the current level. This runs every time we load a new level"""

        # Get the current map based on the level
        map_name = f"platform_level_{self.level:02}.tmx"
        map_path = ASSETS_PATH / map_name

        # use_spatial_hash : If set to True, this will make moving a sprite in the SpriteList slower,
        # but it will speed up collision detection with items in the SpriteList.
        # Great for doing collision detection with static walls/platforms.
        layer_options = {
            "background": {"use_spatial_hash": False},
            "coins": {"use_spatial_hash": True},
        }

        # Load the current map
        game_map = arcade.load_tilemap(
            map_path, layer_options=layer_options, scaling=MAP_SCALING
        )

        # Load the layers
        self.background = game_map.sprite_lists["background"]
        self.goals = game_map.sprite_lists["goal"]
        self.walls = game_map.sprite_lists["ground"]
        self.coins = game_map.sprite_lists["coins"]

        # Only load ladders in maps with some ladders
        if "ladders" in game_map.sprite_lists:
            self.ladders = game_map.sprite_lists["ladders"]

        # Only load traps in maps with some traps
        if "traps" in game_map.sprite_lists:
            self.traps = game_map.sprite_lists["traps"]

        # Set the background color
        background_color = arcade.color.FRESH_AIR
        if game_map.background_color:
            background_color = game_map.background_color
        arcade.set_background_color(background_color)

        # Find the edge of the map to control viewport scrolling
        # game_map.width : width expressed in number of tiles
        # game_map.tile_width : width of a given tile in pixels
        # Subtracting 1 from game_map.width corrects for the tile indexing used by Tiled.
        self.map_width = (game_map.width - 1) * game_map.tile_width

        # Create the player sprite if they're not already set up
        if not self.player:
            self.player = Player().create_player_sprite()

        # Move the player sprite back to the beginning
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        self.player.change_x = 0
        self.player.change_y = 0

        # Reset the viewport (horizontal scroll)
        self.view_left = 0
        self.view_bottom = 0

        # Load the physics engine for this map
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.walls,
            gravity_constant=GRAVITY,
            ladders=self.ladders,
        )
        self.game_player.set_physics_engine(self.physics_engine)

        # Start the process for Speech Recognition
        self.message_queue = Queue()
        self.recognize_proc = Process(target=speech_to_text_continuous, kwargs={
            "message_queue": self.message_queue,
            "api_key": os.environ.get('SPEECH_API_KEY'),
            "speech_region": os.environ.get('SPEECH_REGION')}, name="T1")
        self.recognize_proc.start()

    def get_game_time(self) -> int:
        """Returns the number of seconds since the game was initialised"""
        return int(default_timer() - self.time_start)

    def scroll_viewport(self) -> None:
        """
        Scrolls the viewport, horizontally and vertically, when the player gets close to the edges
        This also catches the player falling from a platform, which counts as a death
        """
        # Scroll left
        # Find the current left boundary
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN

        # Are we to the left of this boundary? Then we should scroll left.
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            # But don't scroll past the left edge of the map
            if self.view_left < 0:
                self.view_left = 0

        # Scroll right
        # Find the current right boundary
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN

        # Are we to the right of this boundary? Then we should scroll right.
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            # Don't scroll past the right edge of the map
            if self.view_left > self.map_width - SCREEN_WIDTH:
                self.view_left = self.map_width - SCREEN_WIDTH

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom

        # Catch a fall of the platform
        # -300 rather than 0 is to let the player fall a bit longer, it looks better
        if self.player.bottom < -300:
            self.handle_player_death()
            return

        # Only scroll to integers, otherwise we end up with pixels that don't line up on the screen.
        self.view_bottom = int(self.view_bottom)
        self.view_left = int(self.view_left)

        # Do the actual scrolling
        arcade.set_viewport(
            left=self.view_left,
            right=SCREEN_WIDTH + self.view_left,
            bottom=self.view_bottom,
            top=SCREEN_HEIGHT + self.view_bottom,
        )

    def handle_player_death(self):
        """
            The player has fallen off the platform or walked into a trap:
            - Play a death sound
            - Decrease life counter
            - Send it back to the beginning of the level
            - Face the player forward
        """
        # Stop the speech recognition process
        self.recognize_proc.terminate()

        # Play the death sound
        arcade.play_sound(self.death_sound)
        # Add 1 second of waiting time to let the user understand they fell
        sleep(1)
        # Decrease life count
        self.life_count -= 1
        # Check if the player has any life left, if not trigger the game over animation
        if self.life_count == 0:
            self.handle_game_over()
        else:
            # Back to the level's beginning
            self.setup()
            # Set the player to face right, otherwise it looks odd as the player still looks like falling
            self.player.state = arcade.FACE_RIGHT

    def on_key_press(self, key: int, modifiers: int):
        """Processes key presses

        Arguments:
            key {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were down at the time
        """

        # Check for player left or right movement
        if key in [arcade.key.LEFT, arcade.key.J]:  # Either left key or J key to go left
            self.player.change_x = -PLAYER_MOVE_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.L]:  # Either right key or L key to go right
            self.player.change_x = PLAYER_MOVE_SPEED

        # Check if player can climb up or down
        elif key in [arcade.key.UP, arcade.key.I]:  # Either up key or I key to go up
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVE_SPEED
        elif key in [arcade.key.DOWN, arcade.key.K]:  # Either down key or K key to down
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVE_SPEED

        # Check if player can jump
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                # Play the jump sound
                arcade.play_sound(self.jump_sound)

    def on_key_release(self, key: int, modifiers: int):
        """Processes key releases

        Arguments:
            key {int} -- Which key was released
            modifiers {int} -- Which modifiers were down at the time
        """
        # Check for player left or right movement
        if key in [
            arcade.key.LEFT,
            arcade.key.J,
            arcade.key.RIGHT,
            arcade.key.L,
        ]:
            self.player.change_x = 0

        # Check if player can climb up or down
        elif key in [
            arcade.key.UP,
            arcade.key.I,
            arcade.key.DOWN,
            arcade.key.K,
        ]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0
    
    def on_update(self, delta_time: float):
        """Updates the position of all game objects

        Arguments:
            delta_time {float} -- How much time since the last call
        """

        # Update the player animation
        self.player.update_animation(delta_time)

        # Update player movement based on the physics engine
        self.physics_engine.update()

        # Restrict user movement so they can't walk off-screen
        if self.player.left < 0:
            self.player.left = 0

        # Check if we've picked up a coin
        coins_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.coins
        )

        for coin in coins_hit:
            # Add the coin score to our score
            self.score += int(coin.properties["point_value"])

            # Play the coin sound
            arcade.play_sound(self.coin_sound)

            # Remove the coin
            coin.remove_from_sprite_lists()

        # Check for trap collision, only in maps with traps
        if self.traps is not None:
            trap_hit = arcade.check_for_collision_with_list(
                sprite=self.player, sprite_list=self.traps
            )

            if trap_hit:
                self.handle_player_death()
                return

        # Now check if we are at the ending goal
        goals_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.goals
        )

        if goals_hit:
            # Stop the speech recognition process
            self.recognize_proc.terminate()

            if self.level == 4:  # Game is finished : Victory !
                self.handle_victory()
            else:
                # Play the level victory sound
                self.level_victory_sound.play()
                # Add a small waiting time to avoid jumping too quickly into the next level
                sleep(1)

                # Set up the next level and call setup again to load the new map
                self.level += 1
                self.setup()
        else:
            # Set the viewport, scrolling if necessary
            self.scroll_viewport()

    def handle_game_over(self):
        """
        Game Over !
        """
        # Show the Game Over Screen
        _game_over_view = game_over_view.GameOverView(self.game_player)
        self.window.show_view(_game_over_view)

    def handle_victory(self):
        """
        Victory !
        """
        # Show the winner Screen
        _winner_view = winner_view.WinnerView(self.game_player)
        # Calculate final score
        _winner_view.score = self.calculate_score()
        self.window.show_view(_winner_view)

    def calculate_score(self) -> int:
        """
        The final score is the score (gained by collecting coins)
        plus a time bonus
        """
        return self.score + (100 - self.get_game_time())

    def on_draw(self):
        """
        This is the display feature. The real logic is in on_update
        """
        arcade.start_render()

        # Draw all the sprites
        self.background.draw()
        self.walls.draw()
        self.coins.draw()
        self.goals.draw()

        # Not all maps have ladders
        if self.ladders is not None:
            self.ladders.draw()

        # Not all maps have traps
        if self.traps is not None:
            self.traps.draw()

        # Draw the dynamic elements : play, score, life count
        self.player.draw()
        self.draw_score()
        self.draw_life_count()
        self.draw_timer()

    def draw_score(self):
        """
        Draw the score in the lower left
        """
        # Find the coin image in the images folder
        score_image_path = ASSETS_PATH / "images" / "items" / "coinGold.png"

        # Load our score image
        score_image = arcade.load_texture(score_image_path)
        arcade.draw_texture_rectangle(
            30 + self.view_left,
            30 + self.view_bottom,
            70, 70, score_image)

        # First set a black background for a shadow effect
        arcade.draw_text(
            str(self.score),
            start_x=60 + self.view_left,
            start_y=15 + self.view_bottom,
            color=arcade.csscolor.BLACK,
            font_size=30
        )
        # Now in white, slightly shifted
        arcade.draw_text(
            str(self.score),
            start_x=62 + self.view_left,
            start_y=17 + self.view_bottom,
            color=arcade.csscolor.WHITE,
            font_size=30
        )

    def draw_life_count(self):
        """
        Display the life count on the bottom left after the score
        """
        # Find the heart images in the images folder
        life_full_path = ASSETS_PATH / "images" / "HUD" / "hudHeart_full.png"
        life_half_path = ASSETS_PATH / "images" / "HUD" / "hudHeart_half.png"
        life_empty_path = ASSETS_PATH / "images" / "HUD" / "hudHeart_empty.png"

        # Display a full heart by default
        life_image_path = life_full_path
        if self.life_count == 2:  # display the half-full heart
            life_image_path = life_half_path
        elif self.life_count == 1:  # display the empty heart
            life_image_path = life_empty_path

        # Load our score image
        life_image = arcade.load_texture(life_image_path)
        arcade.draw_texture_rectangle(
            960 + self.view_left,
            620 + self.view_bottom,
            70, 70, life_image)

    def draw_timer(self):
        """
        Display the game timer on the bottom left after the life count
        """
        # Find the coin image in the images folder
        clock_image_path = ASSETS_PATH / "images" / "items" / "clock.png"

        # Load our score image
        clock_image = arcade.load_texture(clock_image_path)
        arcade.draw_texture_rectangle(
            170 + self.view_left,
            30 + self.view_bottom,
            35, 35, clock_image)

        # Draw the timer in the lower left, after the score
        timer_text = str(self.get_game_time())

        # First set a black background for a shadow effect
        arcade.draw_text(
            timer_text,
            start_x=190 + self.view_left,
            start_y=15 + self.view_bottom,
            color=arcade.csscolor.BLACK,
            font_size=30
        )

        # Now in white
        arcade.draw_text(
            timer_text,
            start_x=192 + self.view_left,
            start_y=17 + self.view_bottom,
            color=arcade.csscolor.WHITE,
            font_size=30
        )
