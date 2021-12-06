import pygame
from pygame.locals import *
import random

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [900, 450]
screen = pygame.display.set_mode(size)

title = "My Game"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
k = 0
FPS = 60

mvKeys = [False, False, False, False]                           # Up Left Down Right
hold_atk_key = False
playerpos=[100,10]

arrows = []
atk_delay = False

player_rect = pygame.Rect(playerpos[0],playerpos[1],16,30)                     ## 플레이어 콜리더
player_foot_rect = pygame.Rect(playerpos[0],playerpos[1],16,3)                 ## 플레이어 점프를 위한 발 콜리더

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)
PINK = (255,0,255)


surf = pygame.Surface((32,32))                      #임시 이미지 저장공간(좌우반전용)
atk_surf = pygame.Surface((70,70))
atkUp_surf = pygame.Surface((70,70)) 

isBoundary = False
player_vely = 0


# 3.2 - 이미지 & 애니메이션 로드

bg = pygame.image.load("resources/images/BackGround.png").convert()
bgX = 0
bgY = 0
bg =pygame.transform.scale(bg, (bg.get_width()*2,bg.get_height()*2))

player_right = True


sheet = pygame.image.load('resources/images/Eri_Kasamoto.png').convert()                             ##플레이어 이미지시트
sheet.set_colorkey(WHITE)

sdSheet = pygame.image.load('resources/images/Rebel Soldier Bazooka.png').convert()                  ##모덴군 이미지시트
sdSheet.set_colorkey(WHITE)

sd2Sheet = pygame.image.load('resources/images/Soldier2.png').convert()                  ##모덴군 이미지시트
sd2Sheet.set_colorkey(WHITE)

tkSheet = pygame.image.load('resources/images/Tank.png').convert()                  ##탱크 이미지시트
tkSheet = pygame.transform.scale(tkSheet, (tkSheet.get_width()*3,tkSheet.get_height()*3))
tkSheet.set_colorkey(WHITE)

tkSheet2 = pygame.image.load('resources/images/Tank.png').convert()                  ##탱크 이미지시트
tkSheet2 = pygame.transform.scale(tkSheet2, (tkSheet2.get_width()*2,tkSheet2.get_height()*2))
tkSheet2.set_colorkey((0,248,0))

sandbagSheet = pygame.image.load('resources/images/Sandbag.png').convert()                  ##모래주머니 이미지시트
sandbagSheet = pygame.transform.scale(sandbagSheet, (sandbagSheet.get_width()*3,sandbagSheet.get_height()*3))
sandbagSheet.set_colorkey((16,216,128))

flyPlateSheet = pygame.image.load('resources/images/flyPlate.png').convert()                  ##공중발판 이미지시트
flyPlateSheet.set_colorkey(BLACK)

fireSheet = pygame.image.load('resources/images/Fire.png').convert()                ## 불 이미지시트
fireSheet.set_colorkey((0,248,0))

helicopterSheet = pygame.image.load('resources/images/Helicopter.png').convert()                ## 헬리콥터 이미지시트
helicopterSheet = pygame.transform.scale(helicopterSheet, (helicopterSheet.get_width()*2,helicopterSheet.get_height()*2))
helicopterSheet.set_colorkey(WHITE)

bossSheet = pygame.image.load('resources/images/Boss.png').convert()                ## 보스 이미지시트
bossSheet.set_colorkey(WHITE)


##플레이어 애니메이션 변수
idle_anim_sec = 0
idled = False
attack_anim_sec = 0
attacking = False
move_anim_sec = 0
moved = False
flied_anim_sec = 0
flied = False

cIdle = 0
nIdle = 3
cShoot = 0
nShoot = 3 ##
cMove1 = 0
nMove1 = 3               #상체
cMove2 = 0                  
nMove2 = 11              #하체

moveAnimPos = [(130,78,25,35),(153,78,26,35),(177,78,28,35),(203,78,26,35),
               (233,78,25,35),(265,78,26,35),(298,78,28,35),(325,78,26,35),
               (347,78,25,35),(372,78,26,35),(401,78,28,35),(435,78,26,35)]

