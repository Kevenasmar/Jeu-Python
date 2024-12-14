# Test_Monde

## Introduction

Le dossier `tester_les_mondes` a été créé pour nous aider dans les premiers jours de test des différentes combinaisons de poids. L'objectif principal était de déterminer la meilleure combinaison de poids pour notre jeu, afin d'optimiser la génération des mondes et d'améliorer l'expérience de jeu.

Ces fichiers ont été récupérés depuis le GitHub de CodingQuest https://github.com/CodingQuest2023/Algorithms/tree/d7c8bcf7a0055683ebbf23cbd2182220da2125ca/WorldGeneration/PerlinNoise, qui a fourni une base solide pour nos tests.

## Rôle des fichiers


Voici un aperçu des fichiers présents dans ce dossier et leur rôle respectif :

- **perlinNoise.py** : Ce fichier contient le code pour tester différentes configurations de génération de cartes en utilisant le bruit Perlin. Il nous permet d'expérimenter avec divers poids pour voir comment ils affectent la topographie des mondes générés.

- **test_generated_world.py** : Ce fichier fournit des fonctions pour visualiser et tester la génération de cartes avec différents poids de terrain. Il est essentiel pour évaluer les résultats des tests effectués avec `perlinNoise.py`.

- **configureWorld.py** : Ce fichier définit les types de terrains et leurs propriétés. Il joue un rôle crucial dans la configuration des mondes que nous générons, en nous permettant de spécifier les caractéristiques de chaque type de terrain.

- **Tiles.py** : Ce fichier décrit les différents types de tuiles utilisées dans le jeu. Il est important pour la représentation visuelle des terrains et pour s'assurer que chaque type de terrain est correctement implémenté.

- **World_Drawer.py** : Ce fichier est responsable de la présentation visuelle du monde dans le jeu. Il utilise les données générées par les autres fichiers pour dessiner le monde à l'écran.

## Conclusion

L'ensemble de ces fichiers a été essentiel pour nos premiers tests. Ils nous ont permis d'explorer différentes configurations de poids et de mieux comprendre comment chaque paramètre influence la génération des mondes dans notre jeu. Grâce à ces tests, nous avons pu identifier les meilleures combinaisons pour offrir une expérience de jeu optimale.