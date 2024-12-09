from datetime import datetime
from posixpath import split
import pygame 
pygame.init()
from constante import GameConstantes as GC # type: ignore
class GameLog : 
    def __init__ (self, width, height, pos_x, pos_y, screen) : 
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.screen = screen
        self.pos_y = pos_y
        self.couleur_fond = (0, 0, 0)
        #self.font = pygame.font.Font("font/Modern.ttf", 26)
        self.font = pygame.font.Font(None, 26)
        self.messages = []
        self.limite = 5
        self.surface = pygame.Surface((self.width, self.height))
    
    def add_message(self,message,type) :
        if len(self.messages) >= self.limite : 
            self.messages.pop(0)
        if type == "mouvement" : 
            couleur_text = (255,255,255)
        elif type == "attack" : 
            couleur_text = (192, 111, 90)
        elif type == "dead" : 
            couleur_text = (42, 13, 6)
        elif type == "win" :
            couleur_text = (42, 13, 254)
        elif type == "lose" :
            couleur_text = (255, 13, 0)
        elif type == "game_over" :
            couleur_text = (248, 51, 84)
        elif type == "other": 
            couleur_text = (255, 255, 255)
        elif type == 'action':
            couleur_text = GC.RED
        elif type == 'info':
            couleur_text = GC.BLUE
        

        timestamp = datetime.now().strftime("%H:%M:%S")
        formated_message = f"[{timestamp}] {message}"

        text_surface =self.font.render(formated_message, True, couleur_text)
        self.messages.append(text_surface)
    
    #------------Calcule la taille du message en pixel et creer une nouvelle ligne si necessaire------------#
    def format_message(self, message, size, color, max_width) :
        words = message.split()
        lines = []
        current_line = []
        current_width = 0
        for word in words : 
            word_surface = self.font.render(word + " ", True, color) 
            word_width = word_surface.get_width()
            if current_width + word_width >= max_width : 
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
            else : 
                current_line.append(word)
                current_width += word_width
            if current_line : 
                lines.append(" ".join(current_line))
        return "\n".join(lines)
    
    def draw(self):
        # Dessiner le fond
        pygame.draw.rect(self.screen, self.couleur_fond, (self.pos_x, self.pos_y, self.width, self.height))
        
        # Dessiner les messages
        y_offset = 10
        for message in self.messages:
            self.screen.blit(message, (self.pos_x + 10, self.pos_y + y_offset))
            y_offset += 25
