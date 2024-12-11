#constantes 
#defini dans ce fichier toutes les constantes que tu utilise dans le code
class GameConstantes : 

    GRID_SIZE = 14
    CELL_SIZE = 45

    
    WIDTH = GRID_SIZE * CELL_SIZE
    HEIGHT = GRID_SIZE * CELL_SIZE
    FPS = 60
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


    #Propriétés des unités
    #ARCHER 
    ARCHER_HP = 100
    ARCHER_ATK = 12
    ARCHER_DEF = 6
    ARCHER_SPEED = 5
    NORMAL_ARROW_RANGE = 5
    FIRE_ARROW_RANGE = 3
    HEADSHOT_PROB = 0.1

    #GIANT
    GIANT_HP = 125
    GIANT_ATK = 25
    GIANT_DEF = 9
    GIANT_SPEED = 2
    PUNCH_RANGE = 2
    STOMP_RANGE = 1

    #MAGE
    MAGE_HP = 75
    MAGE_ATK = 11
    MAGE_DEF = 4
    MAGE_SPEED = 4
    HEAL_RANGE = 1
    POTION_RANGE = 6

    #BOMBER
    BOMBER_HP = 100
    BOMBER_ATK = 18
    BOMBER_DEF = 4
    BOMBER_SPEED = 3
    BOMB_RANGE = 3
    EXPLODE_RANGE = 5

