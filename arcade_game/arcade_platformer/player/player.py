import arcade

from arcade_game.arcade_platformer.config.config import PLAYER_START_X, PLAYER_START_Y, ASSETS_PATH, \
    PLAYER_MOVE_SPEED, PLAYER_JUMP_SPEED


class Player:
    """
    Controls the player animations (images for the various positions) and movements
    """
    def __init__(self):
        self.player = self.create_player_sprite()
        self.physics_engine = None
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
        player.state = arcade.FACE_RIGHT

        # Set the initial texture
        player.texture = player.stand_right_textures[0]

        return player

    def move_left(self):
        self.player.change_x = -PLAYER_MOVE_SPEED

    def move_right(self):
        self.player.change_x = PLAYER_MOVE_SPEED

    def move_up(self):
        # Check if player can climb up or down
        if self.physics_engine.is_on_ladder():
            self.player.change_y = PLAYER_MOVE_SPEED

    def move_down(self):
        if self.physics_engine.is_on_ladder():
            self.player.change_y = -PLAYER_MOVE_SPEED

    def jump(self):
        if self.physics_engine.can_jump():
            self.player.change_y = PLAYER_JUMP_SPEED
            # Play the jump sound
            arcade.play_sound(self.jump_sound)

    def stop(self):
        self.player.change_x = 0
        self.player.change_y = 0
        
