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

#사라질 무기 ,공 정보 저장
weapon_to_remove = -1 
ball_to_remove = -1

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

    # Collision
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    for ball_idx, ball_val in enumerate(balls): #볼 하나하나씩 가져와서 몇번쨰 인덱스인지 
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        if character_rect.colliderect(ball_rect):
            running = False
            break
        #ball and weapon collision
        for weapon_idx, weapon_val in enumerate(weapons): #볼 하나하나씩 가져와서 몇번쨰 인덱스인지
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            #무기 rect 정보 
            weapon_rect=weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx #해당 공 없애기 위한 값 설정

                #가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기 
                if ball_img_idx < 3:
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보 
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    #왼쪽으로 튕겨져 나가는 공 
                    balls.append({
                         "pos_x" : ball_pos_x + (ball_width/2)-(small_ball_width/2),   #공의 x 좌표 
                         "pos_y" : ball_pos_y + (ball_height/2)-(small_ball_height/2),   #공의 y 좌표 
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스 
                            "to_x" : -3,      #x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로 
                            "to_y" : -6, # y축 이동방향
                            "init_spd_y": ball_speed_y[ball_img_idx + 1] #y 의 최초 속도 
                        })
                        #오른쪽
                    balls.append({
                         "pos_x" : ball_pos_x + (ball_width/2)-(small_ball_width/2),   #공의 x 좌표 
                         "pos_y" : ball_pos_y + (ball_height/2)-(small_ball_height/2),   #공의 y 좌표 
                            "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스 
                            "to_x" : 3,      #x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로 
                            "to_y" : -6, # y축 이동방향
                            "init_spd_y": ball_speed_y[ball_img_idx + 1] #y 의 최초 속도 
                        })
                break 

    #충돌된 공 or 무기 없애기 
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove >-1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

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