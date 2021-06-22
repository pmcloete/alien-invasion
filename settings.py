import colors
import os

class Settings:
    """ A class to store all settings for any game"""

    def __init__(self, screen_width=1200, screen_height=800,
                 screen_caption='Alien Invasion',
                 bg_color=colors.MAIN_GAME_BLUE):
        """Initialize the game settings"""

    #  Screen Settings
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_caption = screen_caption
        self.bg_color = bg_color
        self.bg_image_pos = (0, 0)
        # TODO: These coordinates should be refactored to use the size of the button to place it on screen
        self.play_button_pos = (532, 407)
        self.quit_button_pos = (532, 487)
        #  Set the clock speed of the game
        self.FPS = 60

    #  Ship Settings
        self.ship_speed = 10
        self.ship_limit = 3

    #  Bullet Settings
        #  TODO: Add an image for the bullets and different intensities
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = colors.GOLD
        self.bullets_allowed = 3

    #  Alien Settings
        #  This will change the x,y position of where the first alien is
        #  drawn
        self.starting_x_offset = 10
        self.starting_y_offset = 50
        self.alien_speed = 1
        self.fleet_drop_speed = 50
        #  fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    #  Game Speed Settings
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    #  Scoring
        self.alien_points = 25
        self.score_scale = 1.5
        self.high_score = 0

    #  Sound Settings
        self.music_volume = 0.3
        self.play_selected_volume = 0.5
        self.bullet_volume = 0.4
        self.alien_hit_volume = 0.5

    #  Scoring Settings
        self.score_color = colors.WHITE

    def initialize_dynamic_settings(self):
        """Init settings that change throughout the game"""
        #  This can be updated to include difficulty settings in the main menu
        self.ship_speed = 5
        self.bullet_speed = 10
        self.alien_speed = 3.0
        #  fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def save_high_score(self):
        """Save the players high score to a text file"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except FileNotFoundError:
            pass

    def load_high_score(self):
        """Load the previous high score"""
        try:
            with open('high_score.txt', 'a') as f:
                high_score = f.readlines()
                for line in high_score:
                    self.high_score = line
        except:
            #  The game was not loaded previously
            self.high_score = 0