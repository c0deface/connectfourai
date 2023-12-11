
import numpy as np
import random

ROWS = 6
COLS = 7

# players
EMPTY = ' '
PLAYER1 = 'R'
PLAYER2 = 'Y'


def create_board():
    return np.zeros((ROWS, COLS), dtype=int)


# return if chosen column has a valid move
def is_valid(board, col):
    return board[ROWS-1][col] == EMPTY


# drop a piece into the col
def drop(board, col, player):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            board[row][col] = player
            break
        
        
# print the board, current;y in terminal 
def print_board(board):
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]}", end=" |")
        print()
    print("-" * (COLS * 4 + 1))
    
    
    
# basic heuristic for moves
def initiate_heuristic(window, p):
    # i should have 4
    # opponent should not have 3
    # 
    opp = PLAYER2 if p == PLAYER1 else PLAYER1

    if window.count(p) == 4:
        return float('inf')
    elif window.count(opp) == 3 and window.count(EMPTY) == 1:
        return -float('inf')
    elif window.count(p) == 3 and window.count(EMPTY) == 1:
        return 10
    elif window.count(opp) == 2 and window.count(EMPTY) == 2:
        return -10
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
            return True
        
        # check horizontal
        for c in range(COLS-3):
            for r in range(ROWS):
                if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != ' ':
                    return True
        # check vertical
        for c in range(COLS):
            for r in range(ROWS-3):
                if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != ' ':
                    return True
        # check increasing diag
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != ' ':
                    return True
        # check decreasing diag
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] != ' ':
                    return True
        return False


#MINIMAX IMPLEMENTATION with depth
def minimax(board, depth, maximizing_player, printPaths=False):
    # if it's over return as such
    valid_moves = get_valid_moves(board)
    random.shuffle(valid_moves)
    is_terminal = is_terminal_node(board)
    scores = {}
    terminals = {}
    boards = {}

    p = PLAYER1 if maximizing_player else PLAYER2
    if depth == 0 or is_terminal:
        return (None, calc_heuristic(board, p))

    value = -float('inf')
    column = random.choice(valid_moves)
    for col in valid_moves:
        temp_board = [[x for x in row] for row in board]
        drop(temp_board, col, p)
        new_score = minimax(temp_board, depth - 1, not maximizing_player)[1]
        if printPaths:
            scores[col] = new_score
            terminals[col] = is_terminal_node(temp_board)
            boards[col] = temp_board
        if new_score >= value:
            value = new_score
            column = col
    return column, -value, scores, terminals, boards

def winning_move(board, player):
    # Check for a win in all directions

    # Check horizontally
    for col in range(COLS - 3):
        for row in range(ROWS):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return True

    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True

    # Check diagonally (positive slope)
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check diagonally (negative slope)
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid(board, col)]




#########################################################
# PLAY THE GAME

def play_connect_four():
    board = create_board()
    game_over = False
    turn = 0  # 0 for PLAYER1, 1 for PLAYER2

    while not game_over:
        print_board(board)

        if turn == 0:
            # Player 1 (Human) move
            while True:
                try:
                    col = int(input("Player 1 (X), choose a column (0-6): "))
                    if is_valid(board, col):
                        drop(board, col, PLAYER1)
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        else:
            # Player 2 (AI) move using minimax
            
            
            # DEPTH OF MINIMAX CAN BE CAHNGES HERE
            col, _ = minimax(board, 3, True)  
            
            ##################################
            
            drop(board, col, PLAYER2)
            print(f"Player 2 (O) chooses column {col}")

        if winning_move(board, PLAYER1):
            print_board(board)
            print("Player 1 (X) wins!")
            game_over = True
        elif winning_move(board, PLAYER2):
            print_board(board)
            print("Player 2 (O) wins!")
            game_over = True
        elif len(get_valid_moves(board)) == 0:
            print_board(board)
            print("It's a draw!")
            game_over = True

        turn = (turn + 1) % 2

if __name__ == "__main__":
    play_connect_four()

