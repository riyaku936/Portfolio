import pygame



class Solver(object):
    """ This is a class that provides the main function solveSudoku that contains the logic for the backtracking algorithm
    """
     

    grid = None  

    def solveSudoku(self, array, window): 
        """ function that solves the sudoku grid
        Args:
            array: sudoku grid as a matrix
            window: window on which sudoku is drawn
        """

        nextRowColToLookAt=[0,0] 
      
        if(Solver.checkIfEmptyLocationLeft(array,nextRowColToLookAt) == False): 
            return True
      
        row=nextRowColToLookAt[0] 
        col=nextRowColToLookAt[1] 
      
        for num in range(1,10): 

            # only process the current num at posn (row, col) if it does not violate the three rules for sudoku
            if(Solver.checkIfCurrentAssignmentMeetsRules(array,row,col,num)): 
                self.grid.activate(row,col)
                

                # here we are doing temporary assignment which we will explore to see if it leads us to an solution
                array[row][col]=num 
                self.grid.addTempValue(row,col, num, window)
                self.grid.fillGridValues(window)
                pygame.display.update()
                

                # if the assignment of num was successful return as we have managed to successfully fill posn (row, col) 
                if(Solver.solveSudoku(self,array,window)): 
                    return True

                # remove if the assignment of num failed 
                else:
                    array[row][col] = 0
                    self.grid.removeTempValue(row,col, num, window)
                    self.grid.fillGridValues(window)
                    pygame.display.update()
    
        return False 

    

    def __init__(self, grid):
               
        self.grid = grid



    """ these three function below check if the 3 rules of a sudoku grid are met 
    """
    @staticmethod 
    def violatesRowProperty(array,row,num): 
        """ this function check if the row constraint is met
        Args:
            array: matrix form of the sudoku grid
            row: current row we are checking the row property for
            num: the num whose current placement in this row we are currently checking the validity
        """
        for i in range(9): 
            if(array[row][i] == num): 
                return True
        return False
    @staticmethod 
    def violatesColProperty(array,col,num): 
        """ this function check if the col constraint is met
        Args:
            array: matrix form of the sudoku grid
            col: current col we are checking the col property for
            num: the num whose current placement in this col we are currently checking the validity
        """
        for i in range(9): 
            if(array[i][col] == num): 
                return True
        return False
    @staticmethod 
    def violatesBoxProperty(array,row,col,num): 
        """ this function check if the box constraint is met
        Args:
            array: matrix form of the sudoku grid
            row: starting row we are checking the box property for
            col: starting col we are checking the box property for
            num: the num whose current placement in this box we are currently checking the validity
        """
        for i in range(3): 
            for j in range(3): 
                if(array[i+row][j+col] == num): 
                    return True
        return False


    
    @staticmethod   
    def checkIfCurrentAssignmentMeetsRules(array,row,col,num): 
        """this function checks if all 3 properties for a sudoku grid are met with current assignment for (row,col)
        Args:
            row: starting row we are checking the box property for
            col: starting col we are checking the box property for
            nums: the num whose current placement in this (row, col) we are currently checking the validity
        """ 
        return not Solver.violatesRowProperty(array,row,num) and not Solver.violatesColProperty(array,col,num) and not Solver.violatesBoxProperty(array,row - row%3,col - col%3,num) 


    

   
    @staticmethod   
    def checkIfEmptyLocationLeft(array,nextRowColToLookAt): 
        """this function returns the posn (row, col) of the first empty slot in the sudoku grid
        Args:
            nextRowColToLookAt: the data structure that will store the (row, col) coordinates for the next available cell
        """  
        for row in range(9): 
            for col in range(9): 
                if(array[row][col]==0): 
                    nextRowColToLookAt[0]=row 
                    nextRowColToLookAt[1]=col 
                    return True
        return False