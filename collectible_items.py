import pygame
import os  
from pygame import mixer
from constante import GameConstantes as GC
pygame.init()

class Collectible_items:
    def __init__(self, image_path, soudeffect_path, respawn_timer, position , is_active ):
        self.image_path = pygame.image.load(image_path)
        self.s = 'sound'
        self.soudeffect_path = pygame.mixer.Sound(os.path.join(s, soudeffect_path))
        self.respawn_timer = respawn_timer
        self.is_active = True
        self.position = position 

    def update_state(self, player_pos) : 
        if self.is_active : 
            if player_pos == self.position :
                self.is_active = False
                return True 
            
        return False 
    
    
        
    

 
