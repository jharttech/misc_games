"""Platformer game using arcade and tiled"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 1


class MyGame(arcade.Window):
    """Main Application of class."""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are lists that keep track of our sprites. Each sprite should go into a list
        self.player_list = None
        self.wall_list = None
        

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)



    def setup(self):
        """Set up the game here.  CAll this function to restart the game"""
        # Separate variable that holds the player sprite
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite("assets/images/Players/128x256/Green/alienGreen_stand.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite) 

        # Create the ground using a loop NOT TILEMAP
        for x in range(0,1250, 64):
            wall = arcade.Sprite("assets/images/Ground/Grass/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("assets/images/Tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.wall_list.draw()
        self.player_list.draw()

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()