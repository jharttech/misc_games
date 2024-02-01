"""Obstacle game using arcade and tiled"""

import arcade
import random

# Constants
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Zoomer"

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

        # set distance between obstacles
        self.space_between = 200

        # Set object velocity
        self.object_velocity = -2

        # Set temp obstacle start locale 
        self.temp_obstacle_start = SCREEN_WIDTH / 3

        # The GUI camera
        self.gui_camera = None

        # Create a game timer
        self.timer = 0

        # Score
        self.score = 0

        #arcade.set_background_color(arcade.csscolor.GREEN)
        self.background = None

        #Set game sounds
        self.explode = arcade.load_sound("assets/sounds/Explode.wav")

    def setup(self):
        """Set up the game here.  CAll this function to restart the game"""
        # Set background image
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

        # Reset score
        self.score = 0

        # Reset obstacles velocity
        self.object_velocity = -2

        # Reset obstacle distance
        self.space_between = 200

        # Reset timer
        self.timer = 0

        # Reset spawn objects time
        self.spawn_objects = 0

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

            
        # Create physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, platforms=self.obstacles_list)
        #self.physics_engine_wall = arcade.PhysicsEngineSimple(walls=self.wall_list)

    def create_explosion(self):
        """Create the explosion animation"""
        # Create an explosion sprite
        pass
        
        

    def obstacle_update(self):
        # Create obstacles
        self.obstacles_left = arcade.Sprite(random.choice([
            f":resources:images/space_shooter/meteorGrey_big{random.randint(1,3)}.png",
            f":resources:images/space_shooter/meteorGrey_med{random.randint(1,2)}.png"]), TILE_SCALING
        )
        self.obstacles_left.center_x = self.temp_obstacle_start + (random.randint(-60,60))
        self.obstacles_left.angle=random.randint(0,360)
        if self.obstacles_left.center_x < 32:
            self.obstacles_left.center_x = 32
        if self.obstacles_left.center_x > 300:
            self.obstacles_left.center_x = 300
        self.obstacles_left.center_y = SCREEN_HEIGHT
        self.obstacles_left.change_y = self.object_velocity
        self.obstacles_list.append(self.obstacles_left)

        obstacles_right = arcade.Sprite(random.choice([
            f":resources:images/space_shooter/meteorGrey_big{random.randint(1,3)}.png",
            f":resources:images/space_shooter/meteorGrey_med{random.randint(1,2)}.png"]), TILE_SCALING
        )
        obstacles_right.center_x = self.obstacles_left.center_x + self.space_between
        obstacles_right.center_y = self.obstacles_left.center_y
        obstacles_right.change_y = self.obstacles_left.change_y
        self.obstacles_list.append(obstacles_right)
        self.spawn_objects = 0.0

        self.temp_obstacle_start = self.obstacles_left.center_x

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        self.obstacles_list.draw()
        self.player_list.draw()

        #Activate our GUI Camera
        self.gui_camera.use()

        #Draw info to screen
        temp_x = f"temp: {self.temp_obstacle_start}"
        current_x = f"current: {self.obstacles_left.center_x}"
        obj_list = f"objs: {len(self.obstacles_list)}"
        obj_vel = f"objv: {self.object_velocity}"
        score = f"score: {int(self.score)}"
        arcade.draw_text(temp_x, 10, 10, arcade.csscolor.WHITE, 18)
        arcade.draw_text(current_x, 10, 30, arcade.csscolor.WHITE, 18)
        arcade.draw_text(obj_list, 10, 50, arcade.csscolor.WHITE, 18)
        arcade.draw_text(obj_vel, 10, 70, arcade.csscolor.WHITE, 18)
        arcade.draw_text(score, 10, 90, arcade.csscolor.WHITE, 18)


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
        self.score += delta_time
        self.spawn_objects += delta_time
        self.timer += delta_time
        if self.timer < 20:
            if self.spawn_objects > self.object_velocity - self.object_velocity + 0.5:
                self.obstacle_update()
        elif self.timer > 20 and self.timer < 50:
            if self.timer > 25:
                self.object_velocity = -4
                self.space_between = 190
                if self.spawn_objects > .25:
                    self.obstacle_update()
        elif self.timer > 50:
            if self.timer > 52:
                self.object_velocity = -6
                self.space_between = 185
                if self.spawn_objects > .125:
                    self.obstacle_update()

        if self.obstacles_list[0].top < 0:
            self.obstacles_list.pop(0)

        if self.player_sprite.left < SCREEN_WIDTH - SCREEN_WIDTH:
            self.player_sprite.change_x = 0
            self.player_sprite.center_x = self.player_sprite.center_x + 10

        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.change_x = 0
            self.player_sprite.center_x = self.player_sprite.center_x - 10

        if arcade.check_for_collision_with_list(
            self.player_sprite,
            self.obstacles_list
            ):
            self.create_explosion()
            arcade.play_sound(self.explode)
            self.setup()





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
