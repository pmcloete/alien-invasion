
class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai):
        """Initialize statistics"""
        self.settings = ai.settings
        self.reset_stats()
        #  Start the game in an active state
        self.game_active = False
        self.score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit