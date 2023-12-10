# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:08:36 2023

@author: Koji
"""

import numpy as np

ROWS = 6
COLS = 7

# players
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2


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
def initiate_heuristic(window, player):
    score = 0
    opponent = PLAYER1 if player == PLAYER2 else PLAYER2
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 5
    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 10
    return score


def calc_heuristic(board, player):
    score = 0

    # Evaluate horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = list(board[row, col:col+4])
            score += initiate_heuristic(window, player)

    # Evaluate vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = list(board[row:row+4, col])
            score += initiate_heuristic(window, player)

    # Evaluate diagonally (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = list(board[row:row+4, col:col+4].diagonal())
            score += initiate_heuristic(window, player)

    # Evaluate diagonally (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = list(board[row-3:row+1, col:col+4][::-1].diagonal())
            score += initiate_heuristic(window, player)

    return score

# when the game is over
def is_terminal_node(board):
    return winning_move(board, PLAYER1) or winning_move(board, PLAYER2) or len(get_valid_moves(board)) == 0


#MINIMAX IMPLEMENTATION with depth
def minimax(board, depth, maximizing_player):
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER2):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER1):
                return (None, -100000000000000)
            else:  # Game is a draw
                return (None, 0)
        else:  # Depth is zero
            return (None, calc_heuristic(board, PLAYER2))

    if maximizing_player:
        value = -np.inf
        column = np.random.choice(valid_moves)
        for col in valid_moves:
            temp_board = board.copy()
            drop(temp_board, col, PLAYER2)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = np.inf
        column = np.random.choice(valid_moves)
        for col in valid_moves:
            temp_board = board.copy()
            drop(temp_board, col, PLAYER1)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

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
