
import numpy as np
import random
import operator

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

# return a list of columns that are not full/ that yoyu can still place a piece in
def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid(board, col)]


# drop a piece into the col , simulate playong a piece
def drop(board, col, player):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            board[row][col] = player
            break
    
# basic heuristic for moves
def isLoss(window, positions, board, p):
    opp = PLAYER2 if p == PLAYER1 else PLAYER1
    return window.count(opp) == 4

def isWin(window, positions, board, p):
    if window.count(p) == 3 and window.count(EMPTY) == 1:
        blank = window.index(EMPTY)
        return positions[blank][0] == 0 or board[positions[blank][0]-1][positions[blank][1]] != EMPTY
    return False

def initiate_heuristic(window, p):
    # i should have 3
    # opponent should not have 3
    # 
    # p = player , opp = opponent - 
    opp = PLAYER2 if p == PLAYER1 else PLAYER1

    # if we have 3 lined up 
    if window.count(p) == 2 and window.count(EMPTY) == 2:
        return 10
    # if opponent has 2 lined up, denying opponent is a bit more important than your own 2pcs at this stage
    elif window.count(opp) == 3 and window.count(EMPTY) == 1:
        return -10
    # # if we have 2 lined up
    # elif window.count(p) ==2 and window.count(EMPTY) == 1:
    #     return 2
    else:
        return 0

def checkWL(board, p, func):
    for row in range(ROWS):
        for col in range(COLS - 3):
            #print(board)
            
            window = []
            positions = []
            for i in range(4):
                window.append(board[row][col+i])
                positions.append((row, col+i))
            
            if func(window, positions, board, p):
                # print(window)
                # print(positions)
                return True
            
    # Evaluate vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = []
            positions = []
            for i in range(4):
                window.append(board[row+i][col])
                positions.append((row+i, col))
            if func(window, positions, board, p):
                return True

    # Evaluate diagonally (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = []
            positions = []
            for i in range(4):
                window.append(board[row+i][col+i])
                positions.append((row+i, col+i))
            if func(window, positions, board, p):
                return True

    # Evaluate diagonally (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = []
            positions = []
            for i in range(4):
                window.append(board[row-i][col+i])
                positions.append((row-i, col+i))
            if func(window, positions, board, p):
                return True
    return False

def calc_neutral(board, p):
    score = 0

    # Evaluate horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            #print(board)
            
            window = []
            positions = []
            for i in range(4):
                window.append(board[row][col+i])
                positions.append((row, col+1))
            
            w = initiate_heuristic(window, p)
            score += w

    # Evaluate vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = []
            positions = []
            for i in range(4):
                window.append(board[row+i][col])
                positions.append((row+i, col))
            w = initiate_heuristic(window, p)
            score += w

    # Evaluate diagonally (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = []
            positions = []
            for i in range(4):
                window.append(board[row+i][col+i])
                positions.append((row+i, col+i))
            w = initiate_heuristic(window, p)
            score += w

    # Evaluate diagonally (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = []
            positions = []
            for i in range(4):
                window.append(board[row-i][col+i])
                positions.append((row-i, col+i))
            w = initiate_heuristic(window, p)
            score += w

    return score

def calc_heuristic(board, p):
    if checkWL(board, p, isLoss):
        return -float('inf')
    if checkWL(board, p, isWin):
        return float('inf')
    return calc_neutral(board, p)

# when the game is over
def is_terminal_node(board):
    # is draw
        valid_cols = get_valid_moves(board)
        isDraw = len(valid_cols) == 0

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


