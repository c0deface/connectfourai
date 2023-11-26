import pygame
from pygame.locals import *

window = None

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.open = [0 for _ in range(cols)]

        window.fill("blue")
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
        pygame.draw.circle(window, color, (50+(c*100), 50+((self.rows-1-r)*100)), 40, 40)
        pygame.display.update()

    def drawFull(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                self.drawCell(c, r)
                pygame.display.update()
    
    def isValid(self, x):
        return self.open[x // 100] != self.rows

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


pygame.display.init()
window = pygame.display.set_mode((7*100, 6*100))
b = Board(6, 7)

pygame.display.update()
colors = ['R', 'Y']
c = 0
while not b.isOver():
    ev = pygame.event.get()
    for e in ev:
        if e.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if b.isValid(pos[0]):
                print("valid")
                b.drop(pos[0] // 100, colors[c])
                c = 1 - c

print("IT OVER")
