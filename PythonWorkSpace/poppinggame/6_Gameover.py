import os 
import pygame #pygame 모듈을 import 
import random 
########################################################################################
#필수 초기화
pygame.init() #pygame 라이브러리 초기화
#화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption('Popping Popping game in time!')

#FPS 초당 프레임 수 
clock = pygame.time.Clock() 
########################################################################################


#1-사용자 게임 초기화: 배경화면, 캐릭터이미지, 좌표/속도/폰트 설정  등 
current_path = os.path.dirname(__file__) #현재 파일 위치 반환 
image_path = os.path.join(current_path,"images") #image 폴더 위치 반환 

#배경 음악 
pygame.mixer.init() 
pygame.mixer.music.load ("C:/Users/www/OneDrive/바탕 화면/PythonWorkSpace/poppinggame/Wake Up.mp3") #배경음악 
pygame.mixer.music.play(-1,0.0) 
pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.2 ) #음악 볼륨 


background = pygame.image.load(os.path.join(image_path, "background.png")) #배경 삽입 
stage = pygame.image.load(os.path.join(image_path, "stage.png")) #무대 삽입 
stage_size = stage.get_rect().size 
stage_height = stage_size[1] #무대 위에 캐릭터 위치시키기 위해 사용 
 

character = pygame.image.load(os.path.join(image_path, "character.png")) #캐릭터 삽입 
character_size = character.get_rect().size 
character_width = character_size[0]  #캐릭터 가로 세로 
character_height = character_size[1] 
character_x_pos = (screen_width/2)-(character_width/2)   #캐릭터 좌표 
character_y_pos = screen_height - character_height - (stage_height-30)

#character_to_x=0  #캐릭터 이동 방향 
character_to_x_LEFT = 0  #x좌표에서 왼쪽, 오른쪽 이동 방향 정의 
character_to_x_RIGHT = 0 
character_speed=18 #캐릭터 이동 속도 

#Timer 삽입 
game_font = pygame.font.SysFont("bauhaus93", 30)  #폰트 설정  
Total_time = 30  #실제 표시되는 텍스트  
Start_ticks  = pygame.time.get_ticks() 




#무기 삽입
weapon = pygame.image.load(os.path.join(image_path, "weapon.png")) 
weapon_size = weapon.get_rect().size  
weapon_width = weapon_size[0] #무기 가로 길이

weapons = [] 
weapon_speed = 14 



#버블 이미지 리스트 
bubble_images = [ 
    pygame.image.load(os.path.join(image_path, "bubble1.png")),
    pygame.image.load(os.path.join(image_path, "bubble2.png")),
    pygame.image.load(os.path.join(image_path, "bubble3.png")),
    pygame.image.load(os.path.join(image_path, "bubble4.png"))
] 
#버블 크기에 따른 최초 스피드 
bubble_spd_y = [  -17, -14, -11, -8] #인덱스 0,1,2,3 해당하는 값

#버블 리스트 
bubbles = [] 
#bubble1을 버블 리스트에 삽입 
bubbles.append({   
    "pos_x": 50, "pos_y": 50, #버블 좌표 
    "img_idx": 0, #버블 이미지 인덱스 
    "to_x": 4, "to_y":  -9,  #버블 좌우 이동
    "init_spd_y": bubble_spd_y[0] #y좌표 최초 속도(튕길 떄)
})

#소멸할 버블, 무기 변수 
weapon_to_remove = -1 
bubble_to_remove = -1 