#MINIMAX IMPLEMENTATIONS, each are mostly identical with minor changes
def minimax(board, depth, maximizing_player, printPaths=False):
    # if it's over return as such

    # get possible moves
    valid_moves = get_valid_moves(board)
    # run minmax staring with one of the possibilities at random
    random.shuffle(valid_moves)
    # return board , true if we have reached a win OR a tie OR a full board
    result, is_terminal = is_terminal_node(board)

    scores = {}
    terminals = {}
    boards = {}

    p = PLAYER1 if maximizing_player else PLAYER2
    opp = PLAYER2 if p == PLAYER1 else PLAYER1

    if depth == 0 or is_terminal:
        # for i in range(len(board)):
        #     print(board[5 - i])
        # print(calc_heuristic(board, p))
        return (None, -calc_heuristic(board, p), result, None, None, None)

    value = -float('inf')
    column = random.choice(valid_moves)
    result = None

    for col in valid_moves:
        temp_board = [[x for x in row] for row in board]
        drop(temp_board, col, p)

        _, new_score, r, a, b, c = minimax(temp_board, depth - 1, not maximizing_player)

        if printPaths:
            scores[col] = new_score
            terminals[col] = is_terminal_node(temp_board)
            boards[col] = temp_board
        if new_score >= value:
            value = new_score
            column = col
            result = r
        # if result == p: # skip to the end, return
        #     break
    return column, -value, result, scores, terminals, boards

def alphabeta(board, depth, maximizing_player, alpha, beta, printPaths=False):
    # if it's over return as such

    # get possible moves
    valid_moves = get_valid_moves(board)
    # run minmax staring with one of the possibilities at random
    random.shuffle(valid_moves)
    # return board , true if we have reached a win OR a tie OR a full board
    result, is_terminal = is_terminal_node(board)

    scores = {}
    terminals = {}
    boards = {}

    p = PLAYER1 if maximizing_player else PLAYER2
    opp = PLAYER2 if p == PLAYER1 else PLAYER1

    if depth == 0 or is_terminal:
        # for i in range(len(board)):
        #     print(board[5 - i])
        # print(calc_heuristic(board, p))
        return (None, -calc_heuristic(board, p), result, None, None, None)

    valSet = False
    value = -float('inf')
    column = random.choice(valid_moves)
    result = None

    for col in valid_moves:
        temp_board = [[x for x in row] for row in board]
        drop(temp_board, col, p)
        ## ALPHA BETA SPECIFIC
        _, new_score, r, a, b, c = alphabeta(temp_board, depth - 1, not maximizing_player, -beta, -alpha)

        if printPaths:
            scores[col] = new_score
            terminals[col] = is_terminal_node(temp_board)
            boards[col] = temp_board
        if new_score > value or not valSet:
            value = new_score
            column = col
            result = r
            valSet = True
        if value > alpha:
            alpha = value
        if alpha >= beta:
            break
        # if result == p: # skip to the end, return
        #     break
    return column, -value, result, scores, terminals, boards

def moveorder(board, depth, maximizing_player, alpha, beta, printPaths=False):
    # if it's over return as such

    # get possible moves
    valid_moves = get_valid_moves(board)
    # Sort moves for move ordering

    # return board , true if we have reached a win OR a tie OR a full board
    result, is_terminal = is_terminal_node(board)

    scores = {}
    terminals = {}
    boards = {}

    p = PLAYER1 if maximizing_player else PLAYER2
    opp = PLAYER2 if p == PLAYER1 else PLAYER1

    ## MOVE ORDERING SPECIFIC
    approx = []
    for col in valid_moves:
        temp_board = [[x for x in row] for row in board]
        drop(temp_board, col, p)
        approx.append((col, calc_heuristic(temp_board, opp)))
        approx.sort(key=operator.itemgetter(1))
    valid_moves = [x[0] for x in approx]

    if depth == 0 or is_terminal:
        # for i in range(len(board)):
        #     print(board[5 - i])
        # print(calc_heuristic(board, p))
        return (None, -calc_heuristic(board, p), result, None, None, None)

    valSet = False
    value = -float('inf')
    column = random.choice(valid_moves)
    result = None

    for col in valid_moves:
        temp_board = [[x for x in row] for row in board]
        drop(temp_board, col, p)

        _, new_score, r, a, b, c = moveorder(temp_board, depth - 1, not maximizing_player, -beta, -alpha)

        if printPaths:
            scores[col] = new_score
            terminals[col] = is_terminal_node(temp_board)
            boards[col] = temp_board
        if new_score > value or not valSet:
            value = new_score
            column = col
            result = r
            valSet = True
        if value > alpha:
            alpha = value
        if alpha >= beta:
            break
        # if result == p: # skip to the end, return
        #     break
    return column, -value, result, scores, terminals, boards

