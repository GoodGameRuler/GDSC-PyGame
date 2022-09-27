from random import randint
from re import L
import pygame
import start
from spritesheet import Spritesheet 

class gameObject(pygame.sprite.Sprite):
    def __init__(self, scale, speed, src):
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed
        
        self.image = pygame.image.load(src)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        
        
        # self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.rect.width = 40
        # self.rect.height = 80
                
        
class Player(gameObject):

    def __init__(self):
        super().__init__(1, 2, "img/player/idle.png")
        
        self.alive = True
        self.lives = 5
        self.enemies = []
        
        self.movingRight = False
        self.movingLeft = False 
        self.jumping = False 
        self.yVel = 0
        
        self.attackOneCoolDown = 0 # 400
        self.attackOneCoolDown = 0 # 1200
        
        self.facingLeft = False
        
        self.index = 0
        self.movingIndex = 0
        
        self.animations = {}
        self.currentAction = "idle"
        
        idleSpriteSheet = Spritesheet('img/player/idle.png')
        runningSprites = Spritesheet('img/player/run.png')
        # turningSprites = Spritesheet("img/player/turn.png")
        
        jumpSprites = Spritesheet("img/player/jump.png")
        hurtSprite = Spritesheet("img/player/hurt.png")
        attackSprite = Spritesheet("img/player/attack.png")
        self.animations["idle"] = [idleSpriteSheet.parse_sprite(f'f_redHood{i}.png') for i in range(1, 19)]
        self.animations["move"] = [runningSprites.parse_sprite(f'f_redHood{i}.png') for i in range(1, 25)]
        # self.animations["turn"] = [turningSprites.parse_sprite(f'f_redHood{i}.png') for i in range(1, 25)]
        
        self.animations["jump"] = [jumpSprites.parse_sprite(f'f_redHood{i}.png') for i in range(1, 18)]
        self.animations["hurt"] = [hurtSprite.parse_sprite(f'f_redHood{i}.png') for i in range(1, 8)]
        self.animations["attack"] = [attackSprite.parse_sprite(f'f_redHood{i}.png') for i in range(1, 25)]

        
        self.clock = pygame.time.Clock()
        
        self.rect = self.animations["idle"][0].get_rect()
        self.rect.x = 50
        self.rect.y = 200
        
    
    def update(self, left, right, up, down, attack):  
        
        if(self.currentAction == "hurt"):
            return
        
        if(attack and self.currentAction != "attack" and self.attackOneCoolDown == 0):
            
            if(self.attackOneCoolDown == 0):
                self.currentAction = "attack"
                self.attackOneCoolDown = 150
                       
            return
                
        
        if(self.currentAction == "attack"):
            
            if(attack):
               
                if(self.index % 6 == 0):
                    for enemyGroup in self.enemies:
                        for enemy in pygame.sprite.spritecollide(self, enemyGroup, False):
                            # print(enemy.rect.x, self.rect.x)
                            if(enemy.rect.x - self.rect.x >= 3 and self.facingLeft == False):
                                enemy.damage(1)
                                
                            if(enemy.rect.x - self.rect.x <= -3 and self.facingLeft == True):
                                enemy.damage(1)
                            
                # self.movingIndex += 1
                self.attackOneCoolDown = 150          
                return

            self.currentAction = "idle"
            self.index = 0
        
        # change to on the floor
        if(up and self.currentAction != "jump" and self.rect.y == 600):
            self.movingLeft = False
            self.movingRight = False
            
            self.index = 0
            self.jumping = True
            
            self.currentAction = "jump"
        
        if(left and right):
            self.movingLeft = False
            self.movingRight = False
            
            self.index = 0
            
            self.currentAction = "idle"
            
            if(self.movingLeft or self.movingRight or self.jumping):
                self.index = 0
            
            return
        
        if(left and not self.movingLeft):
            self.movingLeft = True
            self.movingRight = False
            self.facingLeft = True
            
            self.index = 0
            
            self.currentAction = "move"
            
        if(not left and self.movingLeft):
            
            if(not right):
                self.currentAction = "idle"
            
            self.movingLeft = False
            self.index = 0
           
            
        if(right and not self.movingRight):
            self.movingRight = True
            self.movingLeft = False
            self.facingLeft = False
            
            self.currentAction = "move"
            
            self.index = 0
        
        if(not right and self.movingRight):
            
            if(not left):
                self.currentAction = "idle"
            
            self.movingRight = False
            self.index = 0
    
    
    def hurt(self):
        
        self.lives -= 1
        if(self.lives == 0):
            self.kill()
            return
        
        
        self.index = 0
        self.currentAction = "hurt"
        
   
    def tick(self, ticks):

        if(self.currentAction == "idle" and ticks % 8 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
            
        elif (self.currentAction == "jump" and ticks % 10 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
            
        elif(self.currentAction == "attack" and ticks & 10 == 0):
            
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1)
            
            else:
                self.index = 0
                self.currentAction = "idle" 
            
        elif (self.currentAction == "hurt"):
            
            if (self.index >= len(self.animations[self.currentAction]) - 1):
                self.index = 0
                self.currentAction = "idle"
                
                self.rect.x = 5
                self.rect.y = 600
                
            else:
                if(ticks % 4 == 0):
                    self.index = (self.index + 1)
                    
        
        elif (ticks % 3 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
            

        if(self.attackOneCoolDown > 0):
            self.attackOneCoolDown -= 1

    
    def move(self, bgScroll):
        
        screenScroll = 0
        
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
                self.yVel += 0.5    
        
        elif(self.yVel != 0 and self.rect.y > 600):
            self.yVel = 0
            self.rect.y = 600
            
            if(self.currentAction == "jump"):
                self.currentAction = "idle"
            
        accY = self.yVel
                          
        self.rect.x += accX
        self.rect.y += accY
    
    
        if((self.rect.right > start.WIDTH - start.SCROLLSTART and self.movingRight and bgScroll < 500) or (self.rect.left < start.SCROLLSTART and self.movingLeft and bgScroll > 0)):
            self.rect.x -= accX
            screenScroll = - accX
            
        elif(self.rect.right > start.WIDTH - start.SCROLLSTART and self.movingRight and bgScroll >= 500):
            self.rect.x -= accX
            
        elif(self.rect.left < start.SCROLLSTART and self.movingLeft and bgScroll <= 0):
            self.rect.x -= accX
            
        return screenScroll
            
    
    def draw(self, screen):
        try:
            screen.blit(pygame.transform.flip(self.animations[self.currentAction][self.index], self.facingLeft, False), self.rect)
        
        except IndexError:
            print(self.currentAction, self.index)
            
            
class Skels(gameObject):
    def __init__(self, x, y):
        super().__init__(1.5, 1, "img/enemies/Skeleton Idle.png")
        
        self.alive = True
        self.health = 4
        self.vision = pygame.Rect(0, 0, 150, 20)
        
        self.movingRight = False
        self.movingLeft = False 
        self.jumping = False 
        self.yVel = 0
        
        self.idleCounter = 0 #200
        self.idleTimer = randint(200, 500)
        
        self.scale = 1.5
        
        self.facingLeft = True
        
        self.index = 0
        self.movingIndex = 0
        
        self.animations = {}
        self.currentAction = "idle"
        
        idleSpriteSheet = Spritesheet('img/enemies/Skeleton Idle.png')
        # runningSprites = Spritesheet('img/player/run.png')
        damageSprites = Spritesheet("img/enemies/Skeleton Hit.png")
        
        deadSprites = Spritesheet("img/enemies/Skeleton Dead.png")
        
        movingSprites = Spritesheet("img/enemies/Skeleton Walk.png")
        
        attackSprites = Spritesheet("img/enemies/Skeleton Attack.png")
        
        # jumpSprites = Spritesheet("img/player/jump.png")
        self.animations["idle"] = [pygame.transform.scale(idleSpriteSheet.parse_sprite(f'skeleton_idle{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 12)]
        
        self.animations["damage"] = [pygame.transform.scale(damageSprites.parse_sprite(f'skeleton_damage{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 8)]
        
        self.animations["dying"] = [pygame.transform.scale(deadSprites.parse_sprite(f'skeleton_dead{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 16)]


        self.animations["moving"] = [pygame.transform.scale(movingSprites.parse_sprite(f'skeleton_walk{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 14)]
        
        # why this? because python works using references
        self.animations["agro"] = [pygame.transform.scale(movingSprites.parse_sprite(f'skeleton_walk{i}.png'),  
                                                          (24 * self.scale, 32 * self.scale)) for i in range(1, 14)]
        
         # why this? because python works using references
        self.animations["attack"] = [pygame.transform.scale(attackSprites.parse_sprite(f'skeleton_attack{i}.png'),  
                                                          (43 * self.scale, 37 * self.scale)) for i in range(1, 19)]
        
        self.clock = pygame.time.Clock()
        
        self.rect = self.animations["idle"][0].get_rect()
        self.rect.x = x
        self.rect.y = y    
    
    def update(self, scroll): 
        
        self.rect.x += scroll
        
        if(self.facingLeft):
            self.vision.center = (self.rect.centerx + 65 * -1, self.rect.centery)
        else:
            self.vision.center = (self.rect.centerx + 65 * 1, self.rect.centery)
        
                     
        if(self.currentAction == "dying"):
            return
        
        if(self.currentAction == "attack"):
            return
       
        if(self.currentAction == "agro"):
            if(self.facingLeft):
                self.movingLeft = True
                self.movingRight = False
                
            else:
                self.movingRight = True
                self.movingLeft = False
           

        if(self.currentAction == "idle"):
            

            # Value changes every call but thats fine
            if self.idleCounter < self.idleTimer:
                # print(self.idleCounter)
                self.idleCounter += 1
                return
            
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

        
        
        self.move()
    
    def tick(self, ticks):
               
        if(self.currentAction == "idle" and ticks % 15 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction])
            
        if(self.currentAction == "damage" and ticks % 6 == 0):
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1) 
                
            
            else:
                self.index = 0
                self.currentAction = "idle"
            
            # self.index = (self.index + 1) % len(self.animations[self.currentAction])
        
        if(self.currentAction == "moving" and ticks % 8 == 0):
            
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1) 
                
            
            else:
                self.index = 0
                self.movingIndex += 1
                
                if(self.movingIndex >= 2):
                    self.currentAction = "idle"
                    self.movingIndex = 0
                    
        if(self.currentAction == "agro" and ticks % 8 == 0):
            self.index = (self.index + 1) % len(self.animations[self.currentAction]) 
            
        if(self.currentAction == "attack" and ticks % 12 == 0):                        
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1)
                
                

            else:
                self.index = 0
                self.currentAction = "idle"
                self.idleCounter = 0
                self.idleTimer = randint(200, 500) 
        
        
        if(self.currentAction == "dying" and ticks % 6 == 0):
            if(self.index < len(self.animations[self.currentAction]) - 1):
                self.index = (self.index + 1) 
            
            else:
                self.kill()
            

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
            
            