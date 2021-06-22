class Background():

    def __init__(self, ai):
        '''Manage the background'''
        #  As with the ship class, we need to give this class access to the
        #  main games' screen
        self.screen = ai.screen
        self.settings = ai.settings
        #  Load the image
        self.bg_image = ai.pygame.image.load(
            ai.os.path.join('assets', 'background.png'))

    def display_background(self):
        '''Displays the loaded images at position 0,0'''
        self.screen.blit(self.bg_image, self.settings.bg_image_pos)
