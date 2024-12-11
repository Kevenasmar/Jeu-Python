from datetime import datetime
from posixpath import split
import pygame 
pygame.init()
from constante import GameConstantes as GC # type: ignore

# Ability descriptions for manual customization
ABILITY_DESCRIPTIONS = {
    "fire_arrow": "Applies damage over time to the target.",
    "normal_arrow": "Simple attack - 4% chance of Headshot!",
    "potion": "Throws a potion to harm the target.",
    "heal_allies": "Restores health to an ally.",
    "punch": "A powerful attack with high damage.",
    "stomp": "Damages and pushes the target away.",
    "throw_bomb": "Throws a bomb, causing area damage.",
    "explode": "Kills itself - massive area damage.",
}

#Multiples de la attack_power de l'unité correspondante
ABILITY_DAMAGE = {
    "fire_arrow": 1,  # Equal to the unit's attack power
    "normal_arrow": 1,  # 1x the unit's attack power
    "potion": 1,  # 0.5x the unit's attack power
    "heal_allies": -1,  # -1 to indicate healing (not damage)
    "punch": 2,  # 2x the unit's attack power
    "stomp": 3,  # 3x the unit's attack power
    "throw_bomb": 1,  # 1x the unit's attack power
    "explode": 3,  # 3x the unit's attack power
}


