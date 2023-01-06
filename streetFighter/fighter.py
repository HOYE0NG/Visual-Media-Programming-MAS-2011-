import pygame

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
    def __init__(self, x, y, player):
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
        
    def update(self, screen, enemy): # fighter move with keyboard
        dx = 0
        dy = 0
        gravity = 2
        key = pygame.key.get_pressed()
        #move
        if key[pygame.K_LEFT]:
            dx = -self.speed
        if key[pygame.K_RIGHT]:
            dx = self.speed
        #jump
        if key[pygame.K_SPACE]:
            if self.rect.bottom == WINDOW_HEIGHT - 10: # one spacebar one jump
                self.jumpSpeed = -35
        #attack
        if key[pygame.K_x] or key[pygame.K_c]:
            self.attack(screen, enemy)
            if key[pygame.K_x]:
                self.attack_type = 'punch'
            self.attacking = False
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
            dy = WINDOW_HEIGHT - 10 - self.rect.bottom
        
        self.rect.x += dx
        self.rect.y += dy  

        #health
        

    def attack(self, screen, enemy):
        self.attacking = True
        self.attackRect = pygame.Rect(self.rect.centerx, self.rect.y, 2*self.rect.width, self.rect.height)
        if self.attackRect.colliderect(enemy.rect): # dectect collision
            enemy.health -= 10
                
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