##모덴군 애니메이션 변수
progress = 0
#  [x좌표, y좌표, width, height, 애니메이션타이머, 애니메이션현재, 애니메이션최대]
sdList = [[450,355,40.8,48,0,0,7,pygame.rect],[400,355,40.8,48,0,0,7,pygame.rect]]
sdBulList = []   

dropSD_sec = 0
sd2List = []
#sd2BulList = []  

#sd3List = []
#sd3BulList = []

ctk = 0
ntk = 4
#tkBulList = []
tkHP = 30
tkRect = pygame.Rect(0,0,0,0)


nfire = 7
fireList = []

chlc = 0
nhlc = 5
chlcBul = 0
nhlcBul = 4
hlcV = 1
hlcPhase = 0
hlcPosX = 5500
hlcPosY = 0
hlcHP = 30
hlcRect = pygame.Rect(0,0,0,0)

cbossLaugh = 0
nbossLaugh = 5
cbossRun = 0
nbossRun = 10
cbossJump = 0
nbossJump = 11
cbossShootH = 0
nbossShootH = 8
cbossShootV = 0
nbossShootV = 8
cbossDie = 0
nbossDie = 12
cbossKnife = 0
nbossKnife = 16
boosRect = pygame.Rect(0,0,0,0)

##발판들 설정
blockList = []
# 3.3 - 함수선언


        

