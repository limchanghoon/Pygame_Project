import pygame
from pygame.locals import *
import random
from typing import List

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [900, 450]
screen = pygame.display.set_mode(size)

title = "Metal Slug Zero"
pygame.display.set_caption(title)

# 3.1 게임 내 필요한 설정
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
RED = (255,0,0)


surf = pygame.Surface((32,32))                      #임시 이미지 저장공간(좌우반전용)
atk_surf = pygame.Surface((70,70))
atkUp_surf = pygame.Surface((70,70)) 

isBoundary = False
player_vely = 0

screenLock = False


# 3.2 - 이미지 & 애니메이션 로드
lobySheet = pygame.image.load('resources/images/loby.jpg').convert()                ## 로비 이미지시트
bg = pygame.image.load("resources/images/BackGround.png").convert()                 ## 배경 이미지시트
bgX = 0
bgY = 0
bg =pygame.transform.scale(bg, (bg.get_width()*2,bg.get_height()*2))


healthbar = pygame.image.load("resources/images/healthbar2.png").convert()
healthbar = pygame.transform.scale(healthbar, (healthbar.get_width()*4,healthbar.get_height()))

health = pygame.image.load("resources/images/health.png").convert()
health = pygame.transform.scale(health, (health.get_width()*14,health.get_height()))

healthvalue = 0


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

eriLastSheet = pygame.image.load('resources/images/eri.png').convert()                ## 엔딩 이미지시트
rovingLastSheet = pygame.image.load('resources/images/Tarma Roving.png').convert()                ## 엔딩 이미지시트

# 3.3 - 사운드 로드

lobyBGM = pygame.mixer.Sound('resources/sounds/02 The Military System.mp3')
stage1BGM = pygame.mixer.Sound('resources/sounds/08 Ridge 256.mp3')
boss1BGM = pygame.mixer.Sound('resources/sounds/04 Steel Beast.mp3')
shootSound = pygame.mixer.Sound('resources/sounds/shootSound.mp3')
genDieSound = pygame.mixer.Sound('resources/sounds/gen_07.wav')
tankShootSound = pygame.mixer.Sound('resources/sounds/tankShoot.mp3')
hittedTankSound = pygame.mixer.Sound('resources/sounds/hittedTank.mp3')
eriDeathSound = pygame.mixer.Sound('resources/sounds/EriDeath.wav')
boomSound = pygame.mixer.Sound('resources/sounds/boom.mp3')
mission1StartSound = pygame.mixer.Sound('resources/sounds/misson1Start.mp3')
missionCompleteSound = pygame.mixer.Sound('resources/sounds/missionComplete.mp3')
clearBGM = pygame.mixer.Sound('resources/sounds/05 Carry Out.mp3')
allenDieSound = pygame.mixer.Sound('resources/sounds/allenDie.mp3')
allenKnifeSound = pygame.mixer.Sound('resources/sounds/allenKnife.mp3')
allenShootSound = pygame.mixer.Sound('resources/sounds/allenShoot.mp3')
allenS1Sound = pygame.mixer.Sound('resources/sounds/allenS1.mp3')
allenS2Sound = pygame.mixer.Sound('resources/sounds/allenS2.mp3')
allenS3Sound = pygame.mixer.Sound('resources/sounds/allenS3.mp3')
allenHaSound = pygame.mixer.Sound('resources/sounds/hahaha.mp3')
coinSound = pygame.mixer.Sound('resources/sounds/coinSound.mp3')

##플레이어 애니메이션 변수
coin = 1
death = 0
myFont = pygame.font.SysFont( "arial", 30, True, False)

player_right = True
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

ctk = 0
ntk = 4

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

timer = 0
################발판들 리스트##########
blockList = []
#################### 3.3 - 함수선언 및 클래스 선언#############################
def eriDeath():
    global death
    playerpos[1] = 100
    death += 1
    eriDeathSound.play()
    
class Mob:
    def hit(self):
        self.hp -=1
        hittedTankSound.play()
