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

#character movement
character_to_x = 0

#character moving speed
character_speed = 5

#Weapon
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#Weapon can have a lot of shots

weapons = []

#weapon speed

weapon_speed = 10

#Event Loop
running = True # is this running?
while running:
    dt = clock.tick(30)                 #frame per sceonds

    # 2. Event Handler
    for event in pygame.event.get():    # What kind of event happened?
        if event.type == pygame.QUIT:   # When user click close window 
            running = False             # Game is not running
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. Game Character Location   
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    
    # weapon location 
    # 100, 200 -> 180 160 140 
    weapons = [[ w[0],w[1] - weapon_speed] for w in weapons] #weapon to up 
    
    #Weapon reach the top no need
    weapons = [[w[0],w[1]] for w in weapons if w[1] > 0]
    
    
    # 5. Draw on Background
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character, (character_x_pos,character_y_pos))
    
    pygame.display.update()             # keep updating redrawing the background


pygame.quit()