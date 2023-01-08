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

swordsmanImgPath = os.path.join(assets_path, 'swordsman')
wizardImgPath = os.path.join(assets_path, 'wizard')

swordsmanSteps = {"Attack1":6, 'Attack2':6, 'Death':6, 'Fall':2, 'Hit':4, 'Idle':8, 'Jump':2, 'Run':8}
wizardSteps = {"Attack1":8, 'Attack2':8, 'Death':7, 'Fall':2, 'Hit':4, 'Idle':6, 'Jump':2, 'Run':8}

swordsmanSize = (200, 200)
wizardSize = (231, 190)

swordsmanData = [swordsmanSize, 4.2,(157,132)]
wizardData = [wizardSize,3,(117,100)]

# font       
myFont = pygame.font.Font(None, 100)
myText = myFont.render("Game Over", True, BLACK) 
f1Text = myFont.render("left player win", True, BLUE)
f2Text = myFont.render("right player win", True, BLUE)

# --
fighter1 = Fighter(100, 650, 'left', swordsmanData, swordsmanImgPath, swordsmanSteps)
fighter2 = Fighter(700, 650, 'right', wizardData, wizardImgPath, wizardSteps)



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
        self.f1HpLose = False
        self.f2HpLose = False
    
    def update(self, screen, f1Hp, f2Hp):
        self.f1HpRectReal.width = self.f1HpRect.width/100 * f1Hp
        self.f2HpRectReal.width = self.f2HpRect.width/100 * f2Hp
        self.f1HpRectReal.right = self.healthBarCenter.left - 3
        self.f2HpRectReal.left = self.healthBarCenter.right + 3
        if f1Hp <= 0 or f2Hp <= 0:
            self.gameIsDone = True
            if f1Hp <= 0:
                self.f1HpLose = True
            else :
                self.f2Hplose = True
    
    def draw(self, screen):
        screen.blit(backgroundImg, (0, 0))
        pygame.draw.rect(screen, BLACK, self.healthBarCenter)
        pygame.draw.rect(screen, BLACK, self.healthBarLeft, 3)
        pygame.draw.rect(screen, BLACK, self.healthBarRight, 3)
        pygame.draw.rect(screen, RED, self.f1HpRectReal)
        pygame.draw.rect(screen, RED, self.f2HpRectReal)   
        if self.gameIsDone:
            screen.blit(myText, [100,400])
            if self.f1HpLose:
                screen.blit(f2Text, [100,500])
            elif self.f2Hplose:    
                screen.blit(f1Text, [100,500])
            
window = Window(fighter1.health, fighter2.health)

# 게임 반복 구간
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 게임 로직 구간
    fighter1.update(screen, fighter2)
    fighter2.update(screen, fighter1)
    window.update(screen, fighter1.health, fighter2.health)

    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # 화면 그리기 구간
    window.draw(screen)
    fighter1.draw(screen)
    fighter1.animationUpdate()
    fighter2.draw(screen)
    fighter2.animationUpdate()

    # 화면 업데이트 / 프레임
    pygame.display.flip()
    clock.tick(FPS)

# 게임 종료

pygame.quit()