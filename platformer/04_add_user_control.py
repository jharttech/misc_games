"""Platformer game using arcade and tiled"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5

# Player Constants
PLAYER_MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """Main Application of class."""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are lists that keep track of our sprites. Each sprite should go into a list
        #self.player_list = None
        #self.wall_list = None
        
        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)



    def setup(self):
        """Set up the game here.  CAll this function to restart the game"""
        # Separate variable that holds the player sprite
        #self.player_list = arcade.SpriteList()
        #self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        self.player_sprite = arcade.Sprite("assets/images/Players/128x256/Green/alienGreen_stand.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 32
        self.player_sprite.center_y = 128
        #self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite) 

        # Create the ground using a loop NOT TILEMAP
        for x in range(0,1250, 64):
            wall = arcade.Sprite("assets/images/Ground/Grass/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("assets/images/Tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Create the 'physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene.get_sprite_list("Walls"))

    def on_draw(self):
        """Render the screen."""

        self.clear()
        
        # Code to draw the screen goes here
        #self.wall_list.draw()
        #self.player_list.draw()

        #Draw our Scene
        self.scene.draw()

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the plyaer with the physics engine
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()
        
    def on_key_release(self, key, modifiers):
        """Called whenever a key is released"""

        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()




def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()