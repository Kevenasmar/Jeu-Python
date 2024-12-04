import pygame
import random
from constante import GameConstantes as GC

class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    defense : int
        La défense de l'unité.
    speed : int
        La vitesse de déplacement de l'unité.
    vision : int
        La portée de vision de l'unité.
    image : Surface
        L'image de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(new_x, new_y)
        Déplace l'unité vers une nouvelle position.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur l'écran.
    draw_healthbar(screen)
        Dessine une barre de santé au-dessus de l'unité.
    """

    def __init__(self, x, y, health, attack_power, defense, speed, vision, image_path, team):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.vision = vision
        self.image = pygame.image.load(image_path).convert_alpha()  # Chargement de l'image
        self.image = pygame.transform.scale(self.image, (int( GC.CELL_SIZE), int( GC.CELL_SIZE)))  # Échelle de l'image
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, new_x, new_y):
        """Déplace l'unité vers une nouvelle position dans son rayon de vitesse."""
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.speed and 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE:
            self.x = new_x
            self.y = new_y
        else:
            print(f"Mouvement invalide : Position cible ({new_x}, {new_y}) hors limites.")

    
    def _in_range(self, target, attack_range):
        """Vérifier si la cible est dans la portée d'attaque."""
        return abs(self.x - target.x) <= attack_range and abs(self.y - target.y) <= attack_range
    
    #TO REMOVE 
    def attack(self, target):
        """Attacks a target unit."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power - target.defense
            if target.health < 0:
                target.health = 0  # Prevent negative health


    def draw(self, screen):
        """Displays the unit with the background, a health bar fully on the side, and the image."""
        # Draw the blue background if the unit is selected
        if self.is_selected:
            pygame.draw.rect(screen, (255,255,255), 
                            (self.x * GC.CELL_SIZE, self.y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE))

        # Draw the health bar
        self.draw_healthbar(screen)

        # Draw the unit's image
        image_rect = self.image.get_rect()
        image_rect.center = (self.x * GC.CELL_SIZE + GC.CELL_SIZE // 2, self.y * GC.CELL_SIZE + GC.CELL_SIZE // 2)
        screen.blit(self.image, image_rect)






    def draw_healthbar(self, screen):
        """Draws a vertical health bar fully aligned on the right side of the unit's cell."""
        bar_width = 5  # Narrow health bar
        bar_height = GC.CELL_SIZE  # Full height of the cell
        bar_x = self.x * GC.CELL_SIZE + GC.CELL_SIZE - bar_width  # Align to the right edge of the cell
        bar_y = self.y * GC.CELL_SIZE  # Align with the top of the cell

        # Red bar (background - max health)
        pygame.draw.rect(screen, GC.RED, (bar_x, bar_y, bar_width, bar_height))

        # Green bar (current health)
        current_health_height = max(0, bar_height * (self.health / 100))  # Prevent negative height
        green_bar_y = bar_y + (bar_height - current_health_height)  # Align green bar to the bottom of the red bar
        pygame.draw.rect(screen, GC.GREEN, (bar_x, green_bar_y, bar_width, current_health_height))






