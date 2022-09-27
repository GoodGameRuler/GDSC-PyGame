from turtle import back
import pygame
from pygame.locals import *
from spritesheet import Spritesheet
from gameObjects import *

HEIGHT = 1280
WIDTH = 720

FPS = 60

clock = pygame.time.Clock()


def main():
    global HEIGHT
    global WIDTH
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    # pygame.display.set_caption('Basic Pygame program')

    # # Fill background
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((250, 250, 250))

    background = pygame.image.load("img/background.png")
    background = pygame.transform.scale(background, (HEIGHT, WIDTH)).convert()


    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    my_spritesheet = Spritesheet('img/player/idle.png')

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
                    



        screen.blit(background, (0, 0))
        
        
        player.tick(pygame.time.get_ticks())
        
        if(player.alive):
            keys = pygame.key.get_pressed()
            
           
            player.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_s])
            player.draw(screen)
        
        
        # if(pygame.sprite.spritecollide(player, skeletons, False) and player.currentAction != "hurt"):
        #     player.hurt()
        skeletons.collidePlayer(player)
        skeletons.update(pygame.time.get_ticks())
        skeletons.draw(screen)
            
        # screen.blit(img, (100, 100))
        pygame.display.update()


if __name__ == '__main__': main()