import random
import sys

import pyasge
import fish_class
from gamedata import GameData


# above is importing different librariess

def restart(self) -> None:
    self.menu = 0
    self.data.score = 0
    self.scoreboard.string = str(self.data.score).zfill(6)
    for self.fish_amount in range(self.fish_number):
        self.fish.Fish.spawn(self, self.fish_amount, self.fishes)
    self.current_time = 0


class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.
        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)  # Background is infront
        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.menu = 0
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0
        # Setting the background
        self.data.background = pyasge.Sprite()
        self.initBackground()

        self.menu_text = None
        self.initMenu()

        self.scoreboard = None
        self.initScoreboard()

        self.current_time = 0
        self.time_limit = 60

        self.fish_amount = 0
        self.fish_number = 5
        self.fishes = []
        self.fish = fish_class

        for self.fish_amount in range(self.fish_number):
            self.fish.Fish.spawn(self, self.fish_amount, self.fishes)

    # for self.fish_amount in range(self.fish_number):

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):
            # loaded, so make sure this gets rendered first
            self.data.background.z_order = -100
            return True
        else:
            return False

    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.x = 1300
        self.scoreboard.y = 75
        self.scoreboard.string = str(self.data.score).zfill(6)

    def initMenu(self) -> bool:

        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "The Fish Game"
        self.menu_text.position = [100, 100]
        self.menu_text.colour = pyasge.COLOURS.HOTPINK

        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.over_text = pyasge.Text(self.data.fonts["MainFont"])
        self.over_text.string = "Game Over"
        self.over_text.position = [100, 300]
        self.over_text.colour = pyasge.COLOURS.HOTPINK

        # Timer text below
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.timer_text = pyasge.Text(self.data.fonts["MainFont"])
        self.timer_text.position = [1100, 75]
        self.timer_text.colour = pyasge.COLOURS.HOTPINK

        # This option starts the game
        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = ">START"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.HOTPINK

        # This option exits the games
        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "EXIT"
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY

        return True

    def isInside(self, sprite, mouse_x, mouse_y) -> bool:
        # grab the sprite's bounding box. the box has 4 vertices

        bounds = sprite.getWorldBounds()

        # check to see if the mouse position falls within the x and y bounds
        if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
            return True

        return False

    def clickHandler(self, event: pyasge.ClickEvent) -> None:
        # look to see if mouse button 1 pressed
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and \
                event.button == pyasge.MOUSE.MOUSE_BTN1:

            # is the mouse position within the sprite's bounding box?
            for self.fish_amount in range(self.fish_number):
                if self.isInside(self.fishes[self.fish_amount], event.x, event.y):
                    self.data.score += 1  # here we add 1 to the score
                    self.scoreboard.string = str(self.data.score).zfill(6)
                    self.fish.Fish.spawn(self, self.fish_amount,
                                         self.fishes)  # now we respawn the fish to keep the game going

    def keyHandler(self, event: pyasge.KeyEvent) -> None:

        # only act when the key is pressed and not released
        if event.action == pyasge.KEYS.KEY_PRESSED:

            # use both the right and left keys to select the play/exit options
            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 0:
                    self.play_option.string = ">START"
                    self.play_option.colour = pyasge.COLOURS.HOTPINK
                    self.exit_option.string = " EXIT"
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                else:
                    self.play_option.string = " START"
                    self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.exit_option.string = " >EXIT"
                    self.exit_option.colour = pyasge.COLOURS.HOTPINK

            # if the enter key is pressed, action the menu option
            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.menu_option == 0:
                    self.menu = 1
                else:
                    self.signal_exit()

            if event.key == pyasge.KEYS.KEY_R:
                restart(self)

    def update(self, game_time: pyasge.GameTime) -> None:

        if self.menu == 0:
            pass
        elif self.menu == 1:
            for self.fish_amount in range(self.fish_number):
                fish_speed = 100
                self.fishes[self.fish_amount].x = self.fishes[self.fish_amount].x + fish_speed * game_time.fixed_timestep
                # Fish movement at a fixed rate for above

                if self.fishes[self.fish_amount].x > self.data.game_res[0]:  # Fish moving left to right
                    self.fishes[self.fish_amount].x = 0 - self.fishes[self.fish_amount].width
                else:
                    pass

    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the game-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """
        self.data.renderer.render(self.data.background)
        if self.menu == 0:
            # render the menu here
            self.render_menu()
        elif self.menu == 1:
            # render the game here
            self.render_game(game_time)
        else:
            # render game over here
            self.render_over()

    def render_over(self):
        self.data.renderer.render(self.over_text)

    def render_game(self, game_time):
        self.current_time = self.current_time + 1 * game_time.fixed_timestep
        self.timer_text.string = str(round(self.current_time))
        self.data.renderer.render(self.timer_text)
        self.data.renderer.render(self.scoreboard)
        for self.fish_amount in range(self.fish_number):
            self.data.renderer.render(self.fishes[self.fish_amount])
        if self.current_time > self.time_limit:
            self.menu = 2

    def render_menu(self):
        self.data.renderer.render(self.menu_text)
        self.data.renderer.render(self.play_option)
        self.data.renderer.render(self.exit_option)


def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """

    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
