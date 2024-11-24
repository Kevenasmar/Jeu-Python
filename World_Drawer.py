#le fichier suivant est le responsable sur la generation du monde
import pygame
from configureWorld import *
from constante import GameConstantes as GC

class WorldDrawer:

    def __init__(self):
        # open window
        pygame.init()
        self.display_surface = pygame.display.set_mode((GC.WIDTH, GC.HEIGHT))

        # get images for all tiles for every terrain type
        self.terrain_tiles = []  # This will store the images for each terrain type
        for tile_path in GC.TILE_IMAGES:
            image = pygame.image.load(tile_path).convert_alpha()  # Ensure the image supports transparency
            scaled_image = pygame.transform.scale(image, (GC.CELL_SIZE, GC.CELL_SIZE))  # Scale images to match tile size
            self.terrain_tiles.append(scaled_image)


    def draw(self, height_map, wait_for_key):
        self.draw_tiles(height_map)
        pygame.display.flip()
        if wait_for_key:
            self.wait_key()


    def wait_key(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                break


    def draw_tiles(self, terrain_type_map):
        for y, row in enumerate(terrain_type_map):
            for x, terrain_type in enumerate(row):
                if x == GC.WORLD_X or y == GC.WORLD_Y:
                    continue

                # Draw the image for the current terrain type
                image = self.terrain_tiles[terrain_type]
                self.display_surface.blit(image, (x * GC.CELL_SIZE, y * GC.CELL_SIZE))