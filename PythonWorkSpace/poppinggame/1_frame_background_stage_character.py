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



current_path = os.path.dirname(__file__)  
image_path = os.path.join(current_path,"images")
background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png")) #무대 삽입 
stage_size = stage.get_rect().size 
stage_height = stage_size[1] #무대 위에 캐릭터 위치시키기 위해 사용 
 

character = pygame.image.load(os.path.join(image_path, "character.png")) #캐릭터 삽입 
character_size = character.get_rect().size 
character_width = character_size[0]  #캐릭터 크기 
character_height = character_size[1] 
character_x_pos = (screen_width/2)-(character_width/2)   #캐릭터 좌표 
character_y_pos = screen_height - character_height - (stage_height-30)






#이벤트 루프 
running = True 
while running:
    dt = clock.tick_busy_loop(80) 
    print("fps는 " + str(clock.get_fps()))

    #2-이벤트 처리: 키보드 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
        
   #3-캐릭터 위치 설정 
    
   #4-충돌 처리 
   

    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos)) 
    pygame.display.update()
    
pygame.quit()