class Allen(Mob):
    def __init__(self):
        self.isLeft = True
        self.posX = 500
        self.posY = 340
        self.changePattern = True
        self.pattern = 0
        self.maxHp = 56
        self.hp = self.maxHp
        self.cbossLaugh = 0
        self.nbossLaugh = 5
        self.cbossRun = 0
        self.nbossRun = 10
        self.cbossJump = 0
        self.nbossJump = 11
        self.cbossShootH = 0
        self.nbossShootH = 8
        self.cbossShootD = 0
        self.nbossShootD = 8
        self.cbossDie = 0
        self.nbossDie = 12
        self.cbossKnife = 0
        self.nbossKnife = 16
        self.bossRect = pygame.Rect(0,0,0,0)
        self.randomSound = 0
        
    def getRect(self):
        return self.bossRect
    
    def playRandomSound(self):
        if self.randomSound == 0:
            allenS1Sound.play()
            self.randomSound = 1
        elif self.randomSound == 1:
            allenS2Sound.play()
            self.randomSound = 2
        elif self.randomSound == 2:
            allenS3Sound.play()
            self.randomSound = 0

    def knifing(self,_timer):
        _timer += 1/FPS
        if(_timer > 0.1):
              self.cbossKnife += 1
              _timer = 0
              if self.cbossKnife == 4 or self.cbossKnife == 7:
                  allenKnifeSound.play()
              if self.cbossKnife == self.nbossKnife:
                  self.cbossKnife = 0
                  self.changePattern = True
                  self.playRandomSound()
        self.bossRect = pygame.Rect((self.posX,345,55,55))
        
        boss_surf = pygame.Surface((100,50))
        boss_surf.fill(WHITE)
        
        if self.cbossKnife >= 14:
            boss_surf.blit(bossSheet,(0,0),(171 + (self.cbossKnife-14)*84,1083,82,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*50,354)) 
            #screen.blit(bossSheet,(500,340),(171 + (self.cbossKnife-14)*84,1083,82,50))
        elif self.cbossKnife >= 12:
            boss_surf.blit(bossSheet,(0,0),(7 + (self.cbossKnife-12)*81,1083,81,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*50,354)) 
            #screen.blit(bossSheet,(500,340),(7 + (self.cbossKnife-12)*81,1083,81,50))
        elif self.cbossKnife >= 9:
            boss_surf.blit(bossSheet,(0,0),(290 + (self.cbossKnife-9)*81,1032,81,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX + 1 - self.isLeft*52,354)) 
            #screen.blit(bossSheet,(501,340),(290 + (self.cbossKnife-9)*81,1032,81,50))
        elif self.cbossKnife >= 8:
            boss_surf.blit(bossSheet,(0,0),(4 + (self.cbossKnife-6)*97,1032,92,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - 10 - self.isLeft*30,354)) 
            #screen.blit(bossSheet,(490,340),(4 + (self.cbossKnife-6)*97,1032,92,50))
        elif self.cbossKnife >= 6:
            boss_surf.blit(bossSheet,(0,0),(6 + (self.cbossKnife-6)*97,1032,97,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - 15 - self.isLeft*20,354)) 
            #screen.blit(bossSheet,(485,340),(6 + (self.cbossKnife-6)*97,1032,97,50))
        elif self.cbossKnife >= 5:
            boss_surf.blit(bossSheet,(0,0),(4 + self.cbossKnife*81,980,100,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - 15 - self.isLeft*20,354)) 
            #screen.blit(bossSheet,(485,340),(4 + self.cbossKnife*81,980,100,50))
        else:
            boss_surf.blit(bossSheet,(0,0),(4 + self.cbossKnife*81,980,81,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*50,354)) 
            #screen.blit(bossSheet,(500,340),(4 + self.cbossKnife*81,980,81,50))
        if self.cbossKnife >= 4 and self.cbossKnife <= 7:
            knifeRect = pygame.Rect((self.posX,self.posY + 25,55,20))
            if(knifeRect.colliderect(playerRect)):
                eriDeath()
        return _timer
    
    def shootH(self,_timer):
        _timer += 1/FPS
        if(_timer > 0.1):
              if self.cbossShootH == 0:
                  allenShootSound.play()
              sdBulList.append([2,self.posX + 45 - self.isLeft*45,self.posY + 40,pygame.rect,self.isLeft])
              self.cbossShootH += 1
              _timer = 0
              if self.cbossShootH == self.nbossShootH:
                  self.cbossShootH = 0
                  self.changePattern = True
                  self.playRandomSound()
        self.bossRect = pygame.Rect((self.posX,345,55,55))
        boss_surf = pygame.Surface((129,70))
        boss_surf.fill(WHITE)
        if self.cbossShootH >= 4:
            #screen.blit(bossSheet,(500,325),(4 + (self.cbossShootH-4)*128,500,128,70))
            boss_surf.blit(bossSheet,(0,0),(4 + (self.cbossShootH-4)*128,500,128,70))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*75,336))
        else:
            #screen.blit(bossSheet,(500,325),(5 + self.cbossShootH*129,430,129,70))
            boss_surf.blit(bossSheet,(0,0),(5 + self.cbossShootH*129,430,129,70))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*75,336))
        return _timer
    
    def shootD(self,_timer):
        _timer += 1/FPS
        if(_timer > 0.1):
              if self.cbossShootD == 0:
                  allenShootSound.play()
              sdBulList.append([3,self.posX + 45 - self.isLeft*45,self.posY + 20,pygame.rect,self.isLeft])
              self.cbossShootD += 1
              _timer = 0
              if self.cbossShootD == self.nbossShootD:
                  self.cbossShootD = 0
                  self.changePattern = True
                  self.playRandomSound()
        self.bossRect = pygame.Rect((self.posX,345,55,55))
        boss_surf = pygame.Surface((105,95))
        boss_surf.fill(WHITE)
        if self.cbossShootD >= 5:
            #screen.blit(bossSheet,(500,300),(5 + (self.cbossShootD-5)*105,728,105,95))
            boss_surf.blit(bossSheet,(0,0),(5 + (self.cbossShootD-5)*105,728,105,95))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*50,309))
        else:
            #screen.blit(bossSheet,(500,300),(4 - self.cbossShootD%2*2 + self.cbossShootD*102,630,102,95))
            boss_surf.blit(bossSheet,(0,0),(4 - self.cbossShootD%2*2 + self.cbossShootD*102,630,102,95))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*50,309))
        return _timer
    
    def jump(self,_timer): ## 점프 왼쪽 구현 X 적용 X
        _timer += 1/FPS
        if(_timer > 0.1):
              self.cbossJump += 1
              _timer = 0
              if self.cbossJump == self.nbossJump:
                  self.cbossJump = 0
                  self.changePattern = True
                  self.playRandomSound()
        self.bossRect = pygame.Rect((self.posX,345,55,55))
        if self.cbossJump >= 8:
            screen.blit(bossSheet,(self.posX,340),(172 + (8 - self.cbossJump)*84,380,84,50))
        elif self.cbossJump >= 4:
            screen.blit(bossSheet,(self.posX,340),(4 + (self.cbossJump-4)*84,380,84,50))
        else:
            screen.blit(bossSheet,(self.posX,340),(4 + self.cbossJump*83,315,83,60))
        return _timer
    
    def run(self,_timer):
        _timer += 1/FPS
        if(_timer > 0.05):
              self.cbossRun += 1
              _timer = 0
              if self.cbossRun == self.nbossRun:
                  self.cbossRun = 0
                  self.changePattern = True
        if self.isLeft:
            self.posX -= 2
        else:
            self.posX += 2
        self.bossRect = pygame.Rect((self.posX,345,55,55))
        boss_surf = pygame.Surface((85,55))
        boss_surf.fill(WHITE)
        if self.cbossRun >= 6:
            #screen.blit(bossSheet,(500,340),(4 + (self.cbossRun - 6)*85,158,85,55))
            boss_surf.blit(bossSheet,(0,0),(4 + (self.cbossRun - 6)*85,158,85,55))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*35,350))
        else:
            #screen.blit(bossSheet,(500,340),(6 + self.cbossRun*85,105,85,55))
            boss_surf.blit(bossSheet,(0,0),(6 + self.cbossRun*85,105,85,55))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*35,350))
        return _timer
    
    def laugh(self,_timer):
        _timer += 1/FPS
        if(_timer > 0.2):
              self.cbossLaugh += 1
              _timer = 0
              if self.cbossLaugh == self.nbossLaugh:
                  self.cbossLaugh = 0
                  self.changePattern = True
        #self.bossRect = pygame.draw.rect(screen, GRAY,(self.posX,345,55,55))
        #screen.blit(bossSheet,(self.posX,340),(5 + self.cbossLaugh*84,0,84,55))
        boss_surf = pygame.Surface((84,55))
        boss_surf.fill(WHITE)
        boss_surf.blit(bossSheet,(0,0),(5 + self.cbossLaugh*84,0,84,55))
        if self.isLeft:
            boss_surf = pygame.transform.flip(boss_surf,True,False)
        boss_surf.set_colorkey(WHITE)
        screen.blit(boss_surf,(self.posX - self.isLeft*35,350))
            
        return _timer
    
    def die(self,_timer):
        _timer += 1/FPS
        if(_timer > 0.1):
              self.cbossDie += 1
              _timer = 0
              if self.cbossDie == self.nbossDie:
                  self.cbossDie = self.nbossDie - 1
                  self.changePattern = True
        #self.bossRect = pygame.draw.rect(screen, GRAY,(self.posX,345,55,55))
        boss_surf = pygame.Surface((85,50))
        boss_surf.fill(WHITE)
        if self.cbossDie >= 6:
            #screen.blit(bossSheet,(500,335),(10 + (self.cbossDie-6)*82,1185,82,45))
            boss_surf.blit(bossSheet,(0,0),(10 + (self.cbossDie-6)*82,1185,82,45))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*35,358))
        else:
            boss_surf.blit(bossSheet,(0,0),(10 + self.cbossDie*85,1135,85,50))
            if self.isLeft:
                boss_surf = pygame.transform.flip(boss_surf,True,False)
            boss_surf.set_colorkey(WHITE)
            screen.blit(boss_surf,(self.posX - self.isLeft*35,353))
        return _timer
