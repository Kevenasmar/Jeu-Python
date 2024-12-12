# cette classe est pour génerer les maps aléatroirement : 
from perlin_noise import PerlinNoise
from Tiles import *
from configureWorld import*


class World: 
    def __init__ (self, size_x,size_y, random_seed) : #size_x et size_y sont la taille de la map
        self.generate_noisemap(size_x, size_y, random_seed)
        #on calcule le minimum et le maximul du bruit 
        # le but ici est de récuperer tout les élements de la list imbriqué et la mettre dans une list avec chaque element individuelle : 
        # [[0,1,20],[0,60]] -> [0,1,20,0,60]
        #for sublist in self.noise_map : sublist parcours chaque sous list de la list self.noise_map : [0,1,20] et [0,60]
        #for item in sublist : item parcours chaque element de la sublist: 0,1,2 apres 0 et 60
        #item est ajouté à la flat_list
        flat_list = [item for sublist in self.noise_map for item in sublist]
        self.min_value = min(flat_list)
        self.max_value = max(flat_list)
        
        

    def generate_noisemap(self, size_x,size_y,random_seed) : 
        #On génere notre monde avec l'integration du bruit perlin 
        noise1 = PerlinNoise(octaves = 3, seed = random_seed)
        noise2 = PerlinNoise(octaves = 6, seed = random_seed)
        noise3 = PerlinNoise(octaves = 12, seed = random_seed)
        noise4 = PerlinNoise(octaves = 24, seed = random_seed)
        noise5 = PerlinNoise(octaves = 48, seed = random_seed)
        noise6 = PerlinNoise(octaves = 48, seed = random_seed)

        xpix , ypix = size_x + 1, size_y + 1 
        self.noise_map = []
        # avec cette methode on genere une array 2D representant la hauteur de nos coordonnées dans notre monde
        for j in range(ypix) : 
            row = []
            for i in range(xpix) :
                noise_val  = noise1([i/xpix, j/ypix]) #noise prends des valeurs réel entre 0 et 1 , c'est pour ça qu'on divise par xpix et ypix
                noise_val += 0.5 * noise2([i/xpix, j/ypix]) 
                noise_val += 0.25 * noise3([i/xpix, j/ypix]) 
                noise_val += 0.125 * noise4([i/xpix, j/ypix]) 
                noise_val += (0.125/2) * noise5([i/xpix, j/ypix])
                noise_val += (0.125/4) * noise6([i/xpix, j/ypix])    
                row.append(noise_val)
            self.noise_map.append(row)

    def get_tiled_map(self,weights):
        total_weights = sum(weights) #utilisé pour la géneration des mondes, plus la tuile a un poids important plus on la voit dans la map.
        total_range = self.max_value - self.min_value

        #On calcule la hauteur maximal pour chaque tuile 
        max_terrain_height = []
        previous_height = self.min_value
        for terrain_type in ALL_TERRAIN_TYPES : 
            height = total_range * (weights[terrain_type]/total_weights) + previous_height
            max_terrain_height.append(height)
            previous_height = height
        max_terrain_height[GC.montain] = self.max_value

        map_int = []
        
        for row in self.noise_map :
            map_row = []
            for value in row : 
                for terrain_type in ALL_TERRAIN_TYPES : 
                    if value <= max_terrain_height[terrain_type] : 
                        map_row.append(terrain_type)
                        break
            
            map_int.append(map_row)
        
        return map_int

class Map_Aleatoire:
    """
    Représente une carte aléatoire générée à partir de données de terrain.
    """
    def __init__(self, terrain_data, terrain_tiles, cell_size):
        """
        Initialise une instance de la classe Map_Aleatoire.
        """
        self.terrain_data = terrain_data  # Données de terrain de la carte
        self.terrain_tiles = terrain_tiles  # Tuiles de terrain associées à chaque type de terrain
        self.cell_size = cell_size  # Taille d'une cellule de la carte

    def is_walkable(self, x, y, unité=None):
        """
        Vérifie si une position donnée sur la carte est accessible.
        """
        if not (0 <= x < len(self.terrain_data[0]) and 0 <= y < len(self.terrain_data)):  # Vérification des limites
            return False
        terrain_type = self.terrain_data[y][x]  # Type de terrain
        tile = self.terrain_tiles[terrain_type]  # Tuile de terrain correspondante
        return tile.interact(unité)  # Vérifie si l'unité peut marcher sur la tuile

    def draw(self, screen):
        """
        Dessine la carte sur l'écran.
        """
        for y, row in enumerate(self.terrain_data):  # Parcourt chaque ligne de la carte
            for x, terrain_type in enumerate(row):  # Parcourt chaque cellule de la ligne
                tile = self.terrain_tiles[terrain_type]  # Tuile de terrain associée
                screen.blit(tile.image, (x * self.cell_size, y * self.cell_size))  # Dessine la tuile de terrain