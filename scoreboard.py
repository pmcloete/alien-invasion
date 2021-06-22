import pygame.font

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai):
        """Initialize score keeping attributes"""
        self.screen = ai.screen
        self.screen_rect = ai.screen.get_rect()
        self.settings = ai.settings
        self.stats = ai.stats

        #  Font settings for scoring
        self.text_color = self.settings.score_color
        self.font = pygame.font.SysFont(None, 39)

        #  Prepare the initial score image
        self.prep_score()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = str(round(self.stats.score, -1))
        score_str = f'SCORE: {rounded_score}'
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #  Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Display the score on the screen"""
        self.screen.blit(self.score_image, self.score_rect)