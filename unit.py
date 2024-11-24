import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


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
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def _init_(self, x, y, health, attack, defense, speed, vision, image_path, team):
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
        self.image = pygame.image.load(image_path)  # chargement de l'image
        self.image = pygame.transform.scale(self.image, (0.75*CELL_SIZE, 0.75*CELL_SIZE))  # Echelle de l'image
        self.team = team  # 'joueur' ou 'ennemi'
        self.is_selected = False

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

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
    def __init__(self, x, y, health, attack_power, speed, defense, team):
        super().__init__(x, y, health, attack_power, speed, defense, team)
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
    def __init__(self, x, y, health, attack_power, speed, defense, team):
        super().__init__(x, y, health, attack_power, speed, defense, team)
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
    def __init__(self, x, y, health, attack_power, speed, defense, team):
        super().__init__(x, y, health, attack_power, speed, defense, team)
        self.range = 4  # Mage's attack range

    def _in_range(self, target):
        """Vérifier si la cible est dans la portée d'attaque"""
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y) <= self.range

    '''Compétences'''
    def heal_alies(self, target):
        """Soigne une unité alliée."""
        if self._in_range(target) and target.team == self.team:
            target.health += self.attack_power
        
