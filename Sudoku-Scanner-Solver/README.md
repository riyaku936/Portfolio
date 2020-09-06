# Sudoku Scanner Solver

## Quick Links

**Youtube video of project demo:** https://youtu.be/lutvnmfVn6k 

## Directory Structure
```
|-MLHELPERFNS
  |-puzzle.py --> contains the functions to find the puzzle in the image and extract the digits from the image
|-MLIMAGEPROC
  |-digit_classifier.h5 --> the ML model we query to classify an image of a digit as a digit
  |-solve_sudoku_puzzle_merged.py --> contains the function that takes in the image, and converts it to a virtual copy of a sudoku board by querying the ML model
|-MLMODEL
  |-sudokunet.py --> contains the neural net we used to traint he ML model
  |-train_digit_classifier.py --> contains the function to initiate the training process
|-SOLVERVISUALISER
  |-sudokuAlgo.py --> contains the backtracking algorithm to solve the sudoku puzzle
  |-sudokuGUI.py --> contains the pygame code to display and visualise the backtracking algorithm as it solves the sudoku code
```
## Project Information

The goal of this Python based project was to develop a system that scans a sudoku puzzle via the webcam and returns the solution to the user. The first step involves extracting the sudoku board from the captured image via Image Processing. The numbers on the sudoku board are then recognised by a Machine Learning model I trained using the MNIST dataset. The sudoku puzzle is then solved via the backtracking algorithm and the solving process is visualised using the pygame library. 

## Additonal information
<ul>
<li>For the Machine Learning and Image Processing part of the application the following tutorial was followed: https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/
<br>
<li>To train the ML algorithm I utilised the MNIST dataset
  </ul>

## Technologies used:
<ul>
  <li> Convolutional Neural Networks
    <li> MNIST dataset
    <li> Image processing
      <li> pygame
        <li> backtracking
  </ul>
