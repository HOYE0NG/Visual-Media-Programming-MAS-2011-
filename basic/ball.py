import pygame
import numpy as np

# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Ball")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

#공 개수
numBalls = 100
 
#class
class Ball:
    def __init__(self,):
        self.x = np.random.randint(low=0, high=WINDOW_WIDTH) 
        self.y = np.random.randint(0, WINDOW_HEIGHT)
        self.radius = np.random.randint(5,20)
        self.dx = 10
        self.dy = 10
        self.color = (np.random.randint(255), np.random.randint(255), np.random.randint(255))
    
    def update(self,):
        self.x += self.dx
        self.y += self.dy
        
        if self.x + self.radius > WINDOW_WIDTH or (self.x - self.radius) < 0:
            self.dx *= -1
            
        if self.y + self.radius > WINDOW_HEIGHT or (self.y - self.radius) < 0:
            self.dy *= -1
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# 게임 종료 전까지 반복
done = False

# Ball 리스트 생성
listOfBalls = []
for i in range(numBalls):
    ball = Ball()
    listOfBalls.append(ball)
    
# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 게임 로직 구간
    # 속도에 따라 원형 위치 변경 : state update / logic update / parameter update
    #---------------------
    for i in range(numBalls):
        ball = listOfBalls[i]
        ball.update()
    #---------------------   
         
    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # 화면 그리기 구간
    # 공 그리기
    for i in range(numBalls):
        ball = listOfBalls[i]
        ball.draw(screen) 
    
    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60) # 60 frames for second
                  # ball_dx = 4
                  # ball_velocity_x = 4 pixels / 1frame * 60 (frames / second)
                  #                 = 240 pixels / second


# 게임 종료
pygame.quit()