import pygame
import random

GRID_SIZE = 16  # 16x16 map
LOG_WIDTH_CELLS = 8  # Log area width in cells
CELL_SIZE = 45  # Size of each cell

# Dimensions
MAP_WIDTH = GRID_SIZE * CELL_SIZE  # Width of the map in pixels
LOG_WIDTH = LOG_WIDTH_CELLS * CELL_SIZE  # Width of the log area in pixels
TOTAL_WIDTH = MAP_WIDTH + LOG_WIDTH  # Total width of the screen
TOTAL_HEIGHT = GRID_SIZE * CELL_SIZE  # Height of the screen
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:

    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack
        self.defense = defense
        self.speed = speed
        self.vision = vision
        self.image = pygame.image.load(image_path)  # chargement de l'image
        self.image = pygame.transform.scale(self.image, (0.75*CELL_SIZE, 0.75*CELL_SIZE))  # Echelle de l'image
        self.team = team  # 'joueur' ou 'ennemi'
        self.is_selected = False

    def attack(self, attacker, target):
        """Gère l'attaque d'une unité sur une cible."""
        target.health -= attacker.attack_power  # Applique les dégâts

        if target.health <= 0:
            target.health = 0
            if target in self.player_units:
                self.player_units.remove(target)
            elif target in self.enemy_units:
                self.enemy_units.remove(target)
            self.add_log(f"{attacker.__class__.__name__} a tué {target.__class__.__name__}!")
        else:
            self.add_log(f"{attacker.__class__.__name__} a attaqué {target.__class__.__name__} pour {attacker.attack_power} dégâts!")



    def draw(self, screen):
        """
        Affiche l'unité sur l'écran avec son image et un rectangle de sélection si sélectionnée.
        """
        # Dessiner le rectangle de sélection si l'unité est sélectionnée
        if self.is_selected:
            pygame.draw.rect(
                screen,
                GREEN,  # Couleur du rectangle de sélection
                (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        # Dessiner l'image de l'unité
        image_rect = self.image.get_rect()
        image_rect.center = (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2)
        screen.blit(self.image, image_rect)

        # Dessiner la barre de santé
        self.draw_healthbar(screen, self.health)

        
    def draw_healthbar(self, screen, health):
        """Dessine une barre de santé au-dessus de la cellule de l'unité."""
        # Dimensions et position de la barre de santé
        bar_width = CELL_SIZE  # Largeur de la cellule
        bar_height = 5         # Hauteur de la barre de santé
        bar_x = self.x * CELL_SIZE  # Position X (alignée avec la cellule)
        bar_y = self.y * CELL_SIZE - bar_height - 2  # Position Y (au-dessus de la cellule)

        # Barre rouge (fond - santé maximale)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))

        # Barre verte (santé actuelle)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * (health / 100), bar_height))

        # pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
        #                      self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
        #                    2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
    def move(self, new_x, new_y):
        """
        Moves the unit to a new position within its speed radius.
        
        Parameters:
        new_x (int): The target x-coordinate.
        new_y (int): The target y-coordinate.
        """
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.speed and 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y
        else:
            print(f"Invalid move: Target position ({new_x}, {new_y}) is out of range or out of bounds.")

    
'''
------------------------------------------------
LES DIFFÉRENTS TYPES D'UNITÉS
------------------------------------------------
'''

'''
----------
L'Archer
----------
'''

class Archer(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.range = 3 #Archer's attack range
        self.dot_targets = {}  #Track units affected by fire arrow 
         
    def _in_range(self,target):
        '''Vérifier si la cible est dans la portée d'attaque'''
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y)
    
    '''Compétences'''    
    def normal_arrow(self,target):
        '''Flèche normale'''
        if self._in_range(target):
            target.health -= self.attack_power
            
    def fire_arrow(self, target):
        '''Flèche en feu, applique des effets de dégâts sur la durée (Damage Over Time DoT)'''
        if self._in_range(target):
            initial_damage = self.attack_power // 2
            dot_damage = self.attack_power // 4
            target.health -= initial_damage
            self.dot_targets[target] = {'damage': dot_damage, 'turns':3}
            
    def apply_dot(self):
        '''Applique le DoT sur les ennemis affectés'''
        for target, effect in list(self.dot_targets.items()):
            if effect['turns'] > 0:
                target.health -= effect['damage']
                effect['turns'] -= 1
            else:
                del self.dot_targets[target]      

'''
-------------
Le Géant
-------------
'''

class Giant(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.range = 1  # Giant's attack range (very low)

    def _in_range(self, target):
        """Vérifier si la cible est dans la portée d'attaque"""
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y) <= self.range

    '''Compétences'''
    def punch(self, target):
        """Inflige des dégâts importants à la cible."""
        if self._in_range(target):
            target.health -= self.attack_power * 2  # High damage

    def stomp(self, target):
        """
        Inflige des dégâts très importants et repousse la cible d'une case.
        La direction du recul est déterminée en fonction de la position relative de la cible.
        """
        if self._in_range(target):
            # High damage
            target.health -= self.attack_power * 3

            # Determine knockback direction
            dx = target.x - self.x
            dy = target.y - self.y

            # Normalize knockback direction to one step (to avoid moving diagonally too far)
            if dx != 0:
                dx = int(dx / abs(dx))
            if dy != 0:
                dy = int(dy / abs(dy))

            # Apply knockback by 1 cell
            new_x = target.x + dx 
            new_y = target.y + dy

            # Ensure the target doesn't get knocked out of the grid
            if 0 <= new_x < GRID_SIZE:
                target.x = new_x
            if 0 <= new_y < GRID_SIZE:
                target.y = new_y


'''
-------------
Le Mage 
-------------
'''

class Mage(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.range = 4  # Mage's attack range

    def _in_range(self, target):
        """Vérifier si la cible est dans la portée d'attaque"""
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y) <= self.range

    '''Compétences'''
    def heal_alies(self, target):
        """Soigne une unité alliée."""
        if self._in_range(target) and target.team == self.team:
            target.health += self.attack_power
        
