import pygame
from pygame import mixer
from constante import GameConstantes as GC 
from unit import * 
from Tiles import *
from world import * 
import random
from GameLog import *
class Effect : 
    def __init__(self, effect_type, sound_path):
        self.effect_type = effect_type
        self.sound = mixer.Sound(sound_path)
        self.is_active = False
        self.value_changed = 0
        self.applied_turn = None  # Store when this effect was applied

    def apply(self, unit):
        if self.effect_type == "speed":
            speed_buff_amount = 3
            current_position = unit.get_position() 
            distance_to_the_left = current_position[0]
            distance_to_the_right = GC.WIDTH - current_position[0]
            distance_to_the_top = current_position[1]
            distance_to_the_bottom = GC.HEIGHT - current_position[1]
            min_distance = min(distance_to_the_left, distance_to_the_right, distance_to_the_top, distance_to_the_bottom)
            effective_speed_buff = min(min_distance, speed_buff_amount)
            unit.speed += effective_speed_buff
            self.value_changed = effective_speed_buff
            self.is_active = True
            self.sound.play()

        elif self.effect_type == "damage":
            increase_amount = 5
            unit.attack_power += increase_amount
            self.value_changed = increase_amount
            self.is_active = True
            self.sound.play()
        self.applied_turn = GC.turn_number
    def revert(self, unit):
        if not self.is_active:
            return

        if self.effect_type == "speed":
            unit.speed = max(unit.speed - self.value_changed, 0)

        elif self.effect_type == "damage":
            unit.attack_power = max(unit.attack_power - self.value_changed, 0)

        self.is_active = False
        self.value_changed = 0
        self.applied_turn = None


 
class CollectibleItem:
    def __init__(self, effect, image_path, sound_path, respawn_time, tile_map, game_log):
        self.effect = effect
        self.image_path = image_path
        Loaded_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(Loaded_image, (GC.CELL_SIZE, GC.CELL_SIZE))
        self.sound = mixer.Sound(sound_path)
        self.respawn_time = respawn_time
        self.is_active = True
        self.respawn_counter = 0
        self.tile_map = tile_map
        self.x = 0
        self.y = 0
        self.game_log = game_log

    def update(self, delta_time):
        if not self.is_active:
            self.respawn_counter += delta_time
            if self.respawn_counter >= self.respawn_time:
                self.is_active = True
                self.respawn_counter = 0
                self.sound.play()  # Play sound when item respawns
                

    def collect(self, unit):
        print("DEBUG: Collect called with unit at", unit.x, unit.y, "and item at", self.x, self.y)
        # Convert unit position from pixels to grid coordinates
        unit_cell_x = unit.x 
        unit_cell_y = unit.y 
        
        # Convert collectible position from pixels to grid coordinates
        item_cell_x = self.x 
        item_cell_y = self.y
        
        # Check if unit is on the same cell as the collectible
        if self.is_active and unit.x == self.x and unit.y == self.y:
            print("DEBUG: Item collected!")
            self.effect.apply(unit)
            self.game_log.add_message("Collectible collected", 'other')
            self.effect.applied_turn = GC.turn_number
            if not hasattr(unit, 'active_effects'):
                unit.active_effects = []
            
            if self.effect.is_active:
                unit.active_effects.append(self.effect)
                print(f"DEBUG: Effect '{self.effect.effect_type}' applied to unit {unit}. Current active effects: {[e.effect_type for e in unit.active_effects]}")
            self.sound.play()
            self.is_active = False
            self.respawn_counter = 0