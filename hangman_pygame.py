import pygame
import random
import os

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

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("H A N G M A N")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False    # 게임이 진행중인지 확인하는 변수
# done이 True라면 게임이 계속 진행중이라는 의미 -> False 일 때 infi-loop

# ------------------------------------------------------
currentPath = os.path.dirname(__file__)
assetsPath = os.path.join(currentPath, 'assets')
HANGMAN_PICS = []
for i in range(1,8):
    picName = "hangman"
    picName += str(i)
    picName += ".png"
    HANGMAN_PICS.append(pygame.image.load(os.path.join(assetsPath, picName)))
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
font = pygame.font.SysFont("avenirnextcondensed", 30)
# ------------------------------------------------------
def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]
# ------------------------------------------------------
missedLetters = ''
correctLetters = ''
secretWord = getRandomWord(words)
blanks = '_' * len(secretWord)
blanks = " ".join(blanks)
enter = ""
enterWord = ""
print(secretWord)
gameIsDone = False
# ------------------------------------------------------

# 게임 반복 구간
while not done: # 게임이 진행되는 동안 계속 반복 작업을 하는 while 루프
    # 이벤트 반복 구간
    for event in pygame.event.get():
        # 어떤 이벤트가 발생했는지 확인
        if event.type == pygame.QUIT:
            # QUIT는 윈도우 창을 닫을 때 발생하는 이벤트
            # 창이 닫히는 이벤트가 발생했다면
            done = True # 반복을 중단시켜 게임 종료
        elif event.type == pygame.KEYDOWN and gameIsDone:
            if len(enter) == 0:
                if event.key == pygame.K_y:
                    enter += "y"
                elif event.key == pygame.K_n:
                    enter += "n"
            else:
                if event.key == pygame.K_RETURN:
                    if enter == "y":
                        missedLetters = ''
                        correctLetters = ''
                        secretWord = getRandomWord(words)
                        blanks = '_' * len(secretWord)
                        blanks = " ".join(blanks)
                        enter = ""
                        enterWord = ""
                        print(secretWord)
                        gameIsDone = False
                    else:
                        done = True
        elif event.type == pygame.KEYDOWN and not gameIsDone:
            if len(enter) == 0 :
                if event.key == pygame.K_a:
                    enter += "a"
                elif event.key == pygame.K_b:
                    enter += "b"
                elif event.key == pygame.K_c:
                    enter += "c" 
                elif event.key == pygame.K_d:
                    enter += "d" 
                elif event.key == pygame.K_e:
                    enter += "e" 
                elif event.key == pygame.K_f:
                    enter += "f" 
                elif event.key == pygame.K_g:
                    enter += "g" 
                elif event.key == pygame.K_h:
                    enter += "h" 
                elif event.key == pygame.K_i:
                    enter += "i" 
                elif event.key == pygame.K_j:
                    enter += "j" 
                elif event.key == pygame.K_k:
                    enter += "k" 
                elif event.key == pygame.K_l:
                    enter += "l" 
                elif event.key == pygame.K_m:
                    enter += "m" 
                elif event.key == pygame.K_n:
                    enter += "n" 
                elif event.key == pygame.K_o:
                    enter += "o" 
                elif event.key == pygame.K_p:
                    enter += "p" 
                elif event.key == pygame.K_q:
                    enter += "q" 
                elif event.key == pygame.K_r:
                    enter += "r" 
                elif event.key == pygame.K_s:
                    enter += "s" 
                elif event.key == pygame.K_t:
                    enter += "t" 
                elif event.key == pygame.K_u:
                    enter += "u" 
                elif event.key == pygame.K_v:
                    enter += "v" 
                elif event.key == pygame.K_w:
                    enter += "w" 
                elif event.key == pygame.K_x:
                    enter += "x" 
                elif event.key == pygame.K_y:
                    enter += "y" 
                elif event.key == pygame.K_z:
                    enter += "z"
            else:
                if event.key == pygame.K_RETURN:
                    if enter in correctLetters or enter in missedLetters:
                        enter = ""
                    else :
                        enterWord += enter
                        enter = ""
                        
    foundAllLetters = True
    for letter in secretWord:
        if letter not in correctLetters:
            foundAllLetters = False
            break
            
    if enterWord in secretWord:
         correctLetters += enterWord
    else:
        missedLetters += enterWord
    enterWord = ""
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:2*i] + secretWord[i] + blanks[2*i+1:]

    screen.fill(WHITE)
    screen.blit(font.render("H A N G M A N", True, BLACK), (100, 20))
    screen.blit(HANGMAN_PICS[len(missedLetters)],(100,50))
    screen.blit(font.render(f"Missed letters:{missedLetters}", True, BLACK), (100, 400))
    screen.blit(font.render(blanks, True, BLACK),(100, 500))
    screen.blit(font.render("Guess a letter : " + enter, True, BLACK), (100, 550))
    
    if len(missedLetters) == len(HANGMAN_PICS)-1:
        screen.blit(font.render('You have run out of guesses!'\
            , True, BLACK),(100,100))
        screen.blit(font.render('After ' + str(len(missedLetters)) + ' missed guesses and ', True, BLACK), (100, 150))
        screen.blit(font.render('After ' + str(len(correctLetters))\
            + ' correct guesses,the word was ' + secretWord, \
                True, BLACK), (100, 200))
        gameIsDone = True
    if foundAllLetters:
        screen.blit(font.render("Yes! The secret word is ", True, BLACK),(100, 450))
        gameIsDone = True
    if gameIsDone:
        screen.blit(font.render("do you want to play again? (y or n)", True, BLACK),(150, 250))
    
    # 화면 업데이트
    pygame.display.flip()
    # 초당 60 프레임으로 업데이트
    clock.tick(60) #frames per second
    
# 게임 종료
pygame.quit()