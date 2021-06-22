from sounds import Sounds


class TitleScreen:
    """The options screen when the game loads"""

    def __init__(self, ai):
        """Initialize the title screen"""

        self.screen = ai.screen
        self.settings = ai.settings
        self.pygame = ai.pygame
        self.sound = Sounds(ai)

        #  Load all images for buttons
        self.title_screen_image = ai.pygame.image.load(ai.os.path.join('assets','title_screen.png')).convert_alpha()

        self.play_button_image = ai.pygame.image.load(ai.os.path.join('assets', 'play_button.png')).convert_alpha()
        self.play_button_image_hl = ai.pygame.image.load(ai.os.path.join('assets', 'play_button_hl.png')).convert_alpha()

        self.quit_button_image = ai.pygame.image.load(ai.os.path.join('assets','quit_button.png')).convert_alpha()
        self.quit_button_image_hl = ai.pygame.image.load(ai.os.path.join('assets', 'quit_button_hl.png')).convert_alpha()

        self.quit_button_rect = self.quit_button_image.get_rect().move(self.settings.quit_button_pos)
        self.play_button_rect = self.play_button_image.get_rect().move(self.settings.play_button_pos)

    def draw_title_screen(self):
        """Draws the title screen"""
        #  Change the image if the mouse hovers over the button
        play_image = self.play_button_image
        quit_image = self.quit_button_image
        mouse_pos = self.pygame.mouse.get_pos()
        #  Change the image if the mouse hovers over a button and play the sound
        if self.pygame.Rect.collidepoint(self.play_button_rect,mouse_pos):
            play_image = self.play_button_image_hl
            self.sound.play_sound(self.sound.mouse_hover_sound)
        elif self.pygame.Rect.collidepoint(self.quit_button_rect, mouse_pos):
            quit_image = self.quit_button_image_hl
            self.sound.play_sound(self.sound.mouse_hover_sound)
        else:
            #  The sound has been played if the mouse has hovered over a button
            self.sound.sound_played = True

        #  Draw the screen accordingly
        self.screen.blit(self.title_screen_image, self.settings.bg_image_pos)
        self.screen.blit(play_image, self.play_button_rect)
        self.screen.blit(quit_image, self.quit_button_rect)
        # self.screen.blit(self.play_button_image_hl, self.play_button_hl_rect)
        # self.screen.blit(self.quit_button_hl, self.quit_button_hl_rect)