class GameLog:
    def __init__(self, width, height, pos_x, pos_y, screen):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.couleur_fond = (0, 0, 0)
        self.font = pygame.font.Font(None, 26)
        self.messages = []
        self.limite = 5
        self.surface = pygame.Surface((self.width, self.height))
        self.selected_unit = None  # To display selected unit details

    def add_message(self, message, type):
        """Adds a message to the GameLog."""
        if len(self.messages) >= self.limite:
            self.messages.pop(0)

        if type == "mouvement":
            couleur_text = (255, 255, 255)
        elif type == "attack":
            couleur_text = (192, 111, 90)
        elif type == "dead":
            couleur_text = (42, 13, 6)
        elif type == "win":
            couleur_text = (42, 13, 254)
        elif type == "lose":
            couleur_text = (255, 13, 0)
        elif type == "game_over":
            couleur_text = (248, 51, 84)
        elif type == "other":
            couleur_text = (255, 255, 255)
        elif type == "action":
            couleur_text = GC.RED
        elif type == "info":
            couleur_text = GC.BLUE

        timestamp = datetime.now().strftime("%H:%M:%S")
        formated_message = f"[{timestamp}] {message}"

        text_surface = self.font.render(formated_message, True, couleur_text)
        self.messages.append(text_surface)

    def set_selected_unit(self, unit):
        self.selected_unit = unit
        if unit:
            abilities = []

            # Explicit mapping for abilities with non-matching range attribute names
            ability_range_map = {
                "throw_bomb": "bomb_range",
                "heal_allies": "heal_range",
            }

            # Detect abilities dynamically
            for attr in dir(unit):
                if callable(getattr(unit, attr)) and not attr.startswith("_"):
                    # Check for matching range attribute
                    range_attr = ability_range_map.get(attr, f"{attr}_range")
                    if hasattr(unit, range_attr):
                        # Calculate actual damage based on attack_power and multiplier
                        damage_multiplier = ABILITY_DAMAGE.get(attr, 0)
                        if damage_multiplier > 0:
                            actual_damage = unit.attack_power * damage_multiplier
                            damage_text = f"{actual_damage}"
                        elif damage_multiplier < 0:
                            actual_damage = abs(unit.attack_power * damage_multiplier)
                            damage_text = f"Restores {actual_damage} life points"
                        else:
                            damage_text = "No damage information available."

                        abilities.append({
                            "name": attr,
                            "range": getattr(unit, range_attr),
                            "description": ABILITY_DESCRIPTIONS.get(attr, "No description available."),
                            "damage": damage_text,
                        })

            # Assign detected abilities to the unit
            setattr(unit, "abilities", abilities)




    def wrap_text(self, text, max_width, font):
        """Wraps text into multiple lines to fit within a specified width."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + " ", True, (0, 0, 0))  # Temporary render to measure width
            word_width = word_surface.get_width()
            if current_width + word_width > max_width:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width

        if current_line:
            lines.append(" ".join(current_line))

        return lines


    def draw_unit_info(self):
        """Displays the selected unit's details and abilities in a structured and visually appealing format."""
        if not self.selected_unit:
            return

        # Define the unit info area
        info_area_height = 350
        info_area_y = self.pos_y + self.height - info_area_height - 60
        padding = 15

        # Draw the background rectangle for unit info
        pygame.draw.rect(
            self.screen,
            (173, 216, 230),  # Dark gray background
            (self.pos_x, info_area_y, self.width, info_area_height + 60)
        )

        # Draw a border around the unit info section
        pygame.draw.rect(
            self.screen,
            GC.BLUE,  # White border
            (self.pos_x, info_area_y, self.width, info_area_height + 60 ),
            2
        )

        # Scale the portrait to fit nicely within the section
        portrait_width = 100
        portrait_height = 100
        portrait = pygame.transform.scale(self.selected_unit.image, (portrait_width, portrait_height))

        # Calculate the position to center the portrait vertically in the section
        portrait_x = self.pos_x + padding
        portrait_y = info_area_y + padding
        self.screen.blit(portrait, (portrait_x, portrait_y))

        # Draw the health bar next to the portrait
        bar_width = 15
        bar_height = portrait_height
        bar_x = portrait_x + portrait_width + 20
        bar_y = portrait_y

        # Health bar logic
        pygame.draw.rect(self.screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red background
        current_health_height = int(bar_height * (self.selected_unit.health / 100))
        green_bar_y = bar_y + (bar_height - current_health_height)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, green_bar_y, bar_width, current_health_height))  # Green foreground
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)  # White border

        # Stats section next to the health bar
        stats_x = bar_x + bar_width + 20
        stats_y = portrait_y

        # Draw the unit name directly above the stats
        unit_name = self.selected_unit.__class__.__name__
        unit_name_surface = self.font.render(unit_name, True, GC.BLACK)  # Gold color for name
        self.screen.blit(unit_name_surface, (stats_x, stats_y))

        # Draw stats below the name
        stats_y += 30
        stats = [
            f"Defense: {self.selected_unit.defense}",
            f"Speed: {self.selected_unit.speed}",
        ]
        for stat in stats:
            stat_surface = self.font.render(stat, True, GC.BLUE)  # Sky blue color
            self.screen.blit(stat_surface, (stats_x, stats_y))
            stats_y += 30
            
        # Add this conditional block for the Mage
        if unit_name == "Mage":
            water_ability_surface = self.font.render("Can walk on water!", True, GC.BLUE)
            self.screen.blit(water_ability_surface, (stats_x, stats_y))
            stats_y += 30

        # Add "Abilities" label below the stats
        abilities_x = self.pos_x + padding
        abilities_y = portrait_y + portrait_height + 20
        abilities_label_surface = self.font.render("Abilities:", True, GC.BLACK)  # White label
        self.screen.blit(abilities_label_surface, (abilities_x, abilities_y))
        abilities_y += 30

        # Display abilities with descriptions, damage, and ranges
        for ability in self.selected_unit.abilities:
            # Ability name
            ability_name_surface = self.font.render(
                f"{ability['name']}", True, (139, 69, 19)  # Brown for ability name
            )
            self.screen.blit(ability_name_surface, (abilities_x, abilities_y))
            abilities_y += 25

            # Ability description
            description_surface = self.font.render(
                f"Description: {ability['description']}", True, (50, 50, 50)  # Gray for description
            )
            self.screen.blit(description_surface, (abilities_x + 20, abilities_y))  # Indent
            abilities_y += 25

            # Ability damage
            damage_surface = self.font.render(
                f"Damage: {ability['damage']}", True, GC.RED  # Red for damage
            )
            self.screen.blit(damage_surface, (abilities_x + 20, abilities_y))  # Indent
            abilities_y += 25

            # Ability range
            range_surface = self.font.render(
                f"Range: {ability['range']}", True, (162, 91, 70)  # Cornflower blue for range
            )
            self.screen.blit(range_surface, (abilities_x + 20, abilities_y))  # Indent
            abilities_y += 30
            
                # Add a warning for the "explode" ability
            if ability['name'] == "explode":
                warning_surface = self.font.render(
                    "CAREFUL! This hurts allies too.", True, (255, 165, 0)  # Orange for warning
                )
                self.screen.blit(warning_surface, (abilities_x + 20, abilities_y))
                abilities_y += 30  # Add spacing after the warning






    def draw(self):
        """Draws the GameLog, including messages and unit info."""
        # Draw the background
        pygame.draw.rect(
            self.screen,
            self.couleur_fond,
            (self.pos_x, self.pos_y, self.width, self.height),
        )


        # Draw the GameLog messages
        y_offset = 10
        for message in self.messages:
            self.screen.blit(message, (self.pos_x + 10, self.pos_y + y_offset))
            y_offset += 25

        # Draw the selected unit's info
        if self.selected_unit:
            self.draw_unit_info()

