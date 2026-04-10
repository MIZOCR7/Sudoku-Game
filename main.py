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
        self._fill_board()
        self.solution = copy.deepcopy(self.board)
        cells_to_remove = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }.get(difficulty, 45)
        self._remove_cells(cells_to_remove)
        self.original = copy.deepcopy(self.board)
        
    
    def _fill_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self._solve(self.board)

    
    def _solve(self, board):
        empty = self._find_empty(board)
        if not empty:
            return True
        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self._is_valid(board, num, (row, col)):
                board[row][col] = num
                if self._solve(board):
                    return True
                board[row][col] = 0
        return False
    
    def _find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def _is_valid(self, board, num, pos):
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
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True
    
    
    def _remove_cells(self, count):
        removed = 0
        attempts = 0
        while removed < count and attempts < count * 3:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0
                temp = copy.deepcopy(self.board)
                if self._count_solutions(temp) == 1:
                    removed += 1
                else:
                    self.board[row][col] = backup
            attempts += 1
    
    def _count_solutions(self, board, limit=2):
        count = [0]
        self._count_helper(board, count, limit)
        return count[0]
    
    def _count_helper(self, board, count, limit):
        if count[0] >= limit:
            return
        empty = self._find_empty(board)
        if not empty:
            count[0] += 1
            return
        row, col = empty
        for num in range(1, 10):
            if self._is_valid(board, num, (row, col)):
                board[row][col] = num
                self._count_helper(board, count, limit)
                board[row][col] = 0
    




    def is_valid_move(self, row, col, num):
        if self.original[row][col] != 0:
            return False
        backup = self.board[row][col]
        self.board[row][col] = 0
        valid = self._is_valid(self.board, num, (row, col))
        self.board[row][col] = backup
        return valid
    



    def make_move(self, row, col, num):
        if self.original[row][col] == 0:
            self.board[row][col] = num
            return True
        return False
    



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
                    return (i, j, self.solution[i][j])
        return None


