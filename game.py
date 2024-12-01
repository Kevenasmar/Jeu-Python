import pygame
import random

from unit import *
from Tiles import *
from constante import GameConstantes as GC
from configureWorld import*
from World_Drawer import *
from world import*
from GameLog import * # type: ignore
# Setup tiles
tiles_kind = [
    SandTile(),  # False veut dire que la case n'est pas solide tu peux marcher
    RockTile(),
    WaterTile()
]

map = Map("map/start.map", tiles_kind, GC.CELL_SIZE)

class Game:
    def __init__(self, screen, tile_map):
        self.screen = screen
        self.game_log = GameLog(300, GC.HEIGHT, GC.WIDTH, 0, self.screen)
        self.player_units = [
           #(x, y, health, attack, defense, speed, vision, image_path, team)
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/archer.jpg', 'player'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/mage.jpg', 'player'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/giant.jpg', 'player')
        ]

        self.enemy_units = [
            Archer(5, 6, 100, 5, 2, 2, 3, 'Photos/enemy_archer.jpg', 'enemy'),
            Mage(6, 6, 100, 3, 1, 1, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(7, 6, 100, 10, 1, 1, 2, 'Photos/enemy_giant.png', 'enemy')
        ]

        self.tile_map = Map_Aleatoire(tile_map, TERRAIN_TILES, GC.CELL_SIZE)
        self.walkable_tiles = self.initisialize_walkable_tiles()
        #Call spawn_units after initializing player_units
        self.spawn_units()


    def calculate_valid_cells(self, unit):
        """Calculate accessible cells for a unit, excluding cells occupied by other units within its speed range."""
        valid_cells = []
        # Combine all units' positions
        all_units_positions = {(u.x, u.y) for u in self.player_units + self.enemy_units}

        for dx in range(-unit.speed, unit.speed + 1):
            for dy in range(-unit.speed, unit.speed + 1):
                if abs(dx) + abs(dy) <= unit.speed:  # Manhattan distance
                    x, y = unit.x + dx, unit.y + dy
                    if (
                        0 <= x < GC.WORLD_X and 0 <= y < GC.WORLD_Y  # Within grid bounds
                        and self.tile_map.is_walkable(x, y, unit)    # Tile is walkable
                        and (x, y) not in all_units_positions        # Not occupied by another unit
                    ):
                        valid_cells.append((x, y))

        return valid_cells

    ##################--------Making sure that the units doesn't spawn on non walkable tiles------------######## 
    def initisialize_walkable_tiles(self) :
        set_walkable_tiles = set () 
        for x in range (GC.WORLD_X):
            for y in range (GC.WORLD_Y):
                if any(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units):
                    set_walkable_tiles.add((x, y))
        return set_walkable_tiles
    
    def get_spawn_sector(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x = 0 #joueur spawn a la partie gauche de la map 
        sector_y = random.randint(0,2) #joueur spawn aleatoirement dans les 3 secteur gauche de la map
        return (player_sector_x*sector_width, sector_y*sector_height, sector_width, sector_height) 
        
    def find_spawn_location (self, nbr_units) :
        sector_x, sector_y, width, height = self.get_spawn_sector()        
        spawn_locations = []
        for x in range(sector_x, sector_x + width):
            for y in range(sector_y, sector_y + height):
                if all(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units):
                    spawn_locations.append((x, y))  
                    if len(spawn_locations) == nbr_units :
                        return spawn_locations
        return spawn_locations
    
    def spawn_units(self) : 
        spawn_location = self.find_spawn_location (len(self.player_units))

        for unit , location in zip (self.player_units, spawn_location) :
            unit.x, unit.y = location 
            self.game_log.add_message(f'{unit.__class__.__name__} spawned', 'other')
    
        self.game_log.draw()

    #################-----------------END OF THIS PART ---------------------------########
    def redraw_static_elements(self):
        """Redraw the grid and units."""
        self.screen.fill(GC.WHITE)  # Fill the screen with GREEN
        self.tile_map.draw(self.screen)
        # Draw the grid
        for x in range(0, GC.WIDTH, GC.CELL_SIZE):
            for y in range(0, GC.HEIGHT, GC.CELL_SIZE):
                rect = pygame.Rect(x, y, GC.CELL_SIZE, GC.CELL_SIZE)
        self.game_log.draw()
        pygame.display.flip()  # Update once
    
    def flip_display(self):
        """Renders the game state."""
        self.screen.fill(GC.WHITE) # Fill the screen with black
        self.tile_map.draw(self.screen)  # Draw the map

        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)  # Draw units
        self.game_log.draw()
        pygame.display.flip()  # Update the display
        



        
    def draw_highlighted_cells(self, valid_cells):
        """Draw an external blue border around the group of valid cells and fill the hovered cell in blue."""
        # Convert the valid_cells list to a set for faster neighbor lookups
        valid_cells_set = set(valid_cells)

        # Directions to check neighbors (top, right, bottom, left)
        directions = [
            (0, -1),  # Top
            (1, 0),   # Right
            (0, 1),   # Bottom
            (-1, 0)   # Left
        ]

        # Clear the screen and redraw the grid before drawing anything
        self.tile_map.draw(self.screen)

        # Loop through all valid cells and draw external borders
        for x, y in valid_cells:
            for i, (dx, dy) in enumerate(directions):
                neighbor = (x + dx, y + dy)

                # If the neighbor is not in valid_cells, draw the border
                if neighbor not in valid_cells_set:
                    start_pos = (x * GC.CELL_SIZE, y * GC.CELL_SIZE)  # Top-left of the cell
                    end_pos = list(start_pos)  # Copy of start_pos

                    # Adjust the line positions based on the direction
                    if i == 0:  # Top border
                        end_pos[0] += GC.CELL_SIZE
                    elif i == 1:  # Right border
                        start_pos = (start_pos[0] + GC.CELL_SIZE, start_pos[1])
                        end_pos = (start_pos[0], start_pos[1] + GC.CELL_SIZE)
                    elif i == 2:  # Bottom border
                        start_pos = (start_pos[0], start_pos[1] + GC.CELL_SIZE)
                        end_pos = (start_pos[0] + GC.CELL_SIZE, start_pos[1])
                    elif i == 3:  # Left border
                        end_pos[1] += GC.CELL_SIZE

                    # Draw the blue border line
                    pygame.draw.line(self.screen, (75, 118, 204), start_pos, end_pos, 2)

        # Highlight the hovered cell by filling it with blue
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_x, hover_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

        # If the hovered cell is in valid cells, fill it with blue
        if (hover_x, hover_y) in valid_cells_set:
            rect = pygame.Rect(hover_x * GC.CELL_SIZE, hover_y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (75, 118, 204, 100), rect)  # Fill the hovered cell with a blue overlay

        # Redraw all units to ensure they appear on top of the highlights
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Update the display to reflect all changes
        self.game_log.draw()
        pygame.display.update()


    def handle_player_turn(self):
        """Handle the player's turn without flickering."""
        for selected_unit in self.player_units:
            if self.check_game_over():
                return False
            
            selected_unit.is_selected = True  # Mark the unit as selected
            valid_cells = self.calculate_valid_cells(selected_unit)

            self.redraw_static_elements()  # Grid and units
            self.draw_highlighted_cells(valid_cells)
            has_acted = False
            
            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        new_x, new_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

                        if (new_x, new_y) in valid_cells:
                            selected_unit.move(new_x, new_y)
                            has_acted = True
                            selected_unit.is_selected = False
                            self.game_log.add_message(f"{selected_unit.__class__.__name__} mouved", 'mouvement')
                            self.game_log.draw()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:  # Skip turn with 's' key
                            has_acted = True
                            selected_unit.is_selected = False  # Deselect after skipping
                            self.game_log.add_message('You skipped your turn.', 'other')
                            self.game_log.draw()
                
                self.draw_highlighted_cells(valid_cells)

        
    def handle_enemy_turn(self):
        """Simple AI for the enemy's turn."""
        for enemy in self.enemy_units:
            if self.check_game_over():
                return

            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            new_x = enemy.x + dx
            new_y = enemy.y + dy

            if abs(new_x - enemy.x) + abs(new_y - enemy.y) <= enemy.speed and self.tile_map.is_walkable(new_x, new_y):
                enemy.move(new_x, new_y)
                self.game_log.add_message('Enemy moved', 'mouvement')

            if abs(enemy.x - target.x) <= enemy.range and abs(enemy.y - target.y) <= enemy.range:
                enemy.attack(target)
                self.game_log.add_message(f"{enemy.__class__.__name__} attacked {target.__class__.__name__}!", 'attack')
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.game_log.add_message(f"{target.__class__.__name__} was defeated!", 'lose')
        self.game_log.draw()
   

    def check_game_over(self):
        """Checks if the game is over and displays the winner."""
        if not self.player_units:
            self.game_log.add_message('Enemy wins', 'lose')
            return True
        elif not self.enemy_units:
            self.game_log.add_message('Player wins', 'win')
            return True
        return False

    def display_game_over(self, message):
        """Displays a game over message and stops the game."""
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render(message, True, (255, 0, 0))  # Assuming RED is defined
        game_over_rect = game_over_surface.get_rect(center=(GC.WIDTH // 2, GC.HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds
        pygame.quit()
        exit()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    WEIGHTS = [25, 40, 10, 40, 10, 10] # TERRAIN_TILES = { # Tuile d'eau,  # Tuile de sable, # Tuile de roche,# Tuile d'herbe, # Tuile de bois, # Tuile de montagne }}
    random_seed = random.randint(0, 1000)

    world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
    tile_map = world.get_tiled_map(WEIGHTS)

    screen = pygame.display.set_mode((GC.WIDTH+300, GC.HEIGHT), pygame.SRCALPHA)  # Added space for the game log

    pygame.display.set_caption("Strategic Game")

    game = Game(screen, tile_map)

    running = True
    while running:
        game.redraw_static_elements()  # Efface et redessine la carte initialement

        game.handle_player_turn()      # Tour du joueur
        if game.check_game_over():
            break

        game.handle_enemy_turn()       # Tour de l'ennemi
        if game.check_game_over():
            break

        pygame.display.flip()          # Un seul flip après tout
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()