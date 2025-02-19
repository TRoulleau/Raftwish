import pygame
from game_config import *
import math

class Torche(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, GameConfig.BAT_W, GameConfig.BAT_H)
        self.image = Torche.IMAGE
    
    def init_sprites():
        Torche.IMAGE=GameConfig.TORCHE_IMG
        
    def draw(self,window):
        window.blit(self.image, self.rect)
        
    def is_dead(self):
        return GameConfig.GRID[math.floor(self.rect[1]/50)][math.floor(self.rect[0]/50)]==0
        