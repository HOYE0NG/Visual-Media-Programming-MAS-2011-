import pygame
import numpy as np
import random
# 게임 윈도우 크기
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 150)

pygame.init()
pygame.display.set_caption("TIC TAC TOE")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# game value
boardRectXy = [None,[0,200,100,100],[100,200,100,100],[200,200,100,100],[0,100,100,100],[100,100,100,100],[200,100,100,100],[0,0,100,100],[100,0,100,100],[200,0,100,100]]
board = [" "] * 10

def printMessage(letter):
    if letter == "player":
        draw_text(screen, "you win", 50, 300, 300)       
    elif letter == "computer":
        draw_text(screen, "you lose, computer win", 50, 300, 300)
    else:
        draw_text(screen, "the game is a tie!", 50, 300, 300)

def clickBoard(x, y):
    if 0<x<100 and 0<y<100:
        return 7
    elif 100<x<200 and 0<y<100:
        return 8
    elif 200<x<300 and 0<y<100:
        return 9
    elif 0<x<100 and 100<y<200:
        return 4
    elif 100<x<200 and 100<y<200:
        return 5
    elif 200<x<300 and 100<y<200:
        return 6
    elif 0<x<100 and 200<y<300:
        return 1
    elif 100<x<200 and 200<y<300:
        return 2
    elif 200<x<300 and 200<y<300:
        return 3 

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def drawBoard():
    draw_text(screen, "TIC TAC TOE", 50, 150, 300)
    for i in range(1,10):
        pygame.draw.rect(screen, BLACK, boardRectXy[i], 1)
        draw_text(screen, board[i], 100, boardRectXy[i][0]+50, boardRectXy[i][1])

def getPlayerMove(letter, num):
    if board[num] == " ":
        board[num] = letter
        return True
    return False

def boardCopy(board):
    copyBoard = []
    for i in board:
        copyBoard.append(i)
    return copyBoard

def getComputerMove(cletter):
    if cletter == 'X':
        pletter = 'O'
    else:
        pletter = 'X'
    
    #check if computer can win in the next move
    for i in range(1, 10):
        copyBoard = boardCopy(board)
        if copyBoard[i] == ' ':
            copyBoard[i] = cletter
            if isWinner(copyBoard, cletter):
                return i        
            
    # check if player can win in the next move and block them
    for i in range(1,10):
        copyBoard = boardCopy(board)
        if copyBoard[i] == ' ':
            copyBoard[i] = pletter
            if isWinner(copyBoard, pletter):
                return i
    
    # try to take one of the corners
    for i in [1,3,7,9]:
        if board[i] == ' ':
            return i
    
    if board[5] == ' ':
        return 5
    
    for i in range(1,10):
        if board[i] == ' ':
            return i
    
    return 0
        
def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or 
    (bo[4] == le and bo[5] == le and bo[6] == le) or 
    (bo[1] == le and bo[2] == le and bo[3] == le) or
    (bo[7] == le and bo[4] == le and bo[1] == le) or
    (bo[8] == le and bo[5] == le and bo[2] == le) or
    (bo[9] == le and bo[6] == le and bo[3] == le) or
    (bo[7] == le and bo[5] == le and bo[3] == le) or
    (bo[9] == le and bo[5] == le and bo[1] == le))

def isBoardFull(board):
    for i in range(1,10):
        if board[i] == " ":
            return False
    return True

# 게임 반복 구간
def main():
    done = False
    start = False
    turn = ""
    playerDone = False
    gameDone = False
    result = ""
    while not done:
        for event in pygame.event.get():           
            if event.type == pygame.QUIT:
                done = True 
            if gameDone == False:
                if event.type == pygame.KEYDOWN:
                    if not start and event.key == pygame.K_o:
                        playerLetter = 'O'
                        computerLetter = 'X'
                        # turn = whoGoesFirst()
                        turn = 'computer'
                        start = True
                    if not start and event.key == pygame.K_x:
                        playerLetter = 'X'
                        computerLetter = 'O'
                        # turn = whoGoesFirst()
                        turn = 'player'
                        start = True
                if turn == 'player' and event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    num = clickBoard(x,y)
                    if getPlayerMove(playerLetter, num):
                        playerDone = True 

        screen.fill(WHITE)
        ################
        if start and gameDone == False:
            if playerDone and turn == 'player':
                if isWinner(board, playerLetter):
                    gameDone = True
                    result = 'player'
                else:
                    if isBoardFull(board):
                        gameDone = True
                        result = 'tie'
                    else:
                        playerDone = False
                        turn = "computer"                
            elif playerDone == False and turn == 'computer':
                if getComputerMove(computerLetter) != 0:
                    board[getComputerMove(computerLetter)] = computerLetter
                    if isWinner(board, computerLetter):
                        gameDone = True
                        result = 'computer'
                    else:
                        if isBoardFull(board):
                            gameDone = True
                            result = 'tie'
                        else:
                            turn = "player"                

        # 화면 그리기 구간
        if gameDone == False:
            if not start:
                draw_text(screen,"O or X? ( Press the key )",30,400,400)
            elif start:
                drawBoard()
        elif gameDone == True and result != "":
            drawBoard()
            printMessage(result)
        # ---------
        pygame.display.flip()
        clock.tick(60) 
        print(gameDone)
    # 게임 종료
    pygame.quit()
    

if __name__ == "__main__":
    main()