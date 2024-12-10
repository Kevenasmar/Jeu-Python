import pygame
import sys
from game import Game
from constante import GameConstantes as GC


def lighten_surface(surface, amount):
    """Applique une couche blanche transparente sur une surface"""
    light_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    light_layer.fill((255, 255, 255, amount))
    surface.blit(light_layer, (0, 0))
    
def draw_text(screen, text, font, color, pos):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)

def main_menu(screen):
    pygame.init()
    clock = pygame.time.Clock()

    # Dimensions de l'écran
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    #Assets
    battlefield_bg = pygame.image.load("Photos/menu_background.png").convert_alpha()
    battlefield_bg = pygame.transform.scale(battlefield_bg, (screen_width, screen_height))

    hero1 = pygame.image.load("Photos/archer.png").convert_alpha()
    hero1 = pygame.transform.scale(hero1, (150, 150))
    hero2 = pygame.image.load("Photos/enemy_archer.png").convert_alpha()
    hero2 = pygame.transform.scale(hero2, (150, 150))

    button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
    button_base = pygame.transform.scale(button_image, (150, 60))

    # Charger les fonts
    font_path = "font/Cinzel-Regular.otf"
    font_size = 30
    font = pygame.font.Font(font_path, font_size)

    # Positions des bouttons
    play_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 50, 150, 60)
    how_to_play_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 120, 150, 60)
    exit_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 190, 150, 60)

    # Variables d'Animation
    hero1_y = screen_height // 2 - 100
    hero2_y = screen_height // 2 - 100
    bobbing_speed = 2
    direction = 1

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return "play"
                if how_to_play_button_rect.collidepoint(event.pos):
                    return "how_to_play"
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Animation Héros
        hero1_y += direction * bobbing_speed * 0.1
        hero2_y += direction * bobbing_speed * 0.1
        if hero1_y <= screen_height // 2 - 110 or hero1_y >= screen_height // 2 - 90:
            direction *= -1

        # Dessine le fond
        screen.blit(battlefield_bg, (0, 0))

        # Titre
        draw_text(screen, "Rise of Heroes", font, (255, 255, 255), (screen_width // 2, 50))

        # Animation
        screen.blit(hero1, (screen_width // 4 - 75, hero1_y))
        screen.blit(hero2, (3 * screen_width // 4 - 75, hero2_y))

        # Bouttons
        play_button = button_base.copy()
        if play_button_rect.collidepoint(mouse_pos):
            lighten_surface(play_button, 100)
        screen.blit(play_button, play_button_rect.topleft)
        draw_text(screen, "  Play", font, (255, 255, 255), play_button_rect.center)

        how_to_play_button = button_base.copy()
        if how_to_play_button_rect.collidepoint(mouse_pos):
            lighten_surface(how_to_play_button, 100)
        screen.blit(how_to_play_button, how_to_play_button_rect.topleft)
        draw_text(screen, "Rules", font, (255, 255, 255), how_to_play_button_rect.center)

        exit_button = button_base.copy()
        if exit_button_rect.collidepoint(mouse_pos):
            lighten_surface(exit_button, 100)
        screen.blit(exit_button, exit_button_rect.topleft)
        draw_text(screen, "   Quit", font, (255, 255, 255), exit_button_rect.center)

        # Mise a jour de l'affichage
        pygame.display.flip()
        clock.tick(60)

def rules_screen(screen, p1_images, p2_images):
    '''Affiche les règles du jeu'''
    #Font
    font_path = "font/Junicode.ttf"  
    font_size = 25
    try:
        font = pygame.font.Font(font_path, font_size)  
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        sys.exit()

    # Dimensions de l'écran
    background = pygame.image.load("Photos/background2.png").convert()  
    background = pygame.transform.scale(background, screen.get_size()) 
    screen.blit(background, (0, 0))  

    # Titre
    center_x = screen.get_width() // 2
    y = 20
    draw_text(screen, "HOW TO PLAY", font, GC.RED, (center_x, y))
    y += 50  

    # Règles Générales
    general_rules = [
        "Objective: Defeat all enemy units.",
        "Each turn, you can move and/or attack with your units.",
        "Each unit can move within a specific speed radius.",
        "When a unit is selected, the game log will display its different abilities.",
        "You can only attack if enemies are within an attack's range or in your line of sight.",
        "Each attack has a unique range and damage intensity,"
        "so plan your strategy carefully!",
        "May the best player win in glory & honor!"
    ]
    
    for index, rule in enumerate(general_rules):
        if index == 0:  # First sentence
            # Render the first rule in bold or a different color
            bold_font = pygame.font.Font(None, 34)  # Larger font to simulate bold
            draw_text(screen, rule, bold_font, (0, 0, 0), (center_x, y))  # Black for emphasis
        elif index == len(general_rules) - 1:  # Last sentence
            # Render the last rule in red
            draw_text(screen, rule, font, (255, 0, 0), (center_x, y))
        else:
            # Render the rest normally
            draw_text(screen, rule, font, (15, 13, 74), (center_x, y))
        y += 30 

    # Section Description des Unités
    # Définir 4 colonnes pour chaque unitÑ
    column_width = screen.get_width() // 4
    unit_y_start = y + 50 

    # Informations sur chaque unité
    units_info = [
        {
            "name": "Archer",
            "abilities": [
                "Ranged attacker with",
                "excellent precision."
            ],
            "images": (p1_images[0], p2_images[0])
        },
        {
            "name": "Mage",
            "abilities": [
                "Master of elemental",
                "magic and healer."
            ],
            "images": (p1_images[1], p2_images[1])
        },
        {
            "name": "Giant",
            "abilities": [
                "Powerhouse with incredible",
                "strength and durability."
            ],
            "images": (p1_images[2], p2_images[2])
        },
        
        {
            "name": "Bomber",
            "abilities": [
                "Explosive fighter",
                "requiring careful",
                "planning to avoid",
                "self-damage.",
                "CAREFUL...",
                "The Bomber can",
                "hurt allies too."
            ],
            "images": (p1_images[3], p2_images[3])  # Placeholder for Bomber images
        }
    ]

    for i, unit in enumerate(units_info):
        # Calcule la position de la colonne
        column_x = i * column_width + column_width // 2

        # Nom de l'unité
        unit_y = unit_y_start
        draw_text(screen, unit["name"], font, GC.RED, (column_x, unit_y))

        # Images
        unit_y += 40
        player_image, enemy_image = unit["images"]
        screen.blit(player_image, (column_x - 50, unit_y))  
        screen.blit(enemy_image, (column_x + 10, unit_y))  

        # Compétences des unités
        unit_y += 60
        for ability in unit["abilities"]:
            draw_text(screen, ability, font, (15, 13, 74), (column_x, unit_y))
            unit_y += 25  

    # Retour au Menu Principale (Boutton)
    button_y = GC.HEIGHT - 80  
    button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
    button_image = pygame.transform.scale(button_image, (150, 50)) 
    back_button_rect = pygame.Rect(center_x - 75, button_y, 150, 50)

    # Dessine l'image du boutton
    screen.blit(button_image, (center_x - 75, button_y))
    draw_text(screen, "Main Menu", font, GC.WHITE, back_button_rect.center)

    # Mise a jour de l'ecran
    pygame.display.flip()

    # Boucle "event"
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return "back_to_menu" 

def game_over_menu(screen, winner, background_path="Photos/background2.png"):
    '''Affiche le menu Game Over'''
    clock = pygame.time.Clock()

    # Font
    font_path = "font/CinzelDecorative-Bold.ttf" 
    font_size = 30 
    try:
        font = pygame.font.Font(font_path, font_size) 
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        sys.exit()

    # Image de fond
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Images des héros pour chaque équipe
    player1_image = pygame.image.load("Photos/archer1_winner.png").convert_alpha()
    player2_image = pygame.image.load("Photos/archer2_winner.png").convert_alpha()

 
    player1_image = pygame.transform.scale(player1_image, (200, 200))
    player2_image = pygame.transform.scale(player2_image, (200, 200))

    # Variables d'Animation
    char_y = screen.get_height() // 2 - 150
    direction = 1
    bobbing_speed = 2

    # Positions de Bouttons
    rematch_button_pos = pygame.Rect(screen.get_width() // 2 - 125, 400, 250, 70)
    quit_button_pos = pygame.Rect(screen.get_width() // 2 - 125, 480, 250, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rematch_button_pos.collidepoint(event.pos):
                    return "rematch"
                if quit_button_pos.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Animation
        char_y += direction * bobbing_speed * 0.1
        if char_y <= screen.get_height() // 2 - 160 or char_y >= screen.get_height() // 2 - 140:
            direction *= -1

        # Fond
        screen.blit(background, (0, 0))

        # Affiche "Game Over" et le gagnant
        draw_text(screen, "Game Over!", font, (255, 0, 0), (screen.get_width() // 2, 50))
        if winner == "Player 1":
            draw_text(screen, "PLAYER 1 WINS!", font, (255, 255, 255), (screen.get_width() // 2, 150))
            screen.blit(player1_image, (screen.get_width() // 2 - 100, char_y))
        else:
            draw_text(screen, "PLAYER 2 WINS!", font, (255, 255, 255), (screen.get_width() // 2, 150))
            screen.blit(player2_image, (screen.get_width() // 2 - 100, char_y))

        # Charge et dessine les bouttons
        button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
        button_base = pygame.transform.scale(button_image, (250, 70))
        
        rematch_button = button_base.copy()
        screen.blit(rematch_button, rematch_button_pos.topleft)
        draw_text(screen, "Rematch", font, (255, 255, 255), rematch_button_pos.center)

        quit_button = button_base.copy()
        screen.blit(quit_button, quit_button_pos.topleft)
        draw_text(screen, "Exit", font, (255, 255, 255), quit_button_pos.center)

        # Mise a Jour de l'Affichage
        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((GC.WIDTH + 500, GC.HEIGHT))
    pygame.display.set_caption("L'Ascension des Héros")
    clock = pygame.time.Clock()

    p1_images = [
        pygame.image.load('Photos/archer.png'),
        pygame.image.load('Photos/mage.png'),
        pygame.image.load('Photos/giant.png'),
    ]
    p2_images = [
        pygame.image.load('Photos/enemy_archer.png'),
        pygame.image.load('Photos/enemy_mage.png'),
        pygame.image.load('Photos/enemy_giant.png'),
    ]
    for i in range(len(p1_images)):
        p1_images[i] = pygame.transform.scale(p1_images[i], (50, 50))
        p2_images[i] = pygame.transform.scale(p2_images[i], (50, 50))

    while True:
        action = main_menu(screen)

        if action == "play":
            random_seed = 42  
            tile_map = Game.generate_random_map(random_seed)
            game = Game(screen, tile_map)
            winner = game.main_loop() 

            action = game_over_menu(screen, winner)
            if action == "rematch":
                continue 
            elif action == "quit":
                pygame.quit()
                sys.exit()

        elif action == "how_to_play":

            rules_action = rules_screen(screen, p1_images, p2_images)
            if rules_action == "back_to_menu":
                continue  

        elif action == "quit":
            pygame.quit()
            sys.exit()

        clock.tick(GC.FPS)

if __name__ == "__main__":
    main()
