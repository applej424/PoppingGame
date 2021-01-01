import os 
import pygame #pygame 모듈을 import 
import time # 00초 후에 플레이 종료하는 경우 
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
#######################################################################################
#1-사용자 게임 초기화: 배경화면, 캐릭터이미지, 좌표/속도/폰트 설정 등 
current_path = os.path.dirname(__file__) #현재 파일 위치 반환 
image_path = os.path.join(current_path,"images") #image 폴더 위치 반환 
#music_path = os.path.join(current_path, "music") #music 폴더 위치 반환 
    
    #사운드 
pygame.mixer.init() 
pygame.mixer.music.load ("C:/Users/www/OneDrive/바탕 화면/PythonWorkSpace/poppinggame/Wake Up.mp3") #배경음악 
pygame.mixer.music.play(-1,0.0) #사운드 재생 계속 
pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.2 ) #음량 설정
game_over_sound = pygame.mixer.Sound("C:/Users/www/OneDrive/바탕 화면/PythonWorkSpace/poppinggame/Mario.wav") #게임 종료 사운드 
#pygame.mixer.Sound.play(game_over_sound)
#game_over_sound.set_volume(0.1) #음량 

##########################################################################################
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

character_to_x=0  #캐릭터 이동 방향 
character_speed=8 #캐릭터 이동 속도 

weapon = pygame.image.load(os.path.join(image_path, "weapon.png")) #무기 삽입
weapon_size = weapon.get_rect().size  
weapon_width = weapon_size[0] #무기 가로 길이

#무기 여러 발 발사 
weapons = [] 
weapon_speed = 10


#이벤트 루프 
running = True 

while running:
    dt = clock.tick_busy_loop(80) 
    print("fps는 " + str(clock.get_fps()))


    #2-이벤트 처리: 키보드 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN: #키 누를 때 
            #방향키 
            if event.key == pygame.K_LEFT: #왼쪽 이동 
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: #오른쪽 이동 
                character = pygame.image.load(os.path.join(image_path, "characterRightKey.png"))
                character_to_x += character_speed 
                break 
            elif event.key == pygame.K_SPACE: #스페이스 클릭 시 무기발사 
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos]) #무기 리스트에 생성한 무기 추가 


        if event.type == pygame.KEYUP: #키 동작 해제
            if event.key == pygame.K_LEFT or pygame.K_RIGHT: 
                character_to_x = 0 #움직이지지 않음 


        if not pygame.mixer.music.get_busy(): #소리가 섞여있지 않을 경우 
                pygame.mixer.music.fadeout(2000) #배경음악 fadeout 
                pygame.time.delay(1000)
                running = False 




   #3-캐릭터 위치 정의 
    character_x_pos += character_to_x

    #화면 경계값 처리 
    if character_x_pos < 0:  #가로 
        character_x_pos = 0 
    elif character_x_pos > screen_width - character_width: 
        character_x_pos = screen_width - character_width
    
    #무기 위치 설정 
    weapons = [ [w[0], w[1] - weapon_speed ]  for w in weapons ] #위로 쏘아올리기 
    #천장에 닿으면 소멸 
    weapons = [ [w[0], w[1]]  for w in weapons if w[1] > 0 ] 




    
   #4-충돌 처리 
   
   #5-화면 그리기 
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons: 
        screen.blit(weapon, [weapon_x_pos, weapon_y_pos])

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()


pygame.quit() #pygame  종료 
