# cette classe est pour génerer les maps aléatroirement : 
from perlin_noise import PerlinNoise
from Tiles import*
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
    Cette classe est utilisée pour représenter une carte aléatoire générée à partir de données de terrain.
    
    Attributes:
    terrain_data (list): Une liste 2D représentant les données de terrain de la carte.
    terrain_tiles (dict): Un dictionnaire contenant les tuiles de terrain associées à chaque type de terrain.
    cell_size (int): La taille d'une cellule de la carte.
    """

    def __init__(self, terrain_data, terrain_tiles, cell_size):
        """
        Initialise une instance de la classe Map_Aleatoire.
        
        Args:
        terrain_data (list): Les données de terrain de la carte.
        terrain_tiles (dict): Les tuiles de terrain associées à chaque type de terrain.
        cell_size (int): La taille d'une cellule de la carte.
        """
        self.terrain_data = terrain_data
        self.terrain_tiles = terrain_tiles
        self.cell_size = cell_size

      
    def is_walkable(self, x, y, unité=None):
        """
        Vérifie si une position donnée sur la carte est accessible.
        
        Args:
        x (int): La coordonnée x de la position.
        y (int): La coordonnée y de la position.
        unité (object): L'unité qui tente de marcher (peut être un mage).
        
        Returns:
        bool: True si la position est accessible, False sinon.
        """
        # Vérification des limites
        if not (0 <= x < len(self.terrain_data[0]) and 0 <= y < len(self.terrain_data)):
            return False
        
        terrain_type = self.terrain_data[y][x]
        tile = self.terrain_tiles[terrain_type]
        
        # Vérification pour le mage en premier
        if isinstance(unité, Mage) and isinstance(tile, WaterTile):
            return True  # Le mage peut marcher sur l'eau
            
        # Vérification si la tuile est solide
        if tile.is_solide:
            return False
            
        return True  # Le terrain est marchable
    

    def draw(self, screen):
        """
        Dessine la carte sur l'écran.
        
        Args:
        screen: L'écran sur lequel dessiner la carte.
        """
        # Parcourt chaque ligne de la carte
        for y, row in enumerate(self.terrain_data):
            # Parcourt chaque cellule de la ligne
            for x, terrain_type in enumerate(row):
                # Récupère la tuile de terrain associée à ce type de terrain
                tile = self.terrain_tiles[terrain_type]
                # Dessine la tuile de terrain à la position correspondante sur l'écran
                screen.blit(tile.image, (x * self.cell_size, y * self.cell_size))
