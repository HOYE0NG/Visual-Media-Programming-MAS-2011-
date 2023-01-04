import pygame
import numpy as np
# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 150)

# --
FPS = 60

pygame.init()
pygame.display.set_caption("WIND MILL")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def rotate(poly, degree, XY):
    radian = np.deg2rad(degree) # 라디안화
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s],
                  [s, c]]) # 회전 변환
    ppT = R @ poly.T # 전채
    pp = ppT.T # 전치    
    pp[0] += XY[0]
    pp[1] += XY[1]
    return pp, degree
    
class Wing:
    def __init__(self, startLoc):
        self.length = 200
        self.poly = np.array(startLoc)
        self.degreeSpeed = 1
        self.degree = 1
        self.loc = []
    def update(self):
        self.degree = self.degree % 360 + self.degreeSpeed
        self.loc, self.degree = rotate(self.poly, self.degree, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    def draw(self):
        # pygame.draw.circle(screen, BLACK, self.loc, 3, 3)
        edge1, something = rotate(np.array([self.loc[0]-WINDOW_WIDTH/2, self.loc[1]-WINDOW_HEIGHT/2]), 15, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        edge2, something = rotate(np.array([self.loc[0]-WINDOW_WIDTH/2, self.loc[1]-WINDOW_HEIGHT/2]), -15, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        pygame.draw.line(screen, PINK, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), edge1, 4)
        pygame.draw.line(screen, PINK, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), edge2, 4)
        pygame.draw.line(screen, PINK, edge1, edge2, 4)
        
w1 = Wing([0, -200])
w2 = Wing([200, 0])
w3 = Wing([0, 200])
w4 = Wing([-200, 0])

def main():
    done = False    

    while not done: 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        # 게임 로직 구간
        w1.update()
        w2.update()
        w3.update()
        w4.update()
        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)

        # 화면 그리기 구간
        pygame.draw.circle(screen, RED, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), 10, 10)
        pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2, 100, 300), 3)
        w1.draw()
        w2.draw()
        w3.draw()
        w4.draw()
        
        # 화면 업데이트 / 초당 60 프레임으로 업데이트
        pygame.display.flip()
        clock.tick(FPS)

    # 게임 종료
    pygame.quit()

if __name__ == "__main__":
    main()
    