mobList : List[Mob] = []

####################### 4.0 로비 ##############################################

lobyBGM.play(-1)
SB = 0
while SB == 0:
    screen.fill((50,50,50))
    screen.blit(lobySheet, (0,0),(0,0,size[0],size[1]))
    text_Title = myFont.render("{}".format(coin), True, WHITE)
    screen.blit(text_Title, [650, 410])
    text_Manipulation = myFont.render("Rudder : Move , z : Jump , x : Shoot", True, WHITE)
    screen.blit(text_Manipulation, [10, 10])
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            SB = 1
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                SB = 1
                pygame.quit() 
                exit(0) 
            if event.key == K_5:
                coinSound.play()
                coin += 1
            if event.key == K_1:
                SB = 1
###################### 4. 메인 이벤트##########################################
lobyBGM.stop()
stage1BGM.play(-1)
mission1StartSound.play()
blockList.append((0,0,400,8000,20))
SB = 0
while SB == 0:
    # 프레임마다 초기화
    isBoundary = False
    # 4.1. 프레임 설정 FPS
    clock.tick(FPS)
    screen.fill((50,50,50))
    
    # 4.1 배경 그리기
    screen.blit(bg, (0,0),(bgX,bgY,size[0],700))
    # 4.1.1 - 플레이어 & 적 애니메이션
    playerRect = pygame.Rect(playerpos[0],playerpos[1],25,35)

    # 장애물 & 블럭 그리기
    for block in blockList:
        pygame.Rect((block[1] - bgX,block[2],block[3],block[4]))
    barricade = pygame.Rect(1700 - bgX, 300, 10, 100)       # 바리게이트
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

    
    if flied:
        playerpos[1] += player_vely
        if player_vely < 10:
            player_vely += 0.5
        idled = False
    else:
        player_vely = 0
        idled = True
        
    
    
    if flied:                              
    
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
            shootSound.play()
            atk_delay = True
        attack_anim_sec += 1/FPS
        if attack_anim_sec > 0.04:
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
        tkRect = pygame.Rect([3000 - bgX, 230, 222, 180])
        dropSD_sec += 1/FPS
        if(dropSD_sec > 0.2):
            ctk += 1
            dropSD_sec = 0
            if ctk == ntk:
                sdBulList.append([1,3000-bgX,300 + 50*random.randint(0, 1),pygame.rect])
                tankShootSound.play()
                ctk = 0
        screen.blit(tkSheet,(3000-bgX,230),(ctk*222,1260,222,180))
        if(tkRect.colliderect(playerRect)):
            eriDeath()
        if(tkHP < 0 ):
            boomSound.play()
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
                        tankShootSound.play()
                    if chlcBul == nhlcBul*2:
                        chlcBul = 0
                        hlcPhase = 1
        elif hlcPhase == 1:
            if hlcPosY > 0:
                hlcPosY -= 200/FPS
            else:
                hlcPhase = 0
        hlcRect = pygame.Rect([hlcPosX - bgX, hlcPosY, 110, 120])
        if(dropSD_sec > 0.1):
            chlc += 1
            dropSD_sec = 0
            if chlc == nhlc:
                #sdBulList.append([1,500-bgX,300 + 50*random.randint(0, 1),pygame.rect])
                chlc = 0
        screen.blit(helicopterSheet,(hlcPosX-bgX,hlcPosY),(20 + chlc*162,10,160,120))
        if(hlcRect.colliderect(playerRect)):
            eriDeath()
        if(hlcHP < 0 ):
            boomSound.play()
            progress = 7
            dropSD_sec = 0
    elif progress == 7:
        if bgX > 6100:  ## 보스전 이벤트시작
            for idx,flyP in enumerate(blockList):
                if flyP[0] == 1:
                    del blockList[idx]
            stage1BGM.stop()
            allenHaSound.play()
            screenLock = True
            allen = Allen()
            mobList.append(allen)
            progress = 8
    elif progress == 8:
        timer = allen.laugh(timer)
        dropSD_sec += 1/FPS
        if dropSD_sec > 2 :
            blockList.append((1,6300,300,68,10))
            blockList.append((1,6400,300,68,10))
            blockList.append((1,6300,200,68,10))
            blockList.append((1,6400,200,68,10))
            blockList.append((1,6550,300,68,10))
            blockList.append((1,6700,300,68,10))
            blockList.append((1,6800,300,68,10))
            blockList.append((1,6700,200,68,10))
            blockList.append((1,6800,200,68,10))
            progress = 9
            boss1BGM.play()
    elif progress == 9:
        for flyP in blockList:
            if flyP[0] == 1:
                screen.blit(flyPlateSheet,(flyP[1] - bgX - 9,flyP[2] - 70),(0,0,100,100))  
        healthvalue = allen.hp
        if allen.changePattern:
            allen.pattern = random.random()
            allen.changePattern = False
        if(allen.hp <= 0):
            del mobList[0]
            boss1BGM.stop()
            dropSD_sec = 0
            allenDieSound.play()
            progress = 10
        else:
            if playerpos[0] <= allen.posX:
                allen.isLeft = True
            else:
                allen.isLeft = False
                
            if allen.pattern > 0.8:
                timer = allen.knifing(timer)
            elif allen.pattern > 0.7:
                timer = allen.shootD(timer)
            elif allen.pattern > 0.5:
                timer = allen.shootH(timer)
            else:
                timer = allen.run(timer)
        ################보스 체력바###################
        screen.blit(healthbar, (60,10))
        for health1 in range(healthvalue):
            screen.blit(health, (health1*14 + 72,13))
    elif progress == 10:
        dropSD_sec += 1/FPS
        if dropSD_sec > 2 :
            progress = 11
            missionCompleteSound.play()
            clearBGM.play()
            dropSD_sec = 0
        timer = allen.die(timer)
        for flyP in blockList:
            if flyP[0] == 1:
                screen.blit(flyPlateSheet,(flyP[1] - bgX - 9,flyP[2] - 70),(0,0,100,100))
    elif progress == 11:
        dropSD_sec += 1/FPS
        if dropSD_sec > 7 :
            SB = 1
        timer = allen.die(timer)
        for flyP in blockList:
            if flyP[0] == 1:
                screen.blit(flyPlateSheet,(flyP[1] - bgX - 9,flyP[2] - 70),(0,0,100,100))  

        
        
