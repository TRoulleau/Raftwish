import pygame
from game_config import *
from pygame.locals import *
from game_state import *
from move import *

# Fonctions utiles pour la gestion du jeu
# (affichage de message, rejouer etc.)

# Boucle de jeu
def game_loop(window):
  quitting=False
  game_state=GameState()
  GameConfig.reset()
  game_state.play_sound(GameConfig.TRAP_MUSIC)
  while not quitting and not game_state.ENDED:
    game_state.controller_state(window)
    next_move=get_next_move()
    game_state.advance_state(next_move,window)
    pygame.mixer.unpause()
    if not next_move.quit:
      game_state.draw(window)
    else:
      return pygame.quit()
    if next_move.escape:
      TIMENOW=time.time()
      pygame.mixer.pause()
      pygame.mixer.Channel(2).unpause()
      game_state.change_cursor(0)
      reprendre=False
      # Ajout d'un filtre à l'écran
      filter_surface = pygame.Surface((GameConfig.WINDOW_W, GameConfig.WINDOW_H),pygame.SRCALPHA)
      pygame.draw.rect(filter_surface, (128, 128, 128, 51), filter_surface.get_rect())
      window.blit(filter_surface, (0, 0), special_flags=BLEND_RGBA_MULT)
      GameState.display_message(window,"PAUSE",60,GameConfig.WINDOW_W/2,GameConfig.WINDOW_H/2,"center",(255,255,255))
      GameState.display_message(window,"Appuyez sur ECHAP pour reprendre",60,GameConfig.WINDOW_W/2,GameConfig.WINDOW_H/2+70,"center",(255,255,255))
      pygame.display.update()
      while True:
        game_state.controller_state(window)
        for event in pygame.event.get():
          if event.type==WINDOWEXPOSED:
            pygame.display.update()
          if GameConfig.CONTROLLER:
            if event.type==JOYBUTTONDOWN and event.button==7:
              reprendre=True
          if event.type == KEYDOWN and event.key == K_ESCAPE:
            reprendre=True
          if event.type==QUIT:
            return pygame.quit()
        if reprendre:
          TIMEDELTA=time.time()-TIMENOW
          game_state.LAST_UPDATE_TIME+=TIMEDELTA
          break
    pygame.display.update()
    pygame.time.delay(35)
  if game_state.ENDED:
    if game_state.animation and game_state.MORT :
        game_state.animation_mort(window)
    return end_menu(window,game_state.MORT, game_state.TEMPS_ECOULE)


# Détection des input du joueur
def get_next_move():
  next_move=Move()
  keys=pygame.key.get_pressed()
  next_move.pos = pygame.mouse.get_pos()
  if keys[K_q]:
    next_move.left = True
  if keys[K_d]:
    next_move.right = True
  if keys[K_z]:
    next_move.up = True
  if keys[K_s]:
    next_move.down = True
  if keys[K_e]:
    next_move.e_pressed = True
  for event in pygame.event.get():
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:  # Left click
          next_move.left_click = True
        elif event.button == 3:  # Right click
          next_move.right_click = True
    if event.type == MOUSEWHEEL:
        if event.y<0:
          next_move.scroll_up = True
        elif event.y>0:
          next_move.scroll_down = True      
    if event.type == KEYDOWN and event.key == K_ESCAPE:
      next_move.escape = True
    if event.type == QUIT:
        next_move.quit = True
    
    if event.type==WINDOWMINIMIZED: # Si fenêtre minimisée, menu pause
      next_move.escape = True
      
    if GameConfig.CONTROLLER: # Si manette connectée
      if event.type==JOYBUTTONDOWN:
        if event.button==7: # START
          next_move.escape = True
        elif event.button==1: # B
          next_move.right_click=True
        elif event.button==2: # X
          next_move.e_pressed=True
        elif event.button==4: # LB
          next_move.scroll_down=True
        elif event.button==5: # RB
          next_move.scroll_up=True
  if GameConfig.CONTROLLER:
    # Joystick gauche
    if GameConfig.CONTROLLER.get_axis(0) > 0.5:
      next_move.right=True
    if  GameConfig.CONTROLLER.get_axis(0) < -0.5:
      next_move.left=True
    if GameConfig.CONTROLLER.get_axis(1) > 0.5:
      next_move.down=True
    if GameConfig.CONTROLLER.get_axis(1) < -0.5:
      next_move.up=True
    # Trigger droit
    if GameConfig.CONTROLLER.get_axis(5) >= 0.6 and GameConfig.COOLDOWN<=0:
      next_move.left_click=True
      GameConfig.CONTROLLER.rumble(1,1,100)
    else:
      GameConfig.CONTROLLER.rumble(0,0,0)
  return next_move

