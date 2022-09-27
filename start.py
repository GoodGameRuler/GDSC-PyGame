import imp
from turtle import back
import pygame
from pygame.locals import *
from spritesheet import Spritesheet
from gameObjects import *
from button import Button

WIDTH = 1280
HEIGHT = 720
LENGTH = 3

SCROLLSTART = 50

scrollLeft = False
scrollRight = False
scroll = 0 
backgroundScroll = 0
scrollSpeed = 1

FPS = 60


clock = pygame.time.Clock()


def loadImage(image):
    img = pygame.image.load(f"img/background/{image}.png")
    img_rect = img.get_rect()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT)).convert_alpha()
    return img, img_rect


def drawBackground(screen, imgLoaded):
    
    screen.fill((0, 0, 255))
    for x in range(LENGTH):
        for image in range(0, len(imgLoaded)):
            screen.blit(imgLoaded[image][0], ((x * WIDTH) -backgroundScroll * (image / 10.0), 0))


def main():
    global WIDTH
    global HEIGHT
    
    global scrollLeft 
    global scrollRight
    global scroll
    global backgroundScroll
    global scrollSpeed    
    
    gameStarted = False
    gameEnded = False
    gamePaused = False
    gameLost = False
    
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dark Hood')

    
    imgSrc = ["Layer_0011_0", "Layer_0010_1", "Layer_0009_2", "Layer_0008_3", "Layer_0007_Lights", "Layer_0006_4", "Layer_0005_5", "Layer_0005_5", "Layer_0003_6", "Layer_0002_7", "Layer_0001_8", "Layer_0000_9"]
    imgLoaded = [loadImage(image) for image in imgSrc]


    player = Player()
    skeleton = Skels(400, 615)
    skeleton2 = Skels(1000, 615)
    skeleton3 = Skels(1400, 615)
    skeletons = skeletonGroup(player)
    player.enemies.append(skeletons)
    skeletons.add(skeleton)
    skeletons.add(skeleton2)
    skeletons.add(skeleton3)
   
   
    running = True
    
    menuPlay = pygame.transform.scale(pygame.image.load(f"img/GUI/menu/play.png"), (40, 40)).convert_alpha()
    startButton = Button(615, 400, menuPlay, 1) 

    menuPause = pygame.transform.scale(pygame.image.load(f"img/GUI/match3/pause.png"), (40, 40)).convert_alpha()
    pauseButton = Button(1220, 20, menuPause, 1) 
    unPauseButton = Button(1220, 20, menuPlay, 1)
    
    menuClose = pygame.transform.scale(pygame.image.load(f"img/GUI/level_select/close_2.png"), (40, 40)).convert_alpha() 
    closeButton = Button(770, 530, menuClose, 1)
    
    gameWonScreen = pygame.transform.scale(pygame.image.load(f"img/GUI/you_win/bg.png"), (400, 400)).convert_alpha()
    gameWonHeader = pygame.transform.scale(pygame.image.load(f"img/GUI/you_win/header.png"), (150, 75)).convert_alpha()
    gameLoseHeader = pygame.transform.scale(pygame.image.load(f"img/GUI/you_lose/header.png"), (150, 75)).convert_alpha()
    
    menuResize = pygame.transform.scale(pygame.image.load(f"img/GUI/bubble/btn_1.png"), (40, 40)).convert_alpha()
    resizeButton =  Button(1160, 20, menuResize, 1) 
    
    heart = pygame.transform.scale(pygame.image.load(f"img/player/Heart.png"), (40, 40)).convert_alpha()
    
    # gameWon = 
    
    # Event loop
    while running:

        clock.tick(FPS)

        
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
                    
                if event.key == pygame.K_w:
                    gameLost = False
                    gameEnded = True
                    
                elif event.key == pygame.K_l:
                    gameLost = True
                    gameEnded = True
                    


        if not gameStarted:
            img = pygame.transform.scale(pygame.image.load(f"img/background.png"), (WIDTH, HEIGHT)).convert_alpha()
            menuLogo = pygame.transform.scale(pygame.image.load(f"img/GUI/menu/logo.png"), (200, 80)).convert_alpha()
            screen.blit(img, (0, 0))
            screen.blit(menuLogo, (535, 80))
            if(startButton.draw(screen)):
                gameStarted = True
            pygame.display.update()
            
            continue
        
        if gameEnded:
            menuLogo = pygame.transform.scale(pygame.image.load(f"img/GUI/menu/logo.png"), (200, 80)).convert_alpha()
            screen.blit(menuLogo, (535, 80))
            screen.blit(gameWonScreen, (440, 200))
            
            if(not gameLost):
                screen.blit(gameWonHeader, (560, 230))
                    
            else:
                screen.blit(gameLoseHeader, (560, 230))
                
            if closeButton.draw(screen):
                running = False
                
            pygame.display.update()
            continue
        
        if gamePaused:
            if(unPauseButton.draw(screen)):
                gamePaused = False
                
            pygame.display.update()
            continue   
        
        drawBackground(screen, imgLoaded)
        
        if(resizeButton.draw(screen)):
            pygame.display.toggle_fullscreen()
        
        if(pauseButton.draw(screen)):
            gamePaused = True
            
        for i in range(0, player.lives):
            screen.blit(heart, (20 + i * 40, 20))
            
        
        # ############################### PLAYER ############################### #
        player.tick(pygame.time.get_ticks())
        
        if(player.alive):
            keys = pygame.key.get_pressed()
            
           
            player.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_s])
            scroll = player.move(backgroundScroll)
            backgroundScroll -= scroll
            player.draw(screen)
        
        
        # ############################### ENEMY ############################### #
        
        skeletons.collidePlayer(player)
        skeletons.update(pygame.time.get_ticks(), scroll)
        skeletons.draw(screen)
        
        if len(skeletons) == 0:
            gameEnded = True
            gameLost = False
        
        
        if(player.alive == False):
            gameEnded = True
            gameLost = True
        
        pygame.display.update()


if __name__ == '__main__': main()