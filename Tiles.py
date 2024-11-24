import pygame
from constante import GameConstantes as GC
from abc import ABC, abstractmethod



class TileKind(ABC): 
    def __init__(self, nom, image_path, is_solide) :
        """
        Initialise un objet TileKind.

        :param nom: Le nom du type de tuile.
        :param image: Chemin du fichier de l'image représentant le type de tuile.
        :param is_solide: Booléen indiquant si le type de tuile est solide (obstacle) ou passable.
        """
        self.nom = nom
        self.image_path = image_path
        Loaded_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(Loaded_image, (GC.CELL_SIZE, GC.CELL_SIZE))
        self.is_solide = is_solide

        def interact(self,unité) : #methode abstraite on l'implementra dans les classes filles (grass, eau, mur)
            pass 

class WalkableTile(TileKind): #class fille de tilekind qui permet de definir les tuiles qui sont passables
    def __init__(self,nom,image) : 
        super().__init__(nom, image, False)
    
    def interact(self,unité) : 
        return True # l'unité peut marcher

class UnwalkableTile(TileKind): #class fille de tilekind qui permet de definir les tuiles qui ne sont pas passables
    def __init__(self,nom,image) : 
        super().__init__(nom, image, True)
    
    def interact(self,unité) : 
        return False # l'unité ne peut pas marcher

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


class Map: 
    def __init__(self,map_file, tiles_kind, tile_size) : 
        self.tiles_kind = tiles_kind
        #tile size : 
        self.tile_size = tile_size
        #load the map file
        file = open(map_file, "r")
        data = file.read()
        file.close()
    
        #donner a chaque caracrtere sa case 
        self.tiles = [] 
        #matrice comme ca [0 1 0 1 0]
        #                 [0 1 0 1 0]
        #                 [0 1 0 1 0]           
        for line in data.split("\n") : 
            row = [] 
            for tiles_number in line : 
                row.append(int(tiles_number))
            self.tiles.append(row)

         

        #afficher map sur l'ecran :
    def draw(self, screen) : 
        for y, row in enumerate(self.tiles) : 
            for x, tile in enumerate(row) : 
                location = (x * self.tile_size, y*self.tile_size)
                image = self.tiles_kind[tile].image
                screen.blit(image,location) 

    def is_walkable(self, x, y) : # n'est pas marchable si la case est solide, sinon elle l'est.
        if not (0 <= x < len(self.tiles[0])  or 0 <= y < len(self.tiles) ): # on doit verifier si la position est dans la map
            return False
        tile = self.tiles_kind[self.tiles[y][x]]
        if tile.is_solide:
            return False            
        return True #marchable