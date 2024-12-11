# Rise of Heroes - Documentation

Pour commencer, installez perlin-noise avec pip :

```bash
pip install perlin-noise
```

Bienvenue dans "Rise of Heroes", un jeu de stratégie 2D où des unités variées s'affrontent sur une carte générée aléatoirement. Ce document décrit le fonctionnement général du projet.

## Structure du Projet

Voici les principaux fichiers et leur rôle dans le projet:

- `game.py`: contient la logique principale du jeu, y compris les mécanismes de déplacement, d'attaque et les tours des joueurs.
- `unit.py`: définit les différentes unités (Archer, Mage, Géant, Bomber) et leurs compétences uniques.
- `Tiles.py`: décrit les différents types de tuiles (eau, herbe, roche, sable, etc.) utilisées pour la carte.
- `constante.py`: contient toutes les constantes utilisées dans le projet (tailles des cellules, couleurs, etc.)
- `world.py`: implémente la génération procédurale de cartes à l'aide du bruit Perlin et associe les types de tuiles aux terrains.
- `GameLog.py`: gère l'affichage des messages du journal de jeu, comme les mouvements, attaques et évènements importants.
- `configureWorld.py`: définit les types de terrains et leurs propriétés pour la carte.
- `perlinNoise.py`: teste différentes combinaisons de cartes en ajustant les paramètres de la génération procédurale.
- `test_generated_world.py`: fournit des fonctions pour visualiser et tester la génération de cartes avec différents poids de terrain.
- `World_Drawer.py`: s'occupe de la présentation visuelle du monde.
- `menu.py`: s'occupe de l'interaction avec le joueur en dehors des mécaniques principales de gameplay.

## Fonctionnalités

### Déplacement et Combat

Les unités peuvent se déplacer sur une grille et attaquer en fonction de leurs portées et compétences spécifiques.

### Carte Générée Procéduralement

Les cartes sont générées aléatoirement avec différents types de terrains, influencés par des poids configurables.

### Types de Héros

- **Archer**: Attaque à distance avec des flèches normales et enflammées. La flèche normale a une probabilité de Headshot (mort instantanée) de 4%.
- **Mage**: Peut marcher sur l'eau, soigner des alliés, et lancer des potions magiques.
- **Géant**: Inflige des dégâts importants avec des coups de poing ou des "stomps".
- **Bomber**: Lance une bombe ou sacrifie sa vie pour infliger des dégâts massifs en explosant.