# 4. 메인 이벤트
blockList.append((0,1700,50,300,20))
blockList.append((0,0,400,8000,20))
SB = 0
while SB == 0:
    # 프레임마다 초기화
    isBoundary = False
    # 4-1. FPS 설정
    clock.tick(FPS)
    screen.fill((50,50,50))
    
    # 4-1 배경 그리기
    screen.blit(bg, (0,0),(bgX,bgY,size[0],700))
    # 6.1.1 - 플레이어 & 적 애니메이션
    playerRect = pygame.Rect(playerpos[0],playerpos[1],25,35)
    

    
    #######################################################################테스트구간
    
    ## 직접 타격 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.1):
    #       cbossKnife += 1
    #       dropSD_sec = 0
    #       if cbossKnife == nbossKnife:
    #           cbossKnife = 0
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,300,55,55))
    # if cbossKnife >= 14:
    #     screen.blit(bossSheet,(500 - bgX,290),(171 + (cbossKnife-14)*84,1083,82,50))
    # elif cbossKnife >= 12:
    #     screen.blit(bossSheet,(500 - bgX,290),(7 + (cbossKnife-12)*81,1083,81,50))
    # elif cbossKnife >= 9:
    #     screen.blit(bossSheet,(501 - bgX,290),(290 + (cbossKnife-9)*81,1032,81,50))
    # elif cbossKnife >= 8:
    #     screen.blit(bossSheet,(490 - bgX,290),(4 + (cbossKnife-6)*97,1032,92,50))
    # elif cbossKnife >= 6:
    #     screen.blit(bossSheet,(485 - bgX,290),(6 + (cbossKnife-6)*97,1032,97,50))
    # elif cbossKnife >= 5:
    #     screen.blit(bossSheet,(485 - bgX,290),(4 + cbossKnife*81,980,100,50))
    # else:
    #     screen.blit(bossSheet,(500 - bgX,290),(4 + cbossKnife*81,980,81,50))
    ####################################
    
        
    ## 사망 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.1):
    #       cbossDie += 1
    #       dropSD_sec = 0
    #       if cbossDie == nbossDie:
    #           cbossDie = nbossDie - 1
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,300,55,55))
    # if cbossDie >= 6:
    #     screen.blit(bossSheet,(500 - bgX,295),(10 + (cbossDie-6)*82,1185,82,45))
    # else:
    #     screen.blit(bossSheet,(500 - bgX,290),(10 + cbossDie*85,1135,85,50))
    #########################################
    
    ## 대각선 사격 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.1):
    #       cbossShootV += 1
    #       dropSD_sec = 0
    #       if cbossShootV == nbossShootV:
    #           cbossShootV = 0
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,300,55,55))
    # if cbossShootV >= 5:
    #     screen.blit(bossSheet,(500 - bgX,290),(5 + (cbossShootV-5)*105,728,105,95))
    # else:
    #     screen.blit(bossSheet,(500 - bgX,290),(4 - cbossShootV%2*2 + cbossShootV*102,630,102,95))
    #######################
    
    ## 수평 사격 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.1):
    #       cbossShootH += 1
    #       dropSD_sec = 0
    #       if cbossShootH == nbossShootH:
    #           cbossShootH = 0
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,350,55,55))
    # if cbossShootH >= 4:
    #     screen.blit(bossSheet,(500 - bgX,335),(4 + (cbossShootH-4)*128,500,128,70))
    # else:
    #     screen.blit(bossSheet,(500 - bgX,335),(5 + cbossShootH*129,430,129,70))
    ######################
        
    ## 점프 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.1):
    #       cbossJump += 1
    #       dropSD_sec = 0
    #       if cbossJump == nbossJump:
    #           cbossJump = 0
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,335,55,55))
    # if cbossJump >= 8:
    #     screen.blit(bossSheet,(500 - bgX,335),(172 + (8 - cbossJump)*84,380,84,50))
    # elif cbossJump >= 4:
    #     screen.blit(bossSheet,(500 - bgX,335),(4 + (cbossJump-4)*84,380,84,50))
    # else:
    #     screen.blit(bossSheet,(500 - bgX,335),(4 + cbossJump*83,315,83,60))
    ################
    
    ## 뛰는 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.05):
    #       cbossRun += 1
    #       dropSD_sec = 0
    #       if cbossRun == nbossRun:
    #           cbossRun = 0
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,340,55,55))
    # if cbossRun >= 6:
    #     screen.blit(bossSheet,(500 - bgX,340),(4 + (cbossRun - 6)*85,158,85,55))
    # else:
    #     screen.blit(bossSheet,(500 - bgX,340),(6 + cbossRun*85,105,85,55))
    ##
    
    ## 웃는 모션 ##
    # dropSD_sec += 1/FPS
    # if(dropSD_sec > 0.2):
    #      cbossLaugh += 1
    #      dropSD_sec = 0
    #      if cbossLaugh == nbossLaugh:
    #          cbossLaugh = 0
    # boosRect = pygame.draw.rect(screen, GRAY,(500 - bgX,340,55,55))
    # screen.blit(bossSheet,(500 - bgX,340),(5 + cbossLaugh*84,0,84,55))
    ##############
    #####################################################################################
    
    #sdBulList.append([1,500-bgX,300 + 50*random.randint(0, 1),pygame.rect])

    # 장애물 & 블럭 그리기
    for block in blockList:
        pygame.draw.rect(screen,GRAY,(block[1] - bgX,block[2],block[3],block[4]))
    barricade = pygame.draw.rect(screen, GRAY, [1700 - bgX, 300, 10, 100])       # 바리게이트
    #if(progress == 3):
    #    tkRect = pygame.draw.rect(screen,GRAY,[3000 - bgX, 230, 222, 180])
    screen.blit(sandbagSheet,(1600 - bgX,250),(0,55,200,200))

#if player_vely > 0:
    onBlock = False
    for block in blockList:
        if player_foot_rect.colliderect((block[1] - bgX,block[2],block[3],block[4])):
            if player_vely > 0:
                flied = False
                player_vely = 0
            onBlock = True
    if not (onBlock):
        flied = True
#        if player_foot_rect.colliderect(b1) or player_foot_rect.colliderect(b2) or player_foot_rect.colliderect(b3) or player_foot_rect.colliderect(b4) or player_foot_rect.colliderect(b5):
#            flied = False
#            player_vely = 0
#    for block in blockList:
#      if not player_foot_rect.colliderect(block):
#          flied = True 
    
