#constantes 
#defini dans ce fichier toutes les constantes que tu utilise dans le code
class GameConstantes : 
    GRID_SIZE = 12
    CELL_SIZE = 60
    WIDTH = GRID_SIZE * CELL_SIZE
    HEIGHT = GRID_SIZE * CELL_SIZE
    FPS = 30
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    TILE_IMAGES = [
    "image/water.png",     # Chemin pour l'image de l'eau
    "image/sand.png",      # Chemin pour l'image du sable
    "image/grass.png",     # Chemin pour l'image de l'herbe
    "image/rock.png",      # Chemin pour l'image des rochers
    "image/log.png",       # Chemin pour l'image des troncs
    "image/mountain.png"   # Chemin pour l'image des montagnes
]
    # Calcul de WORLD_X et WORLD_Y pour savoir combien de tuiles peuvent être affichées à l'écran
    WORLD_X = (WIDTH + CELL_SIZE - 1) // CELL_SIZE
    WORLD_Y = (HEIGHT + CELL_SIZE - 1) // CELL_SIZE

    water = 0
    sand = 1
    grass = 2
    rock = 3
    log = 4
    montain = 5

 
