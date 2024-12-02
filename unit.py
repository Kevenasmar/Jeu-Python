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
        """Inflige des dégâts importants à la cible."""
        target.health -= self.attack_power * 2  # Dégâts élevés

    def stomp(self, target):
        """Inflige des dégâts très importants et repousse la cible d'une case."""
        target.health -= self.attack_power * 3  # Dégâts très élevés

        # Déterminer la direction du recul
        dx = target.x - self.x
        dy = target.y - self.y

        # Normaliser la direction du recul
        if dx != 0:
            dx = int(dx / abs(dx))
        if dy != 0:
            dy = int(dy / abs(dy))

        # Appliquer le recul d'une case
        new_x = target.x + dx
        new_y = target.y + dy

        # S'assurer que la cible ne sort pas de la grille
        if 0 <= new_x < GC.GRID_SIZE:
            target.x = new_x
        if 0 <= new_y < GC.GRID_SIZE:
            target.y = new_y


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
        """Soigne une unité alliée."""
        target.health += self.attack_power  # Soigne selon la puissance d'attaque du mage