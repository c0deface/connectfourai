import pygame
from pygame.locals import *
import random
import time

ROWS = 6
COLS = 7

class Board:
    def __init__(self, w, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.open = [0 for _ in range(cols)]

        self.window = w
        self.window.fill("blue")
        print('BLUE')
        pygame.display.update()

        self.drawFull()
    
    def drop(self, clm, clr):
        self.board[self.open[clm]][clm] = clr
        self.open[clm] += 1
        self.drawCell(clm, self.open[clm] - 1)
    
    def drawCell(self, c, r):
        color = "light blue"
        if self.board[r][c] == 'R':
            color = "red"
        if self.board[r][c] == 'Y':
            color = "yellow"
        pygame.draw.circle(self.window, color, (50+(c*100), 50+((self.rows-1-r)*100)), 40, 40)
        pygame.display.update()

    def drawFull(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                self.drawCell(c, r)
                pygame.display.update()
    
    def isValid(self, x):
        return self.open[x // 100] != self.rows
    
    def openCols(self):
        return [x for x in range(len(self.open)) if self.open[x] != self.rows]

    def isOver(self):
        # is draw
        isDraw = True
        for r in self.open:
            if r != self.rows:
                isDraw = False
                break
        if isDraw:
            return True
        
        # check horizontal
        for c in range(self.cols-3):
            for r in range(self.rows):
                if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] ==self.board[r][c+3] != ' ':
                    return True
        # check vertical
        for c in range(self.cols):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] ==self.board[r+3][c] != ' ':
                    return True
        # check increasing diag
        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] ==self.board[r+3][c+3] != ' ':
                    return True
        # check decreasing diag
        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] ==self.board[r-3][c+3] != ' ':
                    return True
        return False

class Player:
    def __init__(self, b, c):
        self.board = b
        self.color = c
    def move(self):
        pass

class Human(Player):
    def __init__(self, b, c):
        super().__init__(b, c)
    def move(self):
        moved = False
        while not moved:
            ev = pygame.event.get()
            for e in ev:
                if e.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.board.isValid(pos[0]):
                        self.board.drop(pos[0] // 100, self.color)
                        moved = True
                        return

class Computer(Player):
    def __init__(self, b, c):
        super().__init__(b, c)
    def move(self):
        ev = pygame.event.get()
        time.sleep(0.5)
        col = random.choice(self.board.openCols())
        self.board.drop(col, self.color)
        print('COMPUTER')

class Game:
    def __init__(self, w, p1, p2):
        self.board = Board(w, ROWS, COLS)
        self.players = [Human(self.board, 'R') if p1 == 'H' else Computer(self.board, 'R'),
                        Human(self.board, 'Y') if p2 == 'H' else Computer(self.board, 'Y')]
    def start(self):
        c = 0
        while not self.board.isOver():
            self.players[c].move()
            c = 1 - c
        pygame.display.update()
        time.sleep(20)

pygame.display.init()
w = pygame.display.set_mode((COLS*100, ROWS*100))
w.fill("blue")
pygame.display.update()
g = Game(w, 'H', 'C')
g.start()
print("IT OVER")
