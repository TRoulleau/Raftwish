import pygame
from game_config import *
import random

class Baton(pygame.sprite.Sprite):
    DOWN=1
    HALO=2

    def __init__(self,x,vy):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, 0, GameConfig.BAT_W, GameConfig.BAT_H)
        self.vy=vy
        self.image = Baton.IMAGES[Baton.DOWN]
        self.halo = Baton.IMAGES[Baton.HALO]
        self.is_next_to_player=False
    
    def init_sprites():
        Baton.IMAGES={Baton.DOWN:GameConfig.BATON_IMG, Baton.HALO:GameConfig.BATON_HALO}
            
    def advance_state(self):
        self.rect=self.rect.move(random.choice([-1,1]), self.vy*GameConfig.DT)
        
    def draw(self,window):
        if self.is_next_to_player:
            window.blit(self.halo, self.rect)
        else :
            window.blit(self.image, self.rect)
        
    def is_dead(self):
        return self.rect.top>GameConfig.WINDOW_H
        