import pygame
import random
from constante import GameConstantes as GC

class Unit:
    """
    Base class for all units.
    """

    def __init__(self, x, y, health, attack_power, defense, speed, vision, image_path, team):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed
        self.vision = vision
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(GC.CELL_SIZE), int(GC.CELL_SIZE)))
        self.team = team  # 'player' or 'enemy'
        self.is_selected = False

    def move(self, new_x, new_y):
        """
        Moves the unit to a new position if within movement range.
        """
        distance = abs(new_x - self.x) + abs(new_y - self.y)
        if distance <= self.speed and 0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE:
            self.x = new_x
            self.y = new_y
        else:
            print(f"Invalid Movement: Target Cell ({new_x}, {new_y}) out of limits.")

    def _in_range(self, target, attack_range):
        """
        Checks if the target is within the unit's attack range.
        """
        return abs(self.x - target.x) <= attack_range and abs(self.y - target.y) <= attack_range

    def draw(self, screen):
        """
        Draws the unit and its health bar on the screen.
        """
        if self.is_selected:
            pygame.draw.rect(screen, (255, 255, 255),
                             (self.x * GC.CELL_SIZE, self.y * GC.CELL_SIZE, GC.CELL_SIZE, GC.CELL_SIZE))

        self.draw_healthbar(screen)

        image_rect = self.image.get_rect()
        image_rect.center = (self.x * GC.CELL_SIZE + GC.CELL_SIZE // 2, self.y * GC.CELL_SIZE + GC.CELL_SIZE // 2)
        screen.blit(self.image, image_rect)

    def draw_healthbar(self, screen):
        """
        Draws the unit's health bar.
        """
        bar_width = 5
        bar_height = GC.CELL_SIZE
        bar_x = self.x * GC.CELL_SIZE + GC.CELL_SIZE - bar_width
        bar_y = self.y * GC.CELL_SIZE

        pygame.draw.rect(screen, GC.RED, (bar_x, bar_y, bar_width, bar_height))

        current_health_height = max(0, bar_height * (self.health / 100))
        green_bar_y = bar_y + (bar_height - current_health_height)
        pygame.draw.rect(screen, GC.GREEN, (bar_x, green_bar_y, bar_width, current_health_height))

    def is_occupied(self, x, y, game_instance):
        """
        Check if the tile at (x, y) is occupied by any unit.
        """
        for unit in game_instance.player_units_p1 + game_instance.player_units_p2:
            if unit.x == x and unit.y == y:
                return True
        return False


class Archer(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.dot_targets = {}
        self.normal_arrow_range = 3
        self.fire_arrow_range = 5
        self.ranges = [self.normal_arrow_range, self.fire_arrow_range]

    def normal_arrow(self, target):
        target.health -= self.attack_power

    def fire_arrow(self, target):
        initial_damage = self.attack_power - target.defense
        dot_damage = self.attack_power - target.defense
        target.health -= initial_damage
        self.dot_targets[target] = {'damage': dot_damage, 'turns': 3}

    def apply_dot(self):
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
        target.health -= self.attack_power * 2
        if target.health < 0:
            target.health = 0

    def stomp(self, target, all_units, tile_map, game_instance):
        primary_damage = self.attack_power * 3
        secondary_damage = primary_damage // 2

        target.health -= primary_damage
        if target.health < 0:
            target.health = 0
        self.apply_knockback(target, (self.x, self.y), tile_map, game_instance)

        secondary_tiles = [(target.x + dx, target.y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]

        for unit in all_units:
            if (unit.x, unit.y) in secondary_tiles:
                unit.health -= secondary_damage
                if unit.health < 0:
                    unit.health = 0
                self.apply_knockback(unit, (self.x, self.y), tile_map, game_instance)

    def apply_knockback(self, unit, stomp_origin, tile_map, game_instance):
        dx = unit.x - stomp_origin[0]
        dy = unit.y - stomp_origin[1]

        if dx != 0:
            dx = int(dx / abs(dx))
        if dy != 0:
            dy = int(dy / abs(dy))

        new_x = unit.x + dx
        new_y = unit.y + dy

        if (0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and 
                tile_map.is_walkable(new_x, new_y, unit) and not self.is_occupied(new_x, new_y, game_instance)):
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
        target.health -= self.attack_power

    def heal_allies(self, target):
        if target.team == self.team:
            target.health += self.attack_power
            target.health = min(target.health, 100)


class Bomber(Unit):
    def __init__(self, x, y, health, attack, defense, speed, vision, image_path, team):
        super().__init__(x, y, health, attack, defense, speed, vision, image_path, team)
        self.bomb_range = 2
        self.explode_range = 5
        self.ranges = [self.bomb_range, self.explode_range]

    def throw_bomb(self, target, all_units, tile_map, game_instance):
        affected_units = []
        aoe_cells = [(target.x, target.y)]

        for unit in all_units:
            distance = abs(unit.x - target.x) + abs(unit.y - target.y)
            if distance <= self.bomb_range:
                affected_units.append(unit)
                if (unit.x, unit.y) != (target.x, target.y):
                    aoe_cells.append((unit.x, unit.y))

        for unit in affected_units:
            unit.health -= self.attack_power
            if unit.health <= 0:
                game_instance.game_log.add_message(f"{unit.__class__.__name__} was defeated!", 'dead')
            self.apply_knockback(unit, target, game_instance)

        game_instance.draw_highlighted_cells(
            direct_cells=[(target.x, target.y)],
            secondary_cells=[cell for cell in aoe_cells if cell != (target.x, target.y)],
            is_attack_phase=True
        )

    def explode(self, all_units, game_instance):
        affected_units = [unit for unit in all_units if abs(unit.x - self.x) + abs(unit.y - self.y) <= self.explode_range]

        for unit in affected_units:
            unit.health -= self.attack_power * 3
            if unit.health <= 0:
                game_instance.game_log.add_message(f"{unit.__class__.__name__} was defeated!", 'dead')

        self.health = 0
        if self in game_instance.player_units_p1:
            game_instance.player_units_p1.remove(self)
        elif self in game_instance.player_units_p2:
            game_instance.player_units_p2.remove(self)

    def apply_knockback(self, unit, target, game_instance):
        if unit == target:
            self.knockback_random(unit, game_instance)
        else:
            self.knockback_away_from_source(unit, game_instance)

    def knockback_random(self, unit, game_instance):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = unit.x + dx
            new_y = unit.y + dy
            if (0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and 
                    game_instance.tile_map.is_walkable(new_x, new_y, unit) and not self.is_occupied(new_x, new_y, game_instance)):
                unit.x = new_x
                unit.y = new_y
                break

    def knockback_away_from_source(self, unit, game_instance):
        dx = unit.x - self.x
        dy = unit.y - self.y
        if dx != 0:
            dx = int(dx / abs(dx))
        if dy != 0:
            dy = int(dy / abs(dy))

        new_x = unit.x + dx
        new_y = unit.y + dy
        if (0 <= new_x < GC.GRID_SIZE and 0 <= new_y < GC.GRID_SIZE and 
                game_instance.tile_map.is_walkable(new_x, new_y, unit) and not self.is_occupied(new_x, new_y, game_instance)):
            unit.x = new_x
            unit.y = new_y
