import pygame
from pygame.locals import *
import sys

WIDTH = 1280
HEIGHT = 720

FPS = 60

clock = pygame.time.Clock()
running = True

scrollLeft = False
scrollRight = False
scroll = 0 
scrollSpeed = 1


########################### README ###########################
# This entire file should be run on its own using python background.py
# You can use this to muck around with the moving background, and
# attempt to figure out what I've


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BG Test')

def loadImage(image):
    img = pygame.image.load(f"img/background/{image}.png")
    img_rect = img.get_rect()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT)).convert_alpha()
    return img, img_rect

imgSrc = ["Layer_0011_0", "Layer_0010_1", "Layer_0009_2", "Layer_0008_3", "Layer_0007_Lights", "Layer_0006_4", "Layer_0005_5", "Layer_0005_5", "Layer_0003_6", "Layer_0002_7", "Layer_0001_8", "Layer_0000_9"]
imgLoaded = [loadImage(image) for image in imgSrc]


def drawBackground():
    
    screen.fill((0, 0, 255))
    for x in range(3):
        for image in range(0, len(imgLoaded)):
            screen.blit(imgLoaded[image][0], ((x * HEIGHT) -scroll * (image / 10.0), 0))


# Event loop
while running:
    
    clock.tick(60)
    
    if(scrollLeft == True):
        scroll -= 5
        
    if(scrollRight == True):
        scroll += 5
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
            
    
    keys = pygame.key.get_pressed()                    
    if keys[pygame.K_LEFT] and scroll > 0:
        scrollLeft = True
        
    else:
        scrollLeft = False
        
    if keys[pygame.K_RIGHT]:
        scrollRight = True
        
    else:
        scrollRight = False 
    
    
    drawBackground()    
    pygame.display.update()