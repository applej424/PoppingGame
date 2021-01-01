import os 
import pygame #pygame 모듈을 import 
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
pygame.mixer.music.play(-1,0.0) #사운드 재생 계속 
pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.2 ) #음량 설정


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
character_speed=10 #캐릭터 이동 속도 

weapon = pygame.image.load(os.path.join(image_path, "weapon.png")) #무기 삽입
weapon_size = weapon.get_rect().size  
weapon_width = weapon_size[0] #무기 가로 길이

#무기 여러 발 발사 
weapons = [] 
weapon_speed = 10 






#버블 이미지 리스트 
bubble_images = [ 
    pygame.image.load(os.path.join(image_path, "bubble1.png")),
    pygame.image.load(os.path.join(image_path, "bubble2.png")),
    pygame.image.load(os.path.join(image_path, "bubble3.png")),
    pygame.image.load(os.path.join(image_path, "bubble4.png"))
] 

#버블 크기에 따른 최초 스피드 
bubble_spd_y = [ -20, -17, -14, -10 ] #인덱스 0,1,2,3 해당하는 값

#버블 리스트 
bubbles = [] 
#bubble1을 버블 리스트에 삽입 
bubbles.append({   
    "pos_x": 50, "pos_y": 50, #버블 좌표 
    "img_idx": 0, #버블 이미지 인덱스 
    "to_x": 3, "to_y": -9,  #버블 좌우 이동
    "init_spd_y": bubble_spd_y[0] #y좌표 최초 속도(튕길 떄)
})




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
    if character_x_pos < 0:  #가로 
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


        if bubble_pos_x < 0 or bubble_pos_x > screen_width - bubble_width: #x좌표상 왼쪽 화면 밖과 오른쪽 화면 밖으로 나갈 떄 
            bubble_val["to_x"] = bubble_val["to_x"] * (-1) #버블 x좌표 반대로 뒤집기

        #버블이 무대에 닿았을 때 1번 
        if bubble_pos_y >= screen_height - stage_height - bubble_height: 
            bubble_val["to_y"] = bubble_val["to_y"] * (-1) 

        else: #튕기지 않을 떄: 속도 증가 
            bubble_val["to_y"] += 0.7 

        #실제 버블 위치 값
        bubble_val["pos_x"] += bubble_val["to_x"]
        bubble_val["pos_y"] += bubble_val["to_y"]



   #4-충돌 처리 
   
   #5-화면 그리기 
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons: 
        screen.blit(weapon, [weapon_x_pos, weapon_y_pos])

    for idx, val in enumerate(bubbles): 
          bubble_pos_x = val["pos_x"]  #각각의 딕셔너리 값을 가져옴 
          bubble_pos_y = val["pos_y"]
          bubble_img_idx = val["img_idx"] #인덱스값을 받아와 bubble_img_idx에 저장
          screen.blit(bubble_images[bubble_img_idx], (bubble_pos_x, bubble_pos_y))


    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos)) 

    pygame.display.update()


pygame.quit() #pygame  종료 
