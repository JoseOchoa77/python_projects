import sys
from time import sleep

from settings import Settings

from alien import Alien
from ship import Ship
from game_stats import Gamestats
from bullet import Bullet

import pygame

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Dynamically get the display's width and height
        display_info = pygame.display.Info()
        self.settings.screen_width = display_info.current_w
        self.settings.screen_height = display_info.current_h

        # Set the game to fullscreen mode with the display's dimensions
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN
        )
        pygame.display.set_caption("Alien Invasion")

        # Create an instance of store game statistics.
        self.stats = Gamestats(self)

        # Create the ship
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        # Creates alien fleet
        self._create_fleet()

        # Set the background color
        self.bg_color = (230, 230, 230)

        # Start Alien Invasion in an active state.
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #functions that are called to check keypresses and releases, update screen elements and ship position on the screen.
            self._check_events()
            self._update_screen()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            else:
                self._show_game_over()
            # Refreshes the Frame
            self.clock.tick(60)

    # Method that checks keypresses.
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # update bullet positions:
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        if collisions:
            print(f"Aliens remaining: {len(self.aliens)}")

        if len(self.aliens) == 0:
            # Destroy existing bullets and create a new fleet.
            print("All aliens destroyed. Respawning fleet...")
            self.bullets.empty()
            self._create_fleet()
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False


        # Check for bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide( self.bullets, self.aliens, True, True)
                
    def _update_aliens(self):
        """ Check if fleet is at the edge of the screen then update the positions of the aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
        print("New fleet created.")

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    #Method that updates screen images
    def _update_screen(self):
         """Update images on the screen, and flip to the new screen."""
         self.screen.fill(self.settings.bg_color)
         for bullet in self.bullets.sprites():
             bullet.draw_bullet()
         self.ship.blitme()
         self.aliens.draw(self.screen)

         # Make the most recently drawn screen visible. 
         pygame.display.flip()

    def _show_game_over(self):
        """Display the Game Over message."""
        font = pygame.font.SysFont(None, 74)  # Choose a font and size
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))  # Red text
        text_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()  # Update the screen
        sleep(2)  # Pause for 2 seconds
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
