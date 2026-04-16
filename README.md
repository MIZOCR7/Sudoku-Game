# Sudoku Game (Tkinter)

A desktop Sudoku game built with Python and Tkinter. It includes puzzle generation, multiple difficulty levels, hints, undo functionality, and a clean graphical interface.

## Features

- Automatically generated Sudoku puzzles
- Three difficulty levels: Easy, Medium, Hard
- Fully interactive GUI
- Hint system
- Undo functionality
- Timer to track solving time
- Option to solve the puzzle instantly
- Keyboard and mouse support

## Requirements

- Python 3.x
- Tkinter (included with most Python installations)

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/sudoku-game
cd sudoku-game
```

## Usage

Run the game:

```bash
python main.py
```

## How to Play

- Click on any empty cell to select it
- Use:
  - Number keys (1–9) or on-screen buttons to enter values
  - Backspace/Delete or "Erase" to clear a cell
- Fill the board following Sudoku rules:
  - Each row must contain numbers 1–9 without repetition
  - Each column must contain numbers 1–9 without repetition
  - Each 3×3 box must contain numbers 1–9 without repetition

## Controls

- Mouse click: Select a cell
- Keyboard:
  - `1–9`: Enter number
  - `Backspace/Delete`: Erase
  - `H`: Get a hint
  - `Ctrl + Z`: Undo last move

## Game Menu

- New Game (Easy / Medium / Hard)
- Solve Puzzle (fills the board with the solution)
- Exit

## Notes

- You cannot modify the original (pre-filled) cells
- Hints will automatically fill a correct value in an empty cell
- The game ends when the board is completely filled

## Possible Improvements

- Add mistake highlighting
- Add notes/pencil marks feature
- Improve puzzle generation speed
- Add save/load functionality
- Add sound effects or animations

## License

This project is licensed under the MIT License.