#    if not(player_foot_rect.colliderect(b1) or player_foot_rect.colliderect(b2) or player_foot_rect.colliderect(b3) or player_foot_rect.colliderect(b4) or player_foot_rect.colliderect(b5)):
#        flied = True
    
    if flied:
        playerpos[1] += player_vely
        if player_vely < 10:
            player_vely += 0.5
        idled = False
    else:
        player_vely = 0
        idled = True
        
    #if mvKeys[0]:
    #    surf.blit(sheet,(0,0),(85+cMove1*37,368,150,70))
    #else:
    #    screen.blit(sheet,playerpos,(4,113,34,32))       
    
    if flied:                               ##더 디테일 넣자         ##cflied nflied 추가
    
        surf.fill(WHITE)                
        surf.blit(sheet,(0,0),(4,136,35,35))
        if not player_right:
            surf = pygame.transform.flip(surf,True,False)
        surf.set_colorkey(WHITE)
        screen.blit(surf,(playerpos[0],playerpos[1] + 10))
        if not attacking:
            surf.fill(WHITE)
            if mvKeys[0]:
                surf.blit(sheet,(2,3),(85,368,150,70))
            else:
                surf.blit(sheet,(0,0),(4,113,35,35))
            if not player_right:
                surf = pygame.transform.flip(surf,True,False)
            screen.blit(surf,(playerpos[0],playerpos[1]))  
            
 
    if not(mvKeys[1] or mvKeys[3] or flied):
        idled = True
        if idled:                   #if idle anim
            idle_anim_sec += 1 / FPS

            if idle_anim_sec > 0.1:
                if cIdle >= nIdle:
                    cIdle = 0
                    idle_anim_sec = 0
                else:
                    cIdle += 1
                    idle_anim_sec = 0
            surf.fill(WHITE)
            surf.blit(sheet,(0,0),(4 + 4*35,12,35,35))
            if not player_right:
                surf = pygame.transform.flip(surf,True,False)
            surf.set_colorkey(WHITE)
            screen.blit(surf,(playerpos[0],playerpos[1] + 10)) 
            surf.fill(WHITE)
            if not(attacking):
                if mvKeys[0]:
                    surf.blit(sheet,(0,0),(85 + cIdle*37,368,150,70))
                elif cIdle == 2:
                    surf.blit(sheet,(0,0),(4 + cIdle*35,12,35,35))
                else:
                    surf.blit(sheet,(0,0),(3 + cIdle*35,12,35,35))
                if not player_right:
                    surf = pygame.transform.flip(surf,True,False)
            surf.set_colorkey(WHITE)
            screen.blit(surf,(playerpos[0],playerpos[1]))
    else:
        idled = False
        
    if (mvKeys[1] or mvKeys[3]) and not flied:
        moved = True
        if moved:
            move_anim_sec += 1 / FPS

        if move_anim_sec > 0.05:
            if cMove1 >= nMove1:
                cMove1 = 0
                move_anim_sec = 0
            else:
                cMove1 += 1
                move_anim_sec = 0
            if cMove2 >= nMove2:
                cMove2 = 0
                move_anim_sec = 0
            else:
                cMove2 += 1
                move_anim_sec = 0
        ## 이동 애니메이션
        if player_right:##오른쪽으로 이동
            screen.blit(sheet,(playerpos[0],playerpos[1]+10),moveAnimPos[cMove2])
        else:##왼쪽으로 이동
            surf.fill(WHITE)
            surf.blit(sheet,(0,0),moveAnimPos[cMove2])
            fsurf = pygame.transform.flip(surf,True,False)
            fsurf.set_colorkey(WHITE)
            screen.blit(fsurf,(playerpos[0],playerpos[1]+10))
            
        if not(attacking):
            surf.fill(WHITE)
            if mvKeys[0]:
                surf.blit(sheet,(0,0),(85+cMove1*37,368,150,70))
            else:
                if cMove1 == 2:
                    surf.blit(sheet,(0,0),(4 + cMove1*35,12,35,35))
                else:
                    surf.blit(sheet,(0,0),(3 + cMove1*35,12,35,35))
            if not player_right:
                surf = pygame.transform.flip(surf,True,False)
            surf.set_colorkey(WHITE)
            screen.blit(surf,(playerpos[0],playerpos[1]))
                    
    if attacking:
        if not(atk_delay):
            if mvKeys[0]:
                arrows.append([0,playerpos[0],playerpos[1] - 5])
            elif player_right:
                arrows.append([3,playerpos[0] + 10,playerpos[1] - 3])
            else:
                arrows.append([1,playerpos[0] - 10,playerpos[1] - 3])
            atk_delay = True
        attack_anim_sec += 1/FPS
        if attack_anim_sec > 0.01:
            if cShoot >= nShoot:
                cShoot = 0
                attack_anim_sec = 0
                atk_delay = False
                if hold_atk_key:
                    attacking = True
                else:
                    attacking = False
            else:
                cShoot += 1
                attack_anim_sec = 0
        
        if cShoot == nShoot:
            tmp = 43
        else:
            tmp = 62
        if moved:
            if cMove1 ==2:
                tmp += 1
            else:
                tmp = tmp

        atk_surf.fill(WHITE)
        atkUp_surf.fill(WHITE)
        if mvKeys[0]:
            atkUp_surf.fill(WHITE)
            atkUp_surf.blit(sheet,(0,0),(3 + cShoot*29,392,31,70))
        elif flied:
            atk_surf.blit(sheet,(0,0),(cShoot*59,330,tmp,33))
        else:
            atk_surf.blit(sheet,(0,0),(cShoot*59 + 3,333,tmp - 6,33))
        if not player_right:
            atk_surf = pygame.transform.flip(atk_surf,True,False)
            atkUp_surf = pygame.transform.flip(atkUp_surf,True,False)
        atk_surf.set_colorkey(WHITE)
        atkUp_surf.set_colorkey(WHITE)
        if mvKeys[0]:
            if player_right:
                screen.blit(atkUp_surf,(playerpos[0]-7,playerpos[1]-44))
            else:
                screen.blit(atkUp_surf,(playerpos[0]-31,playerpos[1]-44))
        else:
            if player_right:
                screen.blit(atk_surf,(playerpos[0],playerpos[1]))
            else:
                screen.blit(atk_surf,(playerpos[0]-40,playerpos[1]))
            
    ############################## 적 관련 애니메이션 ###################################
    ############################## 진행도에 따라 적 소환 ################################
    ############################## 몹 추가는 여기서 #####################################
    if progress == 0:
        if(bgX > 200):
            sdList.append([1100,355,40.8,48,0,0,7,pygame.rect])
            sdList.append([1200,355,40.8,48,0,0,7,pygame.rect])
            sdList.append([1300,355,40.8,48,0,0,7,pygame.rect])
            sd2List.append([450,0,pygame.rect])
            progress = 1
    elif progress == 1:
        if(bgX > 500):
            sdList.append([2000,355,40.8,48,0,0,7,pygame.rect])
            sdList.append([2200,300,40.8,48,0,0,7,pygame.rect])
            sdList.append([2300,355,40.8,48,0,0,7,pygame.rect])
            progress = 2
    elif progress == 2:
        dropSD_sec += 1/FPS
        if(dropSD_sec > 1):
            sd2List.append([random.randint(900,1300),0,pygame.rect])
            dropSD_sec = 0
        if bgX > 2000:
            progress = 3
            dropSD_sec = 0
    elif progress == 3:
        tkRect = pygame.draw.rect(screen,GRAY,[3000 - bgX, 230, 222, 180])
        dropSD_sec += 1/FPS
        if(dropSD_sec > 0.2):
            ctk += 1
            dropSD_sec = 0
            if ctk == ntk:
                sdBulList.append([1,3000-bgX,300 + 50*random.randint(0, 1),pygame.rect])
                ctk = 0
        screen.blit(tkSheet,(3000-bgX,230),(ctk*222,1260,222,180))
        if(tkRect.colliderect(playerRect)):
            playerpos[1] = 100
        if(tkHP < 0 ):
            progress = 4
            dropSD_sec = 0
    elif progress == 4:
        for i in range(0,19):
            fireList.append([3500 + 55*i,360,0,0])
        sdList.append([4460,305,40.8,48,0,0,7,pygame.rect])
        sdList.append([4270,105,40.8,48,0,0,7,pygame.rect])
        blockList.append((1,3500,300,68,10))
        blockList.append((1,3650,300,68,10))
        blockList.append((1,3800,350,68,10))
        blockList.append((1,3800,250,68,10))
        blockList.append((1,3950,210,68,10))
        blockList.append((1,3950,350,68,10))
        blockList.append((1,4100,170,68,10))
        blockList.append((1,4100,350,68,10))
        blockList.append((1,4250,150,68,10))
        blockList.append((1,4440,350,68,10))
        progress = 5
    elif progress == 5:
        for flyP in blockList:
            if flyP[0] == 1:
                screen.blit(flyPlateSheet,(flyP[1] - bgX - 9,flyP[2] - 70),(0,0,100,100))  
        if bgX > 5000:
            progress = 6
    elif progress == 6:
        dropSD_sec += 1/FPS
        if hlcPhase == 0:
            if hlcPosX > 5500:
                hlcV = 0
                hlcPhase = random.random()
            elif hlcPosX < 5050:
                hlcV = 1
        hlcPosX += hlcV * 200/FPS
        if 0 < hlcPhase  and hlcPhase < 0.7:
            if hlcPosY < 350:
                hlcPosY += 200/FPS
            else:
                if hlcPosX > 4850:
                    hlcPosX -= 700/FPS
                else:
                    hlcPhase = 1
        elif 0.7 <= hlcPhase and hlcPhase < 1:
            if hlcPosY < 300:
                hlcPosY += 200/FPS
            else: 
                if chlc == nhlc - 1 and dropSD_sec > 0.1:
                    chlcBul += 1
                    if chlcBul % 2 == 1:
                        sdBulList.append([1,hlcPosX-bgX,hlcPosY + 50,pygame.rect])
                    if chlcBul == nhlcBul*2:
                        chlcBul = 0
                        hlcPhase = 1
        elif hlcPhase == 1:
            if hlcPosY > 0:
                hlcPosY -= 200/FPS
            else:
                hlcPhase = 0
        hlcRect = pygame.draw.rect(screen,GRAY,[hlcPosX - bgX, hlcPosY, 110, 120])
        if(dropSD_sec > 0.1):
            chlc += 1
            dropSD_sec = 0
            if chlc == nhlc:
                #sdBulList.append([1,500-bgX,300 + 50*random.randint(0, 1),pygame.rect])
                chlc = 0
        screen.blit(helicopterSheet,(hlcPosX-bgX,hlcPosY),(20 + chlc*162,10,160,120))
        if(hlcRect.colliderect(playerRect)):
            playerpos[1] = 100
        if(hlcHP < 0 ):
            progress = 7
            dropSD_sec = 0
    #elif progress == 7:
        #if bgX > 6000:
            
    
        #screen.blit(flyPlateSheet,(3500 - bgX,200),(0,0,100,100))  
        #screen.blit(flyPlateSheet,(3600 - bgX,200),(0,0,100,100))  
        #screen.blit(flyPlateSheet,(3700 - bgX,250),(0,0,100,100))
        #screen.blit(flyPlateSheet,(3700 - bgX,150),(0,0,100,100))  
        
        
        ##################쫄병 적군 애니메이션#########################################
    for idx, sd in enumerate(sdList):   ## 수평 사격 모덴군
        sd[4] += 1 / FPS
        if sd[4] > 0.2:
            if sd[5] >= sd[6]:
                sd[5] = 0
                sd[4] = 0
            else:
                sd[5] += 1
                sd[4] = 0
                if(sd[5] == 5):
                    sdBulList.append([0,sd[0] - bgX,sd[1] + 20,pygame.rect])
        if sd[5] >= 5:
            sd[7] = pygame.draw.rect(screen,WHITE,(sd[0] - bgX + 10,sd[1] + 5,sd[2] - 10,sd[2]))
            screen.blit(sdSheet,(sd[0] - bgX,sd[1]),((sd[5]-5)*46,300,sd[2]+4,sd[3]))
        else:
            sd[7] = pygame.draw.rect(screen,WHITE,(sd[0] - bgX + 10,sd[1] + 5,sd[2] - 10,sd[2]))
            screen.blit(sdSheet,(sd[0] - bgX,sd[1]),(sd[5]*40.8,0,sd[2],sd[3]))
    for idx, sd in enumerate(sd2List):  ## 떨어지는 모덴군
        sd[1] += 4
        sd[2] = pygame.draw.rect(screen,WHITE,(sd[0] - bgX + 10,sd[1] + 15,50,20))
        screen.blit(sd2Sheet,(sd[0] - bgX,sd[1]),(0,440,68,40))
        if(sd[2].colliderect(playerRect)):
            playerpos[1] = 100
        if(sd[1] > 1000):
            del(sd2List[idx])
            
    for fire in fireList:   ## 불 애니메이션
        fire[2] += 1 / FPS
        if fire[2] > 0.1:
            if fire[3] >= nfire:
                fire[3] = 0
                fire[2] = 0
            else:
                fire[3] += 1
                fire[2] = 0
        fireRect = pygame.draw.rect(screen,GRAY,(fire[0] - bgX,fire[1] + 20,55,70))
        screen.blit(fireSheet,(fire[0] - bgX,fire[1]),(2 + fire[3]*55,2010,55,90))
        if(fireRect.colliderect(playerRect)):
            playerpos[1] = 100
        