class SudokuGUI:
    
    COLORS = {
        "bg": "#2c3e50",
        "cell_bg": "#34495e",
        "cell_fixed": "#1abc9c",
        "cell_user": "#3498db",
        "cell_selected": "#e74c3c",
        "cell_highlight": "#9b59b6",
        "text": "#ecf0f1",
        "button": "#2980b9",
        "button_hover": "#3498db"
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Sudoku")
        self.root.configure(bg=self.COLORS["bg"])
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.game = SudokuGame()
        self.selected_cell = None
        self.history = []
        self._create_menu()
        self._create_info_panel()
        self._create_board()
        self._create_controls()
        self.new_game("medium")
        self.root.bind("<Key>", self._on_key_press)
    
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game (Easy)", command=lambda: self.new_game("easy"))
        game_menu.add_command(label="New Game (Medium)", command=lambda: self.new_game("medium"))
        game_menu.add_command(label="New Game (Hard)", command=lambda: self.new_game("hard"))
        game_menu.add_separator()
        game_menu.add_command(label="Solve Puzzle", command=self.solve_puzzle)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
    
    def _create_info_panel(self):
        info_frame = tk.Frame(self.root, bg=self.COLORS["bg"])
        info_frame.pack(pady=10)
        self.diff_label = tk.Label(
            info_frame, text="Medium",
            font=("Arial", 16, "bold"),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text"]
        )
        self.diff_label.pack(side=tk.LEFT, padx=20)
        self.timer_label = tk.Label(
            info_frame, text="Time: 00:00",
            font=("Arial", 16),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text"]
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)
        self.hints_label = tk.Label(
            info_frame, text="Hints: 0",
            font=("Arial", 16),
            bg=self.COLORS["bg"],
            fg=self.COLORS["text"]
        )
        self.hints_label.pack(side=tk.LEFT, padx=20)
        self.elapsed_time = 0
        self.timer_running = False
    
    def _create_board(self):
        board_frame = tk.Frame(
            self.root,
            bg=self.COLORS["bg"],
            bd=3,
            relief=tk.RIDGE
        )
        board_frame.pack(pady=10)
        self.cells = []
        for box_row in range(3):
            row_cells = []
            for box_col in range(3):
                box_frame = tk.Frame(
                    board_frame,
                    bg=self.COLORS["bg"],
                    bd=2,
                    relief=tk.RIDGE
                )
                box_frame.grid(row=box_row, column=box_col, padx=1, pady=1)
                for i in range(3):
                    for j in range(3):
                        row = box_row * 3 + i
                        col = box_col * 3 + j
                        cell = tk.Label(
                            box_frame,
                            text="",
                            font=("Arial", 20, "bold"),
                            width=2,
                            height=1,
                            bg=self.COLORS["cell_bg"],
                            fg=self.COLORS["text"],
                            relief=tk.RAISED,
                            bd=2
                        )
                        cell.grid(row=i, column=j, padx=1, pady=1)
                        cell.bind("<Button-1>", lambda e, r=row, c=col: self._on_cell_click(r, c))
                        row_cells.append((cell, row, col))
            self.cells.extend(row_cells)
        temp_cells = self.cells
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for cell, row, col in temp_cells:
            self.cells[row][col] = cell
    
    def _create_controls(self):
        controls_frame = tk.Frame(self.root, bg=self.COLORS["bg"])
        controls_frame.pack(pady=10)
        num_frame = tk.Frame(controls_frame, bg=self.COLORS["bg"])
        num_frame.pack()
        for i in range(1, 10):
            btn = tk.Button(
                num_frame,
                text=str(i),
                font=("Arial", 14, "bold"),
                width=3,
                bg=self.COLORS["button"],
                fg=self.COLORS["text"],
                activebackground=self.COLORS["button_hover"],
                command=lambda n=i: self._enter_number(n)
            )
            btn.pack(side=tk.LEFT, padx=2)
        action_frame = tk.Frame(controls_frame, bg=self.COLORS["bg"])
        action_frame.pack(pady=10)
        tk.Button(
            action_frame,
            text="Erase",
            font=("Arial", 12),
            width=8,
            bg="#e74c3c",
            fg=self.COLORS["text"],
            command=lambda: self._enter_number(0)
        ).pack(side=tk.LEFT, padx=5)


        tk.Button(
            action_frame,
            text="Undo",
            font=("Arial", 12),
            width=8,
            bg=self.COLORS["button"],
            fg=self.COLORS["text"],
            command=self.undo
        ).pack(side=tk.LEFT, padx=5)



        tk.Button(
            action_frame,
            text="Hint",

            font=("Arial", 12),
            width=8,
            bg="#f39c12",
            fg=self.COLORS["text"],
            command=self.get_hint
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            action_frame,
            text="New Game",
            font=("Arial", 12, "bold"),
            width=10,
            bg="#27ae60",

            fg=self.COLORS["text"],
            command=lambda: self.new_game("medium")
        ).pack(side=tk.LEFT, padx=5)
    




    def new_game(self, difficulty):
        self.game.generate_puzzle(difficulty)
        self.selected_cell = None
        self.history = []
        self.hints_used = 0
        self.elapsed_time = 0
        self.timer_running = True
        self._update_timer()
        self.diff_label.config(text=difficulty.capitalize())
        self.hints_label.config(text="Hints: 0")
        self._update_board()
    


    def _update_board(self):
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                value = self.game.board[row][col]
                is_original = self.game.original[row][col] != 0
                if value == 0:
                    cell.config(text="", bg=self.COLORS["cell_bg"])
                else:
                    cell.config(text=str(value))
                    if is_original:
                        cell.config(bg=self.COLORS["cell_fixed"])
                    else:
                        cell.config(bg=self.COLORS["cell_user"])
    



    def _on_cell_click(self, row, col):
        if self.selected_cell:
            prev_row, prev_col = self.selected_cell

            if self.game.original[prev_row][prev_col] == 0:
                self.cells[prev_row][prev_col].config(bg=self.COLORS["cell_bg"])
            elif self.game.board[prev_row][prev_col] != 0:
                self.cells[prev_row][prev_col].config(bg=self.COLORS["cell_fixed"])

        self.selected_cell = (row, col)

        self.cells[row][col].config(bg=self.COLORS["cell_selected"])
    
    def _on_key_press(self, event):
        key = event.char

        if key in "123456789":
            self._enter_number(int(key))
        elif key in "\x00\x08":
            self._enter_number(0)
        elif key == "h":
            self.get_hint()
        elif key == "z" and event.state & 0x4:
            self.undo()
    
    def _enter_number(self, num):
        if not self.selected_cell:
            return
        

        row, col = self.selected_cell
        if self.game.original[row][col] != 0:
            return
        old_value = self.game.board[row][col]
        self.history.append((row, col, old_value))
        if num == 0:
            self.game.board[row][col] = 0
        else:
            self.game.board[row][col] = num
        self._update_board()
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].config(bg=self.COLORS["cell_selected"])
        if self.game.is_complete():

            self.timer_running = False
            messagebox.showinfo(
                "Congratulations!",
                f"You solved the puzzle in {self.timer_label.cget('text')[6:]}!"
            )
    
    def undo(self):

        if not self.history:
            return
        row, col, old_value = self.history.pop()
        self.game.board[row][col] = old_value
        self._update_board()
    
    def get_hint(self):
        hint = self.game.get_hint()
        if hint:

            row, col, value = hint
            old_value = self.game.board[row][col]
            self.history.append((row, col, old_value))
            self.game.board[row][col] = value
            self._update_board()

            self.hints_used += 1
            self.hints_label.config(text=f"Hints: {self.hints_used}")
            self._on_cell_click(row, col)
            if self.game.is_complete():
                self.timer_running = False
                messagebox.showinfo(
                    "Congratulations!",
                    f"You solved the puzzle in {self.timer_label.cget('text')[6:]}!"
                )
    

    def solve_puzzle(self):
        if messagebox.askyesno("Solve", "This will solve the puzzle. Continue?"):
            self.game.board = copy.deepcopy(self.game.solution)
            self._update_board()
            self.timer_running = False
            
    
    def _update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self._update_timer)


def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()