# Gestion du menu de fin
def end_menu(window, mort, temps_ecoule):
  game_state = GameState()
  while True:
    game_state.controller_state(window)
    next_move=get_next_move()  
    menu_rect=pygame.Rect(1168,641,284,101)
    if temps_ecoule:
        window.blit(GameConfig.END_IMG,(0,0))
        stats_rect=pygame.Rect(841,641,284,101)
        if stats_rect.collidepoint(pygame.mouse.get_pos()):
          window.blit(GameConfig.STATS_IMG,(93,227))
          GameState.display_message(window,"x"+str(GameConfig.RADEAUX),22,182,493,"center",(0,0,0))
          GameState.display_message(window,"x"+str(GameConfig.VOILES),22,287,493,"center",(0,0,0))
          GameState.display_message(window,"x"+str(GameConfig.PIQUES),22,398,493,"center",(0,0,0))
          GameState.display_message(window,"x"+str(GameConfig.FILETS),22,512,493,"center",(0,0,0))
          GameState.display_message(window,"x"+str(GameConfig.TORCHES),22,618.5,493,"center",(0,0,0))
          GameState.display_message(window,"x"+str(GameConfig.REQUINS_TUES),22,245.5,701,"center",(0,0,0))
          GameState.display_message(window,"x"+str(GameConfig.RADEAUX_DETRUITS),22,555.5,701,"center",(0,0,0))
    elif mort:
      window.blit(GameConfig.MORT_IMG,(0,0))
      stats_rect=pygame.Rect(841,641,284,101)
      if stats_rect.collidepoint(pygame.mouse.get_pos()):
        window.blit(GameConfig.STATS_IMG,(93,227))
        GameState.display_message(window,"x"+str(GameConfig.RADEAUX),22,182,493,"center",(0,0,0))
        GameState.display_message(window,"x"+str(GameConfig.VOILES),22,287,493,"center",(0,0,0))
        GameState.display_message(window,"x"+str(GameConfig.PIQUES),22,398,493,"center",(0,0,0))
        GameState.display_message(window,"x"+str(GameConfig.FILETS),22,512,493,"center",(0,0,0))
        GameState.display_message(window,"x"+str(GameConfig.TORCHES),22,618.5,493,"center",(0,0,0))
        GameState.display_message(window,"x"+str(GameConfig.REQUINS_TUES),22,245.5,701,"center",(0,0,0))
        GameState.display_message(window,"x"+str(GameConfig.RADEAUX_DETRUITS),22,555.5,701,"center",(0,0,0))
    pygame.display.update()
    if menu_rect.collidepoint(next_move.pos):
      game_state.change_cursor(1)
      if next_move.left_click:
        GameConfig.END = True
        return main_menu(window)
    else:
      game_state.change_cursor(0)
    if next_move.quit:
      return pygame.quit()

