import pygame
import os
##############################################################################
# Init 
pygame.init() # init 

# Game Window 
screen_width = 640
screen_height = 480 
screen = pygame.display.set_mode((screen_width,screen_height))

#Setting the Title 
pygame.display.set_caption("Jay Game")

#FPS
clock = pygame.time.Clock()
############################################################################################

# 1. User game Init (BackGround, Game Image, Coordinatem, spped, font )
current_path = os.path.dirname(__file__) #return current file path
image_path = os.path.join(current_path,"images") # images folder return 

#background
background = pygame.image.load((os.path.join(image_path,"background.png")))

#stage
stage =  pygame.image.load((os.path.join(image_path,"stage.png")))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#character
character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) -(character_width/2)
character_y_pos = screen_height- character_height - stage_height



#Event Loop
running = True # is this running?
while running:
    dt = clock.tick(30)                 #frame per sceonds

    # 2. Event Handler
    for event in pygame.event.get():    # What kind of event happened?
        if event.type == pygame.QUIT:   # When user click close window 
            running = False             # Game is not running


    # 3. Game Character Location   

    # 4. Collision Handler
    
    # 5. Draw on Background
    screen.blit(background, (0,0))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character, (character_x_pos,character_y_pos))
    pygame.display.update()             # keep updating redrawing the background


pygame.quit()