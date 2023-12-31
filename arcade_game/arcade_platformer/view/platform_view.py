from log.config_log import logger
from time import sleep, time
from timeit import default_timer
from multiprocessing import Process, Queue
from uuid import uuid4
import os
import random
import arcade

from speech.speech_recognition import speech_to_text_continuous
# from arcade_game.arcade_platformer.config.config import BOSS_FIGHT_TEXTS, SCREEN_WIDTH, SCREEN_HEIGHT, TOTAL_LIFE_COUNT, ASSETS_PATH, \
#     MAP_SCALING, PLAYER_START_X, PLAYER_START_Y, GRAVITY, LEFT_VIEWPORT_MARGIN, RIGHT_VIEWPORT_MARGIN, \
#     TOP_VIEWPORT_MARGIN, BOTTOM_VIEWPORT_MARGIN, PLAYER_MOVE_SPEED, PLAYER_JUMP_SPEED, MINIMAP_HEIGHT, MINIMAP_WIDTH, \
#     MAP_WIDTH, MAP_HEIGHT, MINIMAP_BACKGROUND_COLOR, LADDER_TEXTS, WELCOME_TEXTS, ENEMIES, ENEMY_KILLED_TEXTS, \
#     IDLE_COMMAND_TIME, IDLE_TEXTS, IDLE_TEXT_DURATION, IE_KILLED_TEXTS
from arcade_game.arcade_platformer.config.config import *
from arcade_game.arcade_platformer.player.player import Player
from arcade_game.arcade_platformer.enemies.enemy import create_enemy
from . import game_over_view, winner_view


