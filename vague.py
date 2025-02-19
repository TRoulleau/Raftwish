import pygame
from game_config import *
import random

class Vague(pygame.sprite.Sprite):

    def __init__(self,x,vy):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,-200, GameConfig.VAGUE_W, GameConfig.VAGUE_H)
        self.vy=vy
        self.lastupdatevague=pygame.time.get_ticks()
        self.image = Vague.IMAGES[GameConfig.IMAGE]
    
    def init_sprites():
        Vague.IMAGES={1:GameConfig.VAGUE_IMG1, 2:GameConfig.VAGUE_IMG2, 3:GameConfig.VAGUE_IMG3, 4:GameConfig.VAGUE_IMG4, 5:GameConfig.VAGUE_IMG5}
            
    def advance_state(self):
        self.currenttime=pygame.time.get_ticks()
        self.rect=self.rect.move(random.choice([-1,1]), self.vy*GameConfig.DT)
        if self.currenttime-self.lastupdatevague>=GameConfig.cooldownvague:
            GameConfig.IMAGE=((GameConfig.IMAGE)%5)+1
            self.image = Vague.IMAGES[GameConfig.IMAGE]
            self.lastupdatevague=pygame.time.get_ticks()
            
    def draw(self,window):
        window.blit(self.image, self.rect)
        
    def is_dead(self):
        return self.rect.top>GameConfig.WINDOW_H
        