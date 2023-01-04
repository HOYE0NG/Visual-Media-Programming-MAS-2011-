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

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R

def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H

class Arm():
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 100, 200)
        self.rotate = [1, 1]
        self.joint = (self.rect.centerx, self.rect.centery)
    def update(self):
        pass
    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        pygame.draw.circle(screen, RED, self.joint, 2, 2)
        
        
upperArm = Arm()
foreArm = Arm()
hand = Arm()

armList = []
armList.append(upperArm)
armList.append(foreArm)
armList.append(hand)


def main():
    done = False    

    while not done: 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        # 게임 로직 구간
        for arm in armList:
            arm.update()
        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)

        # 화면 그리기 구간
        for arm in armList:
            arm.draw()

        # 화면 업데이트 / 초당 60 프레임으로 업데이트
        pygame.display.flip()
        clock.tick(FPS)

    # 게임 종료
    pygame.quit()

if __name__ == "__main__":
    main()
    