class PlatformerView(arcade.View):
    """
    Displays the platform game view, where you can interact with the player
    """
    def __init__(self, player: Player) -> None:
        """The init method runs only once when the game starts"""
        super().__init__()

        self.game_player = player

        self._init_static_elements()
        self._init_actors()
        self._init_dynamic_elements()
        self._init_map_variables()
        self._init_minimap_variables()
        self._init_sounds()
        self._init_speech_recognizer()
        self._init_cheat_flags()

        # Avoids leaving the mouse pointer in the middle
        self.window.set_mouse_visible(False)

        # Play the game start sound animation
        # There is a lag with the 1st sound played so to avoid having a lag during the game
        # when we take the 1st coin we play a sound for the start of the game
        arcade.play_sound(self.ready_sound)
        sleep(1)
        arcade.play_sound(self.go_sound)

    def _init_static_elements(self):
        self.coins = arcade.SpriteList()
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.traps = None

    def _init_actors(self):
        self.enemies = arcade.SpriteList()
        self.enemies_dead = arcade.SpriteList()
        self.engine = arcade.SpriteList()
        self.player = self.game_player.player

    def _init_dynamic_elements(self):
        self.physics_engine = None
        self.score = 0
        self.life_count = TOTAL_LIFE_COUNT
        self.level = 3
        self.time_start = default_timer()  # integer, expressing the time in seconds
        self.effects = arcade.SpriteList()

    def _speak_random(self, text_list, duration=3, force=False):
        """
        Takes a list of texts to and our character speaks (in a bubble)
        for the duration given.
        """
        logger.info("SPEAK RANDOM INVOKED")
        self._speak(random.choice(text_list), duration, force)

    def _init_map_variables(self):
        self.map_width = 0
        self.view_left = 0
        self.view_bottom = 0

    def _init_minimap_variables(self):
        # List of all our minimaps (there's just one)
        self.minimap_sprite_list = None
        # Texture and associated sprite to render our minimap to
        self.minimap_texture = None
        self.minimap_sprite = None

    def _init_sounds(self):
        self.ready_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "ready.wav"))
        self.go_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "go.wav"))
        self.coin_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "coin.wav"))
        self.jump_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "jump.wav"))
        self.level_victory_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "level_victory.wav"))
        self.death_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "death.wav"))
        self.boss_music = arcade.load_sound(str(ASSETS_PATH / "sounds" / "sound_of_silence.wav"))
        self.ie_death_sound = arcade.load_sound(str(ASSETS_PATH / "sounds" / "win_shut_down.wav"))

    def _init_speech_recognizer(self):
        # Init object for the process
        self.message_queue = Queue()
        self.recognize_proc = Process(target=speech_to_text_continuous, kwargs={
            "message_queue": self.message_queue,
            "api_key": os.environ.get('SPEECH_API_KEY'),
            "speech_region": os.environ.get('SPEECH_REGION')}, name="T1")
        self.recognize_proc.start()
        self.current_command = None

    def _init_cheat_flags(self):
        self.is_speed_boosted = False
        self.is_score_boosted = False

    def _boost_speed(self):
        self.player.speed = PLAYER_MOVE_SPEED * 3
        self.is_speed_boosted = True

    def _boost_score(self):
        self.score = 99999999999999
        self.is_score_boosted = True

    def _screw_physics(self):
        # self.physics_engine = arcade.PhysicsEnginePlatformer(
        #     player_sprite=self.player,
        #     platforms=self.walls,
        #     gravity_constant=0.2,
        #     ladders=self.ladders,
        # )
        # self.game_player.set_physics_engine(self.physics_engine)
        self.game_player.physics_engine.gravity_constant = 0
        self.game_player.player.center_y += 100
        for enemy in self.enemies:
            enemy.physics_engine.gravity_constant = 0.2
            enemy.change_y = 1

    def _update_enemies(self, delta_time):
        enemy_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.enemies
        )
        if enemy_hit:
            # if the player collide with the enemy from the top, the enemy dies
            if ((self.player.center_y > enemy_hit[0].center_y + 80) or
                (("name" in enemy_hit[0].properties) and
                 (enemy_hit[0].properties["name"] == "IE"))):
                self._speak_random(ENEMY_KILLED_TEXTS)
                enemy_hit[0].remove_from_sprite_lists()
                # check if the enemy has a name property
                # if hasattr(enemy_hit[0], "name"):
                if "name" in enemy_hit[0].properties:
                    enemy_name = enemy_hit[0].properties["name"]
                    dead_sprite = arcade.Sprite(
                        filename=str(ASSETS_PATH / "images" / "enemies" / f"{enemy_name}_dead.png"),
                        scale=MAP_SCALING,
                    )
                    dead_sprite.center_x = enemy_hit[0].center_x
                    dead_sprite.center_y = enemy_hit[0].center_y
                    self.enemies_dead.append(dead_sprite)

                    if enemy_hit[0].properties["name"] == "IE":
                        # IE has been killed
                        # Reset the player speed multiplier
                        self.game_player.reset_speed()
                        # Restore the background to its original color
                        arcade.set_background_color(arcade.color.FRESH_AIR)
                        # stop playing the boss fight sound
                        arcade.stop_sound(self.boss_music_playing_object)
                        # Remove the invisible slowing enemies from the sprite list
                        self.enemies = arcade.SpriteList()
                        # Remove the v8 sprite from the effects list
                        for effect in self.effects:
                            if effect.name == "v8":
                                self.effects.remove(effect)
                        self.game_player.stop()
                        self._speak_random(IE_KILLED_TEXTS, force=True)
                        arcade.play_sound(self.ie_death_sound)
                    elif enemy_hit[0].properties.get("name", "") != "IE":
                        self._speak_random(ENEMY_KILLED_TEXTS, force=True)

                        # play the enemy death sound
                        arcade.play_sound(self.death_sound)
            else:
                # if enemy has slow property, update the player speed multiplier
                if "slow" in enemy_hit[0].properties:
                    # import pdb; pdb.set_trace()
                    slow_value = float(enemy_hit[0].properties["slow"])
                    slow_priority = float(enemy_hit[0].properties["priority"])
                    # if the player is slowed down, dont schedule another speed multiplier reset
                    # if not self.game_player.is_slowed_down():
                    self.game_player.slow_down(slow_value, slow_priority)
                    # render the slow sprite
                    # slow_sprite = arcade.Sprite(
                    #     filename=str(ASSETS_PATH / "images" / "items" / "slow.png"),
                    #     scale=MAP_SCALING,
                    # )

                    # slow_sprite.offset_x = 75
                    # slow_sprite.offset_y = 75
                    # self.effects.append(slow_sprite)

                    # def reset_speed_multiplier(value):
                    #     self.game_player.reset_speed()
                    #     self.effects.remove(slow_sprite)
                    #     arcade.unschedule(reset_speed_multiplier)
                    # arcade.schedule(reset_speed_multiplier, 5)

                    # if there is speed property, the enemy moves horizontally (left or right)

        # Handle enemies animation
        for enemy in self.enemies:
            # if the enemy has a speed property, we update the 
            # if "speed" in enemy.properties:
                # enemy.change_x = float(enemy.properties["speed"])
                # # enemy.change_y = 2

            # As the player is getting close to an enemy having name IE, we make the background more darker, based on the distance
            if "name" in enemy.properties and enemy.properties["name"] == "IE":
                if arcade.get_distance_between_sprites(self.player, enemy) < 250:
                    arcade.set_background_color(FRESH_AIR_0)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 500:
                    arcade.set_background_color(FRESH_AIR_10)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 750:
                    arcade.set_background_color(FRESH_AIR_20)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 1000:
                    arcade.set_background_color(FRESH_AIR_30)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 1250:
                    arcade.set_background_color(FRESH_AIR_40)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 1500:
                    arcade.set_background_color(FRESH_AIR_50)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 1750:
                    arcade.set_background_color(FRESH_AIR_60)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 2000:
                    arcade.set_background_color(FRESH_AIR_70)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 2250:
                    arcade.set_background_color(FRESH_AIR_80)
                elif arcade.get_distance_between_sprites(self.player, enemy) < 2500:
                     arcade.set_background_color(FRESH_AIR_90)
                else:
                    arcade.set_background_color(arcade.color.FRESH_AIR)


            if enemy.left < 0:
                enemy.change_direction()

            if "jump_force" in enemy.properties:
                if "last_jumped" in enemy.properties:
                    if time() > (enemy.properties["last_jumped"] + enemy.properties["jump_interval"]):
                        if enemy.physics_engine.can_jump():
                            enemy.physics_engine.jump(enemy.properties["jump_force"])
                            enemy.properties["last_jumped"] = time()
                else:
                    if enemy.physics_engine.can_jump():
                        enemy.physics_engine.jump(enemy.properties["jump_force"])
                        enemy.properties["last_jumped"] = time()

            enemy.physics_engine.update()
            enemy.update_animation(delta_time)

    def _draw_static_elements(self):
        self.walls.draw()
        self.coins.draw()
        self.goals.draw()
        # Not all maps have ladders
        if self.ladders is not None:
            self.ladders.draw()

        # Not all maps have traps
        if self.traps is not None:
            self.traps.draw()

        if self.engine is not None:
            self.engine.draw()

    def _draw_actors(self):
        self.player.draw()
        if self.enemies is not None:
            self.enemies.draw()
        if self.enemies_dead is not None:
            self.enemies_dead.draw()

    def _draw_effects(self):
        for effect in self.effects:
            # offset_x and offset_y used to anchor it to the character
            # sprite
            effect.center_x = self.player.center_x + effect.offset_x
            effect.center_y = self.player.center_y + effect.offset_y

            # If it is a speech bubble, draw the effect and then the
            # text
            if hasattr(effect, "text"):
                effect_text = arcade.Text(
                    text=effect.text,
                    start_x=effect.left + 30,
                    start_y=effect.top - 80,
                    color=arcade.color.BLACK,
                    font_size=12,
                    width=effect.width - 60,
                    align="center",
                    font_name="Kenney Future",
                    multiline=True,
                )
                effect.draw()
                effect_text.draw()
            else:
                effect.draw()

    def _draw_dynamic_elements(self):
        if len(self.effects) > 0:
            self._draw_effects()
            # self.effects.draw()
        self.draw_score()
        self.draw_life_count()
        self.draw_timer()

    def _update_minimap(self):
        self.minimap_sprite.center_x = self.view_left + (MINIMAP_WIDTH[self.level] / 2)
        self.minimap_sprite.center_y = self.view_bottom + SCREEN_HEIGHT - (MINIMAP_HEIGHT[self.level] / 2)
        proj = 0, MAP_WIDTH[self.level], 0, MAP_HEIGHT[self.level]
        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self._draw_static_elements()
            self._draw_actors()

    def _speak(self, text, duration, force=False):
        """Speaks the text (in a bubble) given for the duration"""
        if self.is_speaking and not force:
            return
        speech_sprite = arcade.Sprite(
            filename=str(ASSETS_PATH / "images" / "speech_bubbles" / "two.png"),
            scale=0.5,
        )
        speech_sprite.offset_x = 200
        speech_sprite.offset_y = 100
        speech_sprite.text = text
        self.effects.append(speech_sprite)
        self.is_speaking = True


        def _unset_speech_sprite(value):
            try:
                self.effects.remove(speech_sprite)
            except ValueError:
                # If there is a speech bubble when the level ends,
                # the scheduled function trying to remove a speech
                # sprite that does not exist any more in the new level
                # will throw a ValueError.
                pass
            finally:
                self.is_speaking = False
                arcade.unschedule(_unset_speech_sprite)
        arcade.schedule(_unset_speech_sprite, duration)

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

        size = (MINIMAP_WIDTH[self.level], MINIMAP_HEIGHT[self.level])
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=MINIMAP_WIDTH[self.level] / 2,
                                            center_y=self.window.height - MINIMAP_HEIGHT[self.level] / 2,
                                            texture=self.minimap_texture)

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

        # Load the current map
        game_map = arcade.load_tilemap(
            map_path, layer_options=layer_options, scaling=MAP_SCALING
        )

        # Load the layers
        self.background = game_map.sprite_lists["background"]
        self.goals = game_map.sprite_lists["goal"]
        self.walls = game_map.sprite_lists["ground"]

        if "coins" in game_map.sprite_lists:
            self.coins = game_map.sprite_lists["coins"]

        # Only load ladders in maps with some ladders
        if "ladders" in game_map.sprite_lists:
            self.ladders = game_map.sprite_lists["ladders"]

        # Only load traps in maps with some traps
        if "traps" in game_map.sprite_lists:
            self.traps = game_map.sprite_lists["traps"]

        # Only load enemies in maps with some enemies
        if "enemies" in game_map.sprite_lists:
            self.enemies = game_map.sprite_lists["enemies"]
            # add physycs engine to the enemy
            for enemy in self.enemies:
                if "display" in enemy.properties and enemy.properties["display"] == "none":
                    enemy.visible = False
                enemy.physics_engine = arcade.PhysicsEnginePlatformer(
                    player_sprite=enemy,
                    platforms=self.walls,
                    gravity_constant=GRAVITY,
                    ladders=self.ladders,
                )
        # import pdb; pdb.set_trace()

        # Load enemies from config
        # self.enemies.sprite_list = [Enemy(**e_cfg) for e_cfg in ENEMIES[self.level]]
        for e_cfg in ENEMIES[self.level]:
            self.enemies.append(create_enemy(**e_cfg))
        for enemy in self.enemies:
            enemy.physics_engine = arcade.PhysicsEnginePlatformer(
                player_sprite=enemy,
                platforms=self.walls,
                gravity_constant=GRAVITY,
                ladders=self.ladders,
            )
        # import pdb; pdb.set_trace()
        # Only load engines in maps with some engines
        if "engine" in game_map.sprite_lists:
            self.engine = game_map.sprite_lists["engine"]

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
            platforms=self.walls, # TODO: Add rocks here?
            gravity_constant=GRAVITY,
            ladders=self.ladders,
        )
        self.game_player.set_physics_engine(self.physics_engine)

        # Speak random stuff at the beginning of each level
        self.is_speaking = False
        if self.level == 3:
            # play the boss fight sound
            self.boss_music_playing_object = arcade.play_sound(self.boss_music)
            self._speak_random(BOSS_FIGHT_TEXTS, 3)
        else:
            self._speak_random(WELCOME_TEXTS, 3)
        self.last_command_time = time()
        self.last_player_check_time = time()

    def update_player_direction(self):
        """
        This process will wait for a command from the speech recognition process
        and will update the player direction accordingly
        """

        # print hello world to check if the process is running
        print("Hello World")

    def _process_command(self, command):
        # Process the command
        if command == "up":
            logger.info("[PLATFORM]: Moving up")
            self.game_player.move_up()
        elif command == "down":
            logger.info("[PLATFORM]: Moving down")
            self.game_player.move_down()
        elif command == "left":
            logger.info("[PLATFORM]: Moving left")
            self.game_player.move_left()
        elif command == "right":
            logger.info("[PLATFORM]: Moving right")
            self.game_player.move_right()
        elif command == "jump":
            logger.info("[PLATFORM]: Jumping")
            self.game_player.jump()
        elif command == "stop":
            self.game_player.stop()
            logger.info("[PLATFORM]: Stopping")
        elif command == "step":
            self.game_player.step()
            logger.info("[PLATFORM]: Stepping")
        elif command == "turn":
            logger.info("[PLATFORM]: Turning")
            self.game_player.turn()
        elif command == "barry allen":
            self._boost_speed()
            # import pdb; pdb.set_trace()
            logger.info("[PLATFORM]: BARRY ALLEN")
        elif command == "super lotto":
            self._boost_score()
            self._screw_physics()
            logger.info("[PLATFORM]: SUPER LOTTO")
        self.last_command_time = time()

    def _speak_if_idle(self):
        if time() - self.last_command_time > IDLE_COMMAND_TIME:
            # Check if IE is still alive and store in a variable
            ie_alive = False
            for enemy in self.enemies:
                if enemy.properties.get("name", "") == "IE":
                    ie_alive = True
                    break

            if self.level == 3 and ie_alive:
                self._speak_random(BOSS_FIGHT_TEXTS, IDLE_TEXT_DURATION)
            else:
                self._speak_random(IDLE_TEXTS, IDLE_TEXT_DURATION)
            self.last_command_time = time() + IDLE_TEXT_DURATION

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
            self.game_player.move_left()
        elif key in [arcade.key.RIGHT, arcade.key.L]:  # Either right key or L key to go right
            self.game_player.move_right()
            
        # Check if player can climb up or down
        elif key in [arcade.key.UP, arcade.key.I]:  # Either up key or I key to go up
            if self.physics_engine.is_on_ladder():
                self.game_player.move_up()
        elif key in [arcade.key.DOWN, arcade.key.K]:  # Either down key or K key to down
            if self.physics_engine.is_on_ladder():
                self.game_player.move_down()
                
        # Check if player can jump
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.game_player.jump()
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
        # if there are some effects, draw them
        if self.effects is not None:
            for effect in self.effects:
                # show effect on the right of the player
                effect.center_x = self.player.center_x + 50
                
        # Handle ground animation
        for wall in self.walls:
            wall.update_animation(delta_time)

        # Handle coins animation
        for coin in self.coins:
            coin.update_animation(delta_time)

        for background in self.background:
            background.update_animation(delta_time)

        # Handle traps animation
        if self.traps is not None:
            for trap in self.traps:
                trap.update_animation(delta_time)

        # Handle player animation
        self.player.update_animation(delta_time)


        # Check if we have a command from the speech recognition process
        if not self.message_queue.empty():
            self.current_command = self.message_queue.get()
            self._process_command(self.current_command)


        if self.physics_engine.is_on_ladder():
            for ladder in self.ladders:
                if arcade.check_for_collision(self.player, ladder):
                    current_ladder = ladder
                    break
            if (current_ladder.top - self.player.bottom ) <= 25:
                if self.player.change_y > 0:
                    self.player.change_y = 0
                    self._speak_random(LADDER_TEXTS, 3)

        self._speak_if_idle()

        if (time() - self.last_player_check_time > 0.5):
            if ((self.player.center_x == self.player.previous_x) and
                (self.player.center_y == self.player.previous_y)):
                self.player.stop()
            else:
                self.player.previous_x = self.player.center_x
                self.player.previous_y = self.player.center_y
            self.last_player_check_time = time()

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

        # Updates related to enemies only on maps with enemies
        if self.enemies is not None:
            self._update_enemies(delta_time)

        if self.engine is not None:
            engine_hit = arcade.check_for_collision_with_list(
                sprite=self.player, sprite_list=self.engine
            )
            if engine_hit:
                # if the player collide with the engine, remove the engine from the sprite list
                engine_hit[0].remove_from_sprite_lists()
                engine_sprite = arcade.Sprite(
                    filename=str(ASSETS_PATH / "images" / "items" / "v8.png"),
                    scale=MAP_SCALING,
                )
                engine_sprite.offset_x = 75
                engine_sprite.offset_y = 75
                engine_sprite.name = "v8"
                self.effects.append(engine_sprite)

        # Now check if we are at the ending goal
        goals_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.goals
        )

        if goals_hit:
            if self.level == 4:  # Game is finished : Victory !
                # # Stop the speech recognition process
                # self.recognize_proc.terminate()
                self.handle_victory()
            else:
                # Play the level victory sound
                self.level_victory_sound.play()
                # Add a small waiting time to avoid jumping too quickly into the next level
                sleep(1)

                # Set up the next level and call setup again to load the new map
                self.level += 1

                # remove the dead enemies from the sprite list
                self.enemies_dead = arcade.SpriteList()

                # remove the effects from the sprite list
                self.effects = arcade.SpriteList()

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
        self._draw_static_elements()
        self._draw_actors()
        self._draw_dynamic_elements()

        # Update the minimap
        self._update_minimap()

        # Draw the minimap
        self.minimap_sprite_list.draw()

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

        next_x = 960

        def draw_hearts(image_path, x):
            life_image = arcade.load_texture(image_path)
            arcade.draw_texture_rectangle(
                x + self.view_left,
                50 + self.view_bottom,
                70, 70, life_image)
            return x - 70

        for ix in range(TOTAL_LIFE_COUNT - self.life_count):
            next_x = draw_hearts(life_empty_path, next_x)

        for ix in range(self.life_count):
            next_x = draw_hearts(life_full_path, next_x)

    def draw_timer(self):
        """
        Display the game timer on the bottom left after the life count
        """
        # Find the coin image in the images folder
        clock_image_path = ASSETS_PATH / "images" / "items" / "clock.png"

        # Load our score image
        clock_image = arcade.load_texture(clock_image_path)
        arcade.draw_texture_rectangle(
            170 + self.view_left + (int(self.is_score_boosted) * 250),
            30 + self.view_bottom,
            35, 35, clock_image)

        # Draw the timer in the lower left, after the score
        timer_text = str(self.get_game_time())

        # First set a black background for a shadow effect
        arcade.draw_text(
            timer_text,
            start_x=190 + self.view_left + (int(self.is_score_boosted) * 250),
            start_y=15 + self.view_bottom,
            color=arcade.csscolor.BLACK,
            font_size=30
        )

        # Now in white
        arcade.draw_text(
            timer_text,
            start_x=192 + self.view_left + (int(self.is_score_boosted) * 250),
            start_y=17 + self.view_bottom,
            color=arcade.csscolor.WHITE,
            font_size=30
        )
