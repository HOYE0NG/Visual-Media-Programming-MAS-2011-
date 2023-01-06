import pygame
import os
from fighter import Fighter

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

# Pygame 초기화
pygame.init()
pygame.display.set_caption("Street Fighter")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
# 게임 종료 전까지 반복
done = False   

# --
FPS = 60

# --
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
backgroundImg = pygame.image.load(os.path.join(assets_path, 'background1.png'))
backgroundImg = pygame.transform.scale(backgroundImg, (WINDOW_WIDTH, WINDOW_HEIGHT))
# backgroundList = []
# backgroundList.append(backgroundImg)
       
# font       
myFont = pygame.font.Font(None, 100)
myText = myFont.render("Game Over", True, BLACK) 
# --
fighter1 = Fighter(100, 650, 'left')
fighter2 = Fighter(400, 650, 'right')

# --
class Window:
    
    def __init__(self, f1Hp, f2Hp):
        self.healthBarCenter = pygame.Rect(WINDOW_WIDTH/2-50, 20, 100, 80)
        self.healthBarLeft = pygame.Rect(50, 0, WINDOW_WIDTH/2-100, 50)
        self.healthBarLeft.centery = self.healthBarCenter.centery
        self.healthBarRight = pygame.Rect(WINDOW_WIDTH/2+50, 0, WINDOW_WIDTH/2-100, 50)
        self.healthBarRight.centery = self.healthBarCenter.centery
        self.f1Hp = f1Hp
        self.f2Hp = f2Hp 
        self.f1HpRect = pygame.Rect(self.healthBarLeft.x+3, self.healthBarLeft.y+3, WINDOW_WIDTH/2-100-6, 50-6)
        self.f2HpRect = pygame.Rect(self.healthBarRight.x+3, self.healthBarRight.y+3, WINDOW_WIDTH/2-100-6, 50-6)
        self.f1HpRectReal = pygame.Rect(self.healthBarLeft.x+3, self.healthBarLeft.y+3, WINDOW_WIDTH/2-100-6, 50-6)
        self.f2HpRectReal = pygame.Rect(self.healthBarRight.x+3, self.healthBarRight.y+3, WINDOW_WIDTH/2-100-6, 50-6)
        self.gameIsDone = False
    
    def update(self, screen, f1Hp, f2Hp):
        self.f1HpRectReal.width = self.f1HpRect.width/100 * f1Hp
        self.f2HpRectReal.width = self.f2HpRect.width/100 * f2Hp
        self.f1HpRectReal.right = self.healthBarCenter.left - 3
        self.f2HpRectReal.left = self.healthBarCenter.right + 3
        if f1Hp <= 0 or f2Hp <= 0:
            self.gameIsDone = True
    
    def draw(self, screen):
        screen.blit(backgroundImg, (0, 0))
        pygame.draw.rect(screen, BLACK, self.healthBarCenter)
        pygame.draw.rect(screen, BLACK, self.healthBarLeft, 3)
        pygame.draw.rect(screen, BLACK, self.healthBarRight, 3)
        pygame.draw.rect(screen, RED, self.f1HpRectReal)
        pygame.draw.rect(screen, RED, self.f2HpRectReal)   
        if self.gameIsDone:
            screen.blit(myText, [100,400])
        
# --
window = Window(fighter1.health, fighter2.health)

# 게임 반복 구간
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 게임 로직 구간
    fighter1.update(screen, fighter2)
    window.update(screen, fighter1.health, fighter2.health)

    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # 화면 그리기 구간
    window.draw(screen)
    fighter1.draw(screen)
    fighter2.draw(screen)

    # 화면 업데이트 / 프레임
    pygame.display.flip()
    clock.tick(FPS)

# 게임 종료

pygame.quit()