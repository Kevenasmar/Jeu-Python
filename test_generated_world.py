from world import World
from configureWorld import *
from World_Drawer import *  
from constante import GameConstantes as GC
import pygame
pygame.init()

def test_generate_world(weights, random_seed):
    # Cette fonction génère un monde basé sur des poids spécifiés et un random_seed pour la génération aléatoire.
    # Elle crée une instance de WorldDrawer pour dessiner le monde et gère les événements de fermeture de la fenêtre.
    for event in pygame.event.get():
        # Gestion de la fermeture de la fenêtre
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()    
        world_drawer = WorldDrawer()
        world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
        tile_map = world.get_tiled_map(weights)
        world_drawer.draw(tile_map, wait_for_key = True)


def test_emerge(target_weights, random_seed):
    # Cette fonction simule l'émergence d'un monde en ajustant progressivement les poids des différents types de terrain
    # (eau, sable, herbe, etc.) jusqu'à atteindre des poids cibles.
    # Elle commence par augmenter les poids et les dessine à chaque étape, puis réduit les poids jusqu'à atteindre les valeurs cibles.
    for event in pygame.event.get():
        # Gestion de la fermeture de la fenêtre
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  
        world_drawer = WorldDrawer()
        world = World(GC.WORLD_X, GC.WORLD_Y, random_seed)
        weights = [target_weights[GC.water] - 1, 0, 0, 0, 0, 0, 0]
        done = False

    while not done:
        tile_map = world.get_tiled_map(weights)
        world_drawer.draw(tile_map, wait_for_key = False)

        if weights[GC.water] < target_weights[GC.water]:
            weights[GC.water] += 1
        elif weights[GC.sand] < target_weights[GC.sand]:
            weights[GC.sand] += 1
        elif weights[GC.grass] < target_weights[GC.grass]:
            weights[GC.grass] += 1
        elif weights[GC.rock] < target_weights[GC.rock]:
            weights[GC.rock] += 1
        elif weights[GC.log] < target_weights[GC.log]:
            weights[GC.log] += 1
        elif weights[GC.mountain] < target_weights[GC.mountain]:
            weights[GC.mountain] += 1
        else:
            done = True

    done = False
    target_weights = [weights[GC.water] - 1, 0, 0, 0, 0, 0, 0]

    while not done:
        tile_map = world.get_tiled_map(weights)
        world_drawer.draw(tile_map, wait_for_key = False)

        if weights[GC.mountain] >= target_weights[GC.mountain] and weights[GC.mountain] > 0:
            weights[GC.mountain] -= 1
        elif weights[GC.log] >= target_weights[GC.log] and weights[GC.log] > 0:
            weights[GC.log] -= 1
        elif weights[GC.rock] >= target_weights[GC.rock] and weights[GC.rock] > 0:
            weights[GC.rock] -= 1
        elif weights[GC.grass] >= target_weights[GC.grass] and weights[GC.grass] > 0:
            weights[GC.grass] -= 1
        elif weights[GC.sand] >= target_weights[GC.sand] and weights[GC.sand] > 0:
            weights[GC.sand] -= 1
        elif weights[GC.water] >= target_weights[GC.water] and weights[GC.water] > 0:
            weights[GC.water] -= 1
        else:
            done = True