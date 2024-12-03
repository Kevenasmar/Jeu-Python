import pygame
import sys
from game import Game
from constante import GameConstantes as GC

def draw_text(screen, text, font, color, pos):
    """Utility to render text on the screen."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)

def main_menu(screen):
    """Display the main menu with Play and Exit buttons."""
    font = pygame.font.Font(None, 40)
    screen.fill(GC.BLACK)  # Background color

    # Calculate playable width (excluding game log)
    game_log_width = -500  # Width of the game log
    playable_width = GC.WIDTH - game_log_width  # Adjusted width for centering
    center_x = playable_width // 2  # Horizontal center of the playable area

    # Title
    draw_text(screen, "Bienvenue!", font, GC.WHITE, (center_x, GC.HEIGHT // 4))
    draw_text(screen, "Préparez-vous à écrire votre légende sur le champ de bataille", 
              font, GC.WHITE, (center_x, GC.HEIGHT // 4 + 50))  # Add some spacing for subtitle

    # Buttons
    play_button = pygame.Rect(center_x - 75, GC.HEIGHT // 2 - 50, 150, 50)
    exit_button = pygame.Rect(center_x - 75, GC.HEIGHT // 2 + 20, 150, 50)

    pygame.draw.rect(screen, (0, 200, 0), play_button)
    pygame.draw.rect(screen, (200, 0, 0), exit_button)

    # Button text
    draw_text(screen, "Jouer", font, GC.WHITE, play_button.center)
    draw_text(screen, "Quitter", font, GC.WHITE, exit_button.center)

    # Update display
    pygame.display.flip()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "play"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def rules_screen(screen, p1_images, p2_images):
    """Display game rules and unit images for both players."""
    font = pygame.font.Font(None, 30)
    screen.fill((50, 50, 100))  # Background color

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
        color = GC.WHITE if rule != rules[-1] else GC.RED
        draw_text(screen, rule, font, color, (center_x, y))
        y += 40  # Spacing between lines

    # Player 1 units
    y += 40  # Additional spacing
    draw_text(screen, "Unités du Joueur 1:", font, GC.GREEN, (playable_width // 4, y))
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
    continue_button = pygame.Rect(center_x - 75, button_y, 150, 50)
    pygame.draw.rect(screen, (0, 200, 0), continue_button)
    draw_text(screen, "Continuer", font, GC.WHITE, continue_button.center)

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
            game.main_loop()  # Assumes Game class has a `main_loop()` method

        clock.tick(GC.FPS)

if __name__ == "__main__":
    main()
