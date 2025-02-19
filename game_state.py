import pygame
import time
import math
from game_config import *
from player import *
from random import *
from baton import *
from corde import *
from tissu import *
from shark import *
from vague import *
from torche import *

class GameState:

  # Initialisation des timers et des listes contenant les objets
  
  def __init__(self):
    self.player=Player(780,425)
    self.batons = []
    self.cordes = []
    self.tissus = []
    self.vagues = []
    self.torches = []
    self.current_alpha = 0
    self.time_till_new_baton = GameConfig.TICKS_BETWEEN_BATONS
    self.time_till_new_corde = GameConfig.TICKS_BETWEEN_CORDES
    self.time_till_new_tissu = GameConfig.TICKS_BETWEEN_TISSUS
    self.time_till_new_vague = GameConfig.TICKS_BETWEEN_VAGUES
    self.sharks = []
    self.time_till_new_sharks = GameConfig.TICKS_FIRST_SHARKS
    self.ENDED = False
    self.TEMPS_ECOULE = False
    self.MORT= False
    self.animation = True
    self.lastupdatetr=pygame.time.get_ticks()
    self.LAST_UPDATE_TIME = time.time()
    self.ACCELERATED_TIME = 0

  def newShark(self):
    face=randint(1,4)
    if face==1:
      pos_x=randint(0,GameConfig.WINDOW_W)
      pos_y=0
    elif face==2:
      pos_x=randint(0,GameConfig.WINDOW_H)
      pos_y=GameConfig.WINDOW_H
    elif face==3:
      pos_x=0
      pos_y=randint(0,GameConfig.WINDOW_H)
    elif face==4:
      pos_x=GameConfig.WINDOW_W
      pos_y=randint(0,GameConfig.WINDOW_W)

    s=Shark(pos_x,pos_y,randint(5,15)*choice([-1,1]),randint(5,15)*choice([-1,1]))

    return s

  # Gestion des affichages de textes
  def display_message(window,text,font_size,x,y,position,color):
    img = GameConfig.FONT60.render(text,True,color)
    if font_size==18:
      img = GameConfig.FONT18.render(text,True,color)
    elif font_size==22:
      img = GameConfig.FONT22.render(text,True,color)
    display_rect=img.get_rect()
    display_rect.center=(x,y)
    if position=="top_right":
      display_rect.topright=(x,y)
    elif position=="top_left":
      display_rect.topleft=(x,y)
    window.blit(img,display_rect)
    
  # Affichage des différentes couches : fond, objets, radeaux, joueur, voiles, requins, temps, interface
  def draw(self,window):
    window.blit(GameConfig.BACKGROUND_IMG,(0,GameConfig.bgy-885))
    GameConfig.bgy+=2
    window.blit(GameConfig.BACKGROUND_IMG,(0,GameConfig.bgy))
    if GameConfig.bgy>885:
        GameConfig.bgy=0
    currenttime=pygame.time.get_ticks()
    for b in self.batons:
      b.draw(window)
    for c in self.cordes:
      c.draw(window)
    for t in self.tissus:
      t.draw(window)
    for i in range(32):
      for j in range(18):
        if GameConfig.GRID[j][i]!=0:
          window.blit(GameConfig.TRAINEELIST[GameConfig.IMAGE2],((i)*50,(j+1)*50-9))
          if currenttime-self.lastupdatetr>=GameConfig.cooldowntrainee:                        
            GameConfig.IMAGE2=((GameConfig.IMAGE2+1)%4)+1                                      
            self.lastupdatetr=pygame.time.get_ticks()      
          if GameConfig.GRID[j][i]["type"]=="radeau":
            if GameConfig.GRID[j][i]["vie"]>0:
              if GameConfig.GRID[j][i]["vie"]==100:
                window.blit(GameConfig.RADEAU_IMG,(i*50,j*50))
              else:
                window.blit(GameConfig.RADEAU_DAMAGED_IMG,(i*50,j*50))
            else:
              GameConfig.GRID[j][i]=0
              GameConfig.RADEAUX_DETRUITS += 1
          elif GameConfig.GRID[j][i]["type"]=="voile":
            if GameConfig.GRID[j][i]["vie"]>0:
              if GameConfig.GRID[j][i]["vie"]==100:
                window.blit(GameConfig.RADEAU_IMG,(i*50,j*50))
              else:
                window.blit(GameConfig.RADEAU_DAMAGED_IMG,(i*50,j*50))
            else:
              GameConfig.GRID[j][i]=0
              GameConfig.RADEAUX_DETRUITS += 1
              GameConfig.TIME_ACCELERATION -= 0.05
              GameConfig.NB_VOILES -= 1
          elif GameConfig.GRID[j][i]["type"]=="filet":
            if GameConfig.GRID[j][i]["vie"]>0:
              if GameConfig.GRID[j][i]["vie"]==100:
                window.blit(GameConfig.RADEAU_FILET_IMG,(i*50,j*50))
              else:
                window.blit(GameConfig.RADEAU_FILET_DAMAGED_IMG,(i*50,j*50))
              window.blit(GameConfig.RADEAU_FILET_DAMAGED_IMG,(i*50,j*50))
            else:
              GameConfig.GRID[j][i]=0
              GameConfig.RADEAUX_DETRUITS += 1
          elif GameConfig.GRID[j][i]["type"]=="pique":
            if GameConfig.GRID[j][i]["vie"]>0:
              if GameConfig.GRID[j][i]["vie"]==100:
                window.blit(GameConfig.RADEAU_PIQUES_IMG,((i*50)-7,(j*50)-7))
              else:
                window.blit(GameConfig.RADEAU_PIQUES_DAMAGED_IMG,((i*50)-7,(j*50)-7))
            else:
              GameConfig.GRID[j][i]=0
              GameConfig.RADEAUX_DETRUITS += 1
              
    for t in self.torches:
      t.draw(window)

    for s in self.sharks:
      s.draw(window)

    for v in self.vagues:
      v.draw(window)

    if not self.ENDED:
      self.player.draw(window)
    for i in range(32):
      for j in range(18):
        if GameConfig.GRID[j][i]!=0 and GameConfig.GRID[j][i]["type"]=="voile":
          window.blit(GameConfig.RADEAU_VOILE_IMG,(i*50,(j*50)-20))
    
    # Gestion du filtre jour/nuit
    actualTime=self.get_time()
        
    if 9 <= actualTime[0] < 17:
      # Ajout d'un filtre à l'écran (coucher de soleil)
      self.current_alpha += 180 / (3000 / 1000 * 35)
    if self.current_alpha >= 180 and actualTime[0] <= 17:
      self.current_alpha = 180
      
    if 17 <= actualTime[0] < 18:
      # Ajout d'un filtre à l'écran (lever du soleil)
      self.current_alpha -= 180 / (2000 / 1000 * 35)
      if self.current_alpha <= 0:
          self.current_alpha = 0

    if actualTime[0] >= 18:
      self.current_alpha+=5
      if self.current_alpha >= 255:
        self.ENDED = True
        self.TEMPS_ECOULE = True
        self.player.ENDED = True
        self.current_alpha = 255
        pygame.mixer.Channel(0).fadeout(500)
          
    if 9 <= actualTime[0]:
      # Création de la surface pour le filtre
      filter_surface = pygame.Surface((GameConfig.WINDOW_W, GameConfig.WINDOW_H),pygame.SRCALPHA)
      pygame.draw.rect(filter_surface, (0, 0, 30, int(self.current_alpha)), filter_surface.get_rect())

      # Création de la surface pour les torches
      torches_surface = pygame.Surface((GameConfig.WINDOW_W, GameConfig.WINDOW_H), pygame.SRCALPHA)
      for t in self.torches:
        torches_surface.blit(GameConfig.LIGHT_IMG, (t.rect.center[0]-50,t.rect.center[1]-50))
      
      # Soustraction de la surface des torches à la surface de fond
      filter_surface.blit(torches_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

      # Affiche le résultat sur l'écran
      window.blit(filter_surface, (0, 0))
    
    if self.player.helpCraft==0:
      window.blit(GameConfig.HELP_IMGS[0][self.player.lance_tier],GameConfig.HELP_COORDS[0][self.player.lance_tier])
    if self.player.helpCraft==1:
      window.blit(GameConfig.HELP_IMGS[1][self.player.rod_tier],GameConfig.HELP_COORDS[1][self.player.rod_tier])
    if self.player.helpCraft!=-1 and self.player.helpCraft!=0 and self.player.helpCraft!=1:
      window.blit(GameConfig.HELP_IMGS[self.player.helpCraft],GameConfig.HELP_COORDS[self.player.helpCraft])

    if self.ENDED and self.animation_mort:
      self.current_alpha+=5

    # Interface       
    window.blit(GameConfig.TIMER_IMG,(1250,11))
    if actualTime[1]<10:
      text=""+str((12+actualTime[0])%24)+":0"+str(actualTime[1])
    else:
      text=""+str((12+actualTime[0])%24)+":"+str(actualTime[1])
    img=GameConfig.FONT60.render(text,True,(126,102,85))
    display_rect=img.get_rect()
    display_rect.center=(1423,46)
    window.blit(img,display_rect)
    nb_voilesTXT=GameConfig.FONT22.render(str(GameConfig.NB_VOILES),True,(126,102,85))
    multiplicateurTXT=GameConfig.FONT22.render("x"+str(round(GameConfig.TIME_ACCELERATION,2)),True,(126,102,85))
    display_rect=nb_voilesTXT.get_rect()
    display_rect.center=(1373,124.5)
    window.blit(nb_voilesTXT,display_rect)

    display_rect=multiplicateurTXT.get_rect()
    display_rect.center=(1457.5,124.5)
    window.blit(multiplicateurTXT,display_rect)
    if GameConfig.CONTROLLER:
      window.blit(GameConfig.INV_CONTROLLER_IMG,(378,800))
    else :
      window.blit(GameConfig.INV_IMG,(478,823))
    for i in range(len(GameConfig.QUANTITY_COORDS)):
      GameState.display_message(window,str(list(GameConfig.INVENTORY.values())[i]),18,GameConfig.QUANTITY_COORDS[i][0],GameConfig.QUANTITY_COORDS[i][1],"top_right",(255,255,255))
    self.draw_hotbarIcons(window)
    window.blit(GameConfig.SELECT_IMG[GameConfig.INDICE_OBJET%2],GameConfig.SELECTOR_COORDS[GameConfig.INDICE_OBJET])



  # Gestion des déplacements, appparitions et intéractions
  def advance_state(self,next_move,window):
    self.player.advance_state(next_move)
    GameConfig.COOLDOWN-=1
    for i in range(0,5):  
      if self.player.lance_tier == i:
        lance_range = GameConfig.ROD_RANGES[i]
      if self.player.rod_tier == i:
        rod_range = GameConfig.ROD_RANGES[i]
    for s in self.sharks:
      s.advance_state(self.player.rect.center[0], self.player.rect.center[1])
      if s.play_sound_shark==True:
        self.play_sound(GameConfig.SHARK_SOUND[randint(0,2)])
      if next_move.left_click and GameConfig.COOLDOWN<=0:
        if s.rect[0] < self.player.rect.center[0] + lance_range and s.rect[0] > self.player.rect.center[0] - lance_range and s.rect[1] < self.player.rect.center[1] + lance_range and s.rect[1] > self.player.rect.center[1] - lance_range:
          s.health -= self.player.lance_tier+1
          self.play_sound(GameConfig.HIT_SOUND[randint(0,2)])
        if s.health <= 0:
          self.sharks.remove(s)
          if choice([0,1,2]) == 0:
            GameConfig.INVENTORY["silex"] += 1
          GameConfig.REQUINS_TUES += 1
          self.play_sound(GameConfig.DEATH_SOUND[choice([0,1,2])])

      elif s.is_dead():
        self.sharks.remove(s)
    if self.time_till_new_sharks==0:
      self.time_till_new_sharks=randint(600,2000)
      self.sharks.append(self.newShark())
    self.time_till_new_sharks-=1
    if GameConfig.CONTROLLER:
      if GameConfig.COOLDOWN<=10 and GameConfig.COOLDOWN>1:
        self.rumble()
      else:
        GameConfig.CONTROLLER.stop_rumble()
    if next_move.left_click and GameConfig.COOLDOWN <= 0:
      GameConfig.COOLDOWN = 10
  
    # Gestion de la récolte des objets
    for b in self.batons:
      if b.rect[0] < self.player.rect.center[0] + rod_range and b.rect[0] > self.player.rect.center[0] - rod_range and b.rect[1] < self.player.rect.center[1] + rod_range and b.rect[1] > self.player.rect.center[1] - rod_range:
        b.is_next_to_player=True
        if next_move.e_pressed:
          self.play_sound(GameConfig.PICK_UP_SOUND[randint(0,3)])
          GameConfig.INVENTORY["baton"]+=1
          self.batons.remove(b)
      else :
        b.is_next_to_player=False

    for c in self.cordes:
      if c.rect[0] < self.player.rect.center[0] + rod_range and c.rect[0] > self.player.rect.center[0] - rod_range and c.rect[1] < self.player.rect.center[1] + rod_range and c.rect[1] > self.player.rect.center[1] - rod_range:
        c.is_next_to_player=True
        if next_move.e_pressed:
          self.play_sound(GameConfig.PICK_UP_SOUND[randint(0,3)])
          GameConfig.INVENTORY["corde"]+=1
          self.cordes.remove(c)
      else :
        c.is_next_to_player=False

    for t in self.tissus:
      if t.rect[0] < self.player.rect.center[0] + rod_range and t.rect[0] > self.player.rect.center[0] - rod_range and t.rect[1] < self.player.rect.center[1] + rod_range and t.rect[1] > self.player.rect.center[1] - rod_range:
        t.is_next_to_player=True
        if next_move.e_pressed:
          self.play_sound(GameConfig.PICK_UP_SOUND[randint(0,3)])
          GameConfig.INVENTORY["tissu"]+=1
          self.tissus.remove(t)
      else :
        t.is_next_to_player=False
    

    # Gestion de la récolte des objets dans les filets
    for b in self.batons:
      if (b.rect[0]<=1599 and b.rect[1]<= 899) :
        if GameConfig.GRID[math.floor(b.rect[1]/50)][math.floor(b.rect[0]/50)] != 0 :
          dico = GameConfig.GRID[math.floor(b.rect[1]/50)][math.floor(b.rect[0]/50)]
          if dico.get("type") == "filet":
            self.play_sound(GameConfig.PICK_UP_SOUND[randint(0,3)])
            GameConfig.INVENTORY["baton"]+=1
            self.batons.remove(b)
    
    for c in self.cordes:
      if (c.rect[0]<=1599 and c.rect[1]<= 899) :
        if GameConfig.GRID[math.floor(c.rect[1]/50)][math.floor(c.rect[0]/50)] != 0 :
          dico = GameConfig.GRID[math.floor(c.rect[1]/50)][math.floor(c.rect[0]/50)]
          if dico.get("type") == "filet":
            self.play_sound(GameConfig.PICK_UP_SOUND[randint(0,3)])
            GameConfig.INVENTORY["corde"]+=1
            self.cordes.remove(c)

    for t in self.tissus:
      if (t.rect[0]<= 1599 and t.rect[1]<= 899) :
        if GameConfig.GRID[math.floor(t.rect[1]/50)][math.floor(t.rect[0]/50)] != 0 :
          dico = GameConfig.GRID[math.floor(t.rect[1]/50)][math.floor(t.rect[0]/50)]
          if dico.get("type") == "filet":
            self.play_sound(GameConfig.PICK_UP_SOUND[randint(0,3)])
            GameConfig.INVENTORY["tissu"]+=1
            self.tissus.remove(t)

    if self.player.poser_torche and not self.ENDED:
      self.torches.append(Torche(self.player.rect.center[0],self.player.rect.center[1]))
      self.player.poser_torche=False
      GameConfig.TORCHES+=1
    for t in self.torches:
      if t.is_dead():
        self.torches.remove(t)

    # Gestion de la poussée de la vague 
    for v in self.vagues:
      if v.rect.topleft[0] < self.player.rect.center[0] and v.rect.topright[0] > self.player.rect.center[0] and v.rect.bottomleft[1]-20 > self.player.rect.center[1] and v.rect.bottomleft[1]-90 < self.player.rect.center[1] and self.ENDED!=True:
        self.player.rect[1]+=10
        if self.player.rect.bottom > 899:
          pygame.mixer.Channel(0).fadeout(500)
          self.ENDED=True
          self.MORT=True
          self.player.ENDED=True
    

    # Gestion des "updates" des objets
    # Gestion de l'apparitions/initialisations des objets
    # Gestion de la suppression des objets quand ils sortent de l'écran
    for b in self.batons:
      b.advance_state()
      if b.is_dead():
        self.batons.remove(b)
    for c in self.cordes:
      c.advance_state()
      if c.is_dead():
        self.cordes.remove(c)
    for t in self.tissus:
      t.advance_state()
      if t.is_dead():
        self.tissus.remove(t)
    for v in self.vagues:
      v.advance_state()
      if v.is_dead():
        self.vagues.remove(v)         
    if self.time_till_new_baton==0:
        self.time_till_new_baton=GameConfig.TICKS_BETWEEN_BATONS
        vy=randint(GameConfig.BATON_MIN_SPEED,GameConfig.BATON_MAX_SPEED)
        self.batons.append(Baton(randint(-50,GameConfig.WINDOW_W),vy))
    if self.time_till_new_corde==0:
        self.time_till_new_corde=GameConfig.TICKS_BETWEEN_CORDES
        vy=randint(GameConfig.BATON_MIN_SPEED,GameConfig.BATON_MAX_SPEED)
        self.cordes.append(Corde(randint(-50,GameConfig.WINDOW_W),vy))
    if self.time_till_new_tissu==0:
        self.time_till_new_tissu=GameConfig.TICKS_BETWEEN_TISSUS
        vy=randint(GameConfig.BATON_MIN_SPEED,GameConfig.BATON_MAX_SPEED)
        self.tissus.append(Tissu(randint(-50,GameConfig.WINDOW_W),vy))
    if self.time_till_new_vague==0:
        self.time_till_new_vague=GameConfig.TICKS_BETWEEN_VAGUES
        vy=randint(GameConfig.VAGUE_MIN_SPEED,GameConfig.VAGUE_MAX_SPEED)
        self.vagues.append(Vague(randint(-50,GameConfig.WINDOW_W),vy))
    if not self.ENDED:
      self.time_till_new_baton-=1
      self.time_till_new_corde-=1
      self.time_till_new_tissu-=1
      self.time_till_new_vague-=1

    collided=False
    for i in range(len(GameConfig.CRAFT_RECTs)):
      if GameConfig.CRAFT_RECTs[i].collidepoint(next_move.pos) and not self.ENDED:
        self.player.helpCraft=i
        self.change_cursor(1)
        collided=True
        break
    if not collided and not self.ENDED:  
      self.player.helpCraft=-1
      self.change_cursor(0)


    # Détection de la chute dans l'eau
    if (self.player.rect.bottom <= 899 and self.player.rect.centerx <= 1599) and not self.ENDED:
      if GameConfig.GRID[math.floor(self.player.rect.bottom/50)][math.floor(self.player.rect.centerx/50)] == 0:
        pygame.mixer.Channel(0).fadeout(500)
        self.ENDED=True
        self.MORT=True
        self.player.ENDED=True
        
    # Détection de la fin de la musique
    if not pygame.mixer.Channel(0).get_busy():
        self.play_sound(GameConfig.TRAP_MUSIC_LOOP)
      
  

  # Gestion du temps
  def get_time(self):
    TIMENOW=time.time()
    TIMEDELTA=TIMENOW-(self.LAST_UPDATE_TIME)

    self.ACCELERATED_TIME += TIMEDELTA * GameConfig.TIME_ACCELERATION
    MINUTE = math.floor(self.ACCELERATED_TIME)
    HOURS = math.floor(MINUTE / 60)
    MINUTE = MINUTE % 60

    self.LAST_UPDATE_TIME = TIMENOW
    return HOURS, MINUTE

  # Gestion de l'interface de l'inventaire
  def draw_hotbarIcons(self,window):
    lance_upgrade=[(2,1,0,0),(4,2,1,0),(4,3,2,1),(4,4,4,3)]
    rod_upgrade=[(2,1,0,0),(4,2,1,0),(4,3,2,0),(4,4,4,0)]
    if self.player.lance_tier==4:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[4],GameConfig.HOTBAR_ICONS_COORDS[0])
    else:
      if GameConfig.INVENTORY["baton"]>=lance_upgrade[self.player.lance_tier][0] and GameConfig.INVENTORY["corde"]>=lance_upgrade[self.player.lance_tier][1] and GameConfig.INVENTORY["tissu"]>=lance_upgrade[self.player.lance_tier][2] and GameConfig.INVENTORY["silex"]>=lance_upgrade[self.player.lance_tier][3]:
        window.blit(GameConfig.HOTBAR_ICONS_IMG[2],GameConfig.HOTBAR_ICONS_COORDS[0])
      else:
        window.blit(GameConfig.HOTBAR_ICONS_IMG[3],GameConfig.HOTBAR_ICONS_COORDS[0])
    if self.player.rod_tier==4:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[4],GameConfig.HOTBAR_ICONS_COORDS[1])
    else:
      if GameConfig.INVENTORY["baton"]>=rod_upgrade[self.player.rod_tier][0] and GameConfig.INVENTORY["corde"]>=rod_upgrade[self.player.rod_tier][1] and GameConfig.INVENTORY["tissu"]>=rod_upgrade[self.player.rod_tier][2] and GameConfig.INVENTORY["silex"]>=rod_upgrade[self.player.rod_tier][3]:
        window.blit(GameConfig.HOTBAR_ICONS_IMG[2],GameConfig.HOTBAR_ICONS_COORDS[1])
      else:
        window.blit(GameConfig.HOTBAR_ICONS_IMG[3],GameConfig.HOTBAR_ICONS_COORDS[1])
    window.blit(GameConfig.HOTBAR_ICONS_IMG[4],GameConfig.HOTBAR_ICONS_COORDS[2])
    window.blit(GameConfig.HOTBAR_ICONS_IMG[4],GameConfig.HOTBAR_ICONS_COORDS[3])
    window.blit(GameConfig.HOTBAR_ICONS_IMG[4],GameConfig.HOTBAR_ICONS_COORDS[4])
    window.blit(GameConfig.HOTBAR_ICONS_IMG[4],GameConfig.HOTBAR_ICONS_COORDS[5])
    if GameConfig.INVENTORY["baton"]>=5:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[0],GameConfig.HOTBAR_ICONS_COORDS[6])
    else:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[1],GameConfig.HOTBAR_ICONS_COORDS[6])
    if GameConfig.INVENTORY["baton"]>=3 and GameConfig.INVENTORY["tissu"]>=6 and GameConfig.INVENTORY["corde"]>=2:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[0],GameConfig.HOTBAR_ICONS_COORDS[7])
    else:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[1],GameConfig.HOTBAR_ICONS_COORDS[7])
    if GameConfig.INVENTORY["baton"]>=6 and GameConfig.INVENTORY["corde"]>=3 and GameConfig.INVENTORY["silex"]>=2:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[0],GameConfig.HOTBAR_ICONS_COORDS[8])
    else:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[1],GameConfig.HOTBAR_ICONS_COORDS[8])
    if GameConfig.INVENTORY["baton"]>=2 and GameConfig.INVENTORY["corde"]>=5:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[0],GameConfig.HOTBAR_ICONS_COORDS[9])
    else:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[1],GameConfig.HOTBAR_ICONS_COORDS[9])
    if GameConfig.INVENTORY["baton"]>=2 and GameConfig.INVENTORY["silex"]>=2:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[0],GameConfig.HOTBAR_ICONS_COORDS[10])
    else:
      window.blit(GameConfig.HOTBAR_ICONS_IMG[1],GameConfig.HOTBAR_ICONS_COORDS[10])


  # Affichage des notifications de connexion/déconnexion de la manette
  def controller_notif(self,connected,window,name):
    pygame.mixer.pause()
    pygame.mixer.Channel(2).unpause()
    if connected:
      text1=GameConfig.FONT18.render("Controller",True,(0,0,0))
      text2=GameConfig.FONT18.render(name,True,(0,0,0))
      text3=GameConfig.FONT18.render("connected",True,(0,0,0))
      display_rect1,display_rect2,display_rect3=text1.get_rect(),text2.get_rect(),text3.get_rect()
      display_rect1.center=(1376,171-34.5)
      display_rect2.center=(1376,171)
      display_rect3.center=(1376,171+34.5)
      window.blit(GameConfig.CONTROLLER_CONNECTED_IMG,(1083,102))
      window.blit(text1,display_rect1)
      window.blit(text2,display_rect2)
      window.blit(text3,display_rect3)
    else:
      text1=GameConfig.FONT18.render("Controller",True,(0,0,0))
      text2=GameConfig.FONT18.render(name,True,(0,0,0))
      text3=GameConfig.FONT18.render("disconnected",True,(0,0,0))
      display_rect1,display_rect2,display_rect3=text1.get_rect(),text2.get_rect(),text3.get_rect()
      display_rect1.center=(1376,171-34.5)
      display_rect2.center=(1376,171)
      display_rect3.center=(1376,171+34.5)
      window.blit(GameConfig.CONTROLLER_DISCONNECTED_IMG,(1083,102))
      window.blit(text1,display_rect1)
      window.blit(text2,display_rect2)
      window.blit(text3,display_rect3)
    pygame.display.update()
    pygame.time.delay(1750)

  

  # Gestion de la connexion/déconnexion de la manette
  def controller_state(self,window):
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0 and GameConfig.CONTROLLER:
      nom = GameConfig.CONTROLLER.get_name()
      GameConfig.CONTROLLER=False 
      self.play_sound(GameConfig.CONTROLLER_DISCONNECTED_SOUND)
      self.controller_notif(False,window,nom)
    elif joystick_count > 0:
      var_break=False
      for i in range(joystick_count):
        if "Xbox" in pygame.joystick.Joystick(i).get_name():
          if not GameConfig.CONTROLLER:
            self.play_sound(GameConfig.CONTROLLER_CONNECTED_SOUND)
            self.controller_notif(True,window,pygame.joystick.Joystick(i).get_name())
          GameConfig.CONTROLLER=pygame.joystick.Joystick(i)
          var_break=True
      if var_break:
        return
      else:
        if GameConfig.CONTROLLER:
          nom = GameConfig.CONTROLLER.get_name()
          self.play_sound(GameConfig.CONTROLLER_DISCONNECTED_SOUND)
          self.controller_notif(False,window,nom)
        GameConfig.CONTROLLER=False
    else:
      GameConfig.CONTROLLER=False
  

  # Gestion des sons
  def play_sound(self,sound):
    if GameConfig.SOUND_ON:
      if sound == GameConfig.TRAP_MUSIC_LOOP or sound == GameConfig.TRAP_MUSIC or sound == GameConfig.MENU_MUSIC_LOOP:
        return pygame.mixer.Channel(0).play(sound)
      elif sound == GameConfig.CONTROLLER_CONNECTED_SOUND or sound == GameConfig.CONTROLLER_DISCONNECTED_SOUND:
        return pygame.mixer.Channel(2).play(sound)
      else:
        return pygame.mixer.Channel(1).play(sound)
  

  # Gestion du curseur
  def change_cursor(self,cursor):
    if cursor==0 and GameConfig.CURSOR!=0:
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
      GameConfig.CURSOR=0
    elif cursor==1 and GameConfig.CURSOR!=1:
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
      GameConfig.CURSOR=1
  


  # Gestion de l'importation des images
  def load_img(self,img):
    if img[-3:]=="png":
      image = pygame.image.load(img).convert_alpha()
      if image.get_size()==(21,24):
        if img[-14:]=="standing01.png":
          GameConfig.STANDING_IMGS[0]=image
          GameConfig.STANDING_IMGS[2]=image
          GameConfig.STANDING_MASKS[0]=pygame.mask.from_surface(GameConfig.STANDING_IMGS[0])
          GameConfig.STANDING_MASKS[2]=pygame.mask.from_surface(GameConfig.STANDING_IMGS[2])
        if img[-14:]=="standing02.png":
          GameConfig.STANDING_IMGS[1]=image
          GameConfig.STANDING_MASKS[1]=pygame.mask.from_surface(GameConfig.STANDING_IMGS[1])
        if img[-14:]=="standing03.png":
          GameConfig.STANDING_IMGS[3]=image
          GameConfig.STANDING_MASKS[3]=pygame.mask.from_surface(GameConfig.STANDING_IMGS[3])
        
        if img[-10:]=="left01.png":
          GameConfig.WALKING_LEFT_IMGS[0]=image
          GameConfig.WALKING_LEFT_IMGS[2]=image
          GameConfig.WALKING_LEFT_MASKS[0]=pygame.mask.from_surface(GameConfig.WALKING_LEFT_IMGS[0])
          GameConfig.WALKING_LEFT_MASKS[2]=pygame.mask.from_surface(GameConfig.WALKING_LEFT_IMGS[2])
        if img[-10:]=="left02.png":
          GameConfig.WALKING_LEFT_IMGS[1]=image
          GameConfig.WALKING_LEFT_MASKS[1]=pygame.mask.from_surface(GameConfig.WALKING_LEFT_IMGS[1])
        if img[-10:]=="left03.png":
          GameConfig.WALKING_LEFT_IMGS[3]=image
          GameConfig.WALKING_LEFT_MASKS[3]=pygame.mask.from_surface(GameConfig.WALKING_LEFT_IMGS[3])
        
        if img[-11:]=="right01.png":
          GameConfig.WALKING_RIGHT_IMGS[0]=image
          GameConfig.WALKING_RIGHT_IMGS[2]=image
          GameConfig.WALKING_RIGHT_MASKS[0]=pygame.mask.from_surface(GameConfig.WALKING_RIGHT_IMGS[0])
          GameConfig.WALKING_RIGHT_MASKS[2]=pygame.mask.from_surface(GameConfig.WALKING_RIGHT_IMGS[2])
        if img[-11:]=="right02.png":
          GameConfig.WALKING_RIGHT_IMGS[1]=image
          GameConfig.WALKING_RIGHT_MASKS[1]=pygame.mask.from_surface(GameConfig.WALKING_RIGHT_IMGS[1])
        if img[-11:]=="right03.png":
          GameConfig.WALKING_RIGHT_IMGS[3]=image
          GameConfig.WALKING_RIGHT_MASKS[3]=pygame.mask.from_surface(GameConfig.WALKING_RIGHT_IMGS[3])
        
        if img[-9:]=="top01.png":
          GameConfig.WALKING_TOP_IMGS[0]=image
          GameConfig.WALKING_TOP_IMGS[2]=image
          GameConfig.TOP_MASKS[0]=pygame.mask.from_surface(GameConfig.WALKING_TOP_IMGS[0])
          GameConfig.TOP_MASKS[2]=pygame.mask.from_surface(GameConfig.WALKING_TOP_IMGS[2])
        if img[-9:]=="top02.png":
          GameConfig.WALKING_TOP_IMGS[1]=image
          GameConfig.TOP_MASKS[1]=pygame.mask.from_surface(GameConfig.WALKING_TOP_IMGS[1])
        if img[-9:]=="top03.png":
          GameConfig.WALKING_TOP_IMGS[3]=image
          GameConfig.TOP_MASKS[3]=pygame.mask.from_surface(GameConfig.WALKING_TOP_IMGS[3])
          
  def rumble(self):
    GameConfig.CONTROLLER.rumble(10,10,10)
    
  def animation_mort(self,window):
    # Afficher une image penchée sur le coté
    for i in range(4):
      rotate_standing = pygame.transform.rotate(GameConfig.STANDING_IMGS[0], 20)
      self.draw(window)
      window.blit(rotate_standing,self.player.rect.topleft)
      pygame.display.update()
      pygame.time.delay(175)
      self.draw(window)
      window.blit(GameConfig.STANDING_IMGS[0],(self.player.rect.topleft))
      pygame.display.update()
      pygame.time.delay(175)
      rotate_standing = pygame.transform.rotate(GameConfig.STANDING_IMGS[0], -20)
      self.draw(window)
      window.blit(rotate_standing,self.player.rect.topleft)
      pygame.display.update()
      pygame.time.delay(175)
      self.draw(window)
      window.blit(GameConfig.STANDING_IMGS[0],(self.player.rect.topleft))
      pygame.display.update()
      pygame.time.delay(175)
    self.animation = False

  def menu_music_state(self):
    if not pygame.mixer.Channel(0).get_busy():
        self.play_sound(GameConfig.MENU_MUSIC_LOOP)