from game_config import *
from move import *
import math

class Radeau:
    
    def place(x,y,direction):
        if math.floor(x/50)+1 != 32 :
            if direction == 1 and GameConfig.GRID[math.floor(y/50)][math.floor(x/50)+1] == 0 :   # Droite
                GameConfig.GRID[math.floor(y/50)][math.floor(x/50)+1] = {"type":"radeau","vie":100}  # On ajoute un radeau
                GameConfig.INVENTORY["radeau"] -= 1  # On enlève un radeau de l'inventaire
                GameConfig.RADEAUX += 1
                return
        if math.floor(x/50)-1 != -1 :      
            if direction == -1 and GameConfig.GRID[math.floor(y/50)][math.floor(x/50)-1] == 0 :   # Gauche
                GameConfig.GRID[math.floor(y/50)][math.floor(x/50)-1] = {"type":"radeau","vie":100}  # On ajoute un radeau
                GameConfig.INVENTORY["radeau"] -= 1  # On enlève un radeau de l'inventaire
                GameConfig.RADEAUX += 1
                return
        if math.floor(y/50)-1 != -1 :
            if direction == 2 and GameConfig.GRID[math.floor(y/50)-1][math.floor(x/50)] == 0 :   # Haut
                GameConfig.GRID[math.floor(y/50)-1][math.floor(x/50)] = {"type":"radeau","vie":100}  # On ajoute un radeau
                GameConfig.INVENTORY["radeau"] -= 1  # On enlève un radeau de l'inventaire
                GameConfig.RADEAUX += 1
                return
        if math.floor(y/50)+1 != 18 :
            if direction == 0 and GameConfig.GRID[math.floor(y/50)+1][math.floor(x/50)] == 0 :   # Bas
                GameConfig.GRID[math.floor(y/50)+1][math.floor(x/50)] = {"type":"radeau","vie":100}  # On ajoute un radeau
                GameConfig.INVENTORY["radeau"] -= 1  # On enlève un radeau de l'inventaire
                GameConfig.RADEAUX += 1
                return

    def placeVoile(x,y) :
        if GameConfig.GRID[math.floor(y/50)][math.floor(x/50)] == {"type":"radeau","vie":100} :
            GameConfig.GRID[math.floor(y/50)][math.floor(x/50)] = {"type":"voile","vie":100}
            GameConfig.INVENTORY["voile"] -= 1
            GameConfig.TIME_ACCELERATION += 0.05
            GameConfig.NB_VOILES += 1
            GameConfig.VOILES+=1
            return
    
    def placeFilet(x,y) :
        if GameConfig.GRID[math.floor(y/50)][math.floor(x/50)] == {"type":"radeau","vie":100} :
            GameConfig.GRID[math.floor(y/50)][math.floor(x/50)] = {"type":"filet","vie":100}
            GameConfig.INVENTORY["filet"] -= 1
            GameConfig.FILETS += 1
            return
    
    def placePique(x,y) :
        if GameConfig.GRID[math.floor(y/50)][math.floor(x/50)] == {"type":"radeau","vie":100} :
            GameConfig.GRID[math.floor(y/50)][math.floor(x/50)] = {"type":"pique","vie":100}
            GameConfig.INVENTORY["pique"] -= 1
            GameConfig.PIQUES += 1
            return




