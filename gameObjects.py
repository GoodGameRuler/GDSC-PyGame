from random import randint
from re import L
import pygame
import start
from spritesheet import Spritesheet 


################################### GameObject ###################################

# Kind of like my main class used to represent any actual object part of the game
# Do I need this object? ABSOLUTELY NOT, at least not right now. May be usefull if you add things like powerups, items, and other cool things like that.
# Why? Because it would be easy to check if the player interacts with any object rather than going through enemies, the iterms, then powerup, ...
# Kind useless rn ngl

# Does not really do anything can ignore everything except line to be noted, and maybe self.speed.
class GameObject(pygame.sprite.Sprite):
    def __init__(self, scale, speed, src):
        pygame.sprite.Sprite.__init__(self) # LINE TO BE NOTED at some point all Sprite ojects need to do this
        
        # Alternatively you could try `super().__init()` with no self given to it
        # `pygame.sprite.Sprite.__init__(self)` is equivilant to `super().__init()` but didn't really work on my system.

        self.speed = speed
        
        self.image = pygame.image.load(src)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))    


################################### Player ###################################

# Our main player
# Player and Skelton have alot of overlapping code.
# Ideally we would but the common code in a parent object (like GameObject, but maybe not GameObject was meant to hold more things not just mobs)

class Player(GameObject):

    # Constructor for our player object
    # Every time we do `variable = Player()` this is called 
    def __init__(self):
        
        # Giving some data to GameObject not really necessary though with what I've done
        # You could just do whatever GameObject is doing here
        super().__init__(1, 2, "img/player/idle.png")
        
        # Some basic flags about the player
        self.alive = True
        self.lives = 5
        
        # Used to attack enemies nearby from the player object
        self.enemies = []
        
        # Moving flags as seen in lectures
        self.movingRight = False
        self.movingLeft = False 
        self.jumping = False 
        
        # This is just tracking the velopcity in the y direction
        # Used to incoroprate gravity (that pulls the player down)
        self.yVel = 0
        
        # Attack cool downs, also when I thought I had enough time to implement two attacks
        self.attackOneCoolDown = 0 # 400
        self.attackOneCoolDown = 0 # 1200
        
        # Sprites made technically only face one direction so you have to flip the image to make the sprite look in the other direction
        # You may think that I could have used movingleft and moving right for this, you may be able to that but
        # Think about when a player is not moving, it can still face left and right -> movingLeft is False, movingRight is False, but the PLater is facing right
        self.facingLeft = False
        
        # Index just keeps a track of which sprite on the spriteSheet/animation we are currently on for the current tasks
        self.index = 0
        self.movingIndex = 0
        
        # This is a magical object called a dictionary, truly revolutionary 
        # Maps the current action to the animation list of that animation
        # e.g {"idle" : [sprite1, sprite2, ...]} but ofcourse they aren't really named sprite1, sprite2, ...
        # We set this relation between current action and the sprite sheet below
        self.animations = {}
        
        # The current action that player is doing.
        self.currentAction = "idle"
        
        # Loading all the sprite sheets for the player, try having a look at the pngs first, and then the sprite sheet doc to get a better idea of what this does. 
        idleSpriteSheet = Spritesheet('img/player/idle.png')
        runningSprites = Spritesheet('img/player/run.png')        
        jumpSprites = Spritesheet("img/player/jump.png")
        hurtSprite = Spritesheet("img/player/hurt.png")
        attackSprite = Spritesheet("img/player/attack.png")
        
        
        # This is a truly confusing block of code. [i for i in range(1, 5)] is called a generator
        # We don't really have to understand what this does, just that it is easy to use (for the programmer) but very hard to read
        # This
        #  
        # tempList = []
        #         
        # for i in range(1, 19):
        #   tempSprite = idleSpriteSheet.parse_sprite(f'f_redHood{i}.png')
        #   tempList.append(tempSrite)
        #   
        # self.animations["idle"] = tempList
        # 
        # 
        # is the equivilant of doing the the first line below
          
        self.animations["idle"] = [idleSpriteSheet.parse_sprite(f'f_redHood{i}.png') for i in range(1, 19)]
        self.animations["move"] = [runningSprites.parse_sprite(f'f_redHood{i}.png') for i in range(1, 25)]        
        self.animations["jump"] = [jumpSprites.parse_sprite(f'f_redHood{i}.png') for i in range(1, 18)]
        self.animations["hurt"] = [hurtSprite.parse_sprite(f'f_redHood{i}.png') for i in range(1, 8)]
        self.animations["attack"] = [attackSprite.parse_sprite(f'f_redHood{i}.png') for i in range(1, 25)]

        # Set up the clock object incase we need it to maintain ticks/FPS
        self.clock = pygame.time.Clock()
        
        
        
        # Getting the rect object for the idle (all animations for this sprite have the same dimensions though) movement
        # Technically we could have gotten any sprite didn't really matter
        # self.rect = self.animations["attack"][6].get_rect()
                
        # Also just to explain this notation 
        # self.animations["idle"] gets the value associated withe "idle" in the animations dictionary
        # This is just the sprite list for idle
        # the [0] lets us access the first element in this list 
        
        self.rect = self.animations["idle"][0].get_rect()
        self.rect.x = 50
        self.rect.y = 200
        
    
    # Update just takes flags for whether we are moving up left, right, down, or being attacked.
    def update(self, left, right, up, down, attack):  
        
        # If we are hurt we should not be able do anything else. 
        # The function tick() un'hurts' the player
        if(self.currentAction == "hurt"):
            return
        
        # If we are trying to attakc, and we are not already attacking, and the there is no cooldown right now for the attack do this
        if(attack and self.currentAction != "attack" and self.attackOneCoolDown == 0):
            
            # Why are we checking that the cooldown is 0 again ;-; idk
            # Originally I did not have the check that the cooldown was 0 at the top, and I think I forgot to change it
            if(self.attackOneCoolDown == 0):
                self.currentAction = "attack"
                self.attackOneCoolDown = 150
                       
            return
          
                
        # If we are attacking
        if(self.currentAction == "attack"):
            
            # If we are attacking right now and the player is still holding down the attack button then
            if(attack):
               
                # Every six frames please do this    
                if(self.index % 6 == 0):
                    
                    # This was prepared in case we had differnt kind of enemies in the game (was planning to add slimes)
                    # For every enemy in every enemy grouping that we have check if are close to the enemy
                    for enemyGroup in self.enemies:
                        for enemy in pygame.sprite.spritecollide(self, enemyGroup, False):
                            
                            # If we are close to this current enmey, facing their direction, and attacking damage the enemy
                            if(enemy.rect.x - self.rect.x >= 3 and self.facingLeft == False):
                                enemy.damage(1)
                                
                            if(enemy.rect.x - self.rect.x <= -3 and self.facingLeft == True):
                                enemy.damage(1)
                            
                # Put a cooldown on attack
                # Bit of an arbitrary number
                # But seemed to work best for a cooldown
                self.attackOneCoolDown = 150
                
                # Note that if the player is holding down the attack key then the function would return here   
                return

            # If the player is not holding down the attack key, we want to stop the attack 
            # Mmore of a game design, you could make a tap attack rather than a hold attack
            self.currentAction = "idle"
            self.index = 0
        
        
        # 600 is kind of like our bootleg floor for the player
        # You usually don't want the floor to be part of the background but rather a sererate object, and ther would be a seperate sprite assoicated with that
        
        # If we are pressing jump, on the floor, and not already jumping
        if(up and self.currentAction != "jump" and self.rect.y == 600):
            
            # For the initial part of the jump stop moving
            self.movingLeft = False
            self.movingRight = False
            
            # Reset the animation index so that we can start the jumping animation
            self.index = 0
            self.jumping = True # Set the jumping flag, for our move() function 
            
            # Change the current action to jump
            self.currentAction = "jump"
        
        # If we are pressing left and right don't move
        if(left and right):
            self.movingLeft = False
            self.movingRight = False
            
            # If we were moving and then we started presing both keys, this resets the action and animation for idle.
            self.index = 0 
            self.currentAction = "idle"
            
            # Do not entirely know why I did this lmao, possibly added this before I added the above 
            if(self.movingLeft or self.movingRight or self.jumping):
                self.index = 0
            
            return
        
        # If we are pressing left but not currently moving left
        if(left and not self.movingLeft):
            
            # Set the flags as such
            self.movingLeft = True
            self.movingRight = False
            self.facingLeft = True
            
            # Reset the index and action to start the moving animation
            self.index = 0
            self.currentAction = "move"
            
        # If we are not pressing left but moving left 
        if(not left and self.movingLeft):
            
            # If we are moving left, not pressing left, and not pressing right we should change to idle
            # We do not want to stop moving just because we stopped pressing the left arrow, we could me moving right or jumping
            # Forgot to add jump it seems like
            if(not right):
                self.currentAction = "idle"
            
            # Rest the flags (if we start moving right/jumping we would want the animations to restart) if we weren't we would still want the animations to reset for idle
            self.movingLeft = False
            self.index = 0
           
        # The below is the same thing as seen above but for right
        # If we are pressing right but not moving right quite yet
        if(right and not self.movingRight):
            self.movingRight = True
            self.movingLeft = False
            self.facingLeft = False
            
            self.currentAction = "move"
            self.index = 0
        
        # If we are moving right but not quite pressing right.
        if(not right and self.movingRight):
            
            if(not left):
                self.currentAction = "idle"
            
            self.movingRight = False
            self.index = 0
    
    
    # If a player gets attacked by an enemy(Skeleton), the enemyGroup(SkeletonGroup) calls this
    def hurt(self):
        
        # Reduce our lives
        self.lives -= 1
        
        # If we don't have anymore lives kill us
        if(self.lives == 0):
            
            # Change the flag
            self.alive = False
            
            # Self.kill() actually sets self.alive to False for us anywyas don't need the above code.
            # This is because self.alive is something that pygame.sprite.Sprite already has
            self.kill()
            return
        
        # If we haven't died set the current action to hurt and reset the animation counter for such
        self.index = 0
        self.currentAction = "hurt"
        
    
    # Called to kind of transition between our animation states
    def tick(self, ticks):

        # Used a bunch of magic numbers here but DW not too complicated
        # Note that this function is called 60 times a second (roughly)
        # For each action we check if we have called this function a certain number of times then proceed to do the following
        # Some animations wrap around - once they finish they just do the same thing over and over again
        
        # so self.index = (self.index + 1) % len(self.animations[self.currentAction])
        # basically ensures that the animations keep looping
        # For example the idle animation has (I think) 18 animations
        # So if we remained idle the index would go, 1, 2, 3, ..., 17, 18, 1, 2, 3, ..., 17, 18, ...
        # Techincally 0 - 17, and not 1 - 18, because the first element in a list is called the 0th element. listExample[0].
        
        # If we are idle, for every 8 times we call this function do this
        if(self.currentAction == "idle" and ticks % 8 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
        
        # If we are jumping, for every 10 times we call this function do this
        elif (self.currentAction == "jump" and ticks % 10 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
        
        # If we are attacking, for every 10 times we call this function do this
        elif(self.currentAction == "attack" and ticks & 10 == 0):
            
            # If we haven't finished 1 animation set increase the animation counter
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1)
            
            # If we have reached the end of the attack animation do not keep attacking go back to idle. (not the best, what happens if we attack in air?)
            else:
                self.index = 0
                self.currentAction = "idle" 
        
        # If we are hurt 
        elif (self.currentAction == "hurt"):
            
            # If the animation is over
            if (self.index >= len(self.animations[self.currentAction]) - 1):
                
                # Go back to idle, and respwan the player
                self.index = 0
                self.currentAction = "idle"
                
                # This may not be what you want to do because remember the map technically moves, so  5, 600 might not be the start position of the map
                # It just the begining of the map you can see. 
                # For example in flappy bird if the bird died it wouldn't make sense to spawn him/her back at the left end of the screen.
                # Instead the bird should spwan at the left end point of the map. The game should scroll back all the way to the begining of the map and then spawn the bird
                # However you might want this, you might not.
                
                self.rect.x = 5
                self.rect.y = 600
                
            # If the death animation is not done, increment the animation counter
            else:
                if(ticks % 4 == 0):
                    self.index = (self.index + 1)          

        # If the current animation is not one specified above just sitck to the default move up an animation every 3 times
        # Just for reference the tick fun is called 60 times a sec so this if statement would if the anmimation wasn't any...
        # of the above, would run 20 times a second
        elif (ticks % 3 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
            
        # If we have a cooldown reduce it by 1
        if(self.attackOneCoolDown > 0):
            self.attackOneCoolDown -= 1

    
    # Move function that is called in the main() function in start.py
    # What is bgScroll, its part of making the background move
    # The bgScroll value is how much we have moved from the original backgound. 
    # This onyl starts to change when the player reaches the edge of the visible window
    # That is when the backgound starts moving and hence that is when bgScroll is incremented (or decremented for going back left)
    def move(self, bgScroll):
        
        # Set a local variable for scrolling
        screenScroll = 0
        
        # This is kinda a temp var that hold the speed for the current player to subract from the player's x and y rect values 
        accX = 0
        accY = 0
        
        # If we are mmoving left or right decrement and increment accX respectively
        if self.movingLeft:
            accX = -self.speed
            
        if self.movingRight:
            accX = self.speed
            
        # If we are jumping give us a y velocity and reset jumping (should not be able to double, triple, ... jump)
        if(self.jumping):
            
            # Velocity is negative as going up means getting closer to (0, 0). Recall top left corner is (0, 0)
            self.yVel = -10
            self.jumping = False
        
        # If we are not on the floor yet (floor = 600 pixels y val for the player)  
        if(self.rect.y < 600):
            
            # if we do not have do not have a positive velocity of 5 (if we aren't falling down fast at a the terminal velocity of 5) make us go down faster
            # Remember the positive increment is trying to pull us down, as its trying to make us go away from (0, 0)
            if(not self.yVel > 5):
                self.yVel += 0.5    
        
        # If we have reached the floor, set y velocity to 0 (should be able to move throught the floor (even the fake pixel floor we have made))
        elif(self.yVel != 0 and self.rect.y > 600):
            self.yVel = 0
            self.rect.y = 600
            
            # Set the action to idle now
            if(self.currentAction == "jump"):
                self.currentAction = "idle"
        
        # Not change the accY to the yVel we have assignmed (yVel is kind of a tempVar we do not really need it but makes it easier to read the above) 
        accY = self.yVel

        # Change the rect values accordingly
        self.rect.x += accX
        self.rect.y += accY
    

        # Make sure we havent moved off the screen, and if we are going to move off the screen start scrolling the screen along
        if((self.rect.right > start.WIDTH - start.SCROLLSTART and self.movingRight and bgScroll < 500) or (self.rect.left < start.SCROLLSTART and self.movingLeft and bgScroll > 0)):
            self.rect.x -= accX
            screenScroll = - accX

        # If we have scrolled more than 500 in the right direction stop scrolling its the end of our map
        elif(self.rect.right > start.WIDTH - start.SCROLLSTART and self.movingRight and bgScroll >= 500):
            self.rect.x -= accX
        
        # If we are trying to scroll back left even though the background is at 0, 0 stop scrolling 
        elif(self.rect.left < start.SCROLLSTART and self.movingLeft and bgScroll <= 0):
            self.rect.x -= accX
        
        # Return this value so we can offset everything by the bgScroll (skeletons and stuff should move back when we scroll forward vice versa)
        return screenScroll
            
            
    # The draw function that is called by main
    def draw(self, screen):
        
        # Put this try except block in your code asweell, it is very easy to mess up the numbers for the animation and this prints to the terminal relevant info
        # instead of just crashing the program
        try:
            screen.blit(pygame.transform.flip(self.animations[self.currentAction][self.index], self.facingLeft, False), self.rect)
        
        except IndexError:
            print(self.currentAction, self.index)
            



################################### Skellies ###################################

# This is used to make our skellies
# I won't explaint this as much as I did player because
# That isn't entirely how you are meant to comment (I think I've written up more comments than code)
# Also because they share alot of commanilty, where they don't I have explained.

# This is our skels object that inherits from that useless GameObject that we made earlier
class Skels(GameObject):
    
    # As usualy this is called when we do skeleton = Skels(40, 550)
    def __init__(self, x, y):
        super().__init__(1.5, 1, "img/enemies/Skeleton Idle.png")
        
        # Same basic vairbles
        self.alive = True
        self.health = 4
        
        # This is pretty cool
        # We make rectangle that kind of sets just infront of the skeleton that represents its vision
        # When the player collides with this rectangle it represents that the skeleton can see the player
        # When this happens the skeletons eyes flares and it becomes agro
        # Try experimenting with this 
        self.vision = pygame.Rect(0, 0, 150, 20)
        
        self.movingRight = False
        self.movingLeft = False 
        self.jumping = False 
        self.yVel = 0
        
        # This is also pretty fancy
        # This is the idle counter for our skeletor
        # We kind of want our skeleton to partrol: walk for a bit, go idle for a bit, turnaround and repeat 
        # These variables handle that
        # The idletimer is how we check how long the skelly stays idle for.
        # We don't want this to be a fixed value or all the skeletons would turn around at the same time and it would look robotic.
        # We want the skellies to turn around at diff times and make them seem not entirely brainles
        self.idleCounter = 0 #200
        self.idleTimer = randint(200, 500)
        
        # Our skelly's sprites are way too small (smaller than (dark) red riding hood)
        # So we ant to scale them up by a bit
        self.scale = 1.5
        
        self.facingLeft = True
        
        self.index = 0
        self.movingIndex = 0
        
        
        # Same as we have done for player.
        # Check that out if you haven't yet.
        self.animations = {}
        self.currentAction = "idle"
        
        idleSpriteSheet = Spritesheet('img/enemies/Skeleton Idle.png')
        damageSprites = Spritesheet("img/enemies/Skeleton Hit.png")
        deadSprites = Spritesheet("img/enemies/Skeleton Dead.png")
        movingSprites = Spritesheet("img/enemies/Skeleton Walk.png")
        attackSprites = Spritesheet("img/enemies/Skeleton Attack.png")
        
        
        # Same thing as we have done for player but we scale all the images before putting them in the list.
        # Makes the code very undereadable. Might not want to do it like this for a team project.
        self.animations["idle"] = [pygame.transform.scale(idleSpriteSheet.parse_sprite(f'skeleton_idle{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 12)]
        
        self.animations["damage"] = [pygame.transform.scale(damageSprites.parse_sprite(f'skeleton_damage{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 8)]
        
        self.animations["dying"] = [pygame.transform.scale(deadSprites.parse_sprite(f'skeleton_dead{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 16)]


        self.animations["moving"] = [pygame.transform.scale(movingSprites.parse_sprite(f'skeleton_walk{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 14)]
        
        # why this instead of just doing self.animations[agro] = self.animations[moving]? because python works using references. 
        # Just means that it doesn't copy the list but makes them the same thing.
        self.animations["agro"] = [pygame.transform.scale(movingSprites.parse_sprite(f'skeleton_walk{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 14)]
        
         # why this? because python works using references
        self.animations["attack"] = [pygame.transform.scale(attackSprites.parse_sprite(f'skeleton_attack{i}.png'),  
                                                          (43 * self.scale, 37 * self.scale)) for i in range(1, 19)]
        
        self.clock = pygame.time.Clock()
        
        self.rect = self.animations["idle"][0].get_rect()
        self.rect.x = x
        self.rect.y = y    
    
    
    # The update funciton for skellies are technically different than player
    # In general a group update (the default group update. you can write your own that kinda overrides it.) calls update on each sprite apart of the group.
    # So its quite usefull to call handelling functions update
    def update(self, scroll): 
        
        # If we have scrolled a bit scroll the skeleton a bit
        self.rect.x += scroll
        
        # What is the difference with bgScroll/backgroundScroll and scroll
        # Good question. You might want to check main() in start.py
        # But basiacally scroll is like an increment value (i think its 5). So every second the player moves the map by this value of 5 or smth.
        # bgScroll (or called backgroundScroll in start.py) is the cumalative value that we have move the map. bgScroll = + scroll + scroll + scroll + scroll + scroll = 25 (or smth)
        # We could technically use bgScroll to manage skellies but its easier to increment their position rather than track where they are using bgScroll
        
        # If the skelly is facing left or right change its vision respecitvely.  
        if(self.facingLeft):
            self.vision.center = (self.rect.centerx + 65 * -1, self.rect.centery)
        else:
            self.vision.center = (self.rect.centerx + 65 * 1, self.rect.centery)
        

        # If we (Skellies) are attacking or dying we should not be able to do anything else
        if(self.currentAction == "dying"):
            return
        
        if(self.currentAction == "attack"):
            return
       
       
        # Agro is when we (Skellies) spot a player and we just feel the need to move towards them untill they dissappear or we kill them.    
        if(self.currentAction == "agro"):
            if(self.facingLeft):
                self.movingLeft = True
                self.movingRight = False
                
            else:
                self.movingRight = True
                self.movingLeft = False
           

        # Idle is when we get bore of walking and we stand for a bit
        if(self.currentAction == "idle"):
            

            # If we have been idle for too little we sit tight a bit longer
            if self.idleCounter < self.idleTimer:
                self.idleCounter += 1
                return
            
            # If we have been idle for more than our programmer has told us to, then we turn around and start moving
            self.idleTimer = randint(200, 500)
            self.idleCounter = 0
            self.currentAction = "moving"
            self.index = 0
            
            if(self.facingLeft):
                self.facingLeft = False
                self.movingLeft = False
                self.movingRight = True    
                
            elif(not self.facingLeft):
                self.facingLeft = True
                self.movingLeft = True
                self.movingRight = False

        # Calling the move function directly from update
        # Unlike for player I (the programmer) did not need move and update seperately for skellies (you may need to though)
        self.move()
    
    
    # Called every frame
    def tick(self, ticks):
        
        if(self.currentAction == "idle" and ticks % 15 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
            
        if(self.currentAction == "damage" and ticks % 6 == 0):
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1) 
                
            else:
                self.index = 0
                self.currentAction = "idle"
        
        # We can't keep moving. Every 8 function calls we transition our animation, but we stop after we are done with two moving animations. 
        if(self.currentAction == "moving" and ticks % 8 == 0):
            
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1) 
                
            # Check if we have completed two moving animations and then stop if we have
            else:
                
                # Reset the animations
                self.index = 0
                
                # Increment the times we have moved
                self.movingIndex += 1
                
                if(self.movingIndex >= 2):
                    self.currentAction = "idle"
                    self.movingIndex = 0

        # If we are agro we keep moving until the player dissappears into blackness, or we are close enough to attack the player.
        if(self.currentAction == "agro" and ticks % 8 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction]) 
            
        # Called every 12 function calls, 
        if(self.currentAction == "attack" and ticks % 12 == 0):
                                    
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1)

            else:
                self.index = 0
                self.currentAction = "idle"
                self.idleCounter = 0
                self.idleTimer = randint(200, 500) # changes the idle timer to make the skellies seem a bit more natural as they do want crave to be humans 
                # (and hence they try eating humans to become more human ;-;) 
    
    
        # If we die we go to skelly heaven, but before that we have to go through our dying animation
        # Every 6 function call we move through the dying animation animation  
        if(self.currentAction == "dying" and ticks % 6 == 0):
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1) 
            
            else:
                self.kill()
            
    # If the player attacks an aenmy this is called.
    def damage(self, damage):
        
        if(self.alive == False):
            return
        
        self.health -= damage
        
        self.index = 0
        self.currentAction = "damage"
        if(self.health <= 0):
            
            self.currentAction = "dying"

    
    def move(self):
        accX = 0
        accY = 0

        if self.movingLeft:
            accX = -self.speed
            
        if self.movingRight:
            accX = self.speed
            
        if(self.jumping):
            self.yVel = -10
            self.jumping = False
        
        if(self.rect.y < 600):
            if(not self.yVel > 5):
                self.yVel += 0.75    
        
        elif(self.yVel != 0 and self.rect.y > 600):
            self.yVel = 0
            self.rect.y = 600
            
            if(self.currentAction == "jump"):
                self.currentAction = "idle"
            
        accY = self.yVel

           
        self.rect.x += accX
        self.rect.y += accY
    
    
    def draw(self, screen):
        try:
            
            if self.currentAction == "attack":
                if(self.facingLeft):
                    screen.blit(pygame.transform.flip(self.animations[self.currentAction][self.index], self.facingLeft, False), self.rect.move(-30, -6))
                    self.rect.move(18, 6)
                    
                else:
                    screen.blit(pygame.transform.flip(self.animations[self.currentAction][self.index], self.facingLeft, False), self.rect.move(4, -6))
                    self.rect.move(-2, 6)
                return
            screen.blit(pygame.transform.flip(self.animations[self.currentAction][self.index], self.facingLeft, False), self.rect)
            # pygame.draw.rect(screen, (0xBF,0x0F,0xB5), self.vision)
            
        except IndexError:
            print(self.currentAction, self.index)
            

class skeletonGroup(pygame.sprite.Group):
    def __init__(self, player):
        super().__init__()
        
        self.player = player
        
    def update(self, ticks, scroll):
        for sprite in self.sprites():
            
            sprite.tick(ticks)
            sprite.update(scroll)
            
            # print(sprite.currentAction, sprite.vision.colliderect(self.player.rect))
            
            if(self.player.currentAction == "hurt"):
                return
            
            if(sprite.vision.colliderect(self.player.rect) and sprite.currentAction != "agro" and sprite.currentAction != "attack"):
                sprite.index = 0
                sprite.currentAction = "agro"
                
            if(not sprite.vision.colliderect(self.player.rect) and sprite.currentAction == "agro"):
                sprite.index = 0
                sprite.idleCounter = 0
                sprite.idleTimer = randint(200, 500)
                sprite.currentAction = "idle"
                
            elif(sprite.currentAction == "agro"):
                if(pygame.sprite.collide_rect(self.player, sprite)):
                    sprite.index = 0
                    sprite.currentAction = "attack"
                    sprite.movingLeft = False
                    sprite.movingRight = False
                pass
            
            elif(sprite.currentAction == "attack" and sprite.index >= 6 and pygame.sprite.collide_rect(self.player, sprite)):
                self.player.hurt()
            
            
                
                
    def draw(self, screen):
        
        for sprite in self.sprites():
            
            sprite.draw(screen)
            
            
    def collidePlayer(self, player):
        for sprite in self.sprites():
            # if (player.rect.center)
            
            if (abs(player.rect.center[0] - sprite.rect.center[0]) <= 20 and abs(player.rect.center[1] - sprite.rect.center[1]) <= 25 and player.currentAction != "hurt" and sprite.currentAction != "dying"):
                player.hurt()
            
            # if pygame.sprite.collide_mask(player, sprite):
            #     player.hurt()
            
            