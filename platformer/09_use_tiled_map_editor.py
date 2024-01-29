"""Platformer game using arcade and tiled"""

import arcade
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Player Constants
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20

# Physics Constants
GRAVITY = 1


class MyGame(arcade.Window):
    """Main Application of class."""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are lists that keep track of our sprites. Each sprite should go into a list
        # self.player_list = None
        # self.wall_list = None

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # A Camera that can be used for scrolling the screen
        self.camera = None
        self.gui_camera = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # Our physics engine
        self.physics_engine = None

        # Keep track of the score
        self.score = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here.  CAll this function to restart the game"""
        # Separate variable that holds the player sprite
        # self.player_list = arcade.SpriteList()
        # self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Initialize Scene
        #self.scene = arcade.Scene()

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the gui camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Create the Sprite lists
        #self.scene.add_sprite_list("Player")
        #self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Name of the map file we want to load
        map_name = "assets/platformer_level_01.tmx"

        # Layer specific options are defined based on layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection
        layer_options = {
            "ground" : {
                "use_spacial_hash" : True,
            },
        }
        
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = arcade.Sprite(
            "assets/images/Players/128x256/Green/alienGreen_stand.png",
            CHARACTER_SCALING,
        )
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 256
        # self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground using a loop NOT TILEMAP
        #for x in range(0, 1250, 64):
            #wall = arcade.Sprite(
                #"assets/images/Ground/Grass/grassMid.png", TILE_SCALING
            #)
            #wall.center_x = x
            #wall.center_y = 32
            #self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        #coordinate_list = [[512, 96], [256, 96], [768, 96]]

        #for coordinate in coordinate_list:
            # Add a crate on the ground
            #wall = arcade.Sprite(
                #"assets/images/Tiles/boxCrate_double.png", TILE_SCALING
            #)
            #wall.position = coordinate
            #self.scene.add_sprite("Walls", wall)

        # Use a loop to place some coins for our character to pick up
        #for x in range(128, 1250, random.randrange(256, 1250, 256)):
            #coin = arcade.Sprite("assets/images/Items/coinGold.png", COIN_SCALING)
            #coin.center_x = x
            #coin.center_y = random.randrange(96, 364)
            #self.scene.add_sprite("Coins", coin)

        # Keep track of the score
        self.score = 0

        # ---Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine
        # self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene.get_sprite_list("Walls"))
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["ground"]
        )

    def on_draw(self):
        """Render the screen."""

        self.clear()

        # Code to draw the screen goes here
        # self.wall_list.draw()
        # self.player_list.draw()

        # Activate our camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the gui camera before drawing gui elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.BLACK, 18)

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        # self.player_sprite.change_y = 0

        if (
            self.up_pressed
            and not self.down_pressed
            and self.player_sprite.change_y == 0
        ):
            if self.physics_engine.can_jump():
                arcade.play_sound(self.jump_sound)
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_JUMP_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let the camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the plyaer with the physics engine
        self.physics_engine.update()

        # Check to see if collision with coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["collectables"]
        )

        # Loop through each coin we hit and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play pickup sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # Position the camera
        self.center_camera_to_player()

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

        if key == arcade.key.ESCAPE:
            quit()

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released"""

        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
            # self.player_sprite.change_x = 0
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
