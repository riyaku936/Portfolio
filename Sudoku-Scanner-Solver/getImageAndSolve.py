from MLIMAGEPROC import solve_sudoku_puzzle_merged
from SOLVERVISUALISER import sudokuGUI

# get the puzzle scanned in from the the image:
puzzle = solve_sudoku_puzzle_merged.getGridFromImage(1, '/Users/rakshita/Desktop/CodingProjects/Sudoku-Scanner-Solver/MLIMAGEPROC/digit_classifier.h5') 


# solve and visualise the puzzle using pygame:
sudokuGUI.main(puzzle)

 