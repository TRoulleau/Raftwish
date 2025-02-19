import pygame
from game_config import *
from radeau import *

class Player(pygame.sprite.Sprite):
  LEFT=-1
  RIGHT=1
  NONE=0
  TOP=2
  def __init__(self,x,y):
    self.rect=pygame.Rect(x,y,GameConfig.PLAYER_W,GameConfig.PLAYER_H)
    self.vx=0
    self.vy=0
    self.sprite_count=0
    self.direction=Player.NONE
    self.helpCraft=-1
    self.lance_tier=0
    self.rod_tier=0
    self.poser_torche=False
    self.ENDED=False
    
    self.image=Player.IMAGES[self.direction][self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
    self.mask=Player.MASKS[self.direction][self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
  
  def init_sprites():
    Player.IMAGES={Player.LEFT:GameConfig.WALKING_LEFT_IMGS,Player.RIGHT:GameConfig.WALKING_RIGHT_IMGS,Player.NONE:GameConfig.STANDING_IMGS,Player.TOP:GameConfig.WALKING_TOP_IMGS}
    Player.MASKS={Player.LEFT:GameConfig.WALKING_LEFT_MASKS,Player.RIGHT:GameConfig.WALKING_RIGHT_MASKS,Player.NONE:GameConfig.STANDING_MASKS,Player.TOP:GameConfig.TOP_MASKS}
  
  def draw(self,window):
    if self.vx==0 and self.vy==0:
      self.sprite_count=0
    window.blit(self.image,self.rect.topleft)

  
  def advance_state(self,next_move):
    fx=0
    fy=0
    if self.ENDED!=True:
      if next_move.left:
        fx=GameConfig.FORCE_LEFT
        get_next_caseJ=math.floor(((self.rect.left+self.vx*GameConfig.DT)-5)/50)
        get_next_caseTOPI=math.floor((self.rect.topleft[1]+5)/50)
        get_next_caseBOTTOMI=math.floor((self.rect.bottomleft[1])/50)
        if GameConfig.GRID[get_next_caseTOPI][get_next_caseJ]==0 or GameConfig.GRID[get_next_caseBOTTOMI][get_next_caseJ]==0:
          fx=0
        self.direction=Player.LEFT
        
      if next_move.right:
        fx=GameConfig.FORCE_RIGHT
        get_next_caseJ=math.floor((self.rect.right+self.vx*GameConfig.DT)/50)
        get_next_caseTOPI=math.floor((self.rect.topright[1]+5)/50)
        get_next_caseBOTTOMI=math.floor((self.rect.bottomright[1])/50)
        if get_next_caseJ>31:
          fx=0
        else:
          if GameConfig.GRID[get_next_caseTOPI][get_next_caseJ]==0 or GameConfig.GRID[get_next_caseBOTTOMI][get_next_caseJ]==0:
            fx=0
        self.direction=Player.RIGHT
      if next_move.up:
        fy=GameConfig.FORCE_UP
        get_next_caseI=math.floor(((self.rect.top+self.vy*GameConfig.DT))/50)
        get_next_caseLEFTJ=math.floor((self.rect.topleft[0])/50)
        get_next_caseRIGHTJ=math.floor((self.rect.topright[0]-1)/50)
        if GameConfig.GRID[get_next_caseI][get_next_caseLEFTJ]==0 or GameConfig.GRID[get_next_caseI][get_next_caseRIGHTJ]==0:
          fy=0
        self.direction=Player.TOP
      if next_move.down:
        fy=GameConfig.FORCE_DOWN
        get_next_caseI=math.floor(((self.rect.bottom+self.vy*GameConfig.DT)+5)/50)
        get_next_caseLEFTJ=math.floor((self.rect.bottomleft[0])/50)
        get_next_caseRIGHTJ=math.floor((self.rect.bottomright[0]-1)/50)
        if get_next_caseI>17:
          fy=0
        else:
          if GameConfig.GRID[get_next_caseI][get_next_caseLEFTJ]==0 or GameConfig.GRID[get_next_caseI][get_next_caseRIGHTJ]==0:
            fy=0
        self.direction=Player.NONE
      
      # Partie placement des radeaux et torches :
      
      if GameConfig.INDICE_OBJET == 6:
        if next_move.right_click :
          if GameConfig.INVENTORY["radeau"] != 0 :
            Radeau.place(self.rect.center[0],self.rect.center[1],self.direction)
      if GameConfig.INDICE_OBJET == 7:
        if next_move.right_click :
          if GameConfig.INVENTORY["voile"] != 0 :
            Radeau.placeVoile(self.rect.center[0],self.rect.center[1])
      if GameConfig.INDICE_OBJET == 8:
        if next_move.right_click :
          if GameConfig.INVENTORY["pique"] != 0 :
            Radeau.placePique(self.rect.center[0],self.rect.center[1])
      if GameConfig.INDICE_OBJET == 9:
        if next_move.right_click :
          if GameConfig.INVENTORY["filet"] != 0 :
            Radeau.placeFilet(self.rect.center[0],self.rect.center[1])
      if GameConfig.INDICE_OBJET == 10:
        if next_move.right_click :
          if GameConfig.INVENTORY["torche"] != 0 :
            self.poser_torche=True
            GameConfig.INVENTORY["torche"]-=1

      # Partie scroll :
      
      if next_move.scroll_up:
        GameConfig.INDICE_OBJET = (GameConfig.INDICE_OBJET + 1) % 11
      if next_move.scroll_down:
        GameConfig.INDICE_OBJET = (GameConfig.INDICE_OBJET - 1) % 11

      if next_move.left_click:
        for i in range(len(GameConfig.CRAFT_RECTs)):
          if GameConfig.CRAFT_RECTs[i].collidepoint(next_move.pos):
            self.craft(i)

      self.vx=fx*GameConfig.DT
      self.vy=fy*GameConfig.DT
      x,y=self.rect.topleft
      vx_min=-x/GameConfig.DT
      vx_max=(GameConfig.WINDOW_W-GameConfig.PLAYER_W-x)/GameConfig.DT
      self.vx=min(self.vx,vx_max)
      self.vx=max(self.vx,vx_min)

      vy_min=-y/GameConfig.DT
      vy_max=(GameConfig.WINDOW_H-GameConfig.PLAYER_H-y)/GameConfig.DT
      self.vy=min(self.vy,vy_max)
      self.vy=max(self.vy,vy_min)
      self.rect=self.rect.move(self.vx*GameConfig.DT,self.vy*GameConfig.DT)
      self.sprite_count+=1
      if self.sprite_count>=GameConfig.NB_FRAMES_PER_SPRITE_PLAYER*len(Player.IMAGES[self.direction]):
        self.sprite_count=0
      self.image=Player.IMAGES[self.direction][self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
      self.mask=Player.MASKS[self.direction][self.sprite_count//GameConfig.NB_FRAMES_PER_SPRITE_PLAYER]
      

  def craft(self, idx):
    if idx==0 and self.lance_tier==0 and GameConfig.INVENTORY["baton"]>=2 and GameConfig.INVENTORY["corde"]>=1:
      GameConfig.INVENTORY["baton"]-=2
      GameConfig.INVENTORY["corde"]-=1
      self.lance_tier+=1
    elif idx==0 and self.lance_tier==1 and GameConfig.INVENTORY["baton"]>=4 and GameConfig.INVENTORY["corde"]>=2 and GameConfig.INVENTORY["tissu"]>=1:
      GameConfig.INVENTORY["baton"]-=4
      GameConfig.INVENTORY["corde"]-=2
      GameConfig.INVENTORY["tissu"]-=1
      self.lance_tier+=1
    elif idx==0 and self.lance_tier==2 and GameConfig.INVENTORY["baton"]>=4 and GameConfig.INVENTORY["corde"]>=3 and GameConfig.INVENTORY["tissu"]>=2 and GameConfig.INVENTORY["silex"]>=1:
      GameConfig.INVENTORY["baton"]-=4
      GameConfig.INVENTORY["corde"]-=3
      GameConfig.INVENTORY["tissu"]-=2
      GameConfig.INVENTORY["silex"]-=1
      self.lance_tier+=1
    elif idx==0 and self.lance_tier==3 and GameConfig.INVENTORY["baton"]>=4 and GameConfig.INVENTORY["corde"]>=4 and GameConfig.INVENTORY["tissu"]>=4 and GameConfig.INVENTORY["silex"]>=3:
      GameConfig.INVENTORY["baton"]-=4
      GameConfig.INVENTORY["corde"]-=4
      GameConfig.INVENTORY["tissu"]-=4
      GameConfig.INVENTORY["silex"]-=3
      self.lance_tier+=1
    
    if idx==1 and self.rod_tier==0 and GameConfig.INVENTORY["baton"]>=2 and GameConfig.INVENTORY["corde"]>=1:
      GameConfig.INVENTORY["baton"]-=2
      GameConfig.INVENTORY["corde"]-=1
      self.rod_tier+=1
    elif idx==1 and self.rod_tier==1 and GameConfig.INVENTORY["baton"]>=4 and GameConfig.INVENTORY["corde"]>=2 and GameConfig.INVENTORY["tissu"]>=1:
      GameConfig.INVENTORY["baton"]-=4
      GameConfig.INVENTORY["corde"]-=2
      GameConfig.INVENTORY["tissu"]-=1
      self.rod_tier+=1
    elif idx==1 and self.rod_tier==2 and GameConfig.INVENTORY["baton"]>=4 and GameConfig.INVENTORY["corde"]>=3 and GameConfig.INVENTORY["tissu"]>=2:
      GameConfig.INVENTORY["baton"]-=4
      GameConfig.INVENTORY["corde"]-=3
      GameConfig.INVENTORY["tissu"]-=2
      self.rod_tier+=1
    elif idx==1 and self.rod_tier==3 and GameConfig.INVENTORY["baton"]>=4 and GameConfig.INVENTORY["corde"]>=4 and GameConfig.INVENTORY["tissu"]>=4:
      GameConfig.INVENTORY["baton"]-=4
      GameConfig.INVENTORY["corde"]-=4
      GameConfig.INVENTORY["tissu"]-=4
      self.rod_tier+=1

    if idx==6 and GameConfig.INVENTORY["baton"]>=5:
      GameConfig.INVENTORY["baton"]-=5
      GameConfig.INVENTORY["radeau"]+=1

    if idx==7 and GameConfig.INVENTORY["baton"]>=3 and GameConfig.INVENTORY["tissu"]>=6 and GameConfig.INVENTORY["corde"]>=2:
      GameConfig.INVENTORY["baton"]-=3
      GameConfig.INVENTORY["tissu"]-=6
      GameConfig.INVENTORY["corde"]-=2
      GameConfig.INVENTORY["voile"]+=1

    if idx==8 and GameConfig.INVENTORY["baton"]>=6 and GameConfig.INVENTORY["corde"]>=3 and GameConfig.INVENTORY["silex"]>=2:
      GameConfig.INVENTORY["baton"]-=6
      GameConfig.INVENTORY["corde"]-=3
      GameConfig.INVENTORY["silex"]-=2
      GameConfig.INVENTORY["pique"]+=1

    if idx==9 and GameConfig.INVENTORY["baton"]>=2 and GameConfig.INVENTORY["corde"]>=5:
      GameConfig.INVENTORY["baton"]-=2
      GameConfig.INVENTORY["corde"]-=5
      GameConfig.INVENTORY["filet"]+=1

    if idx==10 and GameConfig.INVENTORY["baton"]>=2 and GameConfig.INVENTORY["silex"]>=2:
      GameConfig.INVENTORY["baton"]-=2
      GameConfig.INVENTORY["silex"]-=2
      GameConfig.INVENTORY["torche"]+=1