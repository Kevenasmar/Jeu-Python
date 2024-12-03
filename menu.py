import pygame
import sys
from game import Game
from constante import GameConstantes as GC


def lighten_surface(surface, amount):
    """Darken a surface by applying a transparent black layer."""
    light_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    light_layer.fill((255, 255, 255, amount))  # Apply a black layer with alpha transparency
    surface.blit(light_layer, (0, 0))
    
    
def draw_text(screen, text, font, color, pos):
    """Utility to render text on the screen."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)

def main_menu(screen):
    pygame.init()
    clock = pygame.time.Clock()

    # Screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Load assets
    battlefield_bg = pygame.image.load("Photos/menu_background.png").convert_alpha()
    battlefield_bg = pygame.transform.scale(battlefield_bg, (screen_width, screen_height))

    hero1 = pygame.image.load("Photos/archer.png").convert_alpha()
    hero1 = pygame.transform.scale(hero1, (150, 150))
    hero2 = pygame.image.load("Photos/enemy_archer.png").convert_alpha()
    hero2 = pygame.transform.scale(hero2, (150, 150))

    button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
    button_base = pygame.transform.scale(button_image, (150, 60))

    # Load a custom title font
    font_path = "font/CinzelDecorative-Bold.ttf"  # Replace with your font's path
    font_size = 50
    try:
        title_font = pygame.font.Font(font_path, font_size)  # Load custom font
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        sys.exit()
    
    # Load custom button fonts
    font_path = "font/Cinzel-Regular.otf"  # Replace with your font's path
    font_size = 50
    try:
        font = pygame.font.Font(font_path, font_size)  # Load custom font
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        sys.exit()

    # Hero animation variables
    hero1_y = screen_height // 2 - 100
    hero2_y = screen_height // 2 - 100
    bobbing_speed = 2
    direction = 1

    # Button positions
    play_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 100, 150, 50)
    exit_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 180, 150, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return "play"
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Bobbing animation for heroes
        hero1_y += direction * bobbing_speed * 0.1
        hero2_y += direction * bobbing_speed * 0.1
        if hero1_y <= screen_height // 2 - 110 or hero1_y >= screen_height // 2 - 90:
            direction *= -1

        # Draw background and title
        screen.blit(battlefield_bg, (0, 0))
        draw_text(screen, "Game Name", title_font, (255, 255, 255), (screen_width // 2, 50))

        # Draw heroes
        screen.blit(hero1, (screen_width // 4 - 75, hero1_y))
        screen.blit(hero2, (3 * screen_width // 4 - 75, hero2_y))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        # Play button hover effect
        play_button = button_base.copy()
        if play_button_rect.collidepoint(mouse_pos):
            lighten_surface(play_button, 100)
        screen.blit(play_button, play_button_rect.topleft)
        draw_text(screen, "Play", font, (255, 255, 255), play_button_rect.center)

        # Exit button hover effect
        exit_button = button_base.copy()
        if exit_button_rect.collidepoint(mouse_pos):
            lighten_surface(exit_button, 100)
        screen.blit(exit_button, exit_button_rect.topleft)
        draw_text(screen, "Exit", font, (255, 255, 255), exit_button_rect.center)

        # Update display
        pygame.display.flip()
        clock.tick(60)

def rules_screen(screen, p1_images, p2_images):
    """Display game rules and unit images for both players."""
    font_path = "font/Junicode.ttf"  # Replace with your font's path
    font_size = 25
    try:
        font = pygame.font.Font(font_path, font_size)  # Load custom font
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        sys.exit()
    # Screen dimensions
    background = pygame.image.load("Photos/background2.png").convert()  # Load your background image here
    background = pygame.transform.scale(background, screen.get_size())  # Scale to fit screen
    screen.blit(background, (0, 0))  # Draw the background onto the screen

    # Calculate playable width (excluding game log)
    game_log_width = -500  # Width of the game log
    playable_width = GC.WIDTH - game_log_width  # Adjusted width for centering
    center_x = playable_width // 2  # Horizontal center of the playable area

    # Title
    y = 50
    draw_text(screen, "Règles du Jeu", font, GC.WHITE, (center_x, y))
    y += 60  # Add spacing

    # Rules text
    rules = [
        "Objectif: Détruire toutes les unités ennemies.",
        "Pendant votre tour, vous pouvez déplacer vos unités ou attaquer les ennemis dans la portée.",
        "Chaque unité a une vitesse spécifique qui détermine combien de cases elle peut parcourir.",
        "Les unités ne peuvent pas traverser des obstacles (sauf exceptions comme le mage qui peut traverser l'eau).",
        "Approchez-vous d'une unité ennemie pour l'attaquer! Le dernier joueur en vie gagne.",
        "Que le meilleur triomphe dans la gloire et l'honneur !"
    ]
    for rule in rules:
        color = (
            (39, 8, 212) if rule == rules[1] else 
            (128, 19, 19) if rule == rules[-1] else 
            (15, 13, 74)
        )
        draw_text(screen, rule, font, color, (center_x, y))
        y += 40  # Spacing between lines

    # Player 1 units
    y += 40  # Additional spacing
    draw_text(screen, "Unités du Joueur 1:", font, (37, 128, 49), (playable_width // 4, y))
    p1_start_x = playable_width // 4 - (len(p1_images) * 60) // 2  # Center player 1 images in their section
    for i, image in enumerate(p1_images):
        screen.blit(image, (p1_start_x + i * 60, y + 30))  # Position images under the text

    # Player 2 units
    draw_text(screen, "Unités du Joueur 2:", font, GC.BLACK, (3 * playable_width // 4, y))
    p2_start_x = 3 * playable_width // 4 - (len(p2_images) * 60) // 2  # Center player 2 images in their section
    for i, image in enumerate(p2_images):
        screen.blit(image, (p2_start_x + i * 60, y + 30))  # Position images under the text

    # Adjust y position for the button
    button_y = GC.HEIGHT - 80  # Position "Continue" button closer to the bottom

    # Load the button image and scale it
    button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
    button_image = pygame.transform.scale(button_image, (150, 50))  # Scale to match the desired button size

    # Define the button's collision rectangle
    continue_button = pygame.Rect(center_x - 75, button_y, 150, 50)

    # Draw the button image
    screen.blit(button_image, (center_x - 75, button_y))

    # Draw text on the button
    draw_text(screen, "Continuer", font, GC.WHITE, continue_button.center)
    
    mouse_pos = pygame.mouse.get_pos()

    # Hover effect for the "Continue" button
    continue_button_image = button_image.copy()
    if continue_button.collidepoint(mouse_pos):
        lighten_surface(continue_button_image, 100)  # Darken the button on hover
    screen.blit(continue_button_image, (center_x - 75, button_y))  # Draw the button
    draw_text(screen, "Continuer", font, GC.WHITE, continue_button.center)  # Draw the text on the button



    # Update the screen
    pygame.display.flip()

    # Event loop for the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return

def game_over_menu(screen, winner, background_path="Photos/background2.png"):
    """Display the Game Over menu with a custom background, winner's animation, title, and options for rematch or quit."""
    clock = pygame.time.Clock()

    # Fonts
    font_path = "font/CinzelDecorative-Bold.ttf"  # Replace with your font's path
    font_size = 30 
    try:
        font = pygame.font.Font(font_path, font_size)  # Load custom font
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        sys.exit()

    # Load the custom background image
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Load images for animation
    player1_image = pygame.image.load("Photos/archer1_winner.png").convert_alpha()
    player2_image = pygame.image.load("Photos/archer2_winner.png").convert_alpha()

    # Scale images
    player1_image = pygame.transform.scale(player1_image, (200, 200))
    player2_image = pygame.transform.scale(player2_image, (200, 200))

    # Animation variables
    char_y = screen.get_height() // 2 - 150
    direction = 1
    bobbing_speed = 2

    # Button positions
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

        # Character bobbing animation
        char_y += direction * bobbing_speed * 0.1
        if char_y <= screen.get_height() // 2 - 160 or char_y >= screen.get_height() // 2 - 140:
            direction *= -1

        # Draw background
        screen.blit(background, (0, 0))

        # Display "Game Over" and winner title
        draw_text(screen, "Game Over!", font, (255, 0, 0), (screen.get_width() // 2, 50))
        if winner == "Player 1":
            draw_text(screen, "PLAYER 1 WINS!", font, (255, 255, 255), (screen.get_width() // 2, 150))
            screen.blit(player1_image, (screen.get_width() // 2 - 100, char_y))
        else:
            draw_text(screen, "PLAYER 2 WINS!", font, (255, 255, 255), (screen.get_width() // 2, 150))
            screen.blit(player2_image, (screen.get_width() // 2 - 100, char_y))

        # Load and draw buttons
        button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
        button_base = pygame.transform.scale(button_image, (250, 70))
        
        rematch_button = button_base.copy()
        screen.blit(rematch_button, rematch_button_pos.topleft)
        draw_text(screen, "Revanche", font, (255, 255, 255), rematch_button_pos.center)

        quit_button = button_base.copy()
        screen.blit(quit_button, quit_button_pos.topleft)
        draw_text(screen, "Quitter", font, (255, 255, 255), quit_button_pos.center)

        # Update display
        pygame.display.flip()
        clock.tick(60)






def main():
    pygame.init()
    screen = pygame.display.set_mode((GC.WIDTH + 500, GC.HEIGHT))
    pygame.display.set_caption("L'Ascension des Héros")
    clock = pygame.time.Clock()

    # Load unit images
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
        # Show the main menu
        action = main_menu(screen)
        if action == "play":
            # Show the rules screen
            rules_screen(screen, p1_images, p2_images)

            # Start the game
            random_seed = 42  # or any other seed logic
            tile_map = Game.generate_random_map(random_seed)
            game = Game(screen, tile_map)
            winner = game.main_loop()  # Assume `main_loop()` returns the winner

            # Show game over menu
            action = game_over_menu(screen, winner)
            if action == "rematch":
                continue  # Restart the game loop
            elif action == "quit":
                pygame.quit()
                sys.exit()

        clock.tick(GC.FPS)


if __name__ == "__main__":
    main()
