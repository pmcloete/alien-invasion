import sys
import os
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from background import Background
from ship import Ship
from alien import Alien
from bullet import Bullet
from title_screen import TitleScreen
from scoreboard import Scoreboard
from sounds import Sounds


class AlienInvasion:
    """
    Class to manage game assets and behaviour
    """

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 64)
        #  Give all the other modules access to one instance of pygame, os
        self.pygame = pygame
        self.clock = pygame.time.Clock()
        self.os = os
    # FULL SCREEN MODE BELOW
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.settings = Settings()
        self.sound = Sounds(self)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.screen_caption)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        #  Passing self to the ship module will give it access to all the
        #  game resources. Without it, the ship will not be able to interact
        #  with the rest of the game
        #  We only make one instance of the ship for the entire game. In the
        #  stats module we keep track of how many lives the player has left.
        #  When the ship is hit, we only change a stat and don't create a new instance
        #  of the ship class.
        self.ship = Ship(self)
        #  We don't have to pass self to settings, as the settings store variables
        #  used throughout the game and doesn't have to interact with the instance of the game
        #  TODO: Load the high score from the previous save file if it exists
        self.settings.load_high_score()

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.background = Background(self)
        self.title_screen = TitleScreen(self)
        self.game_running = True


    def main(self):
        """Start the main loop of the game"""
        #  Load and play the theme song
        self.pygame.mixer.music.load(self.sound.theme_song)
        self.pygame.mixer.music.set_volume(self.settings.music_volume)
        self.pygame.mixer.music.play(-1)
        while self.game_running:
            self.clock.tick(self.settings.FPS)
            self._check_events()
            #  This should only run when the game is active
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """A helper method to check for game events. Helper methods have
        a single leading _ to indicate that it is a helper. These are not
        usually called through an instance."""

        #  Watch for keyboard and mouse events
        #  event.get() returns a list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #  TODO: Save the high score to a file and load it again when opening the game
                self.settings.high_score = self.stats.score
                self.settings.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_title_button(mouse_pos)

    def _check_title_button(self, mouse_pos):
        """"Starts a new game when the player clicks on the play button"""
        if self.pygame.Rect.collidepoint(self.title_screen.quit_button_rect, mouse_pos):
            sys.exit()
        if self.pygame.Rect.collidepoint(self.title_screen.play_button_rect, mouse_pos):
            #  Make sure the speed settings are initialized everytime a player starts a new game
            self.settings.initialize_dynamic_settings()
            #  The game will start
            self.stats.game_active = True
            self.sound.play_sound(self.sound.play_pressed_sound, self.settings.play_selected_volume)
            sleep(0.5)
            self.pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #  Decrement ships left
            self.stats.ships_left -= 1

            #  Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet of aliens and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #  Pause for half a second
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.pygame.mouse.set_visible(True)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sound.play_sound(self.sound.bullet_fired, self.settings.bullet_volume)
            self.sound.sound_played = True

    def _update_bullets(self):
        """Update the position of the bullets and get rid of old bullets"""
        # Update the bullet positions
        self.bullets.update()
        # Get rid of bullets that have moved off the screen
        #  We have to work with a copy of the list of sprites. If
        #  self.bullets.update is called and no bullets exist as they were
        #  deleted, the program will crash(out of bounds in the list)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to collisions between bullets and aliens"""
        #  Check for any bullets that have hit aliens
        #       If so, get rid of the bullet and the alien
        #  This will return a dictionary of keys/values for 1st/2nd item
        #  This tells pygame to check for collisions between the bullets and aliens
        #  The two boolean args tells pygame to delete both elements(Alien and bullet)
        #  You can make a bullet pass through all aliens by passing False for bullets(1st arg)
        #  TODO: The collisions should be updated to include damage done by different bullets(And sounds)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.sound.play_sound(self.sound.alien_hit, self.settings.alien_hit_volume)
            self.sound.sound_played = True

            #  This will ensure that multiple bullet hits will be recorded on every pass of the loop
            #  If this isn't done, only the first bullet will record score
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
        #  When all the aliens are destroyed
        if not self.aliens:
            #  Destroy the existing bullets
            self.bullets.empty()
            #  Create a new fleet of aliens
            self._create_fleet()
            #  Now that all the aliens have been destroyed, speed up the game
            self.settings.increase_speed()
            #  TODO: Save the current high score if greater than the previous one

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in a row"""
        #  Passing the row number enables the population of the different
        #  color aliens
        alien = Alien(self, row_number)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        #  This is where the first alien will be placed and will affect
        #  all the other aliens in the different rows
        alien.rect.x = alien.x - self.settings.starting_x_offset
        alien.rect.y = alien_height + 2 * alien.rect.height * \
            row_number - self.settings.starting_y_offset
        self.aliens.add(alien)

    def _create_fleet(self):
        """Create a fleet of aliens"""
        #  Create an alien and find the number of aliens in a row.
        #  Spacing between each alien is equal to one aliens' width

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - alien_width
        number_alien_x = available_space_x // (alien_width * 2)

        #  Determine the number of rows of aliens that fit on the screen

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height
                             - (2 * alien_height) - ship_height)

        number_of_rows = available_space_y // (2 * alien_height)

        #  Create a full fleet of aliens
        for row_number in range(number_of_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then
        update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        #  This takes two arguments, a sprite and a group
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #  Look for aliens that hit the bottom of the screen
        self._check_alien_bottom()

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_alien_bottom(self):
        """Determine if any alien reach the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #  Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        """Update the images on the screen and flip to a new screen"""
        self.clock.tick(60)
        # self.screen.fill(self.settings.bg_color)
        self.background.display_background()
        self.ship.display_ship()
        #  Draw the bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #  Draw the scoreboard on the screen, behind the aliens
        self.sb.show_score()
        #  Draw the aliens
        self.aliens.draw(self.screen)

        if not self.stats.game_active:
            self.title_screen.draw_title_screen()
        #  Makes the most recently drawn screen visible
        #  Using pygame.display.update(), you can update portions of the
        #  display

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.main()
