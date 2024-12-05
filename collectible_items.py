import pygame
import os  
from pygame import time
from pygame import mixer
from constante import GameConstantes as GC
from unit import *
pygame.init()

class Effect : 
    def __init__(self, duration, strength, speed, effect_type) : 
        self.duration = duration
        self.strength = strength
        self.effect_type = effect_type
        self.active = False 
    
    def apply_item(self, unit) :
        if self.effect_type == "heal" :
            unit.health += self.strength
        elif self.effect_type == "Speed_Buff" :
            unit.speed += self.strength
        elif self.effect_type == "Power_Buff" :
            unit.power += self.strength
    

class Collectible_items:
    def __init__(self, x, y, item_type, image_path, soudeffect_path, respawn_timer, respawn_delay, is_active, effect ):
        self.s = 'sound'
        self.x = x 
        self.y = y
        self.soudeffect_path = pygame.mixer.Sound(os.path.join(s, soudeffect_path))
        self.respawn_timer = respawn_timer
        self.is_active = True
        self.respawn_timer = 0  #compteur depuis la derniere collecte
        self.respawn_delay = respawn_delay # temps fixe pour la reaparition de l'item
        self.pos_item = (x,y)
        self.effect = effect
        if self.is_active : 
            self.image_path = pygame.image.load(image_path)
    def update_state(self) : 
        if not self.is_active : # si l'item n'est pas afficher 
            self.respawn_timer += 1 # on incrémente le compteur de respawn
            if self.respawn_timer  >= self.respawn_delay : # si le compteur est supérieur ou égal au temps de respawn
                self.is_active = True # on active l'item
    def collect(self, unit):
        dx = abs(unit.x - self.x)
        dy = abs(unit.y - self.y)
        collection_radius = 30
        
        if dx <= collection_radius and dy <= collection_radius:
            self.is_active = False
            self.effect.apply_item(unit)
            self.soudeffect_path.play()  # Play sound effect
            self.respawn_timer = 0  # Reset respawn timer
            return True
        return False


class ItemSpawnManager:
    def __init__(self, world_width, world_height, tile_map, game_log):
        self.world_width = world_width
        self.world_height = world_height
        self.tile_map = tile_map
        self.game_log = game_log
        
    def get_spawn_sector(self):
        """Calculate a random sector for item spawning"""
        sector_width = self.world_width // 3
        sector_height = self.world_height // 3
        sector_x = random.randint(0, 2) * sector_width
        sector_y = random.randint(0, 2) * sector_height
        return (sector_x, sector_y, sector_width, sector_height)
    
    def find_spawn_location(self):
        """Find valid spawn locations within a sector"""
        sector_x, sector_y, width, height = self.get_spawn_sector()
        spawn_locations = []
        
        for x in range(sector_x, sector_x + width):
            for y in range(sector_y, sector_y + height):
                if self.tile_map.is_walkable(x, y):
                    spawn_locations.append((x, y))
                    
        return spawn_locations if spawn_locations else None
    
    def spawn_item(self, item_type):
        """Spawn a single item at a valid location"""
        spawn_location = self.find_spawn_location()
        if spawn_location:
            location = random.choice(spawn_location)
            item = item_type(*location)
            self.game_log.add_message(
                f'{item.__class__.__name__} spawned at {location}',
                'item_spawn'
            )
            return item
        return None
            

    
        
    

 
