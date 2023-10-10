"""
Attributes:
images taken from: Vecteezy.com
"""
# import area
import pygame
from pygame.locals import *
import sys
import random



# Global Constants and variables
screen_width=1400
screen_height=700
FPS = 30
screen=pygame.display.set_mode([screen_width, screen_height])
game_images = {}
game_sounds = {}


# Function Area
def start():
    while True:
        screen.blit(game_images["background"], (0, 0))
        screen.blit(game_images["message"], ((screen_width-message_width)/2, (screen_height-message_height)/2))
        screen.blit(game_images["player"], (player_x, player_y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                return


def gameLoop():
    # print("Game loop started...")
    global player_y
    game_sounds["playback1"].play(loops=-1)

    new_pipe1 = getPipe()
    new_pipe2 = getPipe()
    upper_pipes = [
        {"x": screen_width, "y":new_pipe1[0]["y"]},
        {"x": screen_width * 1.5, "y":new_pipe2[0]["y"]}
    ]
    lower_pipes = [
        {"x": screen_width, "y":new_pipe1[1]["y"]},
        {"x": screen_width * 1.5, "y":new_pipe2[1]["y"]}
    ]

    pipeSpeedX = -10
    playerSpeedY = -9
    playerMaxSpeedY = 8
    gravity = 1
    playerFlyingSpeedY = -8
    playerFlying = False

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_UP:
                playerFlying = True
                if player_y > 0:
                    playerSpeedY = playerFlyingSpeedY
                    game_sounds["fly"].play()
                    
        # Moving player up
        player_y = player_y + playerSpeedY
        if playerFlying:
            playerFlying = False

        # Gravity
        if not playerFlying and playerSpeedY < playerMaxSpeedY:
            playerSpeedY = playerSpeedY + gravity

        # Moving the pipes
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            upperPipe["x"] += pipeSpeedX
            lowerPipe["x"] += pipeSpeedX

        # Adding new pipes
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            if upperPipe["x"] < -150:
                new_pipe = getPipe()
                upper_pipes.append(new_pipe[0])
                lower_pipes.append(new_pipe[1])

                # Removing old pipes
                upper_pipes.pop(0)
                lower_pipes.pop(0)


        # blitting everything up
        screen.blit(game_images["background"], (0, 0))
        screen.blit(game_images["player"], (player_x, player_y))
        
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            screen.blit(game_images["pipe"][0], (upperPipe["x"], upperPipe["y"]))
            screen.blit(game_images["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))
        
        screen.blit(game_images["base1"], (0, baseY))
        pygame.time.Clock().tick(FPS)
        pygame.display.update()

def getPipe():
    y2 = random.randint(gap, baseY)
    y1 = y2 - gap - pipe_height
    pipe = [
        {"x" : screen_width, "y" : y1},
        {"x" : screen_width, "y" : y2}
    ]
    return pipe


# Main Program
pygame.init()
pygame.display.set_caption("Angry Bird")
game_images["background"] = pygame.image.load("images/background.png").convert_alpha()
game_images["base1"] = pygame.image.load("images/layer-3-ground.png").convert_alpha()
game_images["player"] = pygame.image.load("images/bird123.png").convert_alpha()
# game_images["player_hit"] = pygame.image.load("images/bird_hit.png").convert_alpha()
game_images["message"] = pygame.image.load("images/message.png").convert_alpha()
game_images["pipe"] = [
    pygame.transform.rotate(pygame.image.load("images/pipe.png").convert_alpha(), 180),
    pygame.image.load("images/pipe.png").convert_alpha()
]
game_images["numbers"] = (
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

game_sounds["playback1"] = pygame.mixer.Sound("audio/fly.mp3")
game_sounds["playback2"] = pygame.mixer.Sound("audio/fly.mp3")
game_sounds["fly"] = pygame.mixer.Sound("audio/60013__qubodup__whoosh.flac")
game_sounds["point"] = pygame.mixer.Sound("audio/collect_point.mp3")
game_sounds["die"] = pygame.mixer.Sound("audio/crash.mp3")

message_height = game_images["message"].get_height()
message_width = game_images["message"].get_width()

player_x = screen_width/5
player_y = screen_height/2

player_height = game_images["player"].get_height()
player_width = game_images["player"].get_width()
gap = player_height * 2

baseY = screen_height - game_images["base1"].get_height()
pipe_height = game_images["pipe"][0].get_height()

start()
gameLoop()

