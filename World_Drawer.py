# Le fichier suivant est responsable de la génération du monde dans le jeu.
# Il utilise la bibliothèque Pygame pour créer une fenêtre et dessiner les éléments du monde.

import pygame
from configureWorld import *
from constante import GameConstantes as GC

# La classe WorldDrawer est utilisée pour dessiner le monde dans la fenêtre Pygame.
class WorldDrawer:
    # La méthode __init__ est appelée lors de la création d'un objet WorldDrawer.
    # Elle initialise la fenêtre Pygame et charge les images des tuiles pour chaque type de terrain.
    def __init__(self):
        # Ouvrir la fenêtre
        pygame.init()
        self.display_surface = pygame.display.set_mode((GC.WIDTH, GC.HEIGHT))

        # Charger les images pour chaque type de terrain
        self.terrain_tiles = []  # Cette liste stocke les images pour chaque type de terrain
        for tile_path in GC.TILE_IMAGES:
            image = pygame.image.load(tile_path).convert_alpha()  # Assurer que l'image supporte la transparence
            scaled_image = pygame.transform.scale(image, (GC.CELL_SIZE, GC.CELL_SIZE))  # Mettre à l'échelle les images pour correspondre à la taille des tuiles
            self.terrain_tiles.append(scaled_image)

    # La méthode draw est utilisée pour dessiner le monde dans la fenêtre.
    # Elle prend en paramètre une carte de hauteur et un booléen pour savoir si elle doit attendre une touche.
    def draw(self, height_map, wait_for_key):
        # Dessiner les tuiles
        self.draw_tiles(height_map)
        # Mettre à jour la fenêtre
        pygame.display.flip()
        # Si wait_for_key est True, attendre une touche
        if wait_for_key:
            self.wait_key()

    # La méthode wait_key est utilisée pour attendre une touche.
    # Elle est appelée lorsque wait_for_key est True dans la méthode draw.
    def wait_key(self):
        # Attendre une touche
        while True:
            event = pygame.event.wait()
            # Si la touche est enfoncée
            if event.type == pygame.KEYDOWN:
                # Si la touche est Échap ou Q, quitter le jeu
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                # Sinon, sortir de la boucle
                break

    # La méthode draw_tiles est utilisée pour dessiner les tuiles du monde.
    # Elle prend en paramètre une carte de type de terrain.
    def draw_tiles(self, terrain_type_map):
        # Pour chaque ligne de la carte
        for y, row in enumerate(terrain_type_map):
            # Pour chaque colonne de la ligne
            for x, terrain_type in enumerate(row):
                # Si la position est en dehors de la carte, ignorer
                if x == GC.WORLD_X or y == GC.WORLD_Y:
                    continue

                # Dessiner l'image pour le type de terrain actuel
                image = self.terrain_tiles[terrain_type]
                self.display_surface.blit(image, (x * GC.CELL_SIZE, y * GC.CELL_SIZE))