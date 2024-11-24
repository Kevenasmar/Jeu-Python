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
    def __init__(self, terrain_data, terrain_tiles, cell_size):
        self.terrain_data = terrain_data
        self.terrain_tiles = terrain_tiles
        self.cell_size = cell_size

    def is_walkable(self, x, y):
    # Check if the coordinates are within bounds
        if 0 <= x < len(self.terrain_data[0]) and 0 <= y < len(self.terrain_data): # type: ignore
            terrain_type = self.terrain_data[y][x]
            return not self.terrain_tiles[terrain_type].is_solide
        return False
    def draw(self, screen):
        for y, row in enumerate(self.terrain_data):
            for x, terrain_type in enumerate(row):
                tile = self.terrain_tiles[terrain_type]
                screen.blit(tile.image, (x * self.cell_size, y * self.cell_size))

