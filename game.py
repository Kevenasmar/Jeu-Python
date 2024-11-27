import pygame
import random
from unit import *

# Constants for the game layout
GRID_SIZE = 16  # 16x16 map
LOG_WIDTH_CELLS = 8  # Log area width in cells
CELL_SIZE = 45  # Size of each cell

# Dimensions
MAP_WIDTH = GRID_SIZE * CELL_SIZE  # Width of the map in pixels
LOG_WIDTH = LOG_WIDTH_CELLS * CELL_SIZE  # Width of the log area in pixels
TOTAL_WIDTH = MAP_WIDTH + LOG_WIDTH  # Total width of the screen
TOTAL_HEIGHT = GRID_SIZE * CELL_SIZE  # Height of the screen

BLACK, WHITE, RED, GREEN = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player_units = [
            Archer(0, 0, 100, 5, 2, 3, 1, 'C:/Users/keven/OneDrive/Desktop/Jeu python/Photos/archer.jpg', 'player'),
            Mage(1, 0, 100, 3, 1, 1, 1, 'C:/Users/keven/OneDrive/Desktop/Jeu python/Photos/mage.jpg', 'player'),
            Giant(2, 0, 100, 10, 1, 1, 3, 'C:/Users/keven/OneDrive/Desktop/Jeu python/Photos/giant.jpg', 'player')
        ]

        self.enemy_units = [
            Archer(5, 6, 100, 5, 2, 3, 1, 'C:/Users/keven/OneDrive/Desktop/Jeu python/Photos/enemy_archer.jpg', 'enemy'),
            Mage(6, 6, 100, 3, 1, 1, 1, 'C:/Users/keven/OneDrive/Desktop/Jeu python/Photos/enemy_mage.png', 'enemy'),
            Giant(7, 6, 100, 10, 1, 1, 3, 'C:/Users/keven/OneDrive/Desktop/Jeu python/Photos/enemy_giant.png', 'enemy')
        ]
        self.logs = []  # Store game logs

    def display_logs(self):
        """Displays game logs in the log area (right side)."""
        font = pygame.font.Font(None, 24)
        log_x = MAP_WIDTH  # Start of the log area (to the right of the map)
        log_y = 0

        # Draw background for log area
        pygame.draw.rect(self.screen, BLACK, (log_x, 0, LOG_WIDTH, TOTAL_HEIGHT))

        # Render each log message
        for i, log in enumerate(self.logs[-16:]):  # Show up to 16 logs
            log_surface = font.render(log, True, WHITE)
            self.screen.blit(log_surface, (log_x + 10, log_y + i * CELL_SIZE))


    def add_log(self, message):
        """Adds a log message."""
        self.logs.append(message)

    def calculate_valid_cells(self, unit):
        """Calculate accessible cells for a unit."""
        valid_cells = []
        for dx in range(-unit.speed, unit.speed + 1):
            for dy in range(-unit.speed, unit.speed + 1):
                if abs(dx) + abs(dy) <= unit.speed:  # Manhattan distance
                    x, y = unit.x + dx, unit.y + dy
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:  # Grid limits
                        valid_cells.append((x, y))
        return valid_cells

    def draw_static_elements(self, valid_cells):
        """
        Redraw the grid, log area, and highlight the cell under the cursor in red 
        if it is within the valid movement cells.
        """
        self.screen.fill(BLACK)

        # Draw grid
        for x in range(0, MAP_WIDTH, CELL_SIZE):
            for y in range(0, TOTAL_HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Highlight valid cells in yellow
        for x, y in valid_cells:
            valid_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), valid_rect, 0)  # Filled yellow

        # Highlight the cell under the mouse cursor in red if valid
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cursor_x, cursor_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

        if (cursor_x, cursor_y) in valid_cells:
            highlight_rect = pygame.Rect(cursor_x * CELL_SIZE, cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, RED, highlight_rect, 0)  # Filled red for the cursor

        # Draw log section
        log_x = MAP_WIDTH  # Start of the log area (right after the game map)
        pygame.draw.rect(self.screen, BLACK, (log_x, 0, LOG_WIDTH, TOTAL_HEIGHT))  # Log area background
        pygame.draw.rect(self.screen, WHITE, (log_x, 0, LOG_WIDTH, TOTAL_HEIGHT), 2)  # Log area border


    def draw_highlighted_cells(self, valid_cells, selected_unit):
        """Highlight accessible cells and the selected unit."""
        for x, y in valid_cells:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 0)  # Yellow fill

        # Highlight the selected unit in green
        rect = pygame.Rect(selected_unit.x * CELL_SIZE, selected_unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, GREEN, rect, 2)

        # Redraw units
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

    def handle_player_turn(self):
        """Handles the player's turn."""
        for selected_unit in self.player_units:
            if self.check_game_over():
                return

            has_acted = False
            valid_cells = self.calculate_valid_cells(selected_unit)

            while not has_acted:
                # Redraw everything: grid, valid cells, and units
                self.draw_static_elements(valid_cells)
                for unit in self.player_units + self.enemy_units:
                    unit.draw(self.screen)  # Redraw all units
                pygame.display.flip()  # Update the screen

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        new_x, new_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                        if (new_x, new_y) in valid_cells:  # Validate move
                            selected_unit.move(new_x, new_y)
                            has_acted = True

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Skip turn
                        has_acted = True

    def handle_enemy_turn(self):
        """Handles the enemy player's turn by moving enemy units toward the nearest player unit."""
        for enemy_unit in self.enemy_units:
            if self.check_game_over():
                return

            # Find the nearest player unit
            nearest_player = None
            min_distance = float('inf')

            for player_unit in self.player_units:
                distance = abs(enemy_unit.x - player_unit.x) + abs(enemy_unit.y - player_unit.y)
                if distance < min_distance:
                    min_distance = distance
                    nearest_player = player_unit

            if nearest_player:
                # Determine movement direction toward the nearest player
                dx = 1 if enemy_unit.x < nearest_player.x else -1 if enemy_unit.x > nearest_player.x else 0
                dy = 1 if enemy_unit.y < nearest_player.y else -1 if enemy_unit.y > nearest_player.y else 0
                new_x, new_y = enemy_unit.x + dx, enemy_unit.y + dy

                # Ensure the move is valid (within grid bounds and unit speed)
                if abs(dx) + abs(dy) <= enemy_unit.speed and 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    enemy_unit.move(new_x, new_y)

                # Redraw the game after the enemy moves
                self.draw_static_elements([])
                for unit in self.player_units + self.enemy_units:
                    unit.draw(self.screen)
                pygame.display.flip()

    def flip_display(self):
        """Renders the game state with health bars."""
        # Fill the screen with black
        self.screen.fill(BLACK)

        # Draw the grid
        for x in range(0, MAP_WIDTH, CELL_SIZE):
            for y in range(0, TOTAL_HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Draw units and their health bars
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)  # Draw the unit image and selection
            unit.draw_healthbar(self.screen, unit.health)  # Draw the health bar

        # Update the display
        pygame.display.flip()
        

    def check_game_over(self):
        """Check if the game is over."""
        if not self.player_units:
            self.display_game_over("Enemy Wins!")
            return True
        elif not self.enemy_units:
            self.display_game_over("Player Wins!")
            return True
        return False

    def display_game_over(self, message):
        """Display the game over message."""
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render(message, True, RED)
        game_over_rect = game_over_surface.get_rect(center=(MAP_WIDTH// 2, TOTAL_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))  # Added space for logs
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
