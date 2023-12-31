import arcade

from arcade_game.arcade_platformer.config.config import PLAYER_START_X, PLAYER_START_Y, ASSETS_PATH, \
    PLAYER_MOVE_SPEED, PLAYER_JUMP_SPEED
from log.config_log import logger


class Player:
    """
    Controls the player animations (images for the various positions) and movements
    """
    def __init__(self):
        self.player = self.create_player_sprite()
        self.physics_engine = None
        self.speed_multiplier = 1
        self.slow_priority = 0
        self.jump_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "jump.wav")
        )

    def set_physics_engine(self, physics_engine: arcade.PhysicsEnginePlatformer):
        self.physics_engine = physics_engine

    def set_player_num(self, player_num):
        self.player = self.create_player_sprite(player_num)

    @staticmethod
    def create_player_sprite(player_num = 1) -> arcade.AnimatedWalkingSprite:
        """Creates the animated player sprite

        Returns:
            The properly set up player sprite
        """
        # Where are the player images stored?
        texture_path = ASSETS_PATH / "images" / "player"

        # Set up the appropriate textures
        climbing_paths = [
            texture_path / f"alienGreen_climb{x}.png" for x in (1, 2)
        ]
        if player_num == 1:
            standing_path = texture_path / "player1_alienGreen_stand.png"
            walking_paths = [texture_path / f"player1_alienGreen_walk{x}.png" for x in (1, 2)]

        if player_num == 2:
            standing_path = texture_path / "player2_alienGreen_stand.png"
            walking_paths = [texture_path / f"player2_alienGreen_walk{x}.png" for x in (1, 2)]

        if player_num == 3:
            standing_path = texture_path / "player3_alienGreen_stand.png"
            walking_paths = [texture_path / f"player3_alienGreen_walk{x}.png" for x in (1, 2)]

        if player_num == 4:
            standing_path = texture_path / "player4_alienGreen_stand.png"
            walking_paths = [texture_path / f"player4_alienGreen_walk{x}.png" for x in (1, 2)]

        # Load them all now
        walking_right_textures = [
            arcade.load_texture(texture) for texture in walking_paths
        ]
        walking_left_textures = [
            arcade.load_texture(texture, mirrored=True)
            for texture in walking_paths
        ]

        walking_up_textures = [
            arcade.load_texture(texture) for texture in climbing_paths
        ]
        walking_down_textures = [
            arcade.load_texture(texture) for texture in climbing_paths
        ]

        standing_right_textures = [arcade.load_texture(standing_path)]

        standing_left_textures = [
            arcade.load_texture(standing_path, mirrored=True)
        ]

        # Create the sprite
        player = arcade.AnimatedWalkingSprite()

        # Add the proper textures
        player.stand_left_textures = standing_left_textures
        player.stand_right_textures = standing_right_textures
        player.walk_left_textures = walking_left_textures
        player.walk_right_textures = walking_right_textures
        player.walk_up_textures = walking_up_textures
        player.walk_down_textures = walking_down_textures

        # Set the player defaults
        player.center_x = PLAYER_START_X
        player.center_y = PLAYER_START_Y
        player.previous_x = player.center_x
        player.previous_y = player.center_y
        player.state = arcade.FACE_RIGHT
        player.speed = PLAYER_MOVE_SPEED

        # Set the initial texture
        player.texture = player.stand_right_textures[0]

        return player

    def move_left(self):
        self.player.change_x = -self.player.speed * self.speed_multiplier

    def move_right(self):
        self.player.change_x = self.player.speed * self.speed_multiplier

    def move_up(self):
        # Check if player can climb up or down
        if self.physics_engine.is_on_ladder():
            self.player.change_y = self.player.speed * self.speed_multiplier

    def move_down(self):
        if self.physics_engine.is_on_ladder():
            self.player.change_y = -self.player.speed * self.speed_multiplier

    def jump(self):
        if self.physics_engine.can_jump():
            self.player.change_y = PLAYER_JUMP_SPEED * self.speed_multiplier
            # Play the jump sound
            arcade.play_sound(self.jump_sound)

    def stop(self):
        logger.info ("STOP INVOKED")
        self.player.change_x = 0
        self.player.change_y = 0
        
    def slow_down(self, value: float, slow_priority: int):
        if slow_priority > self.slow_priority:
            self.speed_multiplier = value ** slow_priority
            self.player.change_x *= self.speed_multiplier
            self.player.change_y *= self.speed_multiplier
            self.slow_priority = slow_priority
        
    def reset_speed(self):
        self.player.change_x /= self.speed_multiplier
        self.player.change_y /= self.speed_multiplier
        self.speed_multiplier = 1
        self.slow_priority = 0
        
    def is_slowed_down(self):
        return self.speed_multiplier != 1

    def step(self):
        def step_stop(_):
            self.stop()
            arcade.unschedule(step_stop)
        if self.player.state == arcade.FACE_RIGHT:
            self.move_right()
            arcade.schedule(step_stop, 0.5)
        else:
            self.move_left()
            arcade.schedule(step_stop, 0.5)

    def turn(self):
        self.stop()
        if self.player.state == arcade.FACE_RIGHT:
            self.player.state = arcade.FACE_LEFT
        else:
            self.player.state = arcade.FACE_RIGHT
