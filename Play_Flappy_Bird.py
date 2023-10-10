import pygame
import sys
from pygame.locals import *
from random import randint

#global variable and constant
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
GAME_IMAGES = {}
GAME_SOUNDS = {}
FPS = 30

playerX = SCREEN_WIDTH/5
playerY = SCREEN_HEIGHT/2

#function area
def welcomeScreen():
    while True:
        SCREEN.blit(GAME_IMAGES["background"],(0,0))
        SCREEN.blit(GAME_IMAGES["basef"],(baseX,baseY))
        SCREEN.blit(GAME_IMAGES["player"],(playerX,playerY))
        SCREEN.blit(GAME_IMAGES["message"],(messageX,messageY))
        pygame.display.update()
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if x.type == KEYDOWN and x.key == K_SPACE:
                return


def gameLoop():
    newPipe1 = getRandomPipes()
    newPipe2 = getRandomPipes()
    

    #list of upper pipes
    upperPipes = [
        {"x":SCREEN_WIDTH,"y":newPipe1[0]["y"]},
        {"x":SCREEN_WIDTH * 1.5,"y":newPipe2[0]["y"]},
        
    ]
     
    lowerPipes = [
        {"x":SCREEN_WIDTH,"y":newPipe1[1]["y"]},
        {"x":SCREEN_WIDTH * 1.5,"y":newPipe2[1]["y"]},
        
    ]

    score = 0
    pipeSpeedX = -15
    playerSpeedY = -9
    playerMaxSpeed = 5
    playerFlyingSpeed = -10
    playerAccY = 1
    playerFlying = False
    pipeHeight = GAME_IMAGES["pipe"][0].get_height()
    playerX = SCREEN_WIDTH/5
    playerY = SCREEN_HEIGHT/2

    while True:
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if x.type == KEYDOWN and (x.key == K_UP or x.key == K_w):
                if playerY > 0:
                    playerSpeedY = playerFlyingSpeed
                    playerFlying = True
                    GAME_SOUNDS["fly"].play()

        #moving player up 
        playerY = playerY + playerSpeedY
        if playerFlying == True:
            playerFlying = False 

        #pulling player down
        if playerSpeedY < playerMaxSpeed and not playerFlying:
            playerSpeedY = playerSpeedY + playerAccY

        #moving pipe
        for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
            upperpipe["x"] = upperpipe["x"] + pipeSpeedX
            lowerpipe["x"] = upperpipe["x"] + pipeSpeedX


        #adding new pipes
        if 0 < upperPipes[0]["x"] <= abs(pipeSpeedX):
            newPipe =  getRandomPipes()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1]) 


        #removing old pipes
        if upperPipes[0]["x"]<0 : 
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Changing the score
        playerCenterX = playerX + GAME_IMAGES["player"].get_width()/2
        for pipe in lowerPipes:
            print(pipe['x'])
            pipeCenterX = pipe['x'] + GAME_IMAGES["pipe"][0].get_width()/2
            if pipeCenterX <= playerCenterX < pipeCenterX + abs(pipeSpeedX):
                 score = score + 1
                 GAME_SOUNDS["collect_point"].play()  
                #  print(score)


        # # Player Dies 
        if isHit(playerX,playerY,upperPipes,lowerPipes):
            GAME_SOUNDS["crash"].play()
            pygame.time.wait(2000)
            return   


        #blitting up everything
        SCREEN.blit(GAME_IMAGES["background"],(0,0))
        SCREEN.blit(GAME_IMAGES["player"],(playerX,playerY))
        #blitting the score
        scoreDigits = [int(x) for x in list(str(score))]
        scoreX = SCREEN_WIDTH/1.15
        scoreY = SCREEN_HEIGHT/1.45
        for digit in scoreDigits:
            SCREEN.blit(GAME_IMAGES["numbers"][digit],(scoreX,scoreY))
            scoreX += GAME_IMAGES["numbers"][digit].get_width()
        for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_IMAGES["pipe"][0],(upperpipe["x"],upperpipe["y"])) 
            SCREEN.blit(GAME_IMAGES["pipe"][1],(lowerpipe["x"],lowerpipe["y"])) 
        SCREEN.blit(GAME_IMAGES["basef"],(baseX,baseY))
        pygame.display.update() 
        pygame.time.Clock().tick(FPS)

