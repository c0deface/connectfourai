
import numpy as np
import random

ROWS = 6
COLS = 7

# players
EMPTY = ' '
PLAYER1 = 'R'
PLAYER2 = 'Y'

# crearte board,  currently not in use
def create_board():
    return np.zeros((ROWS, COLS), dtype=int)


# return if chosen column has a valid move, if top of row is blank return true
def is_valid(board, col):
    return board[ROWS-1][col] == EMPTY


# return a list of columns you can add another piece to
def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid(board, col)]


# drop a piece into the col , simulate playong a piece
def drop(board, col, player):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            board[row][col] = player
            break


# basic heuristic for moves
def initiate_heuristic(window, p):
    # i should have 4
    # opponent should not have 3
    # 
    # p = player , opp = opponent - 
    opp = PLAYER2 if p == PLAYER1 else PLAYER1

    # if we have 4 we win
    if window.count(p) == 4:
        return float('inf')
    # if oppenent has 3 lined up they win
    elif window.count(opp) == 3 and window.count(EMPTY) == 1:
        return -float('inf')
    # if we have 3 lined up 
    elif window.count(p) == 3 and window.count(EMPTY) == 1:
        return 10
    # if opponent has 2 lined up
    elif window.count(opp) == 2 and window.count(EMPTY) == 2:
        return -12
    else:
        return 0


def calc_heuristic(board, p):
    score = 0

    # Evaluate horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            #print(board)
            
            window = []
            for i in range(4):
                window.append(board[row][col+i])
                
            
            w = initiate_heuristic(window, p)
            if w == float('inf'):
                return float('inf')
            elif w == -float('inf'):
                return -float('inf')
            score += w

    # Evaluate vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = []
            for i in range(4):
                window.append(board[row+i][col])
            w = initiate_heuristic(window, p)
            if w == float('inf'):
                return float('inf')
            elif w == -float('inf'):
                return -float('inf')
            score += w

    # Evaluate diagonally (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = []
            for i in range(4):
                window.append(board[row+i][col+i])
            w = initiate_heuristic(window, p)
            if w == float('inf'):
                return float('inf')
            elif w == -float('inf'):
                return -float('inf')
            score += w

    # Evaluate diagonally (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = []
            for i in range(4):
                window.append(board[row-i][col+i])
            w = initiate_heuristic(window, p)
            if w == float('inf'):
                return float('inf')
            elif w == -float('inf'):
                return -float('inf')
            score += w

    return score

# when the game is over
def is_terminal_node(board):
    # is draw
        valid_cols = get_valid_moves(board)
        isDraw = True
        for r in valid_cols:
            if r != ROWS:
                isDraw = False
                break
        if isDraw:
            return 'D', True
        
        # check horizontal
        for c in range(COLS-3):
            for r in range(ROWS):
                if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != ' ':
                    return board[r][c], True
        # check vertical
        for c in range(COLS):
            for r in range(ROWS-3):
                if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != ' ':
                    return board[r][c], True
        # check increasing diag
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != ' ':
                    return board[r][c], True
        # check decreasing diag
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] != ' ':
                    return board[r][c], True
        return None, False

def minimax(board, depth, alpha, beta, maximizing_player, printPaths=False):
    # if it's over return as such

    # get possible moves
    valid_moves = get_valid_moves(board)
    # run minmax staring with one of the possibilities at random
    random.shuffle(valid_moves)
    # return board , true if we have reached a win OR a tie OR a full board
    is_terminal, result = is_terminal_node(board)

    scores = {}
    terminals = {}
    boards = {}

    p = PLAYER1 if maximizing_player else PLAYER2

    
    if depth == 0 or is_terminal:
        return (None, calc_heuristic(board, p), result)

    value = -float('inf')
    column = random.choice(valid_moves)
    result = None

    for col in valid_moves:
        temp_board = [[x for x in row] for row in board]
        drop(temp_board, col, p)
        _, new_score, result = minimax(temp_board, depth - 1,alpha, beta,  not maximizing_player)
        if printPaths:
            scores[col] = new_score
            terminals[col] = is_terminal_node(temp_board)
            boards[col] = temp_board
        # if result == p: # skip to the end, return
        #     pass
        if new_score >= value:
            value = new_score
            column = col
        if maximizing_player:
            alpha = max( value, alpha)
            if alpha >= beta:
                break
        else:   
            beta = min(beta, value)
            if beta<= alpha:
                break   
    return column, -value, result, scores, terminals, boards
            
