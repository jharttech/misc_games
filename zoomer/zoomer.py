"""Platformer game using arcade and tiled"""

import arcade
import random
import time

# Constants
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5

# Constant for player speed
PLAYER_MOVEMENT_SPEED = 5
PLAYER_THRUST = 1

# Physics Constants
GRAVITY = 1


class MyGame(arcade.Window):
    """Main Application of class."""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are lists that keep track of our sprites. Each sprite should go into a list
        self.player_list = None
        self.obstacles_list = None

        # Track the current state of what keys are pressed
        self.left_pressed = False
        self.right_pressed = False

        # set spawn_timer
        self.spawn_objects = 0.0

        # Set object velocity
        self.object_velocity = -2

        # Set temp obstacle start locale 
        self.temp_obstacle_start = SCREEN_WIDTH / 3

        # The GUI camera
        self.gui_camera = None

        # Create a game timer
        self.timer = 0

        arcade.set_background_color(arcade.csscolor.GREEN)

    def setup(self):
        """Set up the game here.  CAll this function to restart the game"""
        # Separate variable that holds the player sprite
        self.player_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(
            ":resources:images/space_shooter/playerShip1_blue.png",
            CHARACTER_SCALING,
        )
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        self.gui_camera = arcade.Camera(self.width, self.height)


        self.obstacle_update()

        


        # Create the spikes using a loop NOT TILEMAP
        # for y in range(0, SCREEN_HEIGHT + 64, 42):
        #     wall_left = arcade.Sprite(
        #         ":resources:images/topdown_tanks/treeGreen_large.png", TILE_SCALING
        #     )
        #     wall_left.center_x = SCREEN_WIDTH / 3 + (random.randint(-10,10))
        #     wall_left.center_y = y
        #     wall_left.change_y = -.5
        #     self.wall_list.append(wall_left)

        # for y in range(0, SCREEN_HEIGHT + 64, 42):
        #     wall_right = arcade.Sprite(
        #         ":resources:images/topdown_tanks/treeGreen_large.png", TILE_SCALING
        #     )
        #     wall_right.center_x = SCREEN_WIDTH - SCREEN_WIDTH / 3
        #     wall_right.center_y = y
        #     self.wall_list.append(wall_right)

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
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, platforms=self.obstacles_list)
        #self.physics_engine_wall = arcade.PhysicsEngineSimple(walls=self.wall_list)

    def obstacle_update(self):
        # Create obstacles
        self.obstacles_left = arcade.Sprite(
            ":resources:images/topdown_tanks/treeGreen_large.png", TILE_SCALING
        )
        self.obstacles_left.center_x = self.temp_obstacle_start + (random.randint(-30,30))
        if self.obstacles_left.center_x < 32:
            self.obstacles_left.center_x = 32
        if self.obstacles_left.center_x > 300:
            self.obstacles_left.center_x = 300
        self.obstacles_left.center_y = SCREEN_HEIGHT
        self.obstacles_left.change_y = self.object_velocity
        self.obstacles_list.append(self.obstacles_left)

        obstacles_right = arcade.Sprite(
            ":resources:images/topdown_tanks/treeGreen_large.png", TILE_SCALING
        )
        obstacles_right.center_x = self.obstacles_left.center_x + 200
        obstacles_right.center_y = self.obstacles_left.center_y
        obstacles_right.change_y = self.obstacles_left.change_y
        self.obstacles_list.append(obstacles_right)
        self.spawn_objects = 0.0

        self.temp_obstacle_start = self.obstacles_left.center_x

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        self.obstacles_list.draw()
        self.player_list.draw()

        #Activate our GUI Camera
        self.gui_camera.use()

        #Draw info to screen
        temp_x = f"temp: {self.temp_obstacle_start}"
        current_x = f"current: {self.obstacles_left.center_x}"
        obj_list = f"objs: {len(self.obstacles_list)}"
        obj_vel = f"objv: {self.object_velocity}"
        arcade.draw_text(temp_x, 10, 10, arcade.csscolor.BLACK, 18)
        arcade.draw_text(current_x, 10, 30, arcade.csscolor.BLACK, 18)
        arcade.draw_text(obj_list, 10, 50, arcade.csscolor.BLACK, 18)
        arcade.draw_text(obj_vel, 10, 70, arcade.csscolor.BLACK, 18)


    def update_player_speed(self):
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_update(self, delta_time):
        """Movement and game logic"""
        #Move the player with the physics engine
        self.player_sprite.change_y = PLAYER_THRUST
        self.physics_engine.update()
        #self.physics_engine_wall.update()
        self.spawn_objects += delta_time
        self.timer += delta_time
        if self.timer < 20:
            if self.spawn_objects > self.object_velocity - self.object_velocity + 0.5:
                self.obstacle_update()
        elif self.timer > 20:
            if self.timer > 25:
                self.object_velocity = -4
                if self.spawn_objects > .25:
                    self.obstacle_update()
        if self.obstacles_list[0].top < 0:
            self.obstacles_list.pop(0)


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