def isHit(playerX,playerY,upperPipes,lowerPipes):
    pipeHeight = GAME_IMAGES["pipe"][0].get_height()
    pipeWidth = GAME_IMAGES["pipe"][0].get_width()
    playerHeight = GAME_IMAGES["player"].get_height()
    playerWidth = GAME_IMAGES["player"].get_width()
    # hit with ceiling or base
    if playerY < 0 or playerY + playerHeight> SCREEN_HEIGHT - GAME_IMAGES["basef"].get_height():
        return True
    
    # hit with upperpipes  
    for pipe in upperPipes:
        if (playerY < pipe["y"] + pipeHeight) and (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth) : 
            return True
        

    #hit with lowerpipes
    for pipe in lowerPipes:
        if (playerY + playerWidth > pipe["y"]) and (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth) : 
            return True 
    return False

def getRandomPipes():
    gap = GAME_IMAGES["player"].get_height()*3
    y2 = randint(gap,SCREEN_HEIGHT-GAME_IMAGES["basef"].get_height())
    y1 = y2 - gap - GAME_IMAGES["pipe"][0].get_height()
    pipeX = SCREEN_WIDTH
    pipe = [
        {"x":pipeX, "y":y1},
        {"x":pipeX, "y":y2}
    ]
    return pipe

# Main Program
pygame.init()
pygame.display.set_caption("Flappy Bird")
GAME_IMAGES["background"] = pygame.image.load("images/background.png").convert_alpha()
GAME_IMAGES["basef"] = pygame.image.load("images/layer-3-ground.png").convert_alpha()
GAME_IMAGES["player"] = pygame.image.load("images/bird123.png").convert_alpha()
GAME_IMAGES["message"] = pygame.image.load("images/message.png").convert_alpha()
GAME_IMAGES["numbers"] = (
    pygame.image.load("images/0.png").convert_alpha(),
    pygame.image.load("images/1.png").convert_alpha(),
    pygame.image.load("images/2.png").convert_alpha(),
    pygame.image.load("images/3.png").convert_alpha(),
    pygame.image.load("images/4.png").convert_alpha(),
    pygame.image.load("images/5.png").convert_alpha(),
    pygame.image.load("images/6.png").convert_alpha(),
    pygame.image.load("images/7.png").convert_alpha(),
    pygame.image.load("images/8.png").convert_alpha(),
    pygame.image.load("images/9.png").convert_alpha()
)

GAME_IMAGES["pipe"] = (
      pygame.transform.rotate(pygame.image.load("images/pipe.png").convert_alpha(), 180), # alt + Z
    pygame.image.load("images/pipe.png").convert_alpha()
)


GAME_SOUNDS["crash"] = pygame.mixer.Sound("audio/crash.mp3")
GAME_SOUNDS["fly"] = pygame.mixer.Sound("audio/60013__qubodup__whoosh.flac")
GAME_SOUNDS["collect_point"] = pygame.mixer.Sound("audio/zapsplat_multimedia_game_sound_digital_retro_simple_positive_tone_collect_point_item_001_80632.mp3")

baseX = 0
baseY = SCREEN_HEIGHT - GAME_IMAGES["basef"].get_height() 
messageX = SCREEN_WIDTH/2 - GAME_IMAGES["message"].get_width()/2
messageY = SCREEN_HEIGHT/2 - GAME_IMAGES["message"].get_height()/2


while True : 
    welcomeScreen()
    gameLoop()



