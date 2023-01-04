import pygame
import os 
import numpy as np
import math

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

# --
FPS = 60

# PATH
currentPath = os.path.join(os.path.dirname(__file__))
assetPath = os.path.join(currentPath, 'assets')

# IMAGES
backgroundImg = pygame.image.load(os.path.join(assetPath, 'space.png'))
backgroundImg = pygame.transform.scale(backgroundImg, (WINDOW_WIDTH, WINDOW_HEIGHT))
earthImg = pygame.image.load(os.path.join(assetPath, 'earth.png'))
earthImg = pygame.transform.scale(earthImg, (10,10))
moonImg = pygame.image.load(os.path.join(assetPath, 'moon.png'))
moonImg = pygame.transform.scale(moonImg, (4, 4))
saturnImg = pygame.image.load(os.path.join(assetPath, 'saturn.png'))
saturnImg = pygame.transform.scale(saturnImg, (30, 30))
sunImg = pygame.image.load(os.path.join(assetPath, 'sun.png'))
sunImg = pygame.transform.scale(sunImg, (50, 50))
titanImg = pygame.image.load(os.path.join(assetPath, 'titan.png'))
titanImg = pygame.transform.scale(titanImg, (5, 5))
venusImg = pygame.image.load(os.path.join(assetPath, 'venus.png'))
venusImg = pygame.transform.scale(venusImg, (10, 10))


pygame.init()
pygame.display.set_caption("Solar System")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

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

def ellipseRotate(poly, degree, degreeSpeed):
    degree += degreeSpeed
    x1 = int(math.cos(degree*2*math.pi/360)*25)
    y1 = int(math.sin(degree*2*math.pi/360)*10)
    loc = [x1, y1]
    return degree, loc

class Planet():
    def __init__(self, image, Speed, distance):
        self.image = image
        rect = self.image.get_rect()
        self.location = np.array([distance, distance])
        self.degree = 0
        self.degreeSpeed = Speed
        self.moveXy = (WINDOW_WIDTH/2 - rect.width/2, WINDOW_HEIGHT/2 - rect.height/2)
        self.loc = [0, 0]
    def update(self):
        self.degree, self.loc = rotate(self.location, self.degree, self.degreeSpeed)
        self.loc[0] += self.moveXy[0]
        self.loc[1] += self.moveXy[1]
    def draw(self):
        screen.blit(self.image, self.loc)
    
class Satellite(Planet):
    def __init__(self, image, Speed, distance, planet):
        super().__init__(image, Speed, distance)
        self.planet = planet
        self.rect = self.image.get_rect()
    def update(self):
        self.degree, self.loc = rotate(self.location, self.degree, self.degreeSpeed)
        self.moveXy = self.planet.loc
        self.loc[0] += self.moveXy[0] - self.rect.width/2 + self.planet.image.get_rect().width/2
        self.loc[1] += self.moveXy[1] - self.rect.height/2 + self.planet.image.get_rect().height/2
    def draw(self):
        screen.blit(self.image, self.loc)      

class ellipseSatellite(Planet):
    def __init__(self, image, Speed, distance, planet):
        super().__init__(image, Speed, distance)
        self.planet = planet
        self.rect = self.image.get_rect()
    def update(self):
        self.degree, self.loc = ellipseRotate(self.location, self.degree, self.degreeSpeed)
        self.moveXy = self.planet.loc
        self.loc[0] += self.moveXy[0] - self.rect.width/2 + self.planet.image.get_rect().width/2
        self.loc[1] += self.moveXy[1] - self.rect.height/2 + self.planet.image.get_rect().height/2
    def draw(self):
        screen.blit(self.image, self.loc)  
             
class Sun():
    def __init__(self, image):
        self.image = image
        rect = self.image.get_rect()
        self.location = (WINDOW_WIDTH/2 - rect.width/2, WINDOW_HEIGHT/2 - rect.height/2)
    def update(self):
        pass
    def draw(self):
        screen.blit(self.image, self.location)

# construction
sun = Sun(sunImg)
earth = Planet(earthImg, 1, 100)
venus = Planet(venusImg, 3/2, 70)
saturn = Planet(saturnImg, 1/30, 250)
moon = Satellite(moonImg, 1, 5, earth)
titan = ellipseSatellite(titanImg, 1, 20, saturn)


def main():
    done = False    

    while not done: 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 

        # 게임 로직 구간
        earth.update()
        venus.update()
        saturn.update()
        moon.update()
        titan.update()
        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)

        # 화면 그리기 구간
        screen.blit(backgroundImg, backgroundImg.get_rect())
        sun.draw()
        earth.draw()
        venus.draw()
        saturn.draw()
        moon.draw()
        titan.draw()
        # 화면 업데이트 / 초당 60 프레임으로 업데이트
        pygame.display.flip()
        clock.tick(FPS)

    # 게임 종료
    pygame.quit()

if __name__ == "__main__":
    main()
    
