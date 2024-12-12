from datetime import datetime
from posixpath import split
import pygame 
pygame.init()
from constante import GameConstantes as GC # type: ignore

# Description des compétences pour facilité
ABILITY_DESCRIPTIONS = {
    "fire_arrow": "Applies damage over time to the target.",
    "normal_arrow": "Simple attack - 10% chance of Headshot!",
    "potion": "Throws a potion to harm the target.",
    "heal_allies": "Restores health to an ally.",
    "punch": "A powerful attack with high damage.",
    "stomp": "Damages and pushes the target away.",
    "throw_bomb": "Throws a bomb, causing area damage.",
    "explode": "Kills itself - massive area damage.",
}

#Multiples de la attack_power de l'unité correspondante
ABILITY_DAMAGE = {
    "fire_arrow": 1,  
    "normal_arrow": 1,  
    "potion": 1,  
    "heal_allies": -2,  
    "punch": 1,  
    "stomp": 2,  
    "throw_bomb": 1,  
    "explode": 3,  
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
        self.selected_unit = None  

    def add_message(self, message, type):
        """Ajouter un message au Game Log"""
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

        formated_message = f"{message}"

        text_surface = self.font.render(formated_message, True, couleur_text)
        self.messages.append(text_surface)

    def set_selected_unit(self, unit):
        self.selected_unit = unit
        if unit:
            abilities = []
            ability_range_map = {
                "throw_bomb": "bomb_range",
                "heal_allies": "heal_range",
            }

            for attr in dir(unit):
                if callable(getattr(unit, attr)) and not attr.startswith("_"):
                    range_attr = ability_range_map.get(attr, f"{attr}_range")
                    if hasattr(unit, range_attr):
                        damage_multiplier = ABILITY_DAMAGE.get(attr, 0)
                        if damage_multiplier > 0:
                            actual_damage = unit.attack_power * damage_multiplier
                            damage_text = f"{actual_damage}"
                        elif damage_multiplier < 0:
                            actual_damage = abs(unit.attack_power * damage_multiplier)
                            damage_text = f"+{actual_damage} LPs"
                        else:
                            damage_text = "No damage information available."

                        abilities.append({
                            "name": attr,
                            "range": getattr(unit, range_attr),
                            "description": ABILITY_DESCRIPTIONS.get(attr, "No description available."),
                            "damage": damage_text,
                        })
            setattr(unit, "abilities", abilities)

    def wrap_text(self, text, max_width, font):
        '''Enroule les textes sur plusieurs lignes pour les faire tenir dans une largeur spécifique.'''
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word + " ", True, (0, 0, 0))  
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
        """Affiche les détails et compétences de l'unité sélectionnée"""
        if not self.selected_unit:
            return

        # Définir la position de la section
        info_area_height = 350
        info_area_y = self.pos_y + self.height - info_area_height - 60
        padding = 15

        # Dessiner le rectangle de fond 
        pygame.draw.rect(
            self.screen,
            (173, 216, 230),  # Fond bleu ciel
            (self.pos_x, info_area_y, self.width, info_area_height + 60)
        )

        # Dessiner une bordure autour de la section 
        pygame.draw.rect(
            self.screen,
            GC.BLUE,  # Blue border
            (self.pos_x, info_area_y, self.width, info_area_height + 60),
            2
        )

        portrait_width = 100
        portrait_height = 100
        portrait = pygame.transform.scale(self.selected_unit.image, (portrait_width, portrait_height))

        # Centrer le portrait verticalement dans la section 
        portrait_x = self.pos_x + padding
        portrait_y = info_area_y + padding
        self.screen.blit(portrait, (portrait_x, portrait_y))

        # Dessine la bar de vie prés du portrait
        bar_width = 15
        bar_height = portrait_height
        bar_x = portrait_x + portrait_width + 20
        bar_y = portrait_y

        max_health = getattr(self.selected_unit, 'max_health', 100)  # 100 par défaut

        pygame.draw.rect(self.screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Fond rouge
        current_health_height = int(bar_height * (self.selected_unit.health / max_health))
        green_bar_y = bar_y + (bar_height - current_health_height)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, green_bar_y, bar_width, current_health_height))  # Vert
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)  # Bordure blanche

        # Section statistiques a coté de la bar de vie 
        stats_x = bar_x + bar_width + 20
        stats_y = portrait_y

        # Afficher le nom de l'unité directement au dessus des statistiques 
        unit_name = self.selected_unit.__class__.__name__
        unit_name_surface = self.font.render(unit_name, True, GC.BLACK)  # Nom en noir
        self.screen.blit(unit_name_surface, (stats_x, stats_y))

        # Statistiques en dessous du nom 
        stats_y += 30
        stats = [
            f"Defense: {self.selected_unit.defense}",
            f"Speed: {self.selected_unit.speed}",
        ]
        for stat in stats:
            stat_surface = self.font.render(stat, True, GC.BLUE) 
            self.screen.blit(stat_surface, (stats_x, stats_y))
            stats_y += 30

        # Ajouter une info supplémentaire pour le Mage 
        if unit_name == "Mage":
            water_ability_surface = self.font.render("Can walk on water!", True, GC.BLUE)
            self.screen.blit(water_ability_surface, (stats_x, stats_y))
            stats_y += 30

        abilities_x = self.pos_x + padding
        abilities_y = portrait_y + portrait_height + 20
        abilities_label_surface = self.font.render("Abilities:", True, GC.BLACK)
        self.screen.blit(abilities_label_surface, (abilities_x, abilities_y))
        abilities_y += 30

        # Afficher les compétences avec description, pouvoir d'attaque et portée
        for ability in self.selected_unit.abilities:
            # Nom de la compétence
            ability_name_surface = self.font.render(
                f"{ability['name']}", True, (139, 69, 19)  # Marron
            )
            self.screen.blit(ability_name_surface, (abilities_x, abilities_y))
            abilities_y += 25

            # Description 
            description_surface = self.font.render(
                f"Description: {ability['description']}", True, (50, 50, 50)  # Gris foncé
            )
            self.screen.blit(description_surface, (abilities_x + 20, abilities_y))  
            abilities_y += 25

            # Dégats
            damage_surface = self.font.render(
                f"Damage: {ability['damage']}", True, GC.RED 
            )
            self.screen.blit(damage_surface, (abilities_x + 20, abilities_y)) 
            abilities_y += 25

            # Portée 
            range_surface = self.font.render(
                f"Range: {ability['range']}", True, (162, 91, 70)  
            )
            self.screen.blit(range_surface, (abilities_x + 20, abilities_y))  
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

