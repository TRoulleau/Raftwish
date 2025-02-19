import pygame
from game_config import *
import math

class Shark():

    def __init__(self,x,y,vx,vy):

        self.rect=pygame.Rect(x,y,vx,vy)
        
        self.health=20
        self.sprite_count=0

        self.aileD=GameConfig.SHARKLR_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
        self.maskD=GameConfig.SHARKLR_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]

        self.aileG=GameConfig.SHARKRL_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
        self.maskG=GameConfig.SHARKRL_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]

        self.image=self.aileD
        self.mask=self.maskD

        self.sur_radeau=False
        self.radeau_casse=False
        self.play_sound_shark=False

        self.dead=False
        
        self.vitesse=4

        self.amplitude = 7 # Amplitude de l'ondulation
        self.frequency = 0.1 # Fréquence de l'ondulation


    def draw(self,window):
        window.blit(self.image,self.rect)
        self.sprite_count+=1
        if self.sprite_count>=GameConfig.NB_FRAMES_PER_SPRITE_PLAYER*len(GameConfig.SHARKLR_IMGS):
            self.sprite_count=0
    
    def perdre_vie(self):
        self.health-=0.5

    def is_dead(self):
        return self.health<=0 or self.dead==True

    def advance_state(self,player_x,player_y):
        # Dans une première partie, on calcule le déplacement du requin
        # Ensuite on teste s'il est sur un radeau
        #   -Si oui on enlève de la vie au radeau et on ne bouge plus le requin
        #   -Sinon on bouge le requin avec le déplacement calculé
        #   -Si le requin a déjà été en contact avec un radeau mais ne l'est plus, cela veut dire que le radeau a été cassé. On fait alors disparaitre le requin.

        # Calcul de la différence entre la position actuelle et la position du joueur
        diff_x = player_x - self.rect.centerx
        diff_y = player_y - self.rect.centery

        # Calcul de l'angle entre la position actuelle et le centre de la fenêtre
        angle = math.atan2(diff_y, diff_x)
        
        # Calcul des déplacements en fonction de l'angle
        move_x = self.vitesse * math.cos(angle)
        move_y = self.vitesse * math.sin(angle)

        # Ajout d'une ondulation à la trajectoire en fonction du temps
        wave_y = self.amplitude * math.sin(self.frequency * GameConfig.time)
        move_y += wave_y # Ajoute l'ondulation à l'axe vertical

        wave_x = (self.amplitude//2) * math.sin(self.frequency * GameConfig.time)
        move_x += wave_x # Ajoute l'ondulation à l'axe horizontal

        # Test si sur un radeau

        top_left_x = math.floor(self.rect.left/50) # Coin en haut à gauche
        top_left_y = math.floor(self.rect.top/50)

        top_right_x=math.ceil(self.rect.right/50) # Coin en haut à droite
        top_right_y=math.floor(self.rect.top/50)

        bottom_right_x = math.ceil(self.rect.right/50) # Coin en bas à droite
        bottom_right_y = math.ceil(self.rect.bottom/50)

        bottom_left_x = math.floor(self.rect.left/50) # Coin en bas à gauche
        bottom_left_y = math.ceil(self.rect.bottom/50)

        maxx=len(GameConfig.GRID[1])
        maxy=len(GameConfig.GRID)


        if (maxy>top_left_y and maxx>bottom_right_x and maxy>bottom_right_y and maxx>top_left_x and maxy>top_right_y and maxx>bottom_left_x and maxy>bottom_left_y and maxx>top_right_x):
            if GameConfig.GRID[top_left_y][top_left_x]!=0 :
                if GameConfig.GRID[top_left_y][top_left_x]["type"]=="pique":
                    self.perdre_vie()

                pos_x_radeau=top_left_x
                pos_y_radeau=top_left_y

                if not self.sur_radeau: # On indique que le requin est sur une case
                    self.sur_radeau=True
                    self.play_sound_shark=True
                else:
                    self.play_sound_shark=False

                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")>0: # Si le radeau a une vie > 0     
                    GameConfig.GRID[pos_y_radeau][pos_x_radeau]["vie"]-=0.25 # Alors on baisse la vie
                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")==0:
                    self.dead=True                    
                GameConfig.time+=1
                self.image=GameConfig.SHARKRL_HIT_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                self.mask=GameConfig.SHARKRL_HIT_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                
            elif GameConfig.GRID[bottom_right_y][bottom_right_x]!=0 :
                if GameConfig.GRID[bottom_right_y][bottom_right_x]["type"]=="pique":
                    self.perdre_vie()

                pos_x_radeau=bottom_right_x
                pos_y_radeau=bottom_right_y

                if not self.sur_radeau: # On indique que le requin est sur une case
                    self.sur_radeau=True
                    self.play_sound_shark=True
                else:
                    self.play_sound_shark=False

                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")>0: # Si le radeau a une vie > 0     
                    GameConfig.GRID[pos_y_radeau][pos_x_radeau]["vie"]-=0.25 # Alors on baisse la vie
                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")==0:
                    self.dead=True
                GameConfig.time+=1
                self.image=GameConfig.SHARKLR_HIT_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                self.mask=GameConfig.SHARKLR_HIT_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]

            elif GameConfig.GRID[top_right_y][top_right_x]!=0 :
                if GameConfig.GRID[top_right_y][top_right_x]["type"]=="pique":
                    self.perdre_vie()

                pos_x_radeau=top_right_x
                pos_y_radeau=top_right_y

                if not self.sur_radeau: # On indique que le requin est sur une case
                    self.sur_radeau=True
                    self.play_sound_shark=True
                else:
                    self.play_sound_shark=False
        
                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")>0: # Si le radeau a une vie > 0     
                    GameConfig.GRID[pos_y_radeau][pos_x_radeau]["vie"]-=0.25 # Alors on baisse la vie
                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")==0:
                    self.dead=True
                GameConfig.time+=1
                self.image=GameConfig.SHARKLR_HIT_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                self.mask=GameConfig.SHARKLR_HIT_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
            
            elif GameConfig.GRID[bottom_left_y][bottom_left_x]!=0 :
                if GameConfig.GRID[bottom_left_y][bottom_left_x]["type"]=="pique":
                    self.perdre_vie()
                pos_x_radeau=bottom_left_x
                pos_y_radeau=bottom_left_y

                if not self.sur_radeau: # On indique que le requin est sur une case
                    self.sur_radeau=True
                    self.play_sound_shark=True
                else:
                    self.play_sound_shark=False

                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")>0: # Si le radeau a une vie > 0     
                    GameConfig.GRID[pos_y_radeau][pos_x_radeau]["vie"]-=0.25 # Alors on baisse la vie
                if GameConfig.GRID[pos_y_radeau][pos_x_radeau].get("vie")==0:
                    self.dead=True
                GameConfig.time+=1
                self.image=GameConfig.SHARKRL_HIT_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                self.mask=GameConfig.SHARKRL_HIT_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]

        # Déplacement si pas sur radeau
        if not self.sur_radeau:
            if int(move_x)>=0:
                self.image=GameConfig.SHARKLR_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                self.mask=GameConfig.SHARKLR_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
            else:
                self.image=GameConfig.SHARKRL_IMGS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
                self.mask=GameConfig.SHARKRL_MASKS[self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
            GameConfig.time+=1
            self.rect=self.rect.move(int(move_x), int(move_y))