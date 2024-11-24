import pygame
import random
from constante import GameConstantes as GC 

class Unit:

    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack
        self.defense = defense
        self.speed = speed
        self.vision = vision
        self.image = pygame.image.load(image_path)  # Load character's image
        self.image = pygame.transform.scale(self.image, (GC.CELL_SIZE, GC.CELL_SIZE))  # Scale to fit a tile
        self.team = team  # 'player' or 'enemy'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GC.GRID_SIZE and 0 <= self.y + dy < GC.GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        # If an image is loaded, blit it onto the screen at the unit's grid position
        if self.image:
            screen.blit(self.image, (self.x * GC.CELL_SIZE, self.y * GC.CELL_SIZE))
        else:
            # Fallback: If no image is loaded, draw a colored rectangle as a placeholder
            color = GC.BLUE if self.team == 'player' else GC.RED
            pygame.draw.rect(screen, color, (self.x * GC.CELL_SIZE, self.y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE))
        
    def draw_healthbar(self, screen, health):
        """Dessine une barre de santé au-dessus de la cellule de l'unité."""
        # Dimensions et position de la barre de santé
        bar_width = GC.CELL_SIZE  # Largeur de la cellule
        bar_height = 5         # Hauteur de la barre de santé
        bar_x = self.x * GC.CELL_SIZE  # Position X (alignée avec la cellule)
        bar_y = self.y * GC.CELL_SIZE - bar_height - 2  # Position Y (au-dessus de la cellule)

        # Barre rouge (fond - santé maximale)
        pygame.draw.rect(screen, GC.RED, (bar_x, bar_y, bar_width, bar_height))

        # Barre verte (santé actuelle)
        pygame.draw.rect(screen, GC.GREEN, (bar_x, bar_y, bar_width * (health / 100), bar_height))
        
  
        
'''UNIT TYPE: The Archer.'''
class Archer(Unit):
    def __init__(self, x, y, health, attack_power, speed, defense,image_path, team):
        super().__init__(x, y, health, attack_power, speed, defense, team)
        self.range = 3 #Archer's attack range
        self.dot_targets = {}  #Track units affected by fire arrow
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y)
    
    '''Abilities'''    
    def normal_arrow(self,target):
        '''Deals direct damage to the target'''
        if self._in_range(target):
            target.health -= self.attack_power
            
    def fire_arrow(self, target):
        '''Applies damage and sets up damage-over time effects'''
        if self._in_range(target):
            initial_damage = self.attack_power // 2
            dot_damage = self.attack_power // 4
            target.health -= initial_damage
            self.dot_targets[target] = {'damage': dot_damage, 'turns':3}
            
    def apply_dot(self):
        '''Apply DoT to affected targets'''
        for target, effect in list(self.dot_targets.items()):
            if effect['turns'] > 0:
                target.health -= effect['damage']
                effect['turns'] -= 1
            else:
                del self.dot_targets[target]