#이벤트 루프 
running = True 
while running:
    dt = clock.tick_busy_loop(80) 
    print("fps는 " + str(clock.get_fps()))

    #2-이벤트 처리: 키보드 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

        if event.type in [pygame.KEYDOWN]: #키 누를 때 왼쪽, 오른쪽 경우 서로 다른 변수 값 설정 
            #방향키 
            if event.key == pygame.K_LEFT: #왼쪽 이동 
                character = pygame.image.load(os.path.join(image_path, "character.png")) 
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT: #오른쪽 이동 
                character = pygame.image.load(os.path.join(image_path, "characterRightKey.png"))
                character_to_x_RIGHT += character_speed 
                break

            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos]) #무기 리스트에 생성한 무기 추가 

            
        if event.type in [pygame.KEYUP]: #키 동작 해제
            if event.key == pygame.K_LEFT: 
                character_to_x_LEFT = 0 
            elif event.key == pygame.K_RIGHT: 
                character_to_x_RIGHT = 0 


        if not pygame.mixer.music.get_busy(): #소리가 섞여있지 않을 경우 
                pygame.mixer.music.fadeout(2000) #배경음악 fadeout 
                pygame.time.delay(1000)
                running = False 




   #3-캐릭터 위치 
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT

    #화면 경계값 처리 
    if character_x_pos < 0:  
        character_x_pos = 0 
    elif character_x_pos > screen_width - character_width: 
        character_x_pos = screen_width - character_width
    
     #무기 위치 설정 
    weapons = [ [w[0], w[1] - weapon_speed ]  for w in weapons ] #위로 쏘아올리기 
    #천장에 닿으면 소멸 
    weapons = [ [w[0], w[1]]  for w in weapons if w[1] > 0 ] 


    #버블 위치 정보 
    for bubble_idx, bubble_val in enumerate(bubbles): 
        bubble_pos_x = bubble_val["pos_x"]
        bubble_pos_y = bubble_val["pos_y"]
        bubble_img_idx = bubble_val["img_idx"]  
        bubble_size = bubble_images[bubble_img_idx].get_rect().size 
        bubble_width =  bubble_size[0]
        bubble_height = bubble_size[1]

         #x좌표상 왼쪽 화면 밖과 오른쪽 화면 밖으로 나갈 떄 
        if bubble_pos_x < 0 or bubble_pos_x > screen_width - bubble_width:
            bubble_val["to_x"] = bubble_val["to_x"] * (-1) #버블 x좌표 반대

        #버블이 무대에 닿았을 때 1번 
        if bubble_pos_y >= screen_height - stage_height - bubble_height: 
            bubble_val["to_y"] = bubble_val["to_y"] * (-1) 

        else: #튕기지 않을 떄: 속도 증가 
            bubble_val["to_y"] += 0.5

        #실제 버블 위치 값
        bubble_val["pos_x"] += bubble_val["to_x"]
        bubble_val["pos_y"] += bubble_val["to_y"]



   #4-충돌 처리 
    #캐릭터 rect 정보 업데이트 
    character_rect = character.get_rect() 
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for bubble_idx, bubble_val in enumerate(bubbles):   #버블 위치 정보
        bubble_pos_x = bubble_val["pos_x"]
        bubble_pos_y = bubble_val["pos_y"]
        bubble_img_idx = bubble_val["img_idx"]  
        #버블 rect 정보 업데이트 
        bubble_rect = bubble_images[bubble_img_idx].get_rect()
        bubble_rect.left = bubble_pos_x 
        bubble_rect.top = bubble_pos_y 
        
        if character_rect.colliderect(bubble_rect): #캐릭터,버블 충돌 시 
            ##충돌 시 종료 음악 추가한 부분 
            pygame.mixer.music.stop() #음악 멈추기 
            oversound = pygame.mixer.music.load("C:/Users/www/OneDrive/바탕 화면/PythonWorkSpace/poppinggame/Gameover.wav") #짧은 사운드 블러오기 
            pygame.mixer.music.play(0) #1번만 재생 
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.2)

            #게임오버 알림 이미지 
            loserCharacter = pygame.image.load(os.path.join(image_path,  "Loser.png"))
            loserCharacter_size = loserCharacter.get_rect().size 
            screen.blit(loserCharacter, (character_x_pos -8, character_y_pos - 20 ))  
            pygame.display.update() 
            pygame.time.delay(1000) 

            gameOver_result = pygame.image.load(os.path.join(image_path, "Gameover.png"))
            gameOver_result_size = gameOver_result.get_rect().size 
            screen.blit(gameOver_result, (250,200)) 
            pygame.display.update()

            pygame.time.delay(2000) 
            running = False #게임종료 
            break  

            #버블과 무기 충돌 처리  
        for weapon_idx, weapon_val in enumerate(weapons):   #무기 위치 정보 
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]
            #무기 rect 정보 업데이트 
            weapon_rect = weapon.get_rect()  #무기는 항상 동일한 것: 1개 
            weapon_rect.left = weapon_x_pos 
            weapon_rect.top = weapon_y_pos 

            #버블과 무기 충돌 시 
            if weapon_rect.colliderect(bubble_rect): 
                #총돌한 버블 소멸 
                weapon_to_remove = weapon_idx #해당 무기,버블 소멸을 위한 설정 
                bubble_to_remove= bubble_idx 
                #가장 작은 크기 버블 아닐 경우 
                if bubble_img_idx < 3: 
                    #현재 버블 크기 정보 로드 
                    bubble_width = bubble_rect.size[0]
                    bubble_height = bubble_rect.size[1]

                    #2개로 분할된 작은 버블 정보 
                    small_bubble_rect =  bubble_images[bubble_img_idx + 1].get_rect()
                    small_bubble_width =   small_bubble_rect.size[0]
                    small_bubble_height =  small_bubble_rect.size[1]

                    #왼쪽으로 바운스되는 작은 버블 
                    bubbles.append({   
                        "pos_x": bubble_pos_x + (bubble_width /2) - (small_bubble_width /2), 
                        "pos_y": bubble_pos_y + (bubble_height /2) - (small_bubble_height /2) , #버블 좌표 
                        "img_idx": bubble_img_idx + 1, #버블 이미지 인덱스 
                        "to_x": -4, "to_y":   -9,  #버블 좌우 이동
                        "init_spd_y": bubble_spd_y[bubble_img_idx + 1]}) #y좌표 최초 속도(튕길 떄)
                    #오른쪽으로 바운스되는 작은 버블 
                    bubbles.append({   
                        "pos_x": bubble_pos_x + (bubble_width /2) - (small_bubble_width /2), 
                        "pos_y": bubble_pos_y + (bubble_height /2) - (small_bubble_height /2) , #버블 좌표 
                        "img_idx": bubble_img_idx + 1, #버블 이미지 인덱스 
                        "to_x": 4, "to_y":  -9,  #버블 좌우 이동
                        "init_spd_y": bubble_spd_y[bubble_img_idx + 1]}) #y좌표 최초 속도(튕길 떄)
            
                break 
        else:  
            continue
        break 


            
    #버블과 무기가 서로 닿으면 1개씩만 항상 소멸됨: for문 밖에 위치 
    if bubble_to_remove> -1:  
        del bubbles[bubble_to_remove]               #버블 소멸 변수의 인덱스가 0,1,2,3 인 버블 리스트에 있는 값들이 지워짐
        bubble_to_remove = -1                  #다음 프레임에서 이 if문을 타야되기에 다시 버블 소멸 변수=-1지정 

    if weapon_to_remove > -1:                     #동일함 
        del weapons[weapon_to_remove] 
        weapon_to_remove = -1 
     
    #모든 버블 제거 시 미션 성공
    if len(bubbles) == 0: 
        pygame.mixer.music.stop() 
        oversound = pygame.mixer.music.load("C:/Users/www/OneDrive/바탕 화면/PythonWorkSpace/poppinggame/winSound.mp3") 
        pygame.mixer.music.play(1) #2번만 재생 
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.3)

        missionComplete = pygame.image.load(os.path.join(image_path, "missioncomplete.png"))
        missionComplete_size = missionComplete.get_rect().size 
        missionComplete_rect = missionComplete.get_rect(center = (int(screen_width/2), int(screen_height/2) + 10))

        #게임 성공 시 꽃 이미지 랜덤 그리기 
        flower_img = pygame.image.load(os.path.join(image_path, "flower.png"))
        flowers = [] 
        clock = pygame.time.Clock() 
        for i in range(25): 
            flower = flower_img.get_rect(left = random.randint(0,screen_width) - flower_img.get_width(), top = random.randint(0, screen_height) - flower_img.get_height()) 
            flowers.append(flower) 
        
        for flower in flowers: 
            screen.blit(flower_img, flower) 
        
        pygame.display.update() #모든 화면 그리기 
        clock.tick(60) 

        screen.blit(missionComplete, missionComplete_rect)
        pygame.display.update()
        pygame.time.delay(2000)

        Win = pygame.image.load(os.path.join(image_path, "Win.png"))
        Win_size = Win.get_rect().size 
        Win_rect = Win.get_rect(center = (int(screen_width/2), int(screen_height/2)))
        screen.blit(Win, Win_rect)
        pygame.display.update() 

        pygame.time.delay(2000) 
        running = False #while문 탈출 
    



   #5-화면 그리기 
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons: 
        screen.blit(weapon, [weapon_x_pos, weapon_y_pos])

    for idx, val in enumerate(bubbles): 
          bubble_pos_x = val["pos_x"]  #각각의 딕셔너리 값을 가져오기  
          bubble_pos_y = val["pos_y"]
          bubble_img_idx = val["img_idx"] #인덱스값을 받아와 bubble_img_idx에 저장
          screen.blit(bubble_images[bubble_img_idx], (bubble_pos_x, bubble_pos_y))


    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos)) 

     #시간계산 
    elapsed_time = (pygame.time.get_ticks() - Start_ticks) / 1000 
    Timer = game_font.render("Timer: {}".format(int(Total_time - elapsed_time)), True, (255,153,000)) 

    #타이머이미지 삽입 
    timerimage = pygame.image.load(os.path.join(image_path, "timerimage.png")) 
    timerimage_size = timerimage.get_rect().size 
    screen.blit(timerimage, (25,20))
    screen.blit(Timer,(50, 20))  

    if Total_time - elapsed_time <=0:  #0초이하 게임종료
        game_over_font = pygame.font.SysFont("bauhaus93", 80) 
        over_message = "Time Out!"  #출력 텍스트 
        TimeOver_msg = game_over_font.render(str(over_message), True, (255,000,204)) 
        TimeOver_msg_rect = TimeOver_msg.get_rect(center = (int(screen_width/2), int(screen_height/2)))
        screen.blit( TimeOver_msg, TimeOver_msg_rect)  
        running = False
    pygame.display.update()
pygame.time.delay(1000) 

pygame.quit() #pygame  종료 
 