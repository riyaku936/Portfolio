from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2

def find_puzzle(image, debug=True):
	""" The purpose of this function is to find all sudoku puzzle in an image
	Args:
		image: The photo of a Sudoku puzzle.
		debug: A optional boolean indicating whether to show intermediate steps so you can better visualize what is happening 
	"""


	# make the image grayscale
	grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# apply a gaussian blur 
	afterGaussianBlur = cv2.GaussianBlur(grayscaleImage, (7, 7), 3)

	# apply adaptive thresholding to peg grayscale pixels toward each end of the [0, 255] pixel range and then invert the threshold map
	afterAdaptiveThresh = cv2.adaptiveThreshold(afterGaussianBlur, 255,
		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	afterAdaptiveThresh = cv2.bitwise_not(afterAdaptiveThresh)


	if debug:
		cv2.imshow("Puzzle Thresh", afterAdaptiveThresh)
		cv2.waitKey(0)

	# TILL THIS POINT IMAGE IS THRESOHOLDED AND LOOKS LIKE BLACK AND WHITE IMAGE


	# find all the contours in the thresholded image
	allContours = cv2.findContours(afterAdaptiveThresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	allContours = imutils.grab_contours(allContours)

	# sort the contours by area in descending order
	allContours = sorted(allContours, key=cv2.contourArea, reverse=True)

	# initialize a contour that corresponds to the puzzle outline
	contourForPuzzle = None
	# loop over the contours starting with the contour with maximum area to find the contour the is equal to a sqaure with 4 corners
	for c in allContours:
		# approx the permimeter of the contour 
		peri = cv2.arcLength(c, True)

		# approximate the contour shape
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if our approximated contour has four points, then we can
		# assume we have found the outline of the puzzle --> break out of the loop
		if len(approx) == 4:
			contourForPuzzle = approx
			break


	
	# raise error if the puzzle contour is empty then our script could not find a square sudoku outline
	if contourForPuzzle is None:
		raise Exception(("Could not find Sudoku puzzle outline. "
			"Try debugging your thresholding and contour steps."))
	
	

	if debug:
		# draw the contour on image an display
		output = image.copy()
		cv2.drawContours(output, [contourForPuzzle], -1, (0, 255, 0), 2)
		cv2.imshow("Puzzle Outline", output)
		cv2.waitKey(0)


	# apply four_point_transform to the image and grayscale version to get a bird's eye image of board
	RGBBirdsEye = four_point_transform(image, contourForPuzzle.reshape(4, 2))
	grayscaleImageBirdsEye = four_point_transform(grayscaleImage, contourForPuzzle.reshape(4, 2))

	if debug:
		cv2.imshow("Puzzle Transform", RGBBirdsEye)
		cv2.waitKey(0)

	# return the RBG and grayscale version of the puzzles
	return (RGBBirdsEye, grayscaleImageBirdsEye)



def extract_digit(cell, debug=True):
	"""
	This section will show you how to examine each of the individual cells in a Sudoku board, detect if there is a digit in the cell, and if so, extract the digit.
	Args:
		cell: current cell we are imagining
	"""


	# clear the pixels touching the outside section of the border / any connected borders for the current cell
	removedForegroundNoise = cv2.threshold(cell, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	removedForegroundNoise = clear_border(removedForegroundNoise)


	if debug:
		cv2.imshow("Cell Thresh", removedForegroundNoise)
		cv2.waitKey(0)

	
	# find contours in the cell
	contours = cv2.findContours(removedForegroundNoise.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)


	# if no contours found return None
	if len(contours) == 0:
		return None


	# otherwise, find the largest contour based on the pixel area in the cell and create a
	# mask for the contour
	# the mask will be 0s apart from where the contours are present 
	largestContourArea = max(contours, key=cv2.contourArea)
	mask = np.zeros(removedForegroundNoise.shape, dtype="uint8")
	cv2.drawContours(mask, [largestContourArea], -1, 255, -1)




	# compute the percentage of masked pixels relative to the total
	# area of the image
	# this gives us the percentFilled value to ensure the contour is not just noise
	(h, w) = removedForegroundNoise.shape
	percentFilledInImage = cv2.countNonZero(mask) / float(w * h)


	# if percent filled is less than 3% ignore since it is probably noise
	if percentFilledInImage < 0.03:
		return None


	# apply the mask to the thresholded cell to isolate the pixels 
	digitInCell = cv2.bitwise_and(removedForegroundNoise, removedForegroundNoise, mask=mask)


	if debug:
		cv2.imshow("Digit", digitInCell)
		cv2.waitKey(0)


	return digitInCell

