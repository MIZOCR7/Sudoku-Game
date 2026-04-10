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
    
    def _find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i,j)
                
        return None
    
    def _is_valid(self,board, num, pos):
        row, col = pos
        for j in range(9):
            if board[row][j] == num and j != col:
                return False
            
        for i in range(9):
            if board[i][col] == num and i != row:
                return False
            
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num and (i,j) != pos:
                    return False
                
        return True
    
    def _remove_cells(self, count):
        removed = 0
        attempts = 0

        while removed < count and attempts < count * 3:
            row = random.randint(0,8)
            col = random.randint(0,8)

            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0

                temp = copy.deepcopy(self.board)
                if self._count_solutions(temp) == 1:
                    removed +=1
                else:
                    self.board[row][col] = backup
            attemps += 1


    def _count_solutions(self, board, limit=2):
        count = [0]
        self._count_helper(board, count, limit)
        return count [0]
    
    def _count_helper(self, board, count ,limit):
        if count[0] > limit:
            return
    
        empty = self._find_empty(board)
        if not empty:
            count[0] += 1
            return
        
        row, col = empty
        for num in range(1,10):
            if self.is_valid(board, num, (row,col)):
                board[row][col] = num
                self._count_helper(board, count,limit)
                board[row][col] = 0


        def is_valid_move(self, row, col, num):
            if self.original[row][col]!= 0:
                return False

            backup = self.board[row][col]
            self.board[row][col] = 0
            valid = self._is_valid(self.board,num, (row,col))
            self.board[row][col] = backup

            return valid
        
        def make_move(self, row, col, num):
            if self.original[row][col] == 0:
                self.board[row][col] = num
            return True
            
        def is_complete(self):
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        return False
            return True
        
        def get_hint(self):
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        return(i,j,self.solution[i][j])
                    
            return None
        
        