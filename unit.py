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
        self.image = pygame.transform.scale(self.image, (int(0.75 * GC.CELL_SIZE), int(0.75 * GC.CELL_SIZE)))  # Échelle de l'image
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

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran avec son image et un rectangle de sélection si sélectionnée."""
        if self.is_selected:
            pygame.draw.rect(screen, (75, 118, 204), (self.x * GC.CELL_SIZE, self.y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE))

        image_rect = self.image.get_rect()
        image_rect.center = (self.x * GC.CELL_SIZE + GC.CELL_SIZE // 2, self.y * GC.CELL_SIZE + GC.CELL_SIZE // 2)
        screen.blit(self.image, image_rect)

    def draw_healthbar(self, screen):
        """Dessine une barre de santé au-dessus de la cellule de l'unité."""
        bar_width = GC.CELL_SIZE  # Largeur de la cellule
        bar_height = 5  # Hauteur de la barre de santé
        bar_x = self.x * GC.CELL_SIZE  # Position X (alignée avec la cellule)
        bar_y = self.y * GC.CELL_SIZE - bar_height - 2  # Position Y (au-dessus de la cellule)

        # Barre rouge (fond - santé maximale)
        pygame.draw.rect(screen, GC.RED, (bar_x, bar_y, bar_width, bar_height))

        # Barre verte (santé actuelle)
        pygame.draw.rect(screen, GC.GREEN, (bar_x, bar_y, bar_width * (self.health / 100), bar_height))


class Archer(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.range = 3  # Portée d'attaque de l'archer
        self.dot_targets = {}  # Suivre les unités affectées par la flèche en feu

    def _in_range(self, target):
        """Vérifier si la cible est dans la portée d'attaque."""
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y) <= self.range

    def normal_arrow(self, target):
        """Flèche normale."""
        if self._in_range(target):
            target.health -= self.attack_power

    def fire_arrow(self, target):
        """Flèche en feu, applique des effets de dégâts sur la durée (Damage Over Time DoT)."""
        if self._in_range(target):
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
        self.range = 1  # Portée d'attaque du géant (très faible)

    def _in_range(self, target):
        """Vérifier si la cible est dans la portée d'attaque."""
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y) <= self.range

    def punch(self, target):
        """Inflige des dégâts importants à la cible."""
        if self._in_range(target):
            target.health -= self.attack_power * 2  # Dégâts élevés

    def stomp(self, target):
        """Inflige des dégâts très importants et repousse la cible d'une case."""
        if self._in_range(target):
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
        self.range = 4  # Portée d'attaque du mage
        self.can_walk_on_water = True
    def _in_range(self, target):
        """Vérifier si la cible est dans la portée d'attaque."""
        return abs(self.x - target.x) <= self.range and abs(self.y - target.y) <= self.range

    def heal_allies(self, target):
        """Soigne une unité alliée."""
        if self._in_range(target) and target.team == self.team:
            target.health += self.attack_power  # Soigne selon la puissance d'attaque du mage