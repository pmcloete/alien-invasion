class Ship:
    """A class to manage the ship"""

    #  When the ship object is created in the main game, you have to pass an
    #  of the game object to this one to give it access to all the game
    #  resources to enable the ship to interact with the rest of the game.
    def __init__(self, ai):
        """Initialize the ship and it's starting position"""
        #  We have to make the screen on which the ship is the same as the
        #  screen on which the game is being played
        self.screen = ai.screen
        self.settings = ai.settings
        #  Get the surface rect of the ship to later access it
        self.screen_rect = ai.screen.get_rect()

    #  TODO: Add an explosion animation and sound for when the ship is destroyed
    # Load the ship image
        self.image = ai.pygame.image.load(ai.os.path.join('assets','spaceship.png')).convert_alpha()
        self.rect = self.image.get_rect()
        #  Start each ship at2 the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #  Store a float value for the ship's horizontal position
        #  This enables you to track the exact position of the ship
        self.x = float(self.rect.x)

    #  Movement Flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ships position based on the movement flag"""
        #  Update the ship's x value, not the rect

        #  The right side of the screen will be whatever the width of the
        #  screen is. By doing it with the code below, you can change the
        #  the size of the screen without having to redo the edge detection
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            #  Remember that the left edge of the screen will be x=0
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #  This updates the position of the rect defined when the class is
        #  instantiated. Rect has an attribute .x to determine position
        self.rect.x = self.x

    def display_ship(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship after it was hit"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