# Gestion du menu principal
def main_menu(window):
  game_state=GameState()
  while True:
    pygame.mixer.unpause()
    game_state.menu_music_state()
    game_state.controller_state(window)
    window.blit(GameConfig.MAIN_MENU_IMG,(0,0))
    window.blit(GameConfig.HELP_MENU_BUTTON_IMG,(654,507))
    window.blit(GameConfig.SETTINGS_MENU_BUTTON_IMG,(654,627))
    GameState.display_message(window,"JOUER",60,GameConfig.WINDOW_W/2,806,"center",(255,255,255))
    if GameConfig.CONTROLLER:
      window.blit(GameConfig.CONTROLLER_A_BUTTON_IMG,(867,806))
    pygame.display.update()
    pos = pygame.mouse.get_pos()
    if GameConfig.HELP_MENU_BUTTON_RECT.collidepoint(pos) or GameConfig.SETTINGS_MENU_BUTTON_RECT.collidepoint(pos) or (GameConfig.WINDOW_W/2)-107 <= pos[0] <= (GameConfig.WINDOW_W/2)+107 and 762 <= pos[1] <= 844:
      game_state.change_cursor(1)
    else:
      game_state.change_cursor(0)
    for event in pygame.event.get([KEYDOWN, QUIT, MOUSEBUTTONDOWN, JOYBUTTONDOWN]):
      if event.type == QUIT:
        return pygame.quit()
      if event.type == MOUSEBUTTONDOWN:
        if GameConfig.HELP_MENU_BUTTON_RECT.collidepoint(pos):
          game_state.play_sound(GameConfig.SELECTED_SOUND)
          return help_menu(window)
        elif GameConfig.SETTINGS_MENU_BUTTON_RECT.collidepoint(pos):
          game_state.play_sound(GameConfig.SELECTED_SOUND)
          return settings_menu(window)
        elif (GameConfig.WINDOW_W/2)-107 <= pos[0] <= (GameConfig.WINDOW_W/2)+107 and 762 <= pos[1] <= 844:
          game_state.play_sound(GameConfig.SELECTED_SOUND)
          return game_loop(window)
      if event.type == JOYBUTTONDOWN and GameConfig.CONTROLLER:
        if event.button==0:
          game_state.play_sound(GameConfig.SELECTED_SOUND)
          return game_loop(window)

# Gestion du menu d'aide
def help_menu(window):
  game_state=GameState()
  HELP_CONTROLS_RECT=pygame.Rect(291,136,282,265)
  HELP_GAMEPLAY_RECT=pygame.Rect(661,136,282,265)
  HELP_FABRICATION_RECT=pygame.Rect(1030,136,319,265)
  HELP_RADEAUX_RECT=pygame.Rect(482,432,282,379)
  HELP_DANGERS_RECT=pygame.Rect(842,432,282,300)
  return_rect = pygame.Rect(13,13,110,110)
  while True:
    pygame.mixer.unpause()
    game_state.menu_music_state()
    game_state.controller_state(window)
    window.blit(GameConfig.HELP_MENU_IMG,(0,0))
    pos = pygame.mouse.get_pos()
    if return_rect.collidepoint(pos) or HELP_CONTROLS_RECT.collidepoint(pos) or HELP_GAMEPLAY_RECT.collidepoint(pos) or HELP_FABRICATION_RECT.collidepoint(pos) or HELP_RADEAUX_RECT.collidepoint(pos) or HELP_DANGERS_RECT.collidepoint(pos):
      game_state.change_cursor(1)
    else:
      game_state.change_cursor(0)
    if HELP_CONTROLS_RECT.collidepoint(pos):
      window.blit(GameConfig.HELP_CONTROLS_POPUP_IMG,(207,87))
    elif HELP_GAMEPLAY_RECT.collidepoint(pos):
      window.blit(GameConfig.HELP_GAMEPLAY_POPUP_IMG,(207,87))
    elif HELP_FABRICATION_RECT.collidepoint(pos):
      window.blit(GameConfig.HELP_FABRICATION_POPUP_IMG,(207,87))
    elif HELP_RADEAUX_RECT.collidepoint(pos):
      window.blit(GameConfig.HELP_RADEAUX_POPUP_IMG,(207,87))
    elif HELP_DANGERS_RECT.collidepoint(pos):
      window.blit(GameConfig.HELP_DANGERS_POPUP_IMG,(207,87))
    pygame.display.update()
    for event in pygame.event.get([KEYDOWN,QUIT,MOUSEBUTTONDOWN]):
      if event.type==QUIT:
        return pygame.quit()
      if event.type==KEYDOWN:
        if event.key==K_ESCAPE:
          return main_menu(window)
      if event.type == MOUSEBUTTONDOWN:
        if return_rect.collidepoint(pos):
          return main_menu(window)

