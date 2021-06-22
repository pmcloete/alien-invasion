from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage the bullets fired from the ship"""

    def __init__(self, ai):
        """Create a bullet at the ship's current position"""

        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings
        self.color = ai.settings.bullet_color
        self.game = ai.pygame
        self.standard_bullet = ai.pygame.image.load(ai.os.path.join('assets', 'standard_bullet.png'))
        self.laser_bullet = ai.pygame.image.load(ai.os.path.join('assets', 'laser_bullet.png'))
        self.slime_bullet = ai.pygame.image.load(ai.os.path.join('assets', 'slime_bullet.png'))
        self.electric_bullet = ai.pygame.image.load(ai.os.path.join('assets', 'electric_bullet.png'))
        self.red_bomb_bullet = ai.pygame.image.load(ai.os.path.join('assets', 'red_bomb_bullet.png'))

        #  All the bullets are the same size and therefore need only one rect
        self.rect = self.standard_bullet.get_rect()
        #  Except this one
        self.red_rect = self.red_bomb_bullet.get_rect()


        #  Create a bullet rect at (0,0) and then set correct position
        # self.rect = ai.pygame.Rect(0, 0, self.settings.bullet_width,
        #                            self.settings.bullet_height)
        self.rect.midtop = ai.ship.rect.midtop

        #  Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        #  Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        #  Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        # self.game.draw.rect(self.screen, self.color, self.bullet_rect)
        #  TODO: Work on bullet power-ups and damage
        #  This image can be changed based on different power-ups
        #  The damage a bullet does should also be updated
        self.screen.blit(self.red_bomb_bullet, self.rect)
