import pygame
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 150)


class Fighter():
    
    def __init__(self, x, y, player, data, imgPath, steps):
        self.player = player
        self.width = 80
        self.height = 140
        self.rect = pygame.Rect((x, y, self.width, self.height))
        self.speed = 10
        self.jumpSpeed = 0
        self.jumpHeight = 600
        self.attack_type = ''
        self.attacking = False
        self.attackRect = pygame.Rect((0,0,0,0))
        self.health = 100
        self.WidthSize = data[0][0]
        self.HeightSize = data[0][1]
        self.scale = data[1]
        self.adjusting = data[2]
        self.animationList = self.loadImages(imgPath, steps)
        # 0 : attack1
        # 1 : attack2
        # 2 : Death
        # 3 : Fall
        # 4 : Hit
        # 5 : Idle
        # 6 : Jump
        # 7 : Run
        self.action = 5
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()
        
        self.isRunning = False
        self.isJumping = False
        self.isAttacking = False
        self.isAttacking1 = False
        self.isAttacking2 = False
        self.Attacked = False
        self.dead = False
    
    def loadImages(self, imgPath, steps): 
        #extract images from image
        animationList = []
        for animation in steps:
            tempImgList = []
            img = pygame.image.load(os.path.join(imgPath, animation+'.png'))
            for x in range(steps[animation]):
                tempImg = img.subsurface(x * self.WidthSize, 0, self.WidthSize, self.HeightSize)
                tempImg = pygame.transform.scale(tempImg, (100*self.scale, 100*self.scale))
                tempImgList.append(tempImg)
            animationList.append(tempImgList)
        return animationList    
        
    def update(self, screen, enemy): 
        dx = 0
        dy = 0
        gravity = 2
        key = pygame.key.get_pressed()
        #move
        self.isRunning = False
        
        if key[pygame.K_LEFT] and self.player == 'left':
            dx = -self.speed
            self.isRunning = True
        if key[pygame.K_RIGHT] and self.player == 'left':
            dx = self.speed
            self.isRunning = True
        #jump
        if key[pygame.K_SPACE] and self.player == 'left':
            if self.rect.bottom == WINDOW_HEIGHT - 10: # one spacebar one jump
                self.jumpSpeed = -35
                self.isJumping = True
        #attack
        if (key[pygame.K_x] or key[pygame.K_c]) and self.player == 'left':
            self.isAttacking = True
            self.attack(screen, enemy)
            if key[pygame.K_x]:
                self.isAttacking1 = True
            elif key[pygame.K_c]:
                self.isAttacking2 = True
            
        #grav
        self.jumpSpeed += gravity
        dy += self.jumpSpeed
        
        # stay on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WINDOW_WIDTH:
            dx = WINDOW_WIDTH - self.rect.right
        if self.rect.bottom + dy > WINDOW_HEIGHT - 10:
            self.jumpSpeed = 0
            self.isJumping = False
            dy = WINDOW_HEIGHT - 10 - self.rect.bottom
        
        self.rect.x += dx
        self.rect.y += dy  
        
    def animationUpdate(self):
        animationCD = 70
        if self.dead :
           self.updateAction(2) 
        elif self.Attacked :
            self.updateAction(4) # hit
        elif self.isRunning :
            self.updateAction(7) # run
        elif self.isJumping :
            self.updateAction(6) # jump
        elif self.isAttacking :
            if self.isAttacking1:
                self.updateAction(0) #attack1
            elif self.isAttacking2:
                self.updateAction(1) #attack2
        else:
            self.updateAction(5)
            
        self.image = self.animationList[self.action][self.frameIndex]
        #check if time has passed since the last update
        if self.action == 2 :
            animationCD = 400
            if pygame.time.get_ticks() - self.updateTime > animationCD:
                self.frameIndex += 1
                self.updateTime = pygame.time.get_ticks()
                if self.frameIndex >= len(self.animationList[self.action]):
                   self.action = 2
                   self.frameIndex = 5
        elif self.action in [0, 1, 4] :
            if pygame.time.get_ticks() - self.updateTime > animationCD:
                self.frameIndex += 1
                self.updateTime = pygame.time.get_ticks()
                if self.frameIndex >= len(self.animationList[self.action]):
                    self.updateAction(5)
                    self.isAttacking = False
                    self.isAttacking1 = False
                    self.isAttacking2 = False
                    self.Attacked = False
                    
        else :
            if pygame.time.get_ticks() - self.updateTime > animationCD:
                self.frameIndex += 1
                self.updateTime = pygame.time.get_ticks()
                if self.frameIndex >= len(self.animationList[self.action]):
                    self.frameIndex = 0
            
    def attack(self, screen, enemy):
        self.attackRect = pygame.Rect(self.rect.x, self.rect.y-20, self.rect.width+160, 180)
        if self.attackRect.colliderect(enemy.rect): # dectect collision
            enemy.beAttacked(screen)
    
    def beAttacked(self, screen):
        self.health -= 1
        self.Attacked = True
        if self.health <= 0:
            self.dead = True
           
    def updateAction(self, newAction):
        #check if the newaction is diffrenet to the previous action
        if newAction != self.action:
            self.action = newAction
            #update 
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()
                
    def draw(self, screen):
        # pygame.draw.rect(screen, BLUE, self.rect)
        if self.player == 'right':
            img = pygame.transform.flip(self.image, True, False)
        else:
            img = self.image
        screen.blit(img, (self.rect.x-self.adjusting[0], self.rect.y-self.adjusting[1]))
        # pygame.draw.rect(screen, RED, (self.rect.x-100, self.rect.y-100, self.image.get_rect().width, self.image.get_rect().height) ,4)
        # pygame.draw.rect(screen, PINK, (self.rect.x, self.rect.y-20, self.rect.width+160, 180), 5)