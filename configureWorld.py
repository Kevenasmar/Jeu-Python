# Ce code est pour definir les differents tuiles utilisé dans le code Game et World et WorldDrawer
#Si tu veux ajouter un autre type de tuile, pense à sa hauteur parmi les autres types de tuiles, s'il vient aprés la montagne c'est snow
#SI tu integre un autre type de tuile, pense a modifier test_generated_world
# Importation des classes de tuiles depuis le module Tiles
from Tiles import*

# Liste des types de terrains disponibles, chaque nombre représente un type de tuile
ALL_TERRAIN_TYPES = [0, 1, 2, 3, 4, 5]


# Dictionnaire associant chaque type de terrain à une instance de sa classe correspondante
TERRAIN_TILES = {
    0: WaterTile(),    # Tuile d'eau
    1: SandTile(),     # Tuile de sable
    2: GrassTile(),    # Tuile d'herbe
    3: RockTile(),     # Tuile de roche
    4: LogTile(),      # Tuile de bois
    5: MountainTile()   # Tuile de montagne
}