#ce code est pour tester les differents maps possible pour savoir quelle sera la bonne combinaiason pour notre jeu
from test_generated_world import test_generate_world , test_emerge



# Définition des poids pour différents types de mondes :
WEIGHTS1 = [70, 10, 10, 10, 10, 10, 10]      # Poids pour générer des îles
WEIGHTS2 = [10, 30, 40, 10, 10, 10, 10]     # Poids pour un autre type de monde
WEIGHTS3 = [10, 15, 15, 15, 50, 15, 45]     # Poids pour générer des lacs


# Appels de la fonction de génération de monde avec différents poids et graines aléatoires
# toucher E pour passer entre les differents mondes
test_generate_world(WEIGHTS1, random_seed = 21)
test_generate_world(WEIGHTS1, random_seed = 258)
test_generate_world(WEIGHTS2, random_seed = 7)
test_generate_world(WEIGHTS2, random_seed = 8)
test_generate_world(WEIGHTS3, random_seed = 16)
test_generate_world(WEIGHTS3, random_seed = 14)

"""
test_emerge(WEIGHTS1, random_seed = 21)
test_emerge(WEIGHTS1, random_seed = 7)
test_emerge(WEIGHTS1, random_seed = 16)
test_emerge(WEIGHTS1, random_seed = 28)
test_emerge(WEIGHTS1, random_seed = 8)
test_emerge(WEIGHTS1, random_seed = 14)
"""