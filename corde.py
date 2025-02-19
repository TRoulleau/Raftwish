import pygame
from game_config import *
import random

class Corde(pygame.sprite.Sprite):
    DOWN=1
    HALO=2

    def __init__(self,x,vy):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, 0, GameConfig.BAT_W, GameConfig.BAT_H)
        self.vy=vy
        self.image = Corde.IMAGES[Corde.DOWN]
        self.halo = Corde.IMAGES[Corde.HALO]
        self.is_next_to_player=False
    
    def init_sprites():
        Corde.IMAGES={Corde.DOWN:GameConfig.CORDE_IMG, Corde.HALO:GameConfig.CORDE_HALO}
            
    def advance_state(self):
        self.rect=self.rect.move(random.choice([-1,1]), self.vy*GameConfig.DT)
        
    def draw(self,window):
        if self.is_next_to_player:
            window.blit(self.halo, self.rect)
        else :
            window.blit(self.image, self.rect)
        
    def is_dead(self):
        return self.rect.top>GameConfig.WINDOW_H
        