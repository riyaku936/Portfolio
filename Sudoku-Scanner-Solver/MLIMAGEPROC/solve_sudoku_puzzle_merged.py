import argparse
from tensorflow.keras.models import load_model
import cv2
import imutils
from MLHELPERFNS import puzzle as puzzleFns
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from sudoku import Sudoku
import cv2 
import os

def captureImage():
	# this function capture the image of the sudoku grid from the user's webcam

    cwd = os.getcwd()
    webcam = cv2.VideoCapture(0)
    while True:
        ret, img = webcam.read()

        cv2.imshow("Test", img)
        
        if cv2.waitKey(100) != -1: # space
            print("Image "+ "puzzleImage" +"saved")
            file=cwd + '/puzzleImage.jpg'
            cv2.imwrite(file, img)
            webcam.release
            cv2.destroyAllWindows
            print("file")
            print(file)
            return file





def getGridFromImage(debug, model):
	""" This function extract the sudoku from the image, solves it and returns this back to the user
	Args:
		imagePath: path of the image we want to extract the image from
		debug: whether or not to show the output of toDo list
		model: ML model to use to find information  
	"""

	# load the ML model you created to identify digits
	modelToClassifyDigits = load_model(model)

	# load the image of sudoku baord and resize the image

	sudokuPath = captureImage()
	if sudokuPath != "":
		sudokuImage = cv2.imread(sudokuPath)
		sudokuImage = imutils.resize(sudokuImage, width=600)


	# call the find_puzzle function to identify the sqaure outline of the sudoku puzzle
	(puzzleImage, warped) = puzzleFns.find_puzzle(sudokuImage, debug=debug > 0)


	# INIT THE 9 BY 9 BOARD:
	sudokuBoard = np.zeros((9, 9), dtype="int")

	# get the X and Y step to advance so that we get the next elements of baord
	x_step = warped.shape[1] // 9
	y_step = warped.shape[0] // 9

	# initialize a list to store (x, y) coordinates of all cells
	listOfAllCells = []


	# look over the rows 
	for y in range(0, 9): 

		row = []

		# loop over cols int he rows
		for x in range(0, 9): # loop over columns 
			
			# use stepX and stepY to get the start and end coordinates of a cell
			topLeftCellX = x * x_step
			topLeftCellY = y * y_step
			bottomRightCellX = (x + 1) * x_step
			bottomRightCellY = (y + 1) * y_step
			
			# add the (x, y)-coordinates to our cell locations list
			row.append((topLeftCellX, topLeftCellY, bottomRightCellX, bottomRightCellY))

			# use these coordinates to crop the cell from the image
			digitsExtractingFromImage = warped[topLeftCellY:bottomRightCellY, topLeftCellX:bottomRightCellX]

			# then extract the number inside this image
			digitAfterPreprocessing = puzzleFns.extract_digit(digitsExtractingFromImage, debug=debug > 0)

			# verify that the digit is not empty
			if digitAfterPreprocessing is not None:

				# preprocess the digit for classification
				digit = cv2.resize(digitAfterPreprocessing, (28, 28))
				digit = digit.astype("float") / 255.0
				digit = img_to_array(digit)
				digit = np.expand_dims(digit, axis=0)

				# Classify the digit
				predictedNo = modelToClassifyDigits.predict(digit).argmax(axis=1)[0]

				# Update the Sudoku puzzle board array with predicted digits
				sudokuBoard[y, x] = predictedNo


		listOfAllCells.append(row)

	puzzle = Sudoku(3, 3, board=sudokuBoard.tolist())
	return sudokuBoard.tolist()
