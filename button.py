import pygame.font
import colors


class Button:
    """Create a simple button"""

    def __init__(self, ai, message):
        """Init button attributes"""
        self.screen = ai.screen
        self.settings = ai.settings
        self.screen_rect = self.screen.get_rect()

        #  Set the dimensions of the button
        self.width, self.height = 200, 50
        self.button_color = colors.MAROON
        self.text_color = colors.AQUA_MARINE
        self.font = pygame.font.SysFont("Ariel", 48)

        #  Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #  The button message needs to be prepared only once
        self._prep_msg(message)

    def _prep_msg(self, msg):
        """Turn message into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw a blank button then draw message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
