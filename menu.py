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

    # Load custom fonts
    font_path = "font/Cinzel-Regular.otf"
    font_size = 30
    font = pygame.font.Font(font_path, font_size)

    # Button positions
    play_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 50, 150, 60)
    how_to_play_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 120, 150, 60)
    exit_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 190, 150, 60)

    # Bobbing animation variables
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

        # Bobbing animation for heroes
        hero1_y += direction * bobbing_speed * 0.1
        hero2_y += direction * bobbing_speed * 0.1
        if hero1_y <= screen_height // 2 - 110 or hero1_y >= screen_height // 2 - 90:
            direction *= -1

        # Draw background
        screen.blit(battlefield_bg, (0, 0))

        # Draw title
        draw_text(screen, "Rise of Heroes", font, (255, 255, 255), (screen_width // 2, 50))

        # Draw heroes with bobbing animation
        screen.blit(hero1, (screen_width // 4 - 75, hero1_y))
        screen.blit(hero2, (3 * screen_width // 4 - 75, hero2_y))

        # Draw buttons
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

        # Update display
        pygame.display.flip()
        clock.tick(60)


def rules_screen(screen, p1_images, p2_images):
    """Display game rules with better alignment for unit descriptions and a 'Back to Main Menu' button."""
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

    # Title
    center_x = screen.get_width() // 2
    y = 20
    draw_text(screen, "HOW TO PLAY", font, GC.RED, (center_x, y))
    y += 50  # Add spacing

    # General Rules Section
    general_rules = [
        "Objective: Defeat all enemy units.",
        "Each turn, you can move and/or attack with your units.",
        "Units have unique abilities that affect gameplay.",
        "May the best player win in glory & honor!"
    ]
    for rule in general_rules:
        draw_text(screen, rule, font, (15, 13, 74), (center_x, y))
        y += 30  # Spacing between lines

    # Unit Descriptions Section
    # Define columns for units
    column_width = screen.get_width() // 4
    unit_y_start = y + 50  # Leave some space after general rules

    # Unit Info
    units_info = [
        {
            "name": "Archer",
            "abilities": [
                "- Normal Arrow:",
                "Medium-range & damage,",
                "4% chance of headshot!",
                " ",
                "- Fire Arrow:",
                "Moderate damage",
                "over time"
            ],
            "images": (p1_images[0], p2_images[0])
        },
        {
            "name": "Mage",
            "abilities": [
                "- Potion:",
                " Low damage",
                " ",
                "- Heal:",
                "Restores health",
                "to allies"
            ],
            "images": (p1_images[1], p2_images[1])
        },
        {
            "name": "Giant",
            "abilities": [
                "- Punch:",
                "Close-range,",
                "high-damage.",
                " ",
                "- Stomp:",
                "Pushes enemy back,",
                "high-damage."
            ],
            "images": (p1_images[2], p2_images[2])
        },
        {
            "name": "Bomber",
            "abilities": [
                "- Bomb Throw:",
                "Medium-range,",
                "explosive attack",
                " ",
                "- Self-Destruct:",
                "Deals massive damage"
            ],
            "images": (p1_images[0], p2_images[0])  # Placeholder for Bomber images
        }
    ]

    for i, unit in enumerate(units_info):
        # Calculate the column position
        column_x = i * column_width + column_width // 2

        # Unit name
        unit_y = unit_y_start
        draw_text(screen, unit["name"], font, GC.RED, (column_x, unit_y))

        # Player and Enemy Images
        unit_y += 40
        player_image, enemy_image = unit["images"]
        screen.blit(player_image, (column_x - 50, unit_y))  # Left-align player image
        screen.blit(enemy_image, (column_x + 10, unit_y))   # Right-align enemy image

        # Unit Abilities
        unit_y += 60
        for ability in unit["abilities"]:
            draw_text(screen, ability, font, (15, 13, 74), (column_x, unit_y))
            unit_y += 25  # Space between abilities

    # Back to Main Menu Button
    button_y = GC.HEIGHT - 80  # Position closer to the bottom
    button_image = pygame.image.load("Photos/BOUTTON.png").convert_alpha()
    button_image = pygame.transform.scale(button_image, (150, 50))  # Scale to match the desired button size
    back_button_rect = pygame.Rect(center_x - 75, button_y, 150, 50)

    # Draw the button image
    screen.blit(button_image, (center_x - 75, button_y))
    draw_text(screen, "Main Menu", font, GC.WHITE, back_button_rect.center)

    # Update the screen
    pygame.display.flip()

    # Event loop for the screen
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return "back_to_menu"  # Explicitly return this action




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
        draw_text(screen, "Rematch", font, (255, 255, 255), rematch_button_pos.center)

        quit_button = button_base.copy()
        screen.blit(quit_button, quit_button_pos.topleft)
        draw_text(screen, "Exit", font, (255, 255, 255), quit_button_pos.center)

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
            # Directly start the game
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

        elif action == "how_to_play":
            # Show the rules screen
            rules_action = rules_screen(screen, p1_images, p2_images)
            if rules_action == "back_to_menu":
                continue  # Return to the main menu

        elif action == "quit":
            pygame.quit()
            sys.exit()

        clock.tick(GC.FPS)




if __name__ == "__main__":
    main()
