from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai, row_number=0):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        # TODO: Add an explosion animation
    #  Default color alien is green
        self.alien_image = 'green_alien.png'
    #  Different aliens depending on which row
        if row_number == 0:
            self.alien_image = 'red_alien.png'
        if row_number == 1:
            self.alien_image = 'yellow_alien.png'

    #  Load the image and place a rect around it
        self.image = ai.pygame.image.load(
            ai.os.path.join('assets', self.alien_image)).convert_alpha()
        self.rect = self.image.get_rect()

    # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width / 2
        self.rect.y = self.rect.height / 5

    #  Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if an alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
