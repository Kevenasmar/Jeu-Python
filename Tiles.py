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
    """
    def __init__(self, nom, image_path, is_solide):
        self.nom = nom
        self.image_path = image_path
        Loaded_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(Loaded_image, (GC.CELL_SIZE, GC.CELL_SIZE))
        self.is_solide = is_solide

    @abstractmethod
    def interact(self, unité):
        pass

class WalkableTile(TileKind):
    """
    Classe pour représenter les tuiles passables.
    """
    def __init__(self, nom, image):
        super().__init__(nom, image, False)

    def interact(self, unité):
        return True

class UnwalkableTile(TileKind):
    """
    Classe pour représenter les tuiles non passables.
    """
    def __init__(self, nom, image):
        super().__init__(nom, image, True)

    def interact(self, unité):
        return False

class ConditionalTile(TileKind):
    """
    Classe pour représenter les tuiles avec des comportements conditionnels.
    """
    def __init__(self, nom, image_path, is_solide):
        super().__init__(nom, image_path, is_solide)

    def interact(self, unité):
        return not self.is_solide
# Définition de classes pour représenter les différents types de tuiles
class GrassTile(WalkableTile):
    def __init__(self):
        super().__init__("grass", "image/grass.png")

class WaterTile(ConditionalTile):
    def __init__(self):
        super().__init__("water", "image/water.png", True)
    
    def interact(self, unité):
        """
        Permet au mage de marcher sur l'eau, mais pas aux autres unités.
        """
        if isinstance(unité, Mage):
            return True  # Le mage peut marcher sur l'eau
        return False  # Les autres unités ne peuvent pas

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