#    for idx, sd3 in enumerate(sd3List):   ## 모덴군 수직
#        sd3[2] += 1 / FPS
        #if sd3[2] > 2:
         #   sd3BulList.append([sd3[0] - bgX,sd3[1]])
    

    

    # 4-2. 각종 입력 감지
        # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type==pygame.QUIT:
            # if it is quit the game
            SB = 1
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            #if event.key == K_UP:
            #    mvKeys[0] = True
            if event.key == K_LEFT:
                mvKeys[1] = True
                player_right = False
            #elif event.key == K_DOWN:
            #    mvKeys[2] = True
            elif event.key == K_RIGHT:
                mvKeys[3] = True
                player_right = True
            if event.key == K_UP:
                mvKeys[0] = True
            if event.key == K_z and not flied:                            #Jump
                flied = True
                player_vely = -10
            if event.key == K_x:
                attacking = True
                hold_atk_key = True 
                
            if event.key == K_ESCAPE:
                SB = 1
                pygame.quit() 
                exit(0) 
        if event.type == pygame.KEYUP:
            #if event.key==pygame.K_UP:
            #    mvKeys[0]=False
            if event.key==pygame.K_LEFT:
                mvKeys[1]=False
            #elif event.key==pygame.K_DOWN:
            #    mvKeys[2]=False
            elif event.key==pygame.K_RIGHT:
                mvKeys[3]=False
            if event.key == K_UP:
                mvKeys[0] = False
            if event.key == K_z:
                if player_vely < 0:
                    player_vely -=player_vely
            if event.key == K_x:
                hold_atk_key = False
                

    # 9 - 플레이어 이동 & Boss rect & 배경 이동
    if mvKeys[1]:
        #playerpos[0]-=2
        if(bgX > 2):
            bgX -=2 #2
        elif bgX <= 2:
            bgX = 2
            isBoundary = True
    elif mvKeys[3]:
        #playerpos[0]+=2
        bgX +=2 #2
    if progress == 6:
        if bgX <= 4800:
            bgX = 4800
            isBoundary = True
        elif bgX >= 5500:
            bgX = 5500
            isBoundary = True

    player_rect.x = playerpos[0] + 8
    if player_vely >0:
        player_rect.y = playerpos[1] + 17
    else:
        player_rect.y = playerpos[1] + 7

    player_foot_rect.x = playerpos[0] + 8
    player_foot_rect.y = playerpos[1] + 40
    
    if(playerpos[1] > 500):
        playerpos[1] = 0
    
    #배경이동

    #if (playerpos[0] > bgX + size[0]):
       #bgX = playerpos[0]-size[0]
        

    # 10 - 총알 이동 및 판정
    #index = 0
    for idx, bullet in enumerate(arrows):   # 플레이어 총알 판정
        if bullet[0] == 0:
            bullet[2] -= 10
            if not isBoundary:
                if mvKeys[1]:
                    bullet[1] += 2
                elif mvKeys[3]:
                    bullet[1] -= 2
        elif bullet[0] == 1:
            bullet[1] -= 10
        elif bullet[0] == 3:
            bullet[1] += 10
        if bullet[1] < -50 or bullet[1] > size[0] + 50 or bullet[2] < -50:
            del arrows[idx]
            #index -= 1
        #index += 1 projectile
    #for idx, projectile in enumerate(arrows):
        surf.fill(WHITE)
        surf.blit(sheet,(0,0),(155,330,25,33))
        bulRect = pygame.draw.rect(screen,WHITE,(bullet[1] + 12,bullet[2] + 13,5,5))
        if(bulRect.colliderect(barricade)):
            del arrows[idx]
        if progress == 3:
            if(bulRect.colliderect(tkRect)):
                del arrows[idx]
                tkHP -= 1
        if progress == 6:
            if(bulRect.colliderect(hlcRect)):
                del arrows[idx]
                hlcHP -= 1
        if bullet[0] == 0:
            surf = pygame.transform.rotate(surf, 90)
        elif bullet[0] == 1:
            surf = pygame.transform.flip(surf,True,False)
        surf.set_colorkey(WHITE)
        screen.blit(surf,(bullet[1],bullet[2]))
        for idx2,sdR in enumerate(sdList):
            if(bulRect.colliderect(sdR[7])):
                del arrows[idx]
                del sdList[idx2]
        for idx2,sdR in enumerate(sd2List):
            if(bulRect.colliderect(sdR[2])):
                del arrows[idx]
                del sd2List[idx2]
    for idx, sdBul in enumerate(sdBulList):
        if mvKeys[1]:
            if(bgX > 2):
                sdBul[1] += 2
                if progress == 6 and bgX <= 4800:
                    sdBul[1] -= 2
        elif mvKeys[3]:
            #playerpos[0]+=2
            sdBul[1] -= 2
        sdBul[1] -= 5
        if sdBul[0] == 0:
            bulRect = pygame.draw.circle(screen,WHITE,(sdBul[1],sdBul[2]),5)
        elif sdBul[0] == 1:
            bulRect = pygame.draw.rect(screen,WHITE,(sdBul[1],sdBul[2],70,50))
            screen.blit(tkSheet2,(sdBul[1],sdBul[2]),(500,1800,100,50))
        if(bulRect.colliderect(playerRect)):
            playerpos[1] = 100
            del sdBulList[idx]
        if(sdBul[1] < -50):
            del sdBulList[idx]
    
    # for idx, tkBul in enumerate(tkBulList):
    #     if mvKeys[1]:
    #         if(bgX > 2):
    #             tkBul[0] += 2
    #     elif mvKeys[3]:
    #         #playerpos[0]+=2
    #         tkBul[0] -= 2
    #     tkBul[0] -= 4
    #     bulRect = pygame.draw.rect(screen,WHITE,(tkBul[0],tkBul[1],70,50))
    #     screen.blit(tkSheet2,(tkBul[0],tkBul[1]),(500,1800,100,50))
    #     if(bulRect.colliderect(playerRect)):
    #         playerpos[1] = 100
    #         del tkBulList[idx]
    #     if(tkBul[0] < -50):
    #         del tkBulList[idx]
            
#    for idx, sd3Bul in enumerate(sd3BulList):
#        if mvKeys[1]:
#            if(bgX > 2):
#                sd3Bul[0] += 2
#        elif mvKeys[3]:
#            #playerpos[0]+=2
#            sd3Bul[0] -= 2
#        sd3Bul[1] += 4
#        bulRect = pygame.draw.rect(screen,WHITE,(sd3Bul[0],sd3Bul[1],10,10))
#        #screen.blit(sd3,(tkBul[0],tkBul[1]),(500,1800,100,50))
#        if(bulRect.colliderect(playerRect)):
#            playerpos[1] = 100
#            del sd3BulList[idx]
#        if(sd3Bul[1] > 1000):
#            del sd3BulList[idx]
            


    # 4-3. 입력, 시간에 따른 변화


    # 4-4. 그리기
    #screen.fill(color)

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()