import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import copy

class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.original = [[0 for _ in range(9)] for _ in range(9)]

    def generate_puzzle(self, difficulty="medium"):
        self.__fill__board()
        self.solution = copy.deepcopy(self.board)


        cells_to_remove = {
            'easy':35,
            'medium':45,
            'hard':55,
        }.get(difficulty, 45)

        self.remove_cells(cells_to_remove)

        self.original = copy.deepcopy(self.board)

    def fill_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(self.board)

    def _solve(self, board):
        empty = self._find_empty(board)
        if not empty:
            return True
        
        row, col = empty
        numbers = list(range(1,10))
        random.shuffle(numbers)

        for num in numbers:
            if self._is_valid(board, num, (row, col)):
                board[row][col] = num
                if self._sovle(board):
                    return True
                board[row][col] = 0
        
        return False
    
    

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

for row in range(len(board)):
    if row % 3 == 0:
        print("-" * 25)

    for column in range(len(board[0])):
        if column % 3 == 0:
            print("|", end=" ")

        print(board[row][column], end=" ")

    print("|")  

print("-" * 25)


def find_position(board):
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 0:
                position = (row,column)
                return position
    return None

def valid(board, number, pos):
    row, col = pos
    for i in range(9):
        if board[row][i] == number and col != i:
            return False
    for j in range(9):
        if board[j][col] == number and row != j:
            return False
        
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i, j) != pos:
                return False

    return True
