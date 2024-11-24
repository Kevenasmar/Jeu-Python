import pygame
import random

from unit import *


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player_units = [
            Archer(0, 0, 100, 5, 2, 3, 1, 'archer.jpg', 'player'),  # Archer with health=10, attack=3, speed=2
            Mage(1, 0, 100, 3, 1, 1, 1, 'mage.jpg', 'player'),    # Mage with health=8, attack=4, speed=1
            Giant(2, 0, 150, 10, 1, 1, 3, 'giant.jpg', 'player')   # Giant with health=15, attack=5, speed=1
        ]

        self.enemy_units = [
            Archer(5, 6, 100, 5, 2, 3, 1, 'enemy_archer.png', 'enemy'),  # Archer with health=10, attack=3, speed=2
            Mage(6, 6, 100, 3, 1, 1, 1, 'enemy_mage.png', 'enemy'),    # Mage with health=8, attack=4, speed=1
            Giant(7, 6, 150, 10, 1, 1, 3, 'enemy_giant.png', 'enemy')   # Giant with health=15, attack=5, speed=1
        ]

    def display_log(self, message):
        """Displays a game log at the bottom of the screen."""
        font = pygame.font.Font(None, 36)
        log_surface = font.render(message, True, WHITE)
        log_rect = log_surface.get_rect(center=(WIDTH // 2, HEIGHT + 20))
        self.screen.blit(log_surface, log_rect)
        pygame.display.flip()

    def handle_player_turn(self):
        """Handles the player's turn."""
        for selected_unit in self.player_units:
            if self.check_game_over():
                return

            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Get the grid coordinates of the mouse click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        new_x = mouse_x // CELL_SIZE
                        new_y = mouse_y // CELL_SIZE
                        
                        # Attempt to move the unit
                        if abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y) <= selected_unit.speed:
                            selected_unit.move(new_x, new_y)
                            has_acted = True
                            selected_unit.is_selected = False
                            self.flip_display()
                        else:
                            print("Invalid move. Out of range!")

                    if event.type == pygame.KEYDOWN:
                        # Skip turn
                        if event.key == pygame.K_s:  # 'S' key to skip turn
                            has_acted = True
                            selected_unit.is_selected = False


    def handle_enemy_turn(self):
        """Simple AI for the enemy's turn."""
        for enemy in self.enemy_units:
            if self.check_game_over():  # Check if the game is over
                return

            # Random movement logic for simplicity
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            new_x = enemy.x + dx
            new_y = enemy.y + dy

            # Ensure the movement is valid within the grid and speed
            if abs(new_x - enemy.x) + abs(new_y - enemy.y) <= enemy.speed:
                enemy.move(new_x, new_y)

            # Attack if in range
            if abs(enemy.x - target.x) <= enemy.range and abs(enemy.y - target.y) <= enemy.range:
                enemy.attack(target)
                self.display_log(f"{enemy.__class__.__name__} attacked {target.__class__.__name__}!")
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.display_log(f"{target.__class__.__name__} was defeated!")


    def flip_display(self):
        """Renders the game state."""
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()
        
    def check_game_over(self):
        """Checks if the game is over and displays the winner."""
        if not self.player_units:
            self.display_game_over("Enemy Wins!")
            return True
        elif not self.enemy_units:
            self.display_game_over("Player Wins!")
            return True
        return False

    def display_game_over(self, message):
        """Displays a game over message and stops the game."""
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render(message, True, RED)
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds
        pygame.quit()
        exit()
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 40))  # Added space for the game log
    pygame.display.set_caption("Strategic Game")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        if game.check_game_over():
            break
        game.handle_enemy_turn()
        if game.check_game_over():
            break


if __name__ == "__main__":
    main()
