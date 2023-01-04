import pygame
import numpy as np
from datetime import datetime

# 게임 윈도우 크기
WINDOW_WIDTH = 600
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
pygame.display.set_caption("CLOCK")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# --
clockCenter = (WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2)
clockRadius = 300
armLenth = 270
startPoly = np.array([0, -armLenth])
degree = 30
nowDegree = 0
clockNumberLocation = [None]

def rotate(poly, degree, degreeSpeed):
    degree += degreeSpeed # 각도
    radian = np.deg2rad(degree) # 라디안화
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s],
                  [s, c]]) # 회전 변환
    ppT = R @ poly.T # 전채
    pp = ppT.T # 전치 
    return degree, pp

for i in range(1, 13):
    nowDegree += degree
    radian = np.deg2rad(nowDegree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s],
                  [s, c]]) # 회전 변환
    ppT = R @ startPoly.T # 전채
    pp = ppT.T # 전치 
    pp[0] += clockCenter[0]
    pp[1] += clockCenter[1]
    clockNumberLocation.append(pp)


class clockArms:
    def __init__(self, color):
        self.color = color
        self.degree = 6
        self.location = [0, 0]
    def update(self, degree):
        radian = np.deg2rad(degree)
        c = np.cos(radian)
        s = np.sin(radian)
        R = np.array([[c, -s],
                    [s, c]]) # 회전 변환
        ppT = R @ startPoly.T # 전채
        pp = ppT.T # 전치 
        pp[0] += clockCenter[0]
        pp[1] += clockCenter[1]
        self.location = pp
    def draw(self):
        pygame.draw.line(screen, self.color, clockCenter, self.location, 3)


hour = clockArms(BLACK)
minute = clockArms(RED)
second = clockArms(GREEN)


def main():
    done = False    

    while not done: 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        # 게임 로직 구간
        hour.update(datetime.now().hour%12*30)
        minute.update(datetime.now().minute*6)
        second.update(datetime.now().second*6)
        
        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(PINK)

        # 화면 그리기 구간
        pygame.draw.circle(screen, BLACK, clockCenter, clockRadius, 5) # draw clock circle 
        myFont = pygame.font.Font(None, 30)
        for i in range(1,13):
            screen.blit(myFont.render(f"{i}",True, BLACK), clockNumberLocation[i])
        hour.draw()
        minute.draw()
        second.draw()
        
        # 화면 업데이트 / 초당 60 프레임으로 업데이트
        pygame.display.flip()
        clock.tick(FPS)

    # 게임 종료
    pygame.quit()

if __name__ == "__main__":
    main()
    
