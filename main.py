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

## Representation of a Board, contains GUI Portion that is currently commented out/optional
class Board:
    ## constructor
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
            pygame.display.update()

        self.drawFull()
    
    ## drop disk of given color in given column
    def drop(self, clm, clr):
        # print(clm)
        self.board[self.open[clm]][clm] = clr
        self.open[clm] += 1
        if self.debug:
            print(f'{clr} dropped a disk in column {clm}')
        self.drawCell(clm, self.open[clm] - 1)
    
    ## redraw cell, prints entire board if GUI off
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

    ## Draws full board, GUI optional
    def drawFull(self):
        if self.window != None:
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    self.drawCell(c, r)
                    pygame.display.update()
####################################################
        elif self.debug:
            for r in range(len(self.board)):
                print(self.board[len(self.board)-1-r])
            # print(calc_heuristic(self.board, 'R'))
####################################################   
    
    ## is a valid mouseclick X coordinate
    def isValid(self, x):
        return self.open[x // 100] != self.rows
    
    ## return open columns
    def openCols(self):
        return [x for x in range(len(self.open)) if self.open[x] != self.rows]

    ## return if game is over
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

## player superclass
class Player:
    ## constructor
    def __init__(self, b, c, t=0):
        self.board = b
        self.color = c
        self.timeControl = t
        self.nextMove = random.choice(self.board.openCols())
    
    ## implemented in subclasses, calls specific function
    def moveInternal(self):
        pass

    ## time control based move function
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
        # print(self.color, self.scores)
        # print(self.terminals)
        # for b in self.boards:
        #     print(b)
        #     for i in range(len(self.boards[b])):
        #         print(self.boards[b][5 - i])
        signal.alarm(0)

## Human Player
class Human(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)
    
    ## Get user input via mouse clicks
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

## AI that picks random column
class RandomAI(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)
    def moveInternal(self):
        # ev = pygame.event.get()
        col = random.choice(self.board.openCols())
        self.nextMove = col

## Plain Minimax
class PlainMinMaxAI(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)

    def moveInternal(self):
        # ev = pygame.event.get()
        ply = 1
        while True:
            self.nextMove, _,  result, scores, terminals, boards = minimax(self.board.board, ply, self.color == 'R', printPaths=True)
            self.scores = scores
            self.terminals = terminals
            self.boards = boards
            if result != None:
                # print(f'PLY: {ply}')
                # print(f'RESULT: {result}')
                break
            ## uses iterative deepening
            ply += 1

## Uses alpha-beta pruning
class AlphaBetaAI(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)

    def moveInternal(self):
        # ev = pygame.event.get()
        ply = 1
        while True:
            self.nextMove, _,  result, scores, terminals, boards = alphabeta(self.board.board, ply, self.color == 'R', -float('inf'), float('inf'), printPaths=True)
            self.scores = scores
            self.terminals = terminals
            self.boards = boards
            if result != None:
                # print(f'PLY: {ply}')
                # print(f'RESULT: {result}')
                break
            ## uses iterative deepening
            ply += 1

## uses move ordering
class MoveOrderAI(Player):
    def __init__(self, b, c, t=0):
        super().__init__(b, c, t)

    def moveInternal(self):
        # ev = pygame.event.get()
        ply = 1
        while True:
            self.nextMove, _,  result, scores, terminals, boards = moveorder(self.board.board, ply, self.color == 'R', -float('inf'), float('inf'), printPaths=True)
            self.scores = scores
            self.terminals = terminals
            self.boards = boards
            if result != None:
                # print(f'PLY: {ply}')
                # print(f'RESULT: {result}')
                break
            ## uses iterative deepening
            ply += 1

## original attempt at GUI/human vs. CPU
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

## Simulates games not for user to view but to gather data
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

## Simulates many games between two players with given time controls
def simulateMany(p1, p2, t1, t2, N):
    result = {"P1": 0, "P2": 0, "D": 0}
    for i in range(N):
        print(f'Playing Game {i+1}')
        if i % 2 == 0:
            g = SimGame(p1, p2, t1, t2)
        else:
            g = SimGame(p2, p1, t2, t1)
        r = g.play()

        if r != 'D':
            if i % 2 == 0:
                r = 'P1' if r == 'R' else 'P2'
            else:
                r = 'P1' if r == 'Y' else 'P2'
        print(f'Result: {r}')
        result[r] += 1
    return result

## simulates one game, allows for debugging
def simulateDebug(p1, p2, t1, t2):
    g = SimGame(p1, p2, t1, t2, debug=True)
    return g.play()

### TEST CASES
# print(simulateMany(PlainMinMaxAI, PlainMinMaxAI, 1, 3, 10))
# print(simulateMany(PlainMinMaxAI, AlphaBetaAI, 1, 1, 10))
# print(simulateMany(PlainMinMaxAI, AlphaBetaAI, 1, 3, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 1, 1, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 1, 3, 10))

# print(simulateMany(PlainMinMaxAI, AlphaBetaAI, 3, 1, 10))
# print(simulateMany(PlainMinMaxAI, AlphaBetaAI, 3, 3, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 3, 1, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 3, 3, 10))

# print(simulateMany(AlphaBetaAI, AlphaBetaAI, 1, 3, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 1, 1, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 1, 3, 10))

# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 3, 1, 10))
# print(simulateMany(PlainMinMaxAI, MoveOrderAI, 3, 3, 10))

# print(simulateMany(MoveOrderAI, MoveOrderAI, 1, 3, 10))

### DEBUGGING

# board = [['Y', ' ', 'R', 'Y', 'Y', ' ', 'R'],
#          [' ', ' ', 'Y', 'R', 'R', ' ', 'R'],
#          [' ', ' ', 'Y', 'Y', 'R', ' ', 'Y'],
#          [' ', ' ', 'R', 'Y', 'R', ' ', 'R'],
#          [' ', ' ', ' ', ' ', 'Y', ' ', 'R'],
#          [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

# nextMove, _,  result, scores, terminals, boards = minimax(board, 4, False, printPaths=True)

# print(scores)
# print(terminals)
# for b in boards:
#     print(b)
#     for i in range(len(boards[b])):
#         print(boards[b][5 - i])