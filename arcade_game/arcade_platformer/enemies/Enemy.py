import arcade

from arcade_game.arcade_platformer.config.config import (
    ASSETS_PATH, ENEMY_STATIC_INFO
)


def create_enemy(name: str, center_x: int, center_y: int,
                 state: int, speed: int):
    enemy = Enemy()
    enemy.name = name
    enemy.center_x = center_x
    enemy.center_y = center_y
    enemy.state = state
    enemy.speed = speed
    enemy.texture = enemy.current_texture

    # Set change_x based on initial facing direction
    if enemy.state == arcade.FACE_LEFT:
        enemy.change_x = -1 * enemy.speed
    else:
        enemy.change_x = enemy.speed

    return enemy


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()

    def change_direction(self):
        self.change_x *= -1

        if self.state == arcade.FACE_LEFT:
            self.state = arcade.FACE_RIGHT
        else:
            self.state = arcade.FACE_LEFT
        self.texture = self.current_texture

    @property
    def texture_path(self):
        return str(ASSETS_PATH / "images" / "enemies" /  f"{self.name}.png")

    @property
    def default_state(self):
        return ENEMY_STATIC_INFO[self.name]["default_state"]

    @property
    def current_texture(self):
        if self.state == self.default_state:
            return arcade.load_texture(self.texture_path)
        return arcade.load_texture(self.texture_path, mirrored=True)
