# Documentation de la Classe `Game`

## 1. **Initialisation de la Partie**

### **Méthodes impliquées :**
- `__init__(self, ...)`
  
### **Rôle :**
La méthode d'initialisation de la classe `Game` sert à configurer les éléments essentiels pour le déroulement du jeu, comme les paramètres de la carte, les unités, les joueurs, et autres éléments associés.

### **Détails :**
- Elle initialise les instances importantes comme la carte (`Map_Aleatoire`), les unités et les journaux d'événements (`GameLog`).
- Crée la liste des unités pour chaque joueur et configure les tuiles nécessaires pour l'apparition.

---

## 2. **Apparition des Unités**

### **Méthodes impliquées :**
1. `initialize_walkable_tiles(self)`
2. `get_spawn_sector(self, ...)`
3. `find_spawn_locations(self, ...)`
4. `spawn_units(self, ...)`

### **Rôle :**
Ces méthodes assurent la configuration des positions initiales où les unités peuvent apparaître, et les placent effectivement sur la carte.

### **Détails des Méthodes :**
- **`initialize_walkable_tiles(self)` :**  
  Identifie toutes les tuiles où une unité peut se déplacer (tuiles `Walkable`), et les stocke pour référence.

- **`get_spawn_sector(self, team)` :**  
  Retourne un secteur spécifique de la carte pour chaque équipe. Par exemple, les équipes pourraient apparaître dans des zones opposées.

- **`find_spawn_locations(self, sector, num_units)` :**  
  Recherche et retourne des emplacements valides dans le secteur défini pour positionner un nombre donné d'unités.

- **`spawn_units(self, units, spawn_locations)` :**  
  Place les unités fournies sur les emplacements valides trouvés précédemment.

### **Interaction entre les Méthodes :**
1. **`initialize_walkable_tiles`** prépare les tuiles accessibles.
2. **`get_spawn_sector`** définit la zone spécifique d'apparition.
3. **`find_spawn_locations`** trouve les tuiles valides dans cette zone.
4. **`spawn_units`** utilise ces tuiles pour placer les unités.

---

## 3. **Gestion des Mouvements**

### **Méthodes impliquées :**
1. `move_unit(self, unit, new_x, new_y)`

### **Rôle :**
Cette méthode permet de déplacer une unité vers une nouvelle position sur la carte.

### **Détails :**
- Vérifie si la position cible est valide (accessible et libre).
- Met à jour les coordonnées de l'unité.

### **Interaction :**
Cette méthode utilise les informations des tuiles walkables pour s'assurer que les déplacements sont autorisés.

---

## 4. **Gestion des Attaques**

### **Méthodes impliquées :**
1. `attack_unit(self, attacker, target)`

### **Rôle :**
Gère les attaques entre deux unités.

### **Détails :**
- Applique les dégâts en prenant en compte la puissance d'attaque et la défense.
- Met à jour la santé de la cible et vérifie si elle est éliminée.

### **Interaction :**
- Utilise les statistiques des unités (`health`, `attack_power`, `defense`).
- Peut également interagir avec le journal (`GameLog`) pour enregistrer les événements d'attaque.

---

## 5. **Gestion des Effets et Objets Collectables**

### **Méthodes impliquées :**
1. `apply_collectible_effect(self, unit, collectible)`

### **Rôle :**
Applique l'effet d'un objet collectable à une unité.

### **Détails :**
- Appelle la méthode `apply()` de l'objet `Effect` lié à `CollectibleItem`.
- Met à jour les attributs de l'unité (ex : vitesse, attaque, etc.).

### **Interaction :**
- Utilise `CollectibleItem` et `Effect`.
- Enregistre l'événement dans le `GameLog`.

---

## 6. **Suivi et Affichage des Événements**

### **Méthodes impliquées :**
1. `log_event(self, message, type)`

### **Rôle :**
Ajoute un message dans le journal des événements (`GameLog`).

### **Détails :**
- Permet de suivre les actions importantes du jeu, comme les déplacements, attaques ou collecte d’objets.

---

## 7. **Gestion de la Fin du Jeu**

### **Méthodes impliquées :**
1. `check_game_over(self)`

### **Rôle :**
Vérifie si les conditions de fin de partie sont remplies.

### **Détails :**
- Évalue si une équipe n'a plus d'unités en vie.
- Déclare la partie terminée et indique le vainqueur.

---

## Conclusion  

La classe `Game` est le cœur de la logique du jeu. Elle orchestre l'initialisation des unités, les déplacements, les interactions avec les tuiles et objets, tout en assurant un suivi des événements. Les méthodes sont organisées en groupes fonctionnels pour faciliter la gestion de chaque aspect du jeu :  
1. **Initialisation des données**  
2. **Placement et gestion des unités**  
3. **Contrôle des actions et interactions**  
4. **Suivi des événements**  
5. **Détermination des conditions de victoire**  

Chaque méthode contribue à un aspect particulier du jeu et interagit avec les autres pour assurer un déroulement fluide et cohérent.
