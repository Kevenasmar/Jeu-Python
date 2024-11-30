import datetime
from posixpath import split
import pygame 
pygame.init()
from constante import GameConstantes as GC # type: ignore
class GameLog : 
    def __init__ (self, width, height) : 
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((GC.WIDTH, GC.HEIGHT))
        self.couleur_fond = (245, 222, 179)
        self.font = pygame.font.Font("font/Modern.ttf", 16)
        pygame.draw.rect(self.surface, self.couleur_fond, pygame.Rect(GC.WIDTH - width, 0, width, GC.HEIGHT))
        pygame.display.flip()
        add_log = []
        self.messages = []
        self.limite = 5
    
    def add_message(self,message,type) :
        if len(self.messages) >= self.limite : 
            self.messages.pop(0)
        if type == "mouvement" : 
            couleur_text = (138,0,0)
        elif type == "attack" : 
            couleur_text = (192, 111, 90)
        else : 
            couleur_text = (225, 153, 116)
        

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
        # Fill the background
        self.surface.fill(self.couleur_fond)
        
        # Draw the messages
        for i, message in enumerate(self.messages):
            self.surface.blit(message, (10, 10 + i * 20))  # Adjust the position as needed
        
        pygame.display.flip()
