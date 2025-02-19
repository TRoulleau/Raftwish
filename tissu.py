import pygame
from game_config import *
import random

class Tissu(pygame.sprite.Sprite):
    DOWN=1
    HALO=2

    def __init__(self,x,vy):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, 0, GameConfig.BAT_W, GameConfig.BAT_H)
        self.vy=vy
        self.image = Tissu.IMAGES[Tissu.DOWN]
        self.halo = Tissu.IMAGES[Tissu.HALO]
        self.is_next_to_player=False
    
    def init_sprites():
        Tissu.IMAGES={Tissu.DOWN:GameConfig.TISSU_IMG, Tissu.HALO:GameConfig.TISSU_HALO}
            
    def advance_state(self):
        self.rect=self.rect.move(random.choice([-1,1]), self.vy*GameConfig.DT)
        
    def draw(self,window):
        if self.is_next_to_player:
            window.blit(self.halo, self.rect)
        else :
            window.blit(self.image, self.rect)
        
    def is_dead(self):
        return self.rect.top>GameConfig.WINDOW_H
        