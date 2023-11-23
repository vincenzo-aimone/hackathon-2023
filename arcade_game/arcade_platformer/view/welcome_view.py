import arcade

from arcade_game.arcade_platformer.config.config import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_PATH
from . import platform_view
from arcade_game.arcade_platformer.player.player import Player


class WelcomeView(arcade.View):
    """
    Displays a welcome screen and prompts the user to begin the game.

    Displays a background image, play a sounds and wait for pressing the Enter key to start the game.
    You do not have to modify these to complete the mandatory challenges.
    """

    def __init__(self, player: Player) -> None:
        super().__init__()

        self.player = player

        self.game_view = None

        # Load & play intro music
        self.intro_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "intro.wav")
        )
        self.sound_player = self.intro_sound.play(volume=0.3, loop=True)

        # Find the title image in the images folder
        title_image_path = ASSETS_PATH / "images" / "welcome.png"

        # Load our title image
        self.title_image = arcade.load_texture(title_image_path)

        # Set our display timer
        self.display_timer = 2.0

        # Are we showing the instructions?
        self.show_instructions = False

    def on_update(self, delta_time: float) -> None:
        """Manages the timer to toggle the instructions

        Arguments:
            delta_time -- time passed since last update
        """

        # First, count down the time
        self.display_timer -= delta_time

        # If the timer has run out, we toggle the instructions
        if self.display_timer < 0:
            # Toggle whether to show the instructions
            self.show_instructions = not self.show_instructions

            # And reset the timer so the instructions flash slowly
            self.display_timer = 1.0

    def on_draw(self) -> None:
        # Start the rendering loop
        arcade.start_render()

        # Draw a rectangle filled with our title image
        arcade.draw_texture_rectangle(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            texture=self.title_image,
        )

        # Should we show our instructions?
        if self.show_instructions:
            arcade.draw_text(
                "Press enter to Start the game",
                start_x=250,
                start_y=170,
                color=arcade.color.SELECTIVE_YELLOW,
                font_size=30,
            )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Start the game when the user presses the enter key

        Arguments:
            key -- Which key was pressed
            modifiers -- What modifiers were active
        """
        if key == arcade.key.RETURN:
            # Stop intro music
            self.intro_sound.stop(self.sound_player)
            # Launch Game view
            self.game_view = platform_view.PlatformerView(self.player)
            self.game_view.setup()
            self.window.show_view(self.game_view)
