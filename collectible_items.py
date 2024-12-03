import pygame
import os  
from pygame import mixer
from constante import GameConstantes as GC
from unit import *
pygame.init()

class Collectible_items:
    def __init__(self, x, y, image_path, soudeffect_path, respawn_timer, respawn_delay, is_active ):
        self.image_path = pygame.image.load(image_path)
        self.s = 'sound'
        self.x = x 
        self.y = y
        self.soudeffect_path = pygame.mixer.Sound(os.path.join(s, soudeffect_path))
        self.respawn_timer = respawn_timer
        self.is_active = True
        self.respawn_timer = 0  #compteur depuis la derniere collecte
        self.respawn_delay = respawn_delay # temps fixe pour la reaparition de l'item
        self.pos_item = (x,y)
    def update_state(self) : 
        if not self.is_active : # si l'item n'est pas afficher 
            self.respawn_timer += 1 # on incrémente le compteur de respawn
            if self.respawn_timer  >= self.respawn_delay : # si le compteur est supérieur ou égal au temps de respawn
                self.is_active = True # on active l'item
    unit_position = unit.get_position
    def collect(self) : 
        self.is_active = False # on désactive l'item
    
        
    

 
