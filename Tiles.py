# Importation des bibliothèques nécessaires
import pygame
pygame.init()
from constante import GameConstantes as GC
from abc import ABC, abstractmethod
from unit import Mage
screen = pygame.display.set_mode((GC.WIDTH,GC.HEIGHT))
# Définition d'une classe abstraite pour représenter les types de tuiles
class TileKind(ABC):
    """
    Classe abstraite pour représenter les types de tuiles.
    
    Attributes:
    nom (str): Le nom du type de tuile.
    image_path (str): Chemin du fichier de l'image représentant le type de tuile.
    is_solide (bool): Booléen indiquant si le type de tuile est solide (obstacle) ou passable.
    """

    def __init__(self, nom, image_path, is_solide):
        """
        Initialise un objet TileKind.
        
        :param nom: Le nom du type de tuile.
        :param image: Chemin du fichier de l'image représentant le type de tuile.
        :param is_solide: Booléen indiquant si le type de tuile est solide (obstacle) ou passable.
        """
        self.nom = nom
        self.image_path = image_path
        Loaded_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(Loaded_image, (GC.CELL_SIZE, GC.CELL_SIZE))
        self.is_solide = is_solide

    # Méthode abstraite pour interagir avec une unité
    @abstractmethod
    def interact(self, unité):
        """
        Méthode abstraite pour interagir avec une unité.
        
        :param unité: L'unité qui interagit avec la tuile.
        :return: Booléen indiquant si l'unité peut interagir avec la tuile.
        """
        pass

# Définition d'une classe pour représenter les tuiles passables
class WalkableTile(TileKind):
    """
    Classe pour représenter les tuiles passables.
    
    Attributes:
    nom (str): Le nom du type de tuile.
    image (str): Chemin du fichier de l'image représentant le type de tuile.
    """

    def __init__(self, nom, image):
        """
        Initialise un objet WalkableTile.
        
        :param nom: Le nom du type de tuile.
        :param image: Chemin du fichier de l'image représentant le type de tuile.
        """
        super().__init__(nom, image, False)

    # Méthode pour interagir avec une unité
    def interact(self, unité):
        """
        Méthode pour interagir avec une unité.
        
        :param unité: L'unité qui interagit avec la tuile.
        :return: Booléen indiquant si l'unité peut interagir avec la tuile.
        """
        return True  # l'unité peut marcher

# Définition d'une classe pour représenter les tuiles non passables
class UnwalkableTile(TileKind):
    """
    Classe pour représenter les tuiles non passables.
    
    Attributes:
    nom (str): Le nom du type de tuile.
    image (str): Chemin du fichier de l'image représentant le type de tuile.
    """

    def __init__(self, nom, image):
        """
        Initialise un objet UnwalkableTile.
        
        :param nom: Le nom du type de tuile.
        :param image: Chemin du fichier de l'image représentant le type de tuile.
        """
        super().__init__(nom, image, True)

    # Méthode pour interagir avec une unité
    def interact(self, unité):
        """
        Méthode pour interagir avec une unité.
        
        :param unité: L'unité qui interagit avec la tuile.
        :return: Booléen indiquant si l'unité peut interagir avec la tuile.
        """
        return False  # l'unité ne peut pas marcher

# Définition de classes pour représenter les différents types de tuiles
class GrassTile(WalkableTile):
    def __init__(self):
        super().__init__("grass", "image/grass.png")

class WaterTile(UnwalkableTile):
    def __init__(self):
        super().__init__("water", "image/water.png")
       

class RockTile(UnwalkableTile):
    def __init__(self):
        super().__init__("rock", "image/rock.png")

class SandTile(WalkableTile):
    def __init__(self):
        super().__init__("sand", "image/sand.png")

class LogTile(UnwalkableTile):
    def __init__(self):
        super().__init__("Log", "image/log.png")

class MountainTile(UnwalkableTile):
    def __init__(self):
        super().__init__("Mountain", "image/mountain.png")

# Définition d'une classe pour représenter la carte
class Map:
    """
    Classe pour représenter la carte.
    
    Attributes:
    tiles_kind (dict): Dictionnaire des types de tuiles.
    tile_size (int): Taille des tuiles.
    tiles (list): Liste des tuiles de la carte.
    """

    def __init__(self, map_file, tiles_kind, tile_size):
        """
        Initialise un objet Map.
        
        :param map_file: Fichier de la carte.
        :param tiles_kind: Dictionnaire des types de tuiles.
        :param tile_size: Taille des tuiles.
        """
        self.tiles_kind = tiles_kind
        self.tile_size = tile_size
        # Chargement du fichier de la carte
        file = open(map_file, "r")
        data = file.read()
        file.close()

        # Création de la liste des tuiles
        self.tiles = []
        for line in data.split("\n"):
            row = []
            for tiles_number in line:
                row.append(int(tiles_number))
            self.tiles.append(row)

    # Méthode pour dessiner la carte
    def draw(self, screen):
        """
        Méthode pour dessiner la carte.
        
        :param screen: Écran de jeu.
        """
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tiles_kind[tile].image
                screen.blit(image, location)

    # Méthode pour vérifier si une position est marchable
    def is_walkable(self, x, y, unité = None ):
        """
        Méthode pour vérifier si une position est marchable.
        
        :param x: Coordonnée x de la position.
        :param y: Coordonnée y de la position.
        :return: Booléen indiquant si la position est marchable.
        """
        if not (0 <= x < len(self.tiles[0]) or 0 <= y < len(self.tiles)):
            return False
        tile = self.tiles_kind[self.tiles[y][x]]
        if isinstance(unité, Mage) and isinstance(tile, WaterTile):
            return True  # Le mage peut marcher sur l'eau
        if tile.is_solide:
            return False
        return True  # marchable