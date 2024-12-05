import pygame
import random

from unit import *
from Tiles import *
from constante import GameConstantes as GC
from configureWorld import*
from World_Drawer import *
from world import*
from GameLog import * # type: ignore
from menu import *  # Import menu functions
from collectible_items import *
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
        self.game_log = GameLog(500, GC.HEIGHT, GC.WIDTH, 0, self.screen)

        self.player_units_p1 = [ 
           #(x, y, health, attack, defense, speed, vision, image_path, team)
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/archer.png', 'player'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/mage.png', 'player'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/giant.png', 'player'),
            Bomber(3, 0, 100, 7, 1, 4, 2, 'Photos/bomber.png', 'player')
        ] 

<<<<<<< HEAD
        self.enemy_units = [
            Archer(5, 6, 100, 5, 2, 2, 3, 'Photos/enemy_archer.png', 'enemy'),
            Mage(6, 6, 100, 3, 1, 1, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(7, 6, 100, 10, 1, 1, 2, 'Photos/enemy_giant.png', 'enemy')
        ]
        
        self.player_units_p2 = [
=======
        self.player_units_p2 = [ 
>>>>>>> origin
           #(x, y, health, attack, defense, speed, vision, image_path, team)
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/enemy_archer.png', 'enemy'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/enemy_giant.png', 'enemy'),
            Bomber(3, 0, 100, 7, 1, 4, 2, 'Photos/enemy_bomber.png', 'enemy')
        ]

        self.tile_map = Map_Aleatoire(tile_map, TERRAIN_TILES, GC.CELL_SIZE)
        self.walkable_tiles = self.initisialize_walkable_tiles()

        # Initialize spawn for bomber units as well
        self.spawn_units()
        # gestionnaires de spawn 
        self.item_manager = ItemSpawnManager(GC.WORLD_X, GC.WORLD_Y, tile_map,self.game_log)

        # Liste des items actifs
        self.active_items = []
    '''--------Making sure that the units doesn't spawn on non walkable tiles------------''' 
    def initisialize_walkable_tiles(self) :
        set_walkable_tiles = set () 
        for x in range (GC.WORLD_X):
            for y in range (GC.WORLD_Y):
                if any(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p1 + self.player_units_p1 ):
                    set_walkable_tiles.add((x, y))
        return set_walkable_tiles
    
    def get_spawn_sector_p1(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x_p1 = 0 #joueur 1 spawn a la partie gauche de la map 
        sector_y = random.randint(0,2) #joueur spawn aleatoirement dans les 3 secteur gauche de la map
        return (player_sector_x_p1*sector_width, sector_y*sector_height, sector_width, sector_height) 
    
    def get_spawn_sector_p2(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x_p2 = 2 #joueur 2 spawn a la partie droite de la map 
        sector_y = random.randint(0,2) #joueur spawn aleatoirement dans les 3 secteur gauche de la map
        return (player_sector_x_p2*sector_width, sector_y*sector_height, sector_width, sector_height) 
    
    def find_spawn_location_p1 (self, nbr_units) :
        sector_x, sector_y, width, height = self.get_spawn_sector_p1()        
        spawn_locations = []
        for x in range(sector_x, sector_x + width):
            for y in range(sector_y, sector_y + height):
                if all(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p1):
                    spawn_locations.append((x, y))  
                    if len(spawn_locations) == nbr_units :
                        return spawn_locations
        return spawn_locations
    
    def find_spawn_location_p2 (self, nbr_units) :
        sector_x, sector_y, width, height = self.get_spawn_sector_p2()        
        spawn_locations = []
        for x in range(sector_x, sector_x + width):
            for y in range(sector_y, sector_y + height):
                if all(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p2):
                    spawn_locations.append((x, y))  
                    if len(spawn_locations) == nbr_units :
                        return spawn_locations
        return spawn_locations
    
    def spawn_units(self) : 
        self.game_log.add_message("May the best player win!", 'attack')

        #spawn joueur 1 
        spawn_location_p1 = self.find_spawn_location_p1 (len(self.player_units_p1))

        for unit , location in zip (self.player_units_p1, spawn_location_p1) :
            unit.x, unit.y = location     
        self.game_log.draw()

        #spawn joueur 2
        spawn_location_p2 = self.find_spawn_location_p2 (len(self.player_units_p2))

        for unit , location in zip (self.player_units_p2, spawn_location_p2) :
            unit.x, unit.y = location     
        self.game_log.draw()

    '''-----------------END OF THIS PART ---------------------------'''
    def is_occupied(self, x, y):
        """
        Checks if a tile is occupied by any unit.
        """
        for unit in self.player_units_p1 + self.player_units_p2:
            if unit.x == x and unit.y == y:
                return True
        return False
    
    #-----------------------Item Spawn------------------------------#
    def update_items(self):
        """Met à jour l'état des items"""
        for item in self.active_items:
            item.update_state()
            # Vérifier les collisions avec les unités
            for unit in self.player_units_p1 + self.player_units_p2:
                if item.collect(unit):
                    break
    
    def spawn_new_items(self):
        """Génère de nouveaux items si nécessaire"""
        # Exemple d'effets
        heal_effect = Effect(100, 20, 0, "heal")
        speed_effect = Effect(200, 2, 0, "Speed_Buff")
        power_effect = Effect(150, 10, 0, "Power_Buff")
        
        # Tenter de spawner différents types d'items
        effects = [heal_effect, speed_effect, power_effect]
        for effect in effects:
            item = self.item_manager.spawn_item(
                lambda x, y: Collectible_items(
                    x, y,
                    "item_type",
                    "images/item.png",
                    "sounds/collect.wav",
                    0, 1000, True,
                    effect
                )
            )
            if item:
                self.active_items.append(item)
    #------------Item spawned------------------#


    '''Utilities, display and movement'''
    def calculate_valid_cells(self, unit):
        """Calculate accessible cells for a unit, excluding cells occupied by other units within its speed range."""
        valid_cells = []
        # Combine all units' positions
        all_units_positions = {(u.x, u.y) for u in self.player_units_p1 + self.player_units_p2}

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
    
    def has_line_of_sight(self, start, end):
        """
        Check if there's an unobstructed line-of-sight between two points.
        Uses Bresenham's line algorithm to trace the line and checks for solid tiles.
        """
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            # Check if the tile at (x0, y0) is a wall
            tile = self.tile_map.terrain_tiles[self.tile_map.terrain_data[y0][x0]]
            if isinstance(tile, UnwalkableTile) and not isinstance(tile, WaterTile):  # Only walls block LoS
                return False

            if (x0, y0) == (x1, y1):  # Reached the target
                return True

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    
    def redraw_static_elements(self):
        """Redraw the grid and units."""
        self.screen.fill(GC.GREEN)  # Fill the screen with GREEN
        self.tile_map.draw(self.screen)
        # Draw the grid
        for x in range(0, GC.WIDTH, GC.CELL_SIZE):
            for y in range(0, GC.HEIGHT, GC.CELL_SIZE):
                rect = pygame.Rect(x, y, GC.CELL_SIZE, GC.CELL_SIZE)
        self.game_log.draw()
        pygame.display.flip()  # Update once
    
    def flip_display(self):
        """Renders the game state."""
        self.screen.fill(GC.GREEN)  # Clear the screen
        self.tile_map.draw(self.screen)  # Draw the map

        # Draw highlighted cells first
        if hasattr(self, 'valid_cells') and self.valid_cells:  # Ensure valid_cells is defined
            self.draw_highlighted_cells(self.valid_cells)

        # Draw all units (including health bars)
        for unit in self.player_units_p1 + self.player_units_p2:
            unit.draw(self.screen)

        self.game_log.draw()  # Draw the game log
        pygame.display.flip()  # Update the display
    
    def draw_highlighted_cells(self, move_cells=None, direct_cells=None, secondary_cells=None, is_attack_phase=False):
        """
        Draw highlighted cells with distinct colors:
        - Movement cells: White.
        - Direct attack cells: Red.
        - Secondary affected cells: Yellow.
        - Hovered cell: White for movement phase, Red for attack phase.
        """
        # Default to empty lists if None
        move_cells = move_cells or []
        direct_cells = direct_cells or []
        secondary_cells = secondary_cells or []

        # Directions to check neighbors (top, right, bottom, left)
        directions = [
            (0, -1),  # Top
            (1, 0),   # Right
            (0, 1),   # Bottom
            (-1, 0)   # Left
        ]

        # Clear the screen and redraw the grid before drawing anything
        self.tile_map.draw(self.screen)

        # Highlight movement cells (white)
        for x, y in move_cells:
            for i, (dx, dy) in enumerate(directions):
                neighbor = (x + dx, y + dy)
                if neighbor not in move_cells:
                    start_pos = (x * GC.CELL_SIZE, y * GC.CELL_SIZE)
                    end_pos = list(start_pos)

                    # Adjust line positions for the border
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

                    # Draw the border line (white for movement cells)
                    pygame.draw.line(self.screen, (255, 255, 255), start_pos, end_pos, 2)

        # Highlight direct attack cells (red)
        for x, y in direct_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)  # Red border for direct cells

        # Highlight secondary affected cells (yellow)
        for x, y in secondary_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)  # Yellow border for secondary cells

        # Highlight the hovered cell
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_x, hover_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
        hover_color = (255, 0, 0, 100) if is_attack_phase else (255, 255, 255, 100)

        if (hover_x, hover_y) in move_cells + direct_cells + secondary_cells:
            rect = pygame.Rect(hover_x * GC.CELL_SIZE, hover_y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, hover_color, rect)  # Fill hovered cell with the appropriate color

        # Redraw all units to ensure they appear on top of the highlights
        for unit in self.player_units_p1 + self.player_units_p2:
            unit.draw(self.screen)

        # Update the display to reflect all changes
        self.game_log.draw()
        pygame.display.update()



    '''Attacks'''
    def calculate_valid_attack_cells(self, unit, attack_range, opponent_units):
        """Update this function to calculate valid cells for the bomber."""
        valid_attack_cells = []
        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                if abs(dx) + abs(dy) <= attack_range:  # Manhattan distance
                    cell_x, cell_y = unit.x + dx, unit.y + dy

                    # Ensure the cell is within the grid boundaries
                    if 0 <= cell_x < GC.WORLD_X and 0 <= cell_y < GC.WORLD_Y:
                        for opponent in opponent_units:
                            if (opponent.x, opponent.y) == (cell_x, cell_y):
                                if self.has_line_of_sight((unit.x, unit.y), (cell_x, cell_y)):
                                    valid_attack_cells.append(opponent)
                                    break
        return valid_attack_cells


    def calculate_valid_heal_cells(self, unit, heal_range, ally_units):
        valid_heal_cells = []
        for dx in range(-heal_range, heal_range + 1):
            for dy in range(-heal_range, heal_range + 1):
                if abs(dx) + abs(dy) <= heal_range:  # Manhattan distance
                    cell_x, cell_y = unit.x + dx, unit.y + dy

                    # Ensure the cell is within the grid boundaries
                    if 0 <= cell_x < GC.WORLD_X and 0 <= cell_y < GC.WORLD_Y:
                        # Check if an ally unit is in the cell
                        for ally in ally_units:
                            if (ally.x, ally.y) == (cell_x, cell_y) and ally.health < 100:  # Only include injured allies
                                valid_heal_cells.append(ally)
                                break  # Stop further checks for this cell

        return valid_heal_cells

    def handle_attack_for_archer(self, archer, opponent_units):
        valid_attacks = {}
        if archer.normal_arrow_range:
            valid_targets = self.calculate_valid_attack_cells(archer, archer.normal_arrow_range, opponent_units)
            if valid_targets:
                valid_attacks["Normal Arrow"] = (archer.normal_arrow, valid_targets)

        if archer.fire_arrow_range:
            valid_targets = self.calculate_valid_attack_cells(archer, archer.fire_arrow_range, opponent_units)
            if valid_targets:
                valid_attacks["Fire Arrow"] = (archer.fire_arrow, valid_targets)

        if not valid_attacks:
            self.game_log.add_message("No enemies in range for Archer.", 'other')
            return

        self.perform_attack(archer, valid_attacks, opponent_units)
     
    def handle_attack_for_giant(self, giant, opponent_units):
        """
        Handles the Giant's attack logic, including Punch and Stomp.
        Highlights:
        - Punch: Direct target cells only.
        - Stomp: Direct cells in red and secondary affected cells in yellow.
        """
        valid_attacks = {}

        # Punch attack
        if giant.punch_range:
            valid_targets = self.calculate_valid_attack_cells(giant, giant.punch_range, opponent_units)
            if valid_targets:
                valid_attacks["Punch"] = (giant.punch, valid_targets)

        # Stomp attack
        if giant.stomp_range:
            valid_targets = self.calculate_valid_attack_cells(giant, giant.stomp_range, opponent_units)
            if valid_targets:
                # Highlight stomp cells
                direct_cells = [(target.x, target.y) for target in valid_targets]
                secondary_cells = [
                    (target.x + dx, target.y + dy)
                    for target in valid_targets
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Surrounding cells
                ]
                self.draw_highlighted_cells(direct_cells=direct_cells, secondary_cells=secondary_cells)

                valid_attacks["Stomp"] = (giant.stomp, valid_targets)

        # If no valid attacks
        if not valid_attacks:
            self.game_log.add_message("No enemies in range for Giant.", 'other')
            return

        # Perform the chosen attack
        self.perform_attack(giant, valid_attacks, opponent_units)


    def handle_attack_for_bomber(self, bomber, opponent_units):
        """
        Handles the Bomber's attack logic, allowing bombs to hit all units within range.
        Highlights:
        - Direct target cells in red.
        - Secondary affected cells in yellow for area-of-effect damage.
        """
        # Calculate valid targets within the Bomber's attack range
        valid_targets = self.calculate_valid_attack_cells(bomber, bomber.bomb_range, opponent_units)

        if not valid_targets:
            self.game_log.add_message("No valid targets for Bomber's bomb.", 'other')
            return

        # Highlight the bomb's AoE
        direct_cells = [(target.x, target.y) for target in valid_targets]
        secondary_cells = [
            (cell_x, cell_y)
            for target in valid_targets
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if (cell_x := target.x + dx) != target.x or (cell_y := target.y + dy) != target.y
        ]
        self.draw_highlighted_cells(direct_cells=direct_cells, secondary_cells=secondary_cells)

        # Perform the bomb attack
        self.perform_attack(bomber, {"Throw Bomb": (bomber.throw_bomb, valid_targets)}, opponent_units)


    
    def handle_attack_for_mage(self, mage, ally_units, opponent_units):
        valid_attacks = {}

        # Handle healing ability
        if mage.heal_range:
            valid_heal_targets = self.calculate_valid_heal_cells(mage, mage.heal_range, ally_units)
            if valid_heal_targets:
                valid_attacks["Heal"] = (mage.heal_allies, valid_heal_targets)

        # Handle attack ability
        if mage.potion_range:
            valid_attack_targets = self.calculate_valid_attack_cells(mage, mage.potion_range, opponent_units)
            if valid_attack_targets:
                valid_attacks["Potion"] = (mage.potion, valid_attack_targets)

        if not valid_attacks:
            self.game_log.add_message("No valid targets for Mage.", 'other')
            return

        self.perform_attack(mage, valid_attacks, opponent_units + ally_units)  # Include all units to validate the target

    def perform_attack(self, unit, valid_attacks, all_units):
        """
        Handles the selection and execution of an attack action for a unit.
        Highlights:
        - Initially, only direct cells are shown.
        - Secondary cells are shown after selecting an ability that involves them.
        """
        if not valid_attacks:
            self.game_log.add_message(f"No valid targets for {unit.__class__.__name__}.", 'other')
            return

        # Display available attack options
        self.game_log.add_message(f"Choose an action for {unit.__class__.__name__}:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            attack_options[i] = (action_name, method, targets)
            self.game_log.add_message(f"{i}: {action_name}", 'attack')

        self.game_log.draw()
        pygame.display.flip()

        # Wait for the player to choose an attack
        chosen_action = None
        while chosen_action is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                    action_index = int(event.unicode)
                    if action_index in attack_options:
                        chosen_action = attack_options[action_index]

        # Extract the chosen action details
        action_name, action_method, valid_targets = chosen_action

        # Calculate cells to highlight for attack
        direct_cells = [(target.x, target.y) for target in valid_targets]
        secondary_cells = []

        # If the chosen action has secondary effects, calculate them
        if hasattr(unit, 'stomp') and action_method == unit.stomp:
            for target in valid_targets:
                dx, dy = target.x - unit.x, target.y - unit.y
                secondary_cells += [
                    (target.x + dx, target.y + dy),       # Cell behind the target
                    (target.x - dy, target.y - dx),       # Perpendicular cell 1
                    (target.x + dy, target.y + dx)        # Perpendicular cell 2
                ]
        elif hasattr(unit, 'throw_bomb') and action_method == unit.throw_bomb:
            for target in valid_targets:
                secondary_cells += [
                    (target.x + dx, target.y + dy)
                    for dx in range(-1, 2)
                    for dy in range(-1, 2)
                    if (dx, dy) != (0, 0)  # Exclude the target cell itself
                ]

        # Highlight the target cells (include secondary cells only after the ability is selected)
        self.draw_highlighted_cells(direct_cells=direct_cells, secondary_cells=secondary_cells)

        # Wait for the player to select a target
        target_chosen = False
        while not target_chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

                    # Check if the selected cell matches any valid target
                    for target in valid_targets:
                        if (target.x, target.y) == (target_x, target_y):
                            # Handle special abilities with additional logic
                            if hasattr(unit, 'stomp') and action_method == unit.stomp:
                                action_method(target, all_units, self.tile_map, self)  # Pass all required context
                            elif hasattr(unit, 'throw_bomb') and action_method == unit.throw_bomb:
                                action_method(target, all_units, self.tile_map, self)
                            else:
                                action_method(target)  # Standard attacks

                            # Check if the target is dead
                            if target.health <= 0:
                                self.game_log.add_message(f"{target.__class__.__name__} has been defeated!", 'dead')
                                if target in self.player_units_p1:
                                    self.player_units_p1.remove(target)
                                elif target in self.player_units_p2:
                                    self.player_units_p2.remove(target)

                            # Log the action and end the target selection
                            self.game_log.add_message(
                                f"{unit.__class__.__name__} used {action_name} on {target.__class__.__name__}.",
                                'attack'
                            )
                            target_chosen = True

                            # Redraw the game state and update the display
                            self.redraw_static_elements()
                            self.flip_display()
                            return




    def handle_player_turn(self, player_name, opponent_units, ally_units):
        """Handle the player's turn, including movement and attacks."""
        self.game_log.add_message(f"{player_name}'s turn", 'other')
        for selected_unit in (self.player_units_p1 if player_name == "Player 1" else self.player_units_p2):
            if self.check_game_over():
                return False

            selected_unit.is_selected = True
            self.redraw_static_elements()  # Ensure grid is drawn
            self.flip_display()  # Ensure screen refresh includes units
            has_acted = False

            # Ask player if they want to move
            self.game_log.add_message(f"{selected_unit.__class__.__name__}'s turn. Move? (y/n)", 'mouvement')
            self.game_log.draw()
            pygame.display.flip()

            moving = None
            while moving is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            moving = True
                        elif event.key == pygame.K_n:
                            moving = False
                            selected_unit.is_selected = False  # Deselect the unit if not moved

            if moving:
                valid_cells = self.calculate_valid_cells(selected_unit)
                self.draw_highlighted_cells(move_cells=valid_cells)  # Highlight move cells in white

                while not has_acted:
                    self.draw_highlighted_cells(move_cells=valid_cells)  # Continuously redraw move highlights

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
                                self.game_log.add_message(f"{selected_unit.__class__.__name__} moved", 'mouvement')
                                self.redraw_static_elements()
                                self.flip_display()


            # Determine attack logic
            valid_attacks = []
            los_blocked = False
            in_range = False

            for opponent in opponent_units:
                for attack_range in selected_unit.ranges:
                    if selected_unit._in_range(opponent, attack_range):
                        in_range = True
                        if self.has_line_of_sight((selected_unit.x, selected_unit.y), (opponent.x, opponent.y)):
                            valid_attacks.append(opponent)
                        else:
                            los_blocked = True

            # Logic for handling various cases
            if in_range and not valid_attacks and los_blocked:
                # Range but no LoS
                self.game_log.add_message("Enemy in range but not in sight. Get a better visual!", 'other')
                selected_unit.is_selected = False  # Deselect the unit
                self.flip_display()
                continue

            if valid_attacks:
                # Range and LoS
                self.game_log.add_message(f"{selected_unit.__class__.__name__}'s turn. Attack? (y/n)", 'attack')
                self.game_log.draw()
                pygame.display.flip()

                attacking = None
                while attacking is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                attacking = True
                            elif event.key == pygame.K_n:
                                attacking = False
                                selected_unit.is_selected = False  # Skip attack, deselect unit

                if attacking:
                    # Call appropriate attack handler
                    if isinstance(selected_unit, Archer):
                        self.handle_attack_for_archer(selected_unit, opponent_units)
                    elif isinstance(selected_unit, Giant):
                        self.handle_attack_for_giant(selected_unit, opponent_units)
                    elif isinstance(selected_unit, Mage):
                        self.handle_attack_for_mage(selected_unit, ally_units, opponent_units)
                    elif isinstance(selected_unit, Bomber):
                        self.handle_attack_for_bomber(selected_unit, opponent_units)

                    selected_unit.is_selected = False  # End turn for the unit
                    self.redraw_static_elements()
                    self.flip_display()
                    continue

            if not in_range and not valid_attacks:
                # No range and no LoS
                self.game_log.add_message("No enemies in range. Moving to the next unit.", 'other')
                selected_unit.is_selected = False  # Deselect the unit
                self.flip_display()
                continue

            if in_range and not valid_attacks:
                # LoS but no range
                self.game_log.add_message("Enemy in range but abilities are out of range. Moving to the next unit.", 'other')
                selected_unit.is_selected = False  # Deselect the unit
                self.flip_display()
                continue


    def handle_enemy_turn(self):
        #Simple AI for the enemy's turn
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

            if abs(enemy.x - target.x) <= enemy.ranges and abs(enemy.y - target.y) <= enemy.ranges:
                enemy.attack(target)
                self.game_log.add_message(f"{enemy.__class__.__name__} attacked {target.__class__.__name__}!", 'attack')
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.game_log.add_message(f"{target.__class__.__name__} was defeated!", 'lose')
        self.game_log.draw()
   
    def check_game_over(self):
        """Checks if the game is over and displays the winner."""
        if not self.player_units_p1:
            self.game_log.add_message('Player 2 wins!', 'win')
            return True
        elif not self.player_units_p2:
            self.game_log.add_message('Player 1 wins!', 'win')
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
    # Initialize the mixer for background music
    pygame.mixer.init()

    
    # Load and play the background music
    try:
        pygame.mixer.music.load("music/music.mp3")  # Replace with your MP3 file's path
        pygame.mixer.music.play(-1)  # -1 makes it loop indefinitely
        pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)
    except pygame.error as e:
        print(f"Error loading music: {e}")
        
    clock = pygame.time.Clock()

    # Initialize the screen with extra space for the game log
    screen = pygame.display.set_mode((GC.WIDTH + 500, GC.HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Rise of Heroes")

<<<<<<< HEAD
    # Display the menu
    Display_menu = False
    if Display_menu: 
        from menu import main_menu, rules_screen  # Import menu functions
        action = main_menu(screen)  # Show the main menu
        if action == "play":
            # Show the rules screen
            p1_images = [
                pygame.image.load('Photos/archer.png'),
                pygame.image.load('Photos/mage.png'),
                pygame.image.load('Photos/giant.png'),
            ]
            p2_images = [
                pygame.image.load('Photos/enemy_archer.png'),
                pygame.image.load('Photos/enemy_mage.png'),
                pygame.image.load('Photos/enemy_giant.png'),
            ]
            for i in range(len(p1_images)):
                p1_images[i] = pygame.transform.scale(p1_images[i], (50, 50))
                p2_images[i] = pygame.transform.scale(p2_images[i], (50, 50))
=======
    rematch = False  # Tracks if the player wants a rematch
>>>>>>> origin

    while True:  # Main loop for handling restarts
        if not rematch:
            action = main_menu(screen)  # Show the main menu
        else:
            action = "play"  # Skip the main menu and go directly to the game

        rematch = False  # Reset rematch flag

        if action == "play":
            # Directly start the game
            random_seed = random.randint(0, 1000)  # Use a random seed for map generation
            WEIGHTS = [25, 40, 10, 40, 10, 10]  # TERRAIN_TILES weights
            world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
            tile_map = world.get_tiled_map(WEIGHTS)

            # Create the game instance
            game = Game(screen, tile_map)
            winner = None
            running = True
            while running:
                game.redraw_static_elements()  # Draw the map and initial state

                # Player 1's turn
                game.handle_player_turn("Player 1", game.player_units_p2, game.player_units_p1)
                if game.check_game_over():
                    winner = "Player 1"
                    break

<<<<<<< HEAD
        # Player 2's turn
        game.handle_player_turn("Player 2", game.player_units_p1, game.player_units_p2)
        if game.check_game_over():
            break
        
        game.update_items()
        game.spawn_new_items()
        pygame.display.flip()  # Update the display once per cycle
        clock.tick(60)
=======
                # Player 2's turn
                game.handle_player_turn("Player 2", game.player_units_p1, game.player_units_p2)
                if game.check_game_over():
                    winner = "Player 2"
                    break

                pygame.display.flip()  # Update the display once per cycle
                clock.tick(60)

            # Display Game Over menu and handle user action
            if winner:
                action = game_over_menu(screen, winner)
                if action == "rematch":
                    rematch = True  # Set rematch to True to restart the game immediately
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

        elif action == "how_to_play":
            # Show the rules screen
            p1_images = [
                pygame.image.load('Photos/archer.png'),
                pygame.image.load('Photos/mage.png'),
                pygame.image.load('Photos/giant.png'),
            ]
            p2_images = [
                pygame.image.load('Photos/enemy_archer.png'),
                pygame.image.load('Photos/enemy_mage.png'),
                pygame.image.load('Photos/enemy_giant.png'),
            ]
            for i in range(len(p1_images)):
                p1_images[i] = pygame.transform.scale(p1_images[i], (50, 50))
                p2_images[i] = pygame.transform.scale(p2_images[i], (50, 50))

            rules_action = rules_screen(screen, p1_images, p2_images)
            if rules_action == "back_to_menu":
                continue  # Return to the main menu

        elif action == "quit":
            pygame.quit()
            sys.exit()
>>>>>>> origin



if __name__ == "__main__":
    main()