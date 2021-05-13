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

#ball make
ball_images = [ 
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
     pygame.image.load(os.path.join(image_path, "balloon2.png")),
      pygame.image.load(os.path.join(image_path, "balloon3.png")),
       pygame.image.load(os.path.join(image_path, "balloon4.png"))]

#ball size initial speed
ball_speed_y = [-18,-15,-12,-9] #index 0 , 1, 2 , 3 

#BALLS
balls = []
balls.append({
    "pos_x" : 50,   #공의 x 좌표 
    "pos_y" : 50,   #공의 y 좌표 
    "img_idx" : 0, # 공의 이미지 인덱스 
    "to_x" : 3,      #x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로 
    "to_y" : -6, # y축 이동방향
    "init_spd_y": ball_speed_y[0] #y 의 최초 속도 
})

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
    
    #ball location
    for ball_idx, ball_val in enumerate(balls): #볼 하나하나씩 가져와서 몇번쨰 인덱스인지 
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        #가로 벽에 닿았을때 공 이동위치 변경 
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        
        #세로 위치 
        #스테이지 튕겨서 올라가는 처리 
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:   #그 외에는 모든 경우는 속도를 증가 
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    # 5. Draw on Background
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x,ball_pos_y))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character, (character_x_pos,character_y_pos))
    
    pygame.display.update()             # keep updating redrawing the background


pygame.quit()