# Gestion du menu des paramètres
def settings_menu(window):
  game_state=GameState()
  current_skin_view=0
  while True:
    pygame.mixer.unpause()
    game_state.menu_music_state()
    game_state.controller_state(window)
    current_skin_view+=.01
    window.blit(GameConfig.SETTINGS_MENU_IMG,(0,0))
    if GameConfig.IS_FULLSCREEN:
      window.blit(GameConfig.BUTTON_ON_IMG,(150,442))
    else:
      window.blit(GameConfig.BUTTON_OFF_IMG,(150,442))
    if GameConfig.SOUND_ON:
      window.blit(GameConfig.BUTTON_ON_IMG,(150,600))
    else:
      window.blit(GameConfig.BUTTON_OFF_IMG,(150,600))
    window.blit(GameConfig.IMPORT_BUTTON_IMG,(1071,604))
    window.blit(pygame.transform.scale(GameConfig.STANDING_IMGS[math.floor(current_skin_view)%4],(309,353)),(1058,255))
    pygame.display.update()
    pos = pygame.mouse.get_pos()
    return_rect = pygame.Rect(13,13,110,110)
    if GameConfig.BUTTON_ON_FULLSCREEN_RECT.collidepoint(pos) or GameConfig.BUTTON_OFF_FULLSCREEN_RECT.collidepoint(pos) or GameConfig.BUTTON_ON_SOUND_RECT.collidepoint(pos) or GameConfig.BUTTON_OFF_SOUND_RECT.collidepoint(pos) or return_rect.collidepoint(pos):
      game_state.change_cursor(1)
    else:
      game_state.change_cursor(0)
    for event in pygame.event.get([KEYDOWN,QUIT,DROPFILE,MOUSEBUTTONDOWN]):
      if event.type==QUIT:
        return pygame.quit()

      if event.type==DROPFILE:
        game_state.load_img(event.file)
        
      if event.type==KEYDOWN:
        if event.key==K_ESCAPE:
          return main_menu(window)
        
      if event.type == MOUSEBUTTONDOWN:
        if GameConfig.BUTTON_ON_FULLSCREEN_RECT.collidepoint(pos) or GameConfig.BUTTON_OFF_FULLSCREEN_RECT.collidepoint(pos):
          GameConfig.IS_FULLSCREEN=not GameConfig.IS_FULLSCREEN
          if GameConfig.IS_FULLSCREEN:
            window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H), FULLSCREEN)
          else:
            window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
        
        if GameConfig.BUTTON_ON_SOUND_RECT.collidepoint(pos) or GameConfig.BUTTON_OFF_SOUND_RECT.collidepoint(pos):
          if GameConfig.SOUND_ON:
            pygame.mixer.stop() 
          GameConfig.SOUND_ON=not GameConfig.SOUND_ON
        
        if return_rect.collidepoint(pos):
          return main_menu(window)

      
# Lancement du jeu
if __name__ == '__main__':
  pygame.init()
  window = pygame.display.set_mode((GameConfig.WINDOW_W, GameConfig.WINDOW_H))
  pygame.display.set_caption('RaftWish')
  window.blit(pygame.image.load('Ressources/loading.png').convert_alpha(),(0,0))
  pygame.display.update()
  pygame.joystick.init()
  pygame.mixer.init()
  GameConfig.init()
  pygame.display.set_icon(GameConfig.STANDING_IMGS[0])
  Player.init_sprites()
  Baton.init_sprites()
  Corde.init_sprites()
  Tissu.init_sprites()
  Vague.init_sprites()
  Torche.init_sprites()
  pygame.mixer.Channel(0).play(pygame.mixer.Sound('Ressources/game_launched.wav')),
  main_menu(window)
  pygame.quit()
  quit()