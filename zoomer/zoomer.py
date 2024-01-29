"""Platformer game using arcade and tiled"""

import arcade
import random

# Constants
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5

# Constant for player speed
PLAYER_MOVEMENT_SPEED = 5

# Physics Constants
GRAVITY = 1


class MyGame(arcade.Window):
    """Main Application of class."""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are lists that keep track of our sprites. Each sprite should go into a list
        self.player_list = None
        self.wall_list = None

        # Track the current state of what keys are pressed
        self.left_pressed = False
        self.right_pressed = False

        arcade.set_background_color(arcade.csscolor.GREEN)

    def setup(self):
        """Set up the game here.  CAll this function to restart the game"""
        # Separate variable that holds the player sprite
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(
            ":resources:images/space_shooter/playerShip1_blue.png",
            CHARACTER_SCALING,
        )
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        # Create the spikes using a loop NOT TILEMAP
        for y in range(0, SCREEN_HEIGHT + 64, 42):
            self.wall_left = arcade.Sprite(
                ":resources:images/topdown_tanks/treeGreen_large.png", TILE_SCALING
            )
            self.wall_left.center_x = SCREEN_WIDTH / 3
            self.wall_left.center_y = y
            self.wall_list.append(self.wall_left)

        for y in range(0, SCREEN_HEIGHT + 64, 42):
            wall_right = arcade.Sprite(
                ":resources:images/topdown_tanks/treeGreen_large.png", TILE_SCALING
            )
            wall_right.center_x = SCREEN_WIDTH - SCREEN_WIDTH / 3
            wall_right.center_y = y
            self.wall_list.append(wall_right)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        #coordinate_list = [[512, 96], [256, 96], [768, 96]]

        #for coordinate in coordinate_list:
            # Add a crate on the ground
        #    wall = arcade.Sprite(
        #        "assets/images/Tiles/boxCrate_double.png", TILE_SCALING
        #    )
        #    wall.position = coordinate
        #    self.wall_list.append(wall)
            
        # Create physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.wall_left, gravity_constant=GRAVITY)

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.wall_list.draw()
        self.player_list.draw()


    def update_player_speed(self):
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_update(self, delta_time):
        """Movement and game logic"""
        #Move the player with the physics engine
        self.player_sprite.change_y = 1
        self.physics_engine.update()
        self.wall_left.change_y = -GRAVITY

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

        if key == arcade.key.ESCAPE:
            quit()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
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
