# Draw a robot arm with multiple joints, controlled with keyboard inputs
#
# -*- coding: utf-8 -*- 

import pygame
import numpy as np
import random

# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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


# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("ROBOT")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False
# 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
font = pygame.font.SysFont('FixedSys', 40, True, False)

# poly: 4 x 3 matrix
poly = np.array( [[0, 0, 1], 
                  [100, 0, 1], 
                  [100, 20, 1], 
                  [0, 20, 1]])
poly = poly.T # 3x4 matrix 

cor = np.array([10, 10, 1])
cor2 = np.array([90, 10, 1])
degree = 1
degree1 = 0
degree2 = 0
degree3 = 0

auto = True
# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if auto:
                    degree1 = degree
                    degree2 = degree
                    degree3 = degree
                auto = not auto
                
            if not auto :
                if event.key == pygame.K_q:
                    degree1 += 10
                    degree2 += 0
                    degree3 += 0
                if event.key == pygame.K_w:
                    degree2 += 10
                    degree3 += 0
                if event.key == pygame.K_e:
                    degree3 += 10             
    # 윈도우 화면 채우기
    screen.fill(WHITE)


    
    # 원래 자리 
    
    
    if auto :
        degree += 1
        H = Tmat(300, 300) @ Tmat(10, 10) @ Rmat(degree) @ Tmat(-10, -10)
        pp = H @ poly
        corp = H @ cor
        q = pp[0:2, :].T
        pygame.draw.polygon(screen, RED, q, 4)
        pygame.draw.circle(screen, GREEN, corp[:2], 3)
        corp2 = H @ cor2
        pygame.draw.circle(screen, RED, corp2[:2], 3)
        
        H2 = Tmat(corp2[0], corp2[1]) @ Rmat(degree) @ Tmat(-corp2[0], -corp2[1]) @ Tmat(300, 300) @  Tmat(10, 10) @ Rmat(degree) @ Tmat(-10, -10)
        pp = H2 @ poly
        corp3 = H2 @ cor
        q = pp[0:2, :].T
        pygame.draw.polygon(screen, BLUE, q, 4)
        pygame.draw.circle(screen, BLUE, corp3[:2], 3)
        corp2 = H2 @ cor2
        pygame.draw.circle(screen, BLACK, corp2[:2], 3)

        H3 = Tmat(corp3[0], corp3[1]) @ Rmat(degree) @ Tmat(-corp3[0], -corp3[1]) @ Tmat(corp2[0], corp2[1]) @ Rmat(degree) @ Tmat(-corp2[0], -corp2[1]) @ Tmat(300, 300) @ Tmat(10, 10) @ Rmat(degree) @ Tmat(-10, -10)
        pp = H3 @ poly
        corp = H3 @ cor
        q = pp[0:2, :].T
        pygame.draw.polygon(screen, BLACK, q, 4)
    else :
        H = Tmat(300, 300) @ Tmat(10, 10) @ Rmat(degree1) @ Tmat(-10, -10)
        pp = H @ poly
        corp = H @ cor
        q = pp[0:2, :].T
        pygame.draw.polygon(screen, RED, q, 4)
        pygame.draw.circle(screen, GREEN, corp[:2], 3)
        corp2 = H @ cor2
        pygame.draw.circle(screen, RED, corp2[:2], 3)
        
        H2 = Tmat(corp2[0], corp2[1]) @ Rmat(degree2) @ Tmat(-corp2[0], -corp2[1]) @ Tmat(300, 300) @  Tmat(10, 10) @ Rmat(degree1) @ Tmat(-10, -10)
        pp = H2 @ poly
        corp3 = H2 @ cor
        q = pp[0:2, :].T
        pygame.draw.polygon(screen, BLUE, q, 4)
        pygame.draw.circle(screen, BLUE, corp3[:2], 3)
        corp2 = H2 @ cor2
        pygame.draw.circle(screen, BLACK, corp2[:2], 3)

        H3 = Tmat(corp3[0], corp3[1]) @ Rmat(degree1) @ Tmat(-corp3[0], -corp3[1]) @ Tmat(corp2[0], corp2[1]) @ Rmat(degree2) @ Tmat(-corp2[0], -corp2[1]) @ Tmat(300, 300) @ Tmat(10, 10) @ Rmat(degree3) @ Tmat(-10, -10)
        pp = H3 @ poly
        corp = H3 @ cor
        q = pp[0:2, :].T
        pygame.draw.polygon(screen, BLACK, q, 4)
    


    # 안티얼리어스를 적용하고 검은색 문자열 렌더링
    text = font.render("ROBOT ARMS", True, BLACK)
    screen.blit(text, [50, 550])
    text = font.render("press a = auto control", True, BLACK)
    screen.blit(text, [10, 600])
    text = font.render("q = upperarm / w = forearm / e = hand", True, BLACK)
    screen.blit(text, [10, 650])

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()