################################쫄병 적군 애니메이션#########################################
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
            sd[7] = pygame.Rect((sd[0] - bgX + 10,sd[1] + 5,sd[2] - 10,sd[2]))
            screen.blit(sdSheet,(sd[0] - bgX,sd[1]),((sd[5]-5)*46,300,sd[2]+4,sd[3]))
        else:
            sd[7] = pygame.Rect((sd[0] - bgX + 10,sd[1] + 5,sd[2] - 10,sd[2]))
            screen.blit(sdSheet,(sd[0] - bgX,sd[1]),(sd[5]*40.8,0,sd[2],sd[3]))
    for idx, sd in enumerate(sd2List):  ## 떨어지는 모덴군
        sd[1] += 4
        sd[2] = pygame.Rect((sd[0] - bgX + 10,sd[1] + 15,50,20))
        screen.blit(sd2Sheet,(sd[0] - bgX,sd[1]),(0,440,68,40))
        if(sd[2].colliderect(playerRect)):
            eriDeath()
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
        fireRect = pygame.Rect((fire[0] - bgX,fire[1] + 20,55,70))
        screen.blit(fireSheet,(fire[0] - bgX,fire[1]),(2 + fire[3]*55,2010,55,90))
        if(fireRect.colliderect(playerRect)):
            eriDeath()

    

    

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
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
                

    # 4.3 - 플레이어 이동 & Boss rect & 배경 이동
    if mvKeys[1]:
        if screenLock:
            playerpos[0] -= 2
            if playerpos[0] <= 10:
                playerpos[0] = 11 
        else:
            #playerpos[0]-=2
            if(bgX > 2):
                bgX -= 2 #2
            elif bgX <= 2:
                bgX = 2
                isBoundary = True
    elif mvKeys[3]:
        if screenLock:
            playerpos[0] += 2
            if playerpos[0] >= size[0] - 30:
                playerpos[0] = size[0] - 29
        else:
            #playerpos[0]+=2
            bgX += 2 #2
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
    

    #  - 총알 이동 및 판정
    #index = 0
    for idx, bullet in enumerate(arrows):   # 플레이어 총알 판정
        if bullet[0] == 0:
            bullet[2] -= 10
            if not (isBoundary or screenLock):
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

        surf.fill(WHITE)
        surf.blit(sheet,(0,0),(155,330,25,33))
        bulRect = pygame.draw.rect(screen,WHITE,(bullet[1] + 12,bullet[2] + 13,5,5))
        if(bulRect.colliderect(barricade)):
            del arrows[idx]
        if progress == 3:
            if(bulRect.colliderect(tkRect)):
                del arrows[idx]
                tkHP -= 1
                hittedTankSound.play()
        if progress == 6:
            if(bulRect.colliderect(hlcRect)):
                del arrows[idx]
                hlcHP -= 1
                hittedTankSound.play()
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
                genDieSound.play()
        for idx2,sdR in enumerate(sd2List):
            if(bulRect.colliderect(sdR[2])):
                del arrows[idx]
                del sd2List[idx2]
                genDieSound.play()
        for idx2,mL in enumerate(mobList):
            if(bulRect.colliderect(mL.getRect())):
                del arrows[idx]
                mL.hit()
                healthvalue = mL.hp
    for idx, sdBul in enumerate(sdBulList):
        if (not sdBul[0] == 2) and (not sdBul[0] == 3):
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
            bulRect = pygame.Rect((sdBul[1],sdBul[2],70,50))
            screen.blit(tkSheet2,(sdBul[1],sdBul[2]),(500,1800,100,50))
        elif sdBul[0] == 2:
            bulRect = pygame.draw.circle(screen,RED,(sdBul[1],sdBul[2]),2)
            if sdBul[4]:
                sdBul[1] -= 5
            else:
                sdBul[1] += 5
        elif sdBul[0] == 3:
            bulRect = pygame.draw.circle(screen,RED,(sdBul[1],sdBul[2]),2)
            sdBul[2] -= 4
            if sdBul[4]:
                sdBul[1] -= 5
            else:
                sdBul[1] += 5
        if(bulRect.colliderect(playerRect)):
            eriDeath()
            del sdBulList[idx]
        if sdBul[1] < -50 or sdBul[1] > size[0] + 50 or sdBul[2] < 0:
            del sdBulList[idx]
    

            


    # 4-4.  UI 그리기
    text_Title= myFont.render("Death : {}".format(death), True, WHITE)
    screen.blit(text_Title, [10, 30])

    # 4-5. 업데이트
    pygame.display.flip()
    
# 5.0 게임끝 점수판 및 게임종료 버튼 안내
SB = 0
while SB == 0:
    screen.fill((50,50,50))
    screen.blit(eriLastSheet, (0,0),(0,0,360,450))
    screen.blit(rovingLastSheet, (540,0),(0,0,360,450))
    text_Title= myFont.render("Death : {} ,press ESC to EXIT".format(death), True, WHITE)
    screen.blit(text_Title, [200, 200])
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            SB = 1
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                SB = 1
                pygame.quit() 
                exit(0) 


# 6. 게임 종료
pygame.quit()