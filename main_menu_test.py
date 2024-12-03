import pygame
import sys

def game_over_menu(screen, winner, background_path):
    """Display the Game Over menu with a custom background, winner's animation, title, and options for rematch or quit."""
    pygame.init()
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

    # Adjust Rect sizes to match the button image
    rematch_button_pos = pygame.Rect(screen.get_width() // 2 - 125, 400, 250, 70)
    quit_button_pos = pygame.Rect(screen.get_width() // 2 - 125, 480, 250, 70)


    # Button colors
    button_color = (0, 200, 0)
    hover_color = (0, 255, 0)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rematch_button.collidepoint(event.pos):
                    return "rematch"
                if quit_button.collidepoint(event.pos):
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

def draw_text(screen, text, font, color, pos):
    """Utility to render centered text."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)

# Test the menu
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Over Menu Test")
    # Test the game_over_menu with a custom background
    game_over_menu(screen, "Player 1", "Photos/background2.png")
