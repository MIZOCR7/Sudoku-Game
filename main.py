import pygame

board = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],   
]

def board_setup(board):
    for row in range(len(board)):
        for column in range(len(board[0])):
            print(board[row][column], end=" ")
            
        print()
        if row % 3 == 0:
            print("_" * 18)


board_setup(board)