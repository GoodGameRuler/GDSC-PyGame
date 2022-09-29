import pygame
from pygame.locals import *
from spritesheet import Spritesheet
from gameObjects import *
from button import Button


# ################################ README ################################ #

# Have a read through gameObject.py before you read this
# Try runnning background.py for a better look at the dynamic background.


# Declaring some congstants
WIDTH = 1280
HEIGHT = 720
LENGTH = 3
FPS = 60
SCROLLSTART = 50


# Not constant but we need these in the global namespace
scrollLeft = False
scrollRight = False
scroll = 0 
backgroundScroll = 0
scrollSpeed = 1



clock = pygame.time.Clock()

# Image/Asset loader for the dynamic background
# Try looking at/running background.py for more clarity
def loadImage(image):
    img = pygame.image.load(f"img/background/{image}.png")
    img_rect = img.get_rect()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT)).convert_alpha()
    return img, img_rect

# Draws in our dyncamic background
# Called every frame
def drawBackground(screen, imgLoaded):
    
    screen.fill((0, 0, 255))
    
    # This essentially prints the backfround LENGTH (or 3) times.
    # Think of it as having three background.pngs beside/alongside each other in the x direction to make a really long map
    # This essentailly spawns in one map and then another and then another, putting one after the other in the x axis
    for x in range(LENGTH):
        
        for image in range(0, len(imgLoaded)):
            
            # This is how it does the dynamic background part
            # This one line of code is proabbyl the most unclear code in the entire program
            # I will attempt to explain it
            # For each image part of the background (there are 11 layers to the background), so for each of them
            # We blit them onto the screen
            # We offset the x position by the bgScoll (i.e how much the player has moved from the original background)
            # We multiply X and Width as x is the number of times we have already added the background
            # Once we add one background we add the next one in beside by offsetting it by the width of the background
            # Lastly how much it is offset depends on the layer of the image.
            # The closser the image (or asset part of the background is), the the more it moves as the player moves
            # So for layer 0 (the closest to the player) we off scale down by nothing because the closer the later the more the layer should move
            # Also not that imgLoaded loads the layers in reverse order [layer11, layer10, layer9, ... , layer0].
            # See main for imgLoaded
            screen.blit(imgLoaded[image][0], ((x * WIDTH) -backgroundScroll * (image / 10.0), 0))


def main():
    
    # Global infront of a variable just indicates for sure that it is the one declared in outside the function in what is called the global namespace
    global WIDTH
    global HEIGHT
    
    global scrollLeft 
    global scrollRight
    global scroll
    global backgroundScroll
    global scrollSpeed    
    
    # A few flags for our GUI
    # Tells us which screen to Show atm
    gameStarted = False
    gameEnded = False
    gamePaused = False
    gameLost = False
    
    # Initialise screen and caption
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Dark Hood')

    # Load in the layers for the background 
    imgSrc = ["Layer_0011_0", "Layer_0010_1", "Layer_0009_2", "Layer_0008_3", "Layer_0007_Lights", "Layer_0006_4", "Layer_0005_5", "Layer_0005_5", "Layer_0003_6", "Layer_0002_7", "Layer_0001_8", "Layer_0000_9"]
    imgLoaded = [loadImage(image) for image in imgSrc]


    # Load in all our game objects
    player = Player()
    skeleton = Skels(400, 615)
    skeleton2 = Skels(1000, 615)
    skeleton3 = Skels(1400, 615)
    skeletons = skeletonGroup(player)
    player.enemies.append(skeletons)
    skeletons.add(skeleton)
    skeletons.add(skeleton2)
    skeletons.add(skeleton3)
   
    # Flag for our infinite loop
    running = True
    
    # ################################ Loading GUI ################################ #
    
    # Just loads in all the buttons and GUI features
    
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
    
    # ##################################################################### #

    while running:

        # Maintains our 60 FPS
        clock.tick(FPS)


        # For all events  
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
                    

        # ################################ Rendering GUI ################################ #
        
        # Menu Screen
        if not gameStarted:
            img = pygame.transform.scale(pygame.image.load(f"img/background.png"), (WIDTH, HEIGHT)).convert_alpha()
            menuLogo = pygame.transform.scale(pygame.image.load(f"img/GUI/menu/logo.png"), (200, 80)).convert_alpha()
            screen.blit(img, (0, 0))
            screen.blit(menuLogo, (535, 80))
            if(startButton.draw(screen)):
                gameStarted = True
            pygame.display.update()
            
            continue
        
        # Game Finished Screen
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
        
        # Paused Game Screen (not really much here)
        if gamePaused:
            if(unPauseButton.draw(screen)):
                gamePaused = False
                
            pygame.display.update()
            # If this game is paused kinda skip the rest of the code in the loop and go to the next iteration of the loop
            continue   
        
        
        
        drawBackground(screen, imgLoaded)
        
        if(resizeButton.draw(screen)):
            pygame.display.toggle_fullscreen()
        
        if(pauseButton.draw(screen)):
            gamePaused = True
            
        for i in range(0, player.lives):
            screen.blit(heart, (20 + i * 40, 20))
        
        # ##################################################################### #
        
        # ############################### PLAYER ############################### #
        player.tick(pygame.time.get_ticks())
        
        if(player.alive):           
           
            ######## IMPORTANT ########
            # Intead of doing pygame.event.type == pygame.KEYDOWN, and pygame.event.type == pygame.KEYUP
            # You can get a dictionary of all the keys, to whether they are currently being pressed looks kinda like {K_RIGHT: True, ...} but has all the keys in pygame
            # There is no beniefit to doing it this way over that way other than this only uses one line, using if statements instead would take a few more lines
            # Though might be more readable
            keys = pygame.key.get_pressed()
            player.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_s])
            
            # Move the player providinf the current background scroll, and if the player is moving to the end of the screen return a scroll value to offset all the other gameobejects by
            # Explained more in gameObjects.py
            scroll = player.move(backgroundScroll)
            
            # The background scroll in the opp diretion to the player. As the player moves forward, the background moves backwards
            # Update the cumalative offset for the backround
            backgroundScroll -= scroll
            player.draw(screen)
        
        
        # ############################### ENEMY ############################### #
        
        # Check for collisions with the player, updaye the skeletons, and then draw them all at once
        # Where groups come in quite handy
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



# If we run this file ever using 'python start.py', start running the code at main()
# Python interprets all lines of code, but starts runnning from main.
if __name__ == '__main__': main()