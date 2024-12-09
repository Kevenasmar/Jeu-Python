import pygame
from pygame import mixer
from constante import GameConstantes as GC 
from unit import * 
from Tiles import *
from world import * 
import random
from GameLog import *
class Effect : 
    def __init__(self, effect_type, sound_path) : 
        self.effect_type = effect_type
        self.sound = mixer.Sound(sound_path)

    def apply(self, unit) : 
        if self.effect_type == "health" :
            unit.max_health = max(unit.health)
            if unit.health < unit.max_health :
                unit.health += 10
                self.sound.play()
    
        elif self.effect_type == "speed":
            speed_buff_amount = 3
            current_position = unit.get_position() 
            distance_to_the_left = current_position[0]
            distance_to_the_right = GC.WIDTH - current_position[0]
            distance_to_the_top = current_position[1]
            distance_to_the_bottom = GC.HEIGHT - current_position[1]
            min_distance = min(distance_to_the_left, distance_to_the_right, distance_to_the_top, distance_to_the_bottom)
            effective_speed_buff = min(min_distance, speed_buff_amount)
            unit.speed += effective_speed_buff
            self.sound.play()
    
        elif self.effect_type == "damage":
            unit.damage += 5
            self.sound.play()

 
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
            # They are on the same tile
            self.effect.apply(unit)
            self.sound.play()
            self.is_active = False
            self.respawn_counter = 0