Bienvenue dans "Rise of Heroes", un jeu de stratégie 2D où des unités variées s'affrontent sur une carte générée aléatoirement. Ce document décrit le fonctionnement général du projet.

- ## **Structure du Projet:**  
Voici les principaux fichiers et leur rôle dans le projet:
1. `game.py`: contient la logique principale du jeu, y compris les mécanismes de déplacement, d'attaque et les tours des joueurs.
2. `unit.py`: définit les différentes unités (Archer, Mage, Géant, Bomber) et leurs compétences uniques.
3. `Tiles.py`: décrit les différents types de tuiles (eau, herbe, roche, sable, etc.) utilisées pour la carte.
4. `constante.py`: contient toutes les constantes utilisées dans le projet (tailles des cellules, couleurs, etc.)
5. `world.py`: implémente la génération procédurale de cartes à l'aide du bruit Perlin et associe les types de tuiles aux terrains.
6. `GameLog.py`: gère l'affichage des messages du journal de jeu, comme les mouvements, attaques et évènements importants.
7. `configureWorld.py`: définit les types de terrains et leurs propriétés pour la carte.
8. `perlinNoise.py`: teste différentes combinaisons de cartes en ajustant les paramètres de la génération procédurale.
9. `test_generated_world.py`: fournit des fonctions pour visualiser et tester la génération de cartes avec différents poids de terrain.
10. `World_Drawer.py`: s'occupe de la présentation visuelle du monde.
11. `menu.py`: s'occupe de l'interaction avec le joueur en dehors des mécaniques principales de gameplay.
    
- ## **Fonctionnalités:** 
1. #### **Déplacement et Combat:**
Les unités peuvent se déplacer sur une grille et attaquer en fonction de leurs portées et compétences spécifiques. À chaque tour, le joueur peut déplacer son unité et/ou exécuter une compétence. Une unité ne peut attaquer qu'à condition qu'un ennemi soit situé dans sa ligne de vue (sans obstacle bloquant) et dans la portée d'attaque de la compétence utilisée.

2. #### **Carte Générée Procéduralement:** 
Les cartes sont générées aléatoirement avec différents types de terrains, influencés par des poids configurables.

3. #### **Types de Héros:**  
**Archer**: Attaque à distance avec des flèches normales et enflammées. La flèche normale a une probabilité de Headshot (mort instantanée) de 10%.  
**Mage**: Peut marcher sur l'eau, soigner des alliés, et lancer des potions magiques.  
**Géant**: Inflige des dégâts importants avec des coups de poing ou des "stomps".  
**Bomber**: Lance une bombe ou sacrifie sa vie pour infliger des dégâts massifs en explosant.  

4. #### **Objets collectables**
Deux types de potions (jaunes et bleues) apparaissent aléatoirement sur la Map au cours du jeu et apparaissent aléatoirement sur la carte au cours du jeu et produisent un effet sur l'unité qui les récupère, pour une durée d’un tour.
**Potion Jaune**: Augmente temporairement le pouvoir dattaque de l'unitéAugmente temporairement la vitesse de déplacement de l'unité.
