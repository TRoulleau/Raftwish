<h1 style="color: #5e9ca0; text-align: center;"><span style="color: #2b2301;">Welcome to </span>Epy Games!</h1>
<p align="center">
  <img width="20%" src="https://i.postimg.cc/PJzTR1T3/epic.png" alt="Logo Epy Games"/>
</p>

---

## ℹ Description

Epy Games est un studio amateur de jeux vidéos né de la fusion entre le célèbre éditeur "Epic Games" et bien sûr l'épy(game) de blé.

---

## ✅ Informations

Pour jouer à notre jeu RaftWish, il suffit de télécharger le repository "Raftwish" et de lancer le fichier "game.py" avec Python3 (avoir pygame d'installé). Le jeu se joue clavier / manette Xbox + souris.

---

## 👤 Répartition des tâches

| Membre     | Rôle          |
| ---------- | ------------- |
| Gabriel S. | Chef du studio |
| Tom. R     | Développeur |
| Elouan. R  | Développeur |
| Gabriel. L | Développeur |
| Loan. R    | Développeur |

---

## 📆 Journal de développement

### Séance du 16/11/2023

- Création d'un espace GitLab.
- Familiarisation avec l'outil Git.
- Décision d'une idée de jeu.
- Création d'une liste "fourre-tout" pour proposer un maximum d'idées à ajouter au jeu qui seront développées au fur et à mesure.
- Premiers pseudos-codes pour poser le fonctionnement et les bases des fonctions élémentaires du jeu.

### Séance du 24/11/2023

- Création d'un personnage temporaire avec des textures lui permettant de regarder dans 4 directions (H,D,B,G).
- Création d'une texture de radeau temporaire pour tester visuellement les bordures.
- Création d'un tableau de tableaux remplis de 0 formant une matrice de 32 de largeur et 18 de hauteur.
- Les 4 cases centrales sont définies à 1 pour représenter le radeau de départ.
- Affichage du "plateau de jeu" dans la fonction `draw` de la classe **GameState**. Une texture (qui changera plus tard) est dessinée là où doit se trouver un radeau tel que :

```
Si tab[j][i] = 1 :
  Image de radeau dessinée aux coordonnées (i*50, j*50)
```

- Ajout des mouvements du personnage.
- Ajout d'un test dans la fonction `advance_state` de la classe **Player** pour annuler le mouvement si le mouvement du joueur l'emmène hors du radeau.
- Planification des classes qui seront nécessaires en pseudo code.
- Recherche / création de meilleures textures.
- Reflexion sur les fonctionnalités qui rendront le jeu vivant.
  <img width="50%" src="https://i.postimg.cc/XYPdQ1rH/Capture-d-cran-2023-11-27-222106.png" alt="Capture d'écran du jeu en V0.2"/>

### Séance du 28/11/2023

- Ajout d'un chrono qui fait passer 18 heures dans le jeu en 20 minutes dans la vraie vie (durée d'une partie sujette à changement).
  - Permet de visualiser l'avancement du jeu.
  - Servira pour l'augmentation de la difficulté en fonction du temps ainsi que la fin du jeu.
  - Servira pour le cycle jour/nuit.
- Affichage de ce chrono et stockage du temps passé dans un attribut de la classe **GameState**.
- Ajout du système de pose d'un nouveau radeau :
  - Le radeau est posé lorsque le joueur effectue un clic gauche.
  - Le radeau est posé sur la première case vide rencontrée en fonction de la direction actuelle du joueur.
  - Ce système sera ensuite relié au système d'inventaire et un radeau ne sera posé que si le joueur possède et équipe le radeau "dans sa main".
  - Problème à régler : l'event du clic se déclenche plusieurs fois par secondes et il est donc difficile de poser un radeau.
- Création d'un premier requin se dirigeant toujours vers le centre du jeu et dessinant une courbe sinusoïdale pour imiter la nage.
- Finalisation de l'animation du radeau pour donner une impression de mouvement.
- Tests pour animer l'eau.
- Développement du script permettant la génération et le mouvement aléatoire d'objets.
  - Création de la classe Bâton.
  - Tous les objets dériveront de la même manière, ainsi, ce script nous servira de base pour tous les débris.

### Séance du 5/12/2023
  - Ajout inventaire et son affichage pour les 5 premiers items
  - Ajout classe baton
  - Changement des touches de déplacement : z,q,s,d
  - Les radeaux ne sont plus représentés par 1 dans la matrice mais par un dictionnaire (caractéristiques : type et vie)
  - Ajout variable indiceObjet + son utilisation pour placer des radeaux
  - Baton dessiné derrière les radeaux
  - Le scroll change l'indice sélectionné
  - Changement de la détection des input
  - Possibilité d'actionner 2 touches en meme temps (aller en diagonale, poser en marchant)
  - Ajout du menu du jeu

### Séance du 7/12/2023
  - Correction et ajouts d'objets
  - Mise à jour de la hotbar
  - Fonction d'amélioration du radeau par Rouillard Elouan.
  - Ajout de la récupération d'objets
  - Hotbar fonctionnelle

### En décembre 2023
  - Ajout de la gestion du son
  - Ajout de notifications de connexion/déconnexion de la manette
  - Ajout d'une page d'aide aux ressources premières et d'amélioration des outils
  - Ajout des requins
  - Corrections de fautes d'orthographe
  - Ajout d'une icône de craft (OK/NOK) + correction de bug de pose du radeau
  - Réutilisation de pygame.quit() plutôt que sys.exit()
  - Ajout de l'halo de récupération des items
  - Ajout de la possibilité de passer en plein écran
  - Optimisation grâce au .convert_alpha()

### En janvier 2024
  - Ajout de sons pour les coups et mort des requins
  - Correction de la force de la vague
  - Suppression du module tkinter pour éviter un crash sur Ubuntu
  - Modifications au démarrage donc un écran de chargement
  - Correction d'importations pour l'apparence du joueur
  - Nouveaux sprites pour le requin et animations
  - Correction de divers bugs dans le menu pause et la gestion du curseur
  - Ajout de sons pour la connexion/déconnexion de la manette et pause des sons dans le menu pause
  - Ajout de musiques dans le menu et le jeu
  - Ajout d'animation pour la mort
  - Ajout de fonctionnalités telles que la torche et des améliorations d'outils
  - Ajout d'un écran de fin avec un bouton pour retourner au menu principal et la possibilité de voir ses stats
  - Ajout d'une fonctionnalité de récupération d'items par le filet 
  - Correction de problèmes liés aux bords de la carte
  - Ajout du cycle jour/nuit
  - Nettoyage du code

---

Bon jeu !
