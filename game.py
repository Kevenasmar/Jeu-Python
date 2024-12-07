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
           #(x, y, points de vie, statistique d'attaque, statistique de défense, vitesse, vision, image, équipe)
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/archer.png', 'player'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/mage.png', 'player'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/giant.png', 'player'),
            Bomber(3, 0, 100, 7, 1, 4, 2, 'Photos/bomber.png', 'player')
        ] 

        self.player_units_p2 = [ 
            Archer(0, 0, 100, 5, 2, 5, 3, 'Photos/enemy_archer.png', 'enemy'),
            Mage(1, 0, 100, 3, 1, 4, 2, 'Photos/enemy_mage.png', 'enemy'),
            Giant(2, 0, 100, 10, 1, 3, 2, 'Photos/enemy_giant.png', 'enemy'),
            Bomber(3, 0, 100, 7, 1, 4, 2, 'Photos/enemy_bomber.png', 'enemy')
        ]

        self.tile_map = Map_Aleatoire(tile_map, TERRAIN_TILES, GC.CELL_SIZE)
        self.walkable_tiles = self.inititialize_walkable_tiles()
        self.spawn_units()

    '''--------S'assurer que les unités n'apparaissent pas sur des cases non praticables------------''' 
    def inititialize_walkable_tiles(self) :
        set_walkable_tiles = set () 
        for x in range (GC.WORLD_X):
            for y in range (GC.WORLD_Y):
                if any(self.tile_map.is_walkable(x, y, unit) for unit in self.player_units_p1 + self.player_units_p1 ):
                    set_walkable_tiles.add((x, y))
        return set_walkable_tiles
    
    '''Ici, on gère l'apparition des unités sur la map en début de jeu'''
    def get_spawn_sector_p1(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x_p1 = 0 #Le joueur 1 apparait dans la partie gauche de la map 
        sector_y = random.randint(0,2) 
        return (player_sector_x_p1*sector_width, sector_y*sector_height, sector_width, sector_height) 
    
    def get_spawn_sector_p2(self) :
        sector_width = GC.WORLD_X // 3 
        sector_height = GC.WORLD_Y // 3
        player_sector_x_p2 = 2 #Le joueur 2 apparait dans la partie droite de la map 
        sector_y = random.randint(0,2) 
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
        self.game_log.add_message("May the best player win!", 'action')

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

    
        def is_occupied(self, x, y):
            """
            Checks if the given tile (x, y) is occupied by any unit.
            Returns True if occupied, False otherwise.
            """
            for unit in self.player_units_p1 + self.player_units_p2:
                if unit.x == x and unit.y == y:
                    return True
            return False

    '''------------------Utilitaires, affichage et déplacement-----------------------'''
  
    def calculate_valid_cells(self, unit):
        """Retourne les cases accessibles pour une unité, en excluant les cases occupées par d'autres unités dans son rayon de déplacement."""
        valid_cells = []
        # Combiner les positions des unités
        all_units_positions = {(u.x, u.y) for u in self.player_units_p1 + self.player_units_p2}

        for dx in range(-unit.speed, unit.speed + 1):
            for dy in range(-unit.speed, unit.speed + 1):
                if abs(dx) + abs(dy) <= unit.speed:  # Distance de Manhattan 
                    x, y = unit.x + dx, unit.y + dy
                    if (
                        0 <= x < GC.WORLD_X and 0 <= y < GC.WORLD_Y  # Dans les limites de la grille
                        and self.tile_map.is_walkable(x, y, unit)    # La case est praticable
                        and (x, y) not in all_units_positions        # Non occupée par une unité
                    ):
                        valid_cells.append((x, y))

        return valid_cells
    
    def has_line_of_sight(self, start, end):
        """
        Vérifie s'il existe une ligne de vue dégagée entre deux points afin de gérer les attaques.
        Utilise l'algorithme de Bresenham pour tracer la ligne et vérifier les cases solides.
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
        """Redessine la grille et les unités"""
        self.screen.fill(GC.GREEN)  # Remplir l'écran avec du vert
        self.tile_map.draw(self.screen)
        # Dessine la grille
        for x in range(0, GC.WIDTH, GC.CELL_SIZE):
            for y in range(0, GC.HEIGHT, GC.CELL_SIZE):
                rect = pygame.Rect(x, y, GC.CELL_SIZE, GC.CELL_SIZE)
        self.game_log.draw()
        pygame.display.flip()  # Mise a jour
    
    def flip_display(self):
        """Retourne l'état du jeu."""
        self.screen.fill(GC.GREEN)  # Effacer l'écran
        self.tile_map.draw(self.screen)  # Dessine la map

        # Dessiner d'abord les cases surlignées
        if hasattr(self, 'valid_cells') and self.valid_cells:  # S'assurer que valid_cells soit bien définie
            self.draw_highlighted_cells(self.valid_cells)

        # Dessiner toutes les unités avec leurs bars de vie 
        for unit in self.player_units_p1 + self.player_units_p2:
            unit.draw(self.screen)

        self.game_log.draw()  # Dessiner le game log
        pygame.display.flip()  # Mettre à jour l'affichage 
    
    def draw_highlighted_cells(self, move_cells=None, direct_cells=None, secondary_cells=None, is_attack_phase=False):
        """
        Draw highlighted cells with distinct colors:
        - Movement cells: White external borders.
        - Direct attack cells: Red.
        - Secondary affected cells: Yellow.
        - Hovered cell: White for movement phase, Red for attack phase.
        """
        move_cells = move_cells or []
        direct_cells = direct_cells or []
        secondary_cells = secondary_cells or []

        # Redraw the grid before adding highlights
        self.tile_map.draw(self.screen)

        # Highlight movement cells (white borders)
        for x, y in move_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            if (x, y - 1) not in move_cells:  # Top border
                pygame.draw.line(self.screen, (255, 255, 255), rect.topleft, rect.topright, 2)
            if (x + 1, y) not in move_cells:  # Right border
                pygame.draw.line(self.screen, (255, 255, 255), rect.topright, rect.bottomright, 2)
            if (x, y + 1) not in move_cells:  # Bottom border
                pygame.draw.line(self.screen, (255, 255, 255), rect.bottomright, rect.bottomleft, 2)
            if (x - 1, y) not in move_cells:  # Left border
                pygame.draw.line(self.screen, (255, 255, 255), rect.bottomleft, rect.topleft, 2)

        # Highlight direct attack cells (red)
        for x, y in direct_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)  # Red border for attack cells

        # Highlight secondary affected cells (yellow)
        for x, y in secondary_cells:
            rect = pygame.Rect(x * GC.CELL_SIZE, y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 2)  # Yellow border for secondary cells

        # Highlight hovered cell
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_x, hover_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
        hover_color = (255, 0, 0, 100) if is_attack_phase else (255, 255, 255, 100)
        if (hover_x, hover_y) in move_cells + direct_cells + secondary_cells:
            rect = pygame.Rect(hover_x * GC.CELL_SIZE, hover_y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE)
            pygame.draw.rect(self.screen, hover_color, rect)

        # Redraw units on top of highlighted cells
        for unit in self.player_units_p1 + self.player_units_p2:
            unit.draw(self.screen)

        # Update the game log and display
        self.game_log.draw()
        pygame.display.update()


    '''--------------------------------------Attaques-----------------------------------------'''
    
    def calculate_valid_attack_cells(self, unit, attack_range, opponent_units):
        '''Retourne les cases d'attaques valides pour une unité'''
        valid_attack_cells = []
        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                if abs(dx) + abs(dy) <= attack_range:  # Distance de Manhattan 
                    cell_x, cell_y = unit.x + dx, unit.y + dy

                    # S'assurer que la cellule soit dans la limite de la grille
                    if 0 <= cell_x < GC.WORLD_X and 0 <= cell_y < GC.WORLD_Y:
                        for opponent in opponent_units:
                            if (opponent.x, opponent.y) == (cell_x, cell_y):
                                if self.has_line_of_sight((unit.x, unit.y), (cell_x, cell_y)):
                                    valid_attack_cells.append(opponent)
                                    break
        return valid_attack_cells

    def calculate_valid_heal_cells(self, unit, heal_range, ally_units):
        '''Retourne les cases valides pour le mage lors de la selection "Heal"'''
        valid_heal_cells = []
        for dx in range(-heal_range, heal_range + 1):
            for dy in range(-heal_range, heal_range + 1):
                if abs(dx) + abs(dy) <= heal_range:  # Distance de Manhattan
                    cell_x, cell_y = unit.x + dx, unit.y + dy

                    # S'assurer que la cellule soit dans la limite de la grille
                    if 0 <= cell_x < GC.WORLD_X and 0 <= cell_y < GC.WORLD_Y:
                        # Vérifier si une unité alliée est dans la cellule
                        for ally in ally_units:
                            if (ally.x, ally.y) == (cell_x, cell_y) and ally.health < 100:  # Inclure uniquement les unités blessées
                                valid_heal_cells.append(ally)
                                break  

        return valid_heal_cells

    '''Les fonctions suivantes gèrent les attaques spécifiques de chaque type d'unité. 
    Elles déterminent les cibles valides pour chaque type d'attaque de l'unité 
    et exécutent l'action appropriée en fonction de la portée et des capacités disponibles.'''
    
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
            self.game_log.add_message("No enemies in range for Archer.", 'info')
            return

        self.perform_attack(archer, valid_attacks, opponent_units)
     
    def handle_attack_for_giant(self, giant, opponent_units):
        valid_attacks = {}

        # Check for punch targets
        if giant.punch_range:
            valid_targets = self.calculate_valid_attack_cells(giant, giant.punch_range, opponent_units)
            if valid_targets:
                valid_attacks["Punch"] = (giant.punch, valid_targets)

        # Check for stomp targets
        if giant.stomp_range:
            valid_targets = self.calculate_valid_attack_cells(giant, giant.stomp_range, opponent_units)
            if valid_targets:
                valid_attacks["Stomp"] = (giant.stomp, valid_targets)

        if not valid_attacks:
            self.game_log.add_message("No valid actions for Giant.", 'info')
            return

        # Present options to the player
        self.game_log.add_message("Choose your action:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            attack_options[i] = (method, targets)
            self.game_log.add_message(f"{i}: {action_name}", 'attack')

        self.game_log.draw()
        pygame.display.flip()

        # Let the player choose an action
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

        action_method, targets = chosen_action

        # Handle the chosen action
        valid_cells = [(unit.x, unit.y) for unit in targets]
        self.draw_highlighted_cells(direct_cells=valid_cells, is_attack_phase=True)

        # Execute the action
        target_chosen = False
        while not target_chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
                    if (target_x, target_y) in valid_cells:
                        selected_target = next(
                            (target for target in targets if (target.x, target.y) == (target_x, target_y)), None
                        )
                        if selected_target:
                            if action_method == giant.stomp:
                                action_method(
                                    target=selected_target,
                                    all_units=self.player_units_p1 + self.player_units_p2,
                                    tile_map=self.tile_map,
                                    game_instance=self
                                )
                            else:
                                action_method(selected_target)

                            self.game_log.add_message(
                                f"{giant.__class__.__name__} used {action_method.__name__} on {selected_target.__class__.__name__}.",
                                'attack'
                            )
                            target_chosen = True

        self.redraw_static_elements()
        self.flip_display()

    def handle_attack_for_bomber(self, bomber, opponent_units):
        valid_attacks = {}

        # Check for throw_bomb targets
        if bomber.bomb_range:
            valid_targets = self.calculate_valid_attack_cells(bomber, bomber.bomb_range, opponent_units)
            if valid_targets:
                valid_attacks["Throw Bomb"] = (bomber.throw_bomb, valid_targets)

        # Add explode action (doesn't require valid targets)
        if bomber.explode_range:
            all_units = self.player_units_p1 + self.player_units_p2
            valid_attacks["Explode"] = (bomber.explode, all_units)

        if not valid_attacks:
            self.game_log.add_message("No valid actions for Bomber.", 'info')
            return

        # Present options to the player
        self.game_log.add_message("Choose your action:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            attack_options[i] = (method, targets)
            self.game_log.add_message(f"{i}: {action_name}", 'attack')

        self.game_log.draw()
        pygame.display.flip()

        # Let the player choose an action
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

        action_method, targets = chosen_action

        # Handle the chosen action
        if action_method == bomber.explode:
            affected_units = action_method(targets, self)  # Execute explode
            affected_units_names = [unit.__class__.__name__ for unit in affected_units]
            self.game_log.add_message(
                f"Bomber sacrificed itself & exploded, affecting: {', '.join(affected_units_names)}.", 'attack'
            )
            # Remove the Bomber from the game
            if bomber in self.player_units_p1:
                self.player_units_p1.remove(bomber)
            elif bomber in self.player_units_p2:
                self.player_units_p2.remove(bomber)
        else:  # Handle throw_bomb
            valid_cells = [(unit.x, unit.y) for unit in targets]
            self.draw_highlighted_cells(direct_cells=valid_cells, is_attack_phase=True)
            self.game_log.add_message("Choose a target for the bomb.", 'attack')
            self.game_log.draw()
            pygame.display.flip()

            target_chosen = False
            while not target_chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
                        if (target_x, target_y) in valid_cells:
                            selected_target = targets[valid_cells.index((target_x, target_y))]
                            action_method(
                                target=selected_target,
                                all_units=self.player_units_p1 + self.player_units_p2,
                                tile_map=self.tile_map,
                                game_instance=self
                            )
                            self.game_log.add_message(
                                f"Bomber threw a bomb at ({selected_target.x}, {selected_target.y}).", 'attack'
                            )
                            target_chosen = True

        self.redraw_static_elements()
        self.flip_display()


    def handle_attack_for_mage(self, mage, ally_units, opponent_units):
        valid_attacks = {}

        if mage.heal_range:
            valid_heal_targets = self.calculate_valid_heal_cells(mage, mage.heal_range, ally_units)
            if valid_heal_targets:
                valid_attacks["Heal"] = (mage.heal_allies, valid_heal_targets)

        if mage.potion_range:
            valid_attack_targets = self.calculate_valid_attack_cells(mage, mage.potion_range, opponent_units)
            if valid_attack_targets:
                valid_attacks["Potion"] = (mage.potion, valid_attack_targets)

        if not valid_attacks:
            self.game_log.add_message("No valid targets for Mage.", 'info')
            return

        self.perform_attack(mage, valid_attacks, opponent_units + ally_units) 

    def perform_attack(self, unit, valid_attacks, all_units):
        """
        This function executes an attack for a given unit. It displays available actions,
        allows the player to choose an action, and applies the selected action to a target.
        """
        if not valid_attacks:
            self.game_log.add_message(f"No valid targets for {unit.__class__.__name__}.", 'info')
            return

        # Display available attack options
        self.game_log.add_message("Choose your action:", 'attack')
        attack_options = {}
        for i, (action_name, (method, targets)) in enumerate(valid_attacks.items(), start=1):
            # Extract valid target positions
            attack_options[i] = (method, [(target.x, target.y) for target in targets])
            self.game_log.add_message(f"{i}: {action_name}", 'attack')

        self.game_log.draw()
        pygame.display.flip()

        # Let the player choose an action
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

        action_method, valid_cells = chosen_action

        # Highlight the attack cells in red during the attack phase
        self.draw_highlighted_cells(direct_cells=valid_cells, is_attack_phase=True)

        # Handle Bomber-specific actions (e.g., explode or throw_bomb)
        if isinstance(unit, Bomber) and action_method in [unit.throw_bomb, unit.explode]:
            if action_method == unit.explode:
                # Execute explode action
                affected_units = action_method(all_units, self)
                affected_units_names = [unit.__class__.__name__ for unit in affected_units]
                self.game_log.add_message(
                    f"Bomber sacrificed itself and exploded, affecting: {', '.join(affected_units_names)}.", 'attack'
                )

                # Remove the Bomber after explosion
                if unit in self.player_units_p1:
                    self.player_units_p1.remove(unit)
                elif unit in self.player_units_p2:
                    self.player_units_p2.remove(unit)

                self.redraw_static_elements()
                self.flip_display()
                return
            else:
                # Handle throw_bomb action
                self.game_log.add_message("Choose a target for the bomb.", 'attack')
                self.game_log.draw()
                pygame.display.flip()

                target_chosen = False
                while not target_chosen:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE
                            if (target_x, target_y) in valid_cells:
                                selected_target = next(
                                    (target for target in all_units if (target.x, target.y) == (target_x, target_y)), None
                                )
                                if selected_target:
                                    action_method(
                                        target=selected_target,
                                        all_units=self.player_units_p1 + self.player_units_p2,
                                        tile_map=self.tile_map,
                                        game_instance=self
                                    )
                                    self.game_log.add_message(
                                        f"Bomber threw a bomb at ({selected_target.x}, {selected_target.y}).", 'attack'
                                    )
                                    target_chosen = True

                self.redraw_static_elements()
                self.flip_display()
                return

        # Standard attack logic for other units
        target_chosen = False
        while not target_chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    target_x, target_y = mouse_x // GC.CELL_SIZE, mouse_y // GC.CELL_SIZE

                    # Verify if the clicked cell corresponds to a valid target position
                    for target in all_units:
                        if (target.x, target.y) == (target_x, target_y) and (target_x, target_y) in valid_cells:
                            action_method(target)

                            # Check if the target has died
                            if target.health <= 0:
                                self.game_log.add_message(f"{target.__class__.__name__} has died!", 'dead')
                                if target in self.player_units_p1:
                                    self.player_units_p1.remove(target)
                                elif target in self.player_units_p2:
                                    self.player_units_p2.remove(target)

                            target_chosen = True
                            self.redraw_static_elements()
                            self.flip_display()
                            return



    '''----------------------------Logique de Jeu--------------------------------------'''

    def handle_player_turn(self, player_name, opponent_units, ally_units):
        """Gère le tour du joueur, incluant le mouvement et les attaques."""
        self.game_log.add_message(f"{player_name}'s turn", 'other')

        # Applique les effets DoT (Damage Over Time) pour l'Archer
        for archer in filter(lambda unit: isinstance(unit, Archer), self.player_units_p1 if player_name == "Player 1" else self.player_units_p2):
            archer.apply_dot()

        for selected_unit in (self.player_units_p1 if player_name == "Player 1" else self.player_units_p2):
            if self.check_game_over():
                return False

            selected_unit.is_selected = True
            self.redraw_static_elements()  # S'assurer que la grille est bien dessinée
            self.flip_display()
            has_acted = False

            # Phase de mouvement
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
                            selected_unit.is_selected = False

            if moving:
                valid_cells = self.calculate_valid_cells(selected_unit)
                self.draw_highlighted_cells(valid_cells)

                while not has_acted:
                    self.draw_highlighted_cells(valid_cells)

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

            # Phase d'attaque
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

            if in_range and not valid_attacks and los_blocked:
                # Ennemi dans la "Range" mais pas dans la "Line of Sight"
                self.game_log.add_message("Enemy in range but not in sight!", 'info')
                selected_unit.is_selected = False  # Désélectionner l'unité
                self.flip_display()
                continue

            if valid_attacks:
                # Ennemi dans la "Range" et dans la "Line of Sight"
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
                                selected_unit.is_selected = False

                if attacking:
                    self.game_log.add_message("Choose an action or skip (S) :", 'attack')
                    self.game_log.draw()
                    pygame.display.flip()

                    skipping = None
                    while skipping is None:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                    # Skip attack phase
                                    self.game_log.add_message("Attack skipped.", 'other')
                                    skipping = True
                                    selected_unit.is_selected = False  # Désélectionner l'unité
                                elif event.key == pygame.K_y:
                                    # Proceed to attack phase
                                    skipping = False

                    if skipping:
                        continue  # Skip to the next unit

                    # Appeler la fonction d'attaque correspondante
                    if isinstance(selected_unit, Archer):
                        self.handle_attack_for_archer(selected_unit, opponent_units)
                    elif isinstance(selected_unit, Giant):
                        self.handle_attack_for_giant(selected_unit, opponent_units)
                    elif isinstance(selected_unit, Mage):
                        self.handle_attack_for_mage(selected_unit, ally_units, opponent_units)
                    elif isinstance(selected_unit, Bomber):
                        self.handle_attack_for_bomber(selected_unit, opponent_units)

                    selected_unit.is_selected = False  # Fin du tour de l'unité
                    self.redraw_static_elements()
                    self.flip_display()
                    continue

            if not in_range and not valid_attacks:
                # No range and no LoS
                self.game_log.add_message("No enemies in range.", 'info')
                selected_unit.is_selected = False  # Désélectionner l'unité
                self.flip_display()
                continue

            if in_range and not valid_attacks:
                # LoS but no range
                self.game_log.add_message("Enemy in range but abilities are out of range.", 'info')
                selected_unit.is_selected = False  # Désélectionner l'unité
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
        """Vérifie si la partie est terminée et affiche le joueur gagnant."""
        if not self.player_units_p1:
            self.game_log.add_message('Player 2 wins!', 'win')
            return True
        elif not self.player_units_p2:
            self.game_log.add_message('Player 1 wins!', 'win')
            return True
        return False

    def display_game_over(self, message):
        """Affiche un message de fin de partie et ferme le jeu"""
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render(message, True, (255, 0, 0))  # Assuming RED is defined
        game_over_rect = game_over_surface.get_rect(center=(GC.WIDTH // 2, GC.HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds
        pygame.quit()
        exit()


    '''------------------Boucle Main-----------------------------------------------------------'''
    
def main():
    pygame.init()
    # Musique de fond
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("music/music.mp3")  
        pygame.mixer.music.play(-1)  
        pygame.mixer.music.set_volume(0.5) 
    except pygame.error as e:
        print(f"Error loading music: {e}") 
         
    clock = pygame.time.Clock()

    # Initialiser l'écran avec un espace supplémentaire pour le Game Log
    screen = pygame.display.set_mode((GC.WIDTH + 500, GC.HEIGHT), pygame.SRCALPHA)
    pygame.display.set_caption("Rise of Heroes")

    rematch = False  # Suivre si le joueur veut une revanche.

    while True:  # Boucle principale 
        if not rematch:
            action = main_menu(screen)  # Afficher le menu principal
        else:
            action = "play" 

        rematch = False  

        if action == "play":
            # Lancer le jeu
            random_seed = random.randint(0, 1000)  # Utiliser une graine aléatoire pour la génération de la carte
            WEIGHTS = [25, 40, 10, 40, 10, 10]  # TERRAIN_TILES poids
            world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
            tile_map = world.get_tiled_map(WEIGHTS)

            # Créer l'instance du jeu
            game = Game(screen, tile_map)
            winner = None
            running = True
            while running:
                game.redraw_static_elements()  # Dessine la map et l'état initial

                # Tour du Joueur 1
                game.handle_player_turn("Player 1", game.player_units_p2, game.player_units_p1)
                if game.check_game_over():
                    winner = "Player 1"
                    break

                # Tour du Joueur 2
                game.handle_player_turn("Player 2", game.player_units_p1, game.player_units_p2)
                if game.check_game_over():
                    winner = "Player 2"
                    break

                pygame.display.flip()  # Mise a jour de l'affichage une fois par cycle
                clock.tick(60)

            # Afficher le menu de fin de jeu 
            if winner:
                action = game_over_menu(screen, winner)
                if action == "rematch":
                    rematch = True  
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

        elif action == "how_to_play":
            # Afficher la page des règles du jeu
            p1_images = [
                pygame.image.load('Photos/archer.png'),
                pygame.image.load('Photos/mage.png'),
                pygame.image.load('Photos/giant.png'),
                pygame.image.load('Photos/bomber.png')
            ]
            p2_images = [
                pygame.image.load('Photos/enemy_archer.png'),
                pygame.image.load('Photos/enemy_mage.png'),
                pygame.image.load('Photos/enemy_giant.png'),
                pygame.image.load('Photos/enemy_bomber.png')
            ]
            for i in range(len(p1_images)):
                p1_images[i] = pygame.transform.scale(p1_images[i], (50, 50))
                p2_images[i] = pygame.transform.scale(p2_images[i], (50, 50))

            rules_action = rules_screen(screen, p1_images, p2_images)
            if rules_action == "back_to_menu":
                continue  # Retourner au menu principal

        elif action == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()