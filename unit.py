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

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
def move(self, game):
    '''
    Allows the unit to move within its speed range.
    Highlights possible moves and lets the player choose a target position.'''
    
    possible_moves = []

    # Calculate possible moves within the speed radius
    for dx in range(-self.speed, self.speed + 1):
        for dy in range(-self.speed, self.speed + 1):
            if abs(dx) + abs(dy) <= self.speed:  # Ensure Manhattan distance is within speed
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    possible_moves.append((new_x, new_y))

    # Allow the player to choose a target position
    selected_pos = (self.x, self.y)  # Start at the unit's current position
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Confirm movement
                    if selected_pos in possible_moves:
                        self.x, self.y = selected_pos
                        selecting = False

                # Update selection cursor based on arrow keys
                elif event.key == pygame.K_UP:
                    new_selected = (selected_pos[0], selected_pos[1] - 1)
                    if new_selected in possible_moves:
                        selected_pos = new_selected
                elif event.key == pygame.K_DOWN:
                    new_selected = (selected_pos[0], selected_pos[1] + 1)
                    if new_selected in possible_moves:
                        selected_pos = new_selected
                elif event.key == pygame.K_LEFT:
                    new_selected = (selected_pos[0] - 1, selected_pos[1])
                    if new_selected in possible_moves:
                        selected_pos = new_selected
                elif event.key == pygame.K_RIGHT:
                    new_selected = (selected_pos[0] + 1, selected_pos[1])
                    if new_selected in possible_moves:
                        selected_pos = new_selected

        # Redraw the grid and highlights
        game.flip_display()  # Redraw the grid and units

        # Highlight possible moves
        for pos in possible_moves:
            highlight_x, highlight_y = pos[0] * CELL_SIZE, pos[1] * CELL_SIZE
            pygame.draw.rect(game.screen, (0, 255, 0, 128), (highlight_x, highlight_y, CELL_SIZE, CELL_SIZE), 0)

        # Highlight the currently selected position
        sel_x, sel_y = selected_pos[0] * CELL_SIZE, selected_pos[1] * CELL_SIZE
        pygame.draw.rect(game.screen, (255, 255, 0, 128), (sel_x, sel_y, CELL_SIZE, CELL_SIZE), 0)

        pygame.display.flip()
       


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
        Inflige des dégâts très importants et repousse la cible de 2 cases.
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

            # Apply knockback by 2 cells
            new_x = target.x + dx * 2
            new_y = target.y + dy * 2

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
        
