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
    image : Surface
        L'image de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.
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


    '''Méthodes'''

    def move(self, new_x, new_y):
        """Déplace l'unité vers une nouvelle position dans son rayon de vitesse."""
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.speed and 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE:
            self.x = new_x
            self.y = new_y
        else:
            print(f"Invalid Movement : Target Cell ({new_x}, {new_y}) out of limits.")

    def _in_range(self, target, attack_range):
        """Vérifier si la cible est dans la portée d'attaque."""
        return abs(self.x - target.x) <= attack_range and abs(self.y - target.y) <= attack_range
    
    def draw(self, screen):
        """Affiche l'unité avec une bar de vie et son image."""
        
        # Dessiner un fond blanc si l'unité est sélectionnée
        if self.is_selected:
            pygame.draw.rect(screen, (255,255,255), 
                            (self.x * GC.CELL_SIZE, self.y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE))

        # Dessiner la bar de vie
        self.draw_healthbar(screen)

        # Dessiner l'image de l'unité
        image_rect = self.image.get_rect()
        image_rect.center = (self.x * GC.CELL_SIZE + GC.CELL_SIZE // 2, self.y * GC.CELL_SIZE + GC.CELL_SIZE // 2)
        screen.blit(self.image, image_rect)

    def draw_healthbar(self, screen):
        """Dessine une bar de vie verticale alignée sur la bordure droite de a cellule de l'unité."""
        bar_width = 5 
        bar_height = GC.CELL_SIZE  
        bar_x = self.x * GC.CELL_SIZE + GC.CELL_SIZE - bar_width  
        bar_y = self.y * GC.CELL_SIZE  

        pygame.draw.rect(screen, GC.RED, (bar_x, bar_y, bar_width, bar_height))
        
        current_health_height = max(0, bar_height * (self.health / 100))  
        green_bar_y = bar_y + (bar_height - current_health_height)  
        pygame.draw.rect(screen, GC.GREEN, (bar_x, green_bar_y, bar_width, current_health_height))


'''--------------------------Les Différents Types d'unité et leurs Compétences-----------------------------------'''
'''Chaque unité a deux compétences propres a elle. Chaque compétence a une portée.'''


'''L'Archer'''

class Archer(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.dot_targets = {}  # Suivre les unités affectées par la flèche en feu
        #Portées d'attaque
        self.normal_arrow_range = 3
        self.fire_arrow_range = 5
        self.ranges = [self.normal_arrow_range, self.fire_arrow_range]

    def normal_arrow(self, target):
        """Flèche normale avec possibilité de mort instantanée. Le Headshot est géré dans le fichier game.py."""
        target.health -= self.attack_power - target.defense

    def fire_arrow(self, target):
        """Flèche en feu, applique des effets de dégâts sur la durée (Damage Over Time DoT)."""
        initial_damage = self.attack_power - target.defense
        dot_damage = self.attack_power - target.defense
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


'''Le Géant'''

class Giant(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.punch_range = 1
        self.stomp_range = 2 
        self.ranges = [self.punch_range, self.stomp_range]

    def is_occupied(self, x, y, units):
        """
        Vérifier si la case (x, y) est occupée par une unité.
        units: liste de toutes les unités dans le jeu.
        """
        return any(unit.x == x and unit.y == y for unit in units)

    def punch(self, target):
        """Inflige des dégâts importants à la cible."""
        target.health -= self.attack_power * 2 - target.defense  # Dégâts élevés

    def stomp(self, target, tile_map, units):
        """Inflict heavy damage and knock back the target. Finds an alternative
        valid tile if the initial knockback position is non-walkable.
        """
        target.health -= self.attack_power * 3 - target.defense  # Very high damage

        # Determine the knockback direction
        dx = target.x - self.x
        dy = target.y - self.y

        # Normalize the knockback direction
        if dx != 0:
            dx = int(dx / abs(dx))
        if dy != 0:
            dy = int(dy / abs(dy))

        # Apply the knockback
        new_x = target.x + dx
        new_y = target.y + dy

        # Check if the new position is within bounds and walkable
        if 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and tile_map.is_walkable(new_x, new_y, target) and not self.is_occupied(new_x,new_y,units):
            target.x, target.y = new_x, new_y
        else:
            # Collect adjacent valid tiles excluding the Giant's position
            adjacent_cells = [
                (target.x + nx, target.y + ny)
                for nx, ny in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                if 0 <= target.x + nx < GC.GRID_SIZE and 0 <= target.y + ny < GC.GRID_SIZE
                and tile_map.is_walkable(target.x + nx, target.y + ny, target)
                and (target.x + nx, target.y + ny) != (self.x, self.y)  # Exclude Giant's position
            ]

            # If valid tiles are found, choose one randomly
            if adjacent_cells:
                new_x, new_y = random.choice(adjacent_cells)
                target.x, target.y = new_x, new_y





'''Le Mage'''

class Mage(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.can_walk_on_water = True
        self.heal_range = 1
        self.potion_range = 6
        self.ranges = [self.heal_range, self.potion_range]
        
    def potion(self, target):
        """Jette une potion magique"""
        target.health -= self.attack_power - target.defense  # Dégâts faibles

    def heal_allies(self, target):
        """Soigne une unité alliée."""
        if target.team == self.team:  # Only heal allies
            target.health += self.attack_power
            target.health = min(target.health, 100)  # Cap health at 100
            if target.name == 'Giant':
                target.health = min(target.health, 125)
            if target.name == 'Mage':
                target.health = min(target.health, 75)
            print(f"Cannot heal {target.__class__.__name__}, they are not an ally!")


'''Le Bomber'''

class Bomber(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.bomb_range = 2  
        self.explode_range = 5
        self.ranges = [self.bomb_range, self.explode_range]  

    def throw_bomb(self, target, all_units, tile_map, game_instance):
        """
        Lance une bombe sur la cible spécifiée, infligeant des dégâts de zone (AoE) à toutes les unités dans la portée.
        Applique un effet de recul à toutes les unités affectées.
        """
        affected_units = []  #Liste pour stocker toutes les unités affectées par la bombe

        # Identifier les unités dans la portée de la bombe (Distance de Manhattan)
        for unit in all_units:
            distance = abs(unit.x - target.x) + abs(unit.y - target.y)

            if distance <= self.bomb_range:  # S'assurer que la cible est dans la portée d'attaque
                affected_units.append(unit)

        # Appliquer les dégâts pour toutes les unités affectées, y compris le Bomber 
        for unit in affected_units:
            # Appliquer le dégât 
            damage = self.attack_power  
            unit.health -= damage - target.defense

            # Vérifier si les points de vie de l'unité deviennent nuls
            if unit.health <= 0:
                game_instance.game_log.add_message(
                    f"{unit.__class__.__name__} at ({unit.x}, {unit.y}) has been defeated!", 'dead'
                )

            # Appliquer l'effet de recul 
            self.apply_knockback(unit, target, game_instance)

        game_instance.game_log.draw()

    def apply_knockback(self, unit, target, game_instance):
        """
        Applique un effet de recul à l'unité.
        Si c'est la cible, le recul se fait dans une direction aléatoire.
        Sinon, le recul s'éloigne de la source.
        """
        # Si l'unité est la cible, appliquer un effet de recul random 
        if unit == target:
            self.knockback_random(unit, game_instance)  # Ensure this method exists
        else:
            # Appliquer un effet de recul loin du Bomber
            self.knockback_away_from_source(unit, game_instance)

    def knockback_random(self, unit, game_instance):
        """
        Appliquer un effet de recul aléatoire à l'unité cible.
        Cela évitera les cases occupées (y compris celle du Bomber lui-même)
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, bas, gauche, droite
        random.shuffle(directions)  # Ordre de directions random

        for dx, dy in directions:
            new_x = unit.x + dx
            new_y = unit.y + dy

            # Vérifier si la nouvelle position est dans la limite de la grille, praticable et non-occupée
            if 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE:
                if game_instance.tile_map.is_walkable(new_x, new_y, unit) and not self.is_occupied(new_x, new_y, game_instance):
                    unit.x = new_x
                    unit.y = new_y
                    break  

    def knockback_away_from_source(self, unit, game_instance):
        """
        Appliquer un effet de recul à l'unité, en s'éloignant de la source (Bomber).
        Cela garantit que le Bomber subit également un recul s'il est affecté.
        """
        # Calculer la direction loin de la source 
        dx = unit.x - self.x  # Différence en x
        dy = unit.y - self.y  # Différence en y

        # Normaliser la direction pour obtenir un vecteur unitaire.
        if dx != 0:
            dx = int(dx / abs(dx))  # Direction x
        if dy != 0:
            dy = int(dy / abs(dy))  # Direction y

        # Calculer la nouvelle position
        new_x = unit.x + dx
        new_y = unit.y + dy

        if 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and game_instance.tile_map.is_walkable(new_x, new_y, unit):
            unit.x = new_x
            unit.y = new_y

    def is_occupied(self, x, y, game_instance):
        """
        Vérifier si la case (x,y) est occupée par une unité.
        """
        for unit in game_instance.player_units_p1 + game_instance.player_units_p2:
            if unit.x == x and unit.y == y:
                return True  # La case est occupée
        return False 

    def explode(self, all_units):
        """ Le Bomber se sacrifie et explose, causant des dégâts pour toutes les unités dans la portée d'attaque 
        et meurt."""
        targets = []
        for unit in all_units:
            # Distance de Manhattan Bomber - Cible
            distance = abs(unit.x - self.x) + abs(unit.y - self.y)
            if distance <= self.explode_range:
                targets.append(unit)
                unit.health -= (self.attack_power*3 - unit.defense)  
                if unit.health <= 0:
                    unit.health = 0  

        # Tuer le Bomber
        self.health = 0
        return targets  # Retourne la liste des unités affectées
