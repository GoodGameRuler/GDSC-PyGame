import pygame
from pygame.locals import *
from spritesheet import Spritesheet
from gameObjects import *

WIDTH = 1280
HEIGHT = 720

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
    for x in range(3):
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
    
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dark Hood')

    
    imgSrc = ["Layer_0011_0", "Layer_0010_1", "Layer_0009_2", "Layer_0008_3", "Layer_0007_Lights", "Layer_0006_4", "Layer_0005_5", "Layer_0005_5", "Layer_0003_6", "Layer_0002_7", "Layer_0001_8", "Layer_0000_9"]
    imgLoaded = [loadImage(image) for image in imgSrc]


    player = Player()
    skeleton = Skels()
    skeletons = skeletonGroup(player)
    player.enemies.append(skeletons)
    skeletons.add(skeleton)
   
   
    running = True

    # Event loop
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()


        drawBackground(screen, imgLoaded)
        
        
        # ############################### PLAYER ############################### #
        player.tick(pygame.time.get_ticks())
        
        if(player.alive):
            keys = pygame.key.get_pressed()
            
           
            player.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_s])
            scroll = player.move()
            backgroundScroll -= scroll
            player.draw(screen)
        
        
        # ############################### ENEMY ############################### #
        
        skeletons.collidePlayer(player)
        skeletons.update(pygame.time.get_ticks())
        skeletons.draw(screen)
            
        pygame.display.update()


if __name__ == '__main__': main()