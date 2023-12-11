import pygame
from pygame.locals import *
import random
import time
import signal
from minimax import *

ROWS = 6
COLS = 7

def handleTimeout(signum, frame):
    raise TimeoutError

class Board:
    def __init__(self, w, rows, cols, debug=False):
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.open = [0 for _ in range(cols)]
        self.result = None
        self.debug = debug

        self.window = w
        if self.window != None:
            self.window.fill("blue")
            print('BLUE')
            pygame.display.update()

        self.drawFull()
    
    def drop(self, clm, clr):
        print(clm)
        self.board[self.open[clm]][clm] = clr
        self.open[clm] += 1
        if self.debug:
            print(f'{clr} dropped a disk in column {clm}')
        self.drawCell(clm, self.open[clm] - 1)
    
    def drawCell(self, c, r):
        if self.window != None:
            color = "light blue"
            if self.board[r][c] == 'R':
                color = "red"
            if self.board[r][c] == 'Y':
                color = "yellow"
            pygame.draw.circle(self.window, color, (50+(c*100), 50+((self.rows-1-r)*100)), 40, 40)
            pygame.display.update()
        else:
            self.drawFull()

    def drawFull(self):
        if self.window != None:
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    self.drawCell(c, r)
                    pygame.display.update()
        elif self.debug:
            for r in range(len(self.board)):
                print(self.board[len(self.board)-1-r])
            print(calc_heuristic(self.board, 'R'))
    
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
            self.result = 'D'
            return True
        
        # check horizontal
        for c in range(self.cols-3):
            for r in range(self.rows):
                if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] ==self.board[r][c+3] != ' ':
                    self.result = self.board[r][c]
                    return True
        # check vertical
        for c in range(self.cols):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] ==self.board[r+3][c] != ' ':
                    self.result = self.board[r][c]
                    return True
        # check increasing diag
        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] ==self.board[r+3][c+3] != ' ':
                    self.result = self.board[r][c]
                    return True
        # check decreasing diag
        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] ==self.board[r-3][c+3] != ' ':
                    self.result = self.board[r][c]
                    return True
        return False
    def getResult(self):
        return self.result

class Player:
    def __init__(self, b, c, t=0):
        self.board = b
        self.color = c
        self.timeControl = t
        self.nextMove = random.choice(self.board.openCols())
    def moveInternal(self):
        pass
    def move(self):
        self.nextMove = random.choice(self.board.openCols())
        signal.signal(signal.SIGALRM, handleTimeout)
        signal.alarm(self.timeControl)
        try:
            self.moveInternal()
        except TimeoutError:
            self.board.drop(self.nextMove, self.color)
        else:
            self.board.drop(self.nextMove, self.color)
        print(self.color, self.scores)
        print(self.terminals)
        for b in self.boards:
            print(b)
            for i in range(len(self.boards[b])):
                print(self.boards[b][5 - i])
        signal.alarm(0)

class Human(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)
    def moveInternal(self):
        moved = False
        while not moved:
            ev = pygame.event.get()
            for e in ev:
                if e.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.board.isValid(pos[0]):
                        self.nextMove = pos[0] // 100
                        moved = True
                        return

class RandomAI(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)
    def moveInternal(self):
        # ev = pygame.event.get()
        col = random.choice(self.board.openCols())
        self.nextMove = col

class PlainMinMaxAI(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)

    def moveInternal(self):
        # ev = pygame.event.get()
        ply = 1
        while True:
            self.nextMove, _, scores, result, terminals, boards = minimax(self.board.board, ply, True, printPaths=True)
            self.scores = scores
            self.terminals = terminals
            self.boards = boards
            if result != None:
                break
            ply += 1


class Game:
    def __init__(self, w, p1, p2):
        self.board = Board(w, ROWS, COLS)
        self.players = [Human(self.board, 'R') if p1 == 'H' else RandomAI(self.board, 'R'),
                        Human(self.board, 'Y') if p2 == 'H' else RandomAI(self.board, 'Y')]
    def start(self):
        c = 0
        while not self.board.isOver():
            self.players[c].move()
            c = 1 - c
        pygame.display.update()
        time.sleep(20)

class SimGame:
    def __init__(self, p1, p2, t1, t2, debug=False):
        self.board = Board(None, ROWS, COLS, debug=debug)
        self.players = [p1(self.board, 'R', t=t1), p2(self.board, 'Y', t=t2)]
    def play(self):
        c = 0
        while True:
            self.players[c].move()
            if self.board.isOver():
                return self.board.getResult()
            c = 1 - c

# pygame.display.init()
# w = pygame.display.set_mode((COLS*100, ROWS*100))
# w.fill("blue")
# pygame.display.update()

def simulateMany(p1, p2, N):
    result = {"R": 0, "Y": 0, "D": 0}
    for _ in range(N):
        # print(_)
        g = SimGame(p1, p2)
        r = g.play()
        result[r] += 1
    return result

def simulateDebug(p1, p2, t1, t2):
    g = SimGame(p1, p2, t1, t2, debug=True)
    return g.play()

# print(simulateMany(Computer, Computer, 1000))
print(simulateDebug(PlainMinMaxAI, PlainMinMaxAI, 1, 1))