class Archer(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.dot_targets = {}  # Suivre les unités affectées par la flèche en feu
        #Attack ranges
        self.normal_arrow_range = 3
        self.fire_arrow_range = 5
        self.ranges = [self.normal_arrow_range, self.fire_arrow_range]

    def normal_arrow(self, target):
        """Flèche normale."""
        target.health -= self.attack_power

    def fire_arrow(self, target):
        """Flèche en feu, applique des effets de dégâts sur la durée (Damage Over Time DoT)."""
        initial_damage = self.attack_power // 2
        dot_damage = self.attack_power // 4
        target.health -= initial_damage
        self.dot_targets[target] = {'damage': dot_damage, 'turns': 3}

    def apply_dot(self):
        """Applique le DoT sur les ennemis affectés."""
        for target, effect in list(self.dot_targets.items()):
            if effect['turns'] > 0:
                target.health -= effect['damage']
                effect['turns'] -= 1
            else:
                del self.dot_targets[target]


class Giant(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.punch_range = 1
        self.stomp_range = 2
        self.ranges = [self.punch_range, self.stomp_range]

    def punch(self, target):
        """
        Punch ability:
        - Deals heavy damage to the target.
        """
        target.health -= self.attack_power * 2  # High damage
        if target.health < 0:
            target.health = 0  # Prevent health from going negative

    def stomp(self, target, all_units, tile_map, game_instance):
        """
        Executes the stomp ability:
        - Deals full damage to the primary target (red tile).
        - Deals 50% damage to enemies on secondary tiles (yellow tiles).
        - Knocks all affected units back away from the Giant.
        """
        primary_damage = self.attack_power * 3  # Full damage
        secondary_damage = primary_damage // 2  # 50% damage

        # Apply full damage and knockback to the primary target
        target.health -= primary_damage
        if target.health < 0:
            target.health = 0
        self.apply_knockback(target, (self.x, self.y), tile_map, game_instance)

        # Determine all secondary tiles (yellow tiles)
        secondary_tiles = [
            (target.x - 1, target.y - 1),  # Top-left
            (target.x, target.y - 1),     # Top-center
            (target.x + 1, target.y - 1), # Top-right
            (target.x - 1, target.y),     # Left
            (target.x + 1, target.y),     # Right
            (target.x - 1, target.y + 1), # Bottom-left
            (target.x, target.y + 1),     # Bottom-center
            (target.x + 1, target.y + 1)  # Bottom-right
        ]

        # Apply damage and knockback to enemies in secondary tiles
        for unit in all_units:
            if (unit.x, unit.y) in secondary_tiles:
                # Apply 50% damage
                unit.health -= secondary_damage
                if unit.health < 0:
                    unit.health = 0

                # Apply knockback to secondary units
                self.apply_knockback(unit, (self.x, self.y), tile_map, game_instance)

    def apply_knockback(self, unit, stomp_origin, tile_map, game_instance):
        """
        Knocks a unit away from the stomp origin.
        If the resulting position is invalid, the unit doesn't move.
        """
        dx = unit.x - stomp_origin[0]
        dy = unit.y - stomp_origin[1]

        # Normalize direction to calculate knockback
        if dx != 0:
            dx = int(dx / abs(dx))
        if dy != 0:
            dy = int(dy / abs(dy))

        # Calculate the new position for knockback
        new_x = unit.x + dx
        new_y = unit.y + dy

        # Validate the new position
        if (0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and 
                tile_map.is_walkable(new_x, new_y, unit) and not game_instance.is_occupied(new_x, new_y)):
            unit.x = new_x
            unit.y = new_y



class Mage(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.can_walk_on_water = True
        self.heal_range = 1
        self.potion_range = 6
        self.ranges = [self.heal_range, self.potion_range]
        
    def potion(self, target):
        """Jette une potion magique"""
        target.health -= self.attack_power  # Dégâts faibles

    def heal_allies(self, target):
        """Heal an allied unit."""
        if target.team == self.team:  # Only heal allies
            target.health += self.attack_power
            target.health = min(target.health, 100)  # Cap health at 100
        else:
            print(f"Cannot heal {target.__class__.__name__}, they are not an ally!")

class Bomber(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.bomb_range = 2  # AoE radius for the bomb
        self.ranges = [self.bomb_range]  # Bomb's attack range

    def throw_bomb(self, target, all_units, tile_map, game_instance):
        """
        Throws a bomb at the specified target, dealing AoE damage to all units within range.
        Applies knockback to all affected units.
        """
        affected_units = []  # List to store all units affected by the bomb

        # Identify units within the bomb's AoE (Manhattan distance)
        for unit in all_units:
            # Calculate Manhattan distance between the bomb target and the unit
            distance = abs(unit.x - target.x) + abs(unit.y - target.y)

            if distance <= self.bomb_range:  # Check if the unit is within AoE
                affected_units.append(unit)

        # Apply AoE damage to all affected units, including the Bomber
        for unit in affected_units:
            # Apply the damage based on the Bomber's attack power
            damage = self.attack_power  # Ensure `self.attack_power` is an integer
            unit.health -= damage

            # Check if the unit's health drops to 0 or below
            if unit.health <= 0:
                # We can log the death of the unit but not the knockback
                game_instance.game_log.add_message(
                    f"{unit.__class__.__name__} at ({unit.x}, {unit.y}) has been defeated!", 'dead'
                )

            # Apply knockback effect (without logging)
            self.apply_knockback(unit, target, game_instance)

        # Ensure game_log is drawn after all updates
        game_instance.game_log.draw()

    def apply_knockback(self, unit, target, game_instance):
        """
        Applies knockback to the unit.
        - If it's the target (B), knockback happens in a random direction.
        - Otherwise, knockback happens away from the source (the Bomber).
        """
        # If the unit is the target (B), apply random knockback
        if unit == target:
            self.knockback_random(unit, game_instance)  # Ensure this method exists
        else:
            # Apply knockback away from the Bomber
            self.knockback_away_from_source(unit, game_instance)

    def knockback_random(self, unit, game_instance):
        """
        Apply random knockback to the target unit (B).
        This will avoid occupied tiles (including the Bomber's own tile).
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        random.shuffle(directions)  # Randomize the order of directions

        for dx, dy in directions:
            new_x = unit.x + dx
            new_y = unit.y + dy

            # Check if the new position is within bounds, walkable, and unoccupied
            if 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE:
                # Ensure that the new position is not occupied by any other unit
                if game_instance.tile_map.is_walkable(new_x, new_y, unit) and not self.is_occupied(new_x, new_y, game_instance):
                    # If walkable and unoccupied, move the unit
                    unit.x = new_x
                    unit.y = new_y
                    break  # Stop after the first valid knockback direction

    def knockback_away_from_source(self, unit, game_instance):
        """
        Apply knockback to the unit away from the source (Bomber).
        This ensures the Bomber gets knocked back if it is affected.
        """
        # Calculate direction away from the bomber (source)
        dx = unit.x - self.x  # Difference in x
        dy = unit.y - self.y  # Difference in y

        # Normalize direction to get a unit vector
        if dx != 0:
            dx = int(dx / abs(dx))  # Normalize x direction
        if dy != 0:
            dy = int(dy / abs(dy))  # Normalize y direction

        # Calculate the new position
        new_x = unit.x + dx
        new_y = unit.y + dy

        # Check if the new position is within bounds and walkable
        if 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and game_instance.tile_map.is_walkable(new_x, new_y, unit):
            unit.x = new_x
            unit.y = new_y

    def is_occupied(self, x, y, game_instance):
        """
        Check if the tile at (x, y) is occupied by any unit.
        """
        for unit in game_instance.player_units_p1 + game_instance.player_units_p2:
            if unit.x == x and unit.y == y:
                return True  # The tile is occupied
        return False  # The tile is not occupied
