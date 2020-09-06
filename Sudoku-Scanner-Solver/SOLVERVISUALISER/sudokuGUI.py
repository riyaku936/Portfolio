import tkinter as tk
# from tkinter import messagebox
# import pygame
# import sudokuAlgo
import pygame
from SOLVERVISUALISER import sudokuAlgo 
pygame.font.init()



"""some important colours used in the GUI
"""
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
black = (0,0,0)


class Box(object):
    """ This class is used to represent each block/box that makes the 9 by 9 grid of the sudoku grid. 
    Each Box has three attibutes: x position (xpos), y position (ypos), value (value)
    """

    xpos = 0
    ypos = 0
    value = 0

    def __init__(self, xpos, ypos, value):
        self.xpos = xpos
        self.ypos = ypos
        self.value = value

        
    def plotBox(self, win, activated):
        """ This function is called to display each box of the grid. It adjusts the display of the Box based on the "activated" value of the Box.
        Args:
            win: window on which all cells are present 
            activated : tells you the status of the current cell 
        """
        

        if activated == 'a':
            font = pygame.font.Font('freesansbold.ttf', 32) 
            text = font.render(str(self.value), True, green) 
            textRect = text.get_rect()  
            # textRect.border_radius = 3
            textRect.center = (int(self.xpos),int(self.ypos) )
            win.blit(text, textRect)
        
        elif activated == 'b':
            font = pygame.font.Font('freesansbold.ttf', 32) 
            text = font.render(str(self.value), True, white) 
            textRect = text.get_rect()  
            textRect.center = (int(self.xpos),int(self.ypos) )
            win.blit(text, textRect)
    
        elif activated == 'c':
            font = pygame.font.Font('freesansbold.ttf', 32) 
            text = font.render(str(self.value), True, black) 
            textRect = text.get_rect()  
            textRect.center = (int(self.xpos),int(self.ypos) )
            win.blit(text, textRect)



    def changeValue(newValue):
        value = newValue





class Grid(object):
    """ This class is used to represent the full 9 by 9 sudoky grid.
    The "array" instance variable of Grid stores each "Box" object.
    The "activated" instance variable of the Grid stores information on how each box in the grid should be displayed.
    """

    nCols = 9
    nRows = 9
    array = [[None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None]]



    activated = [['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
    
    ]



    def __init__(self):
        pass

       
    def addBlock(self, i, j, block):
        """ This function adds a Box object to the array instance variable
        Args:
            i: row in grid to update
            j: col in grid to update
            block: value to update grid with
        """ 
        self.array[i][j] = block

    
       
    def activate(self, i, j):
        """ This function is used to activate a box that that was already filled in by the question
        Args:
            i: row in grid to activate 
            j: col in grid to activate
        """ 
        self.activated[i][j] = 'a'


       
    def addTempValue(self, i, j, value, window):
        """ This function is used to activate a Box when we are temporarily assigning a value to the Box
        Args:
            i: row in grid to update
            j: col in grid to update
            value: possible ans to assign at position (i,j)
            window: the window to update 
        """ 
        self.array[i][j].value = value
        self.activated[i][j] = 'a'
        

    
    def removeTempValue(self, i, j, value, window):
        """ This function is used to remove the temporary assignment given to the Box
        Args:
            i: row in grid to update
            j: col in grid to update
            value: value to update at position (i,j)
        """ 
        self.array[i][j].value = value
        self.activated[i][j] = 'c'
        


    
    def fillGridValues(self, win):
        """ This function draws the grid with the current "activated" state of each Box 
        Args:
            win: window to update
        """ 
        for i in range(9):
            for j in range(9):
                if(self.array[i][j].value != 0):
                    self.array[i][j].plotBox(win, self.activated[i][j])






def drawGrid(width, row, surface):
    """ This function is used to draw the lines that form part of the sudoku grid 
    Args:
        width: width of the grid
        row: number of rows
        surface: the window we draw the grid on
    """
    sizeBetweenLines = width // row

    x = 0
    y = 0
    for i in range(row):
        x = x + sizeBetweenLines
        y = y + sizeBetweenLines

        if i==2 or i==5 :
            
            pygame.draw.line(surface, (255,255,255), (x,0),(x,width), 6)
            pygame.draw.line(surface, (255,255,255), (0,y),(width,y), 6)

        else:
            pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
            pygame.draw.line(surface, (255,255,255), (0,y),(width,y))
        


        
        

        


def redrawWindow(width, row, surface):
    """ This function is called to redraw and update the appearance of the grid
    Args:
        width: width of grid
        row: number of rows
        surface:  the window we draw the grid on
    """
    surface.fill((0,0,0))


    drawGrid(width, row, surface)

    global grid

    grid = Grid()

    x = 25
    y = 25

    for i in range(9):
        for j in range(9):
           # add
           box = Box(x,y,values[i][j])
           grid.addBlock(i, j, box)
           x = x + 500/9

           # increase x 
        y = y + 500/9
        x = 25

    grid.fillGridValues(surface)

    pygame.draw.rect(surface, [0, 225, 0], (0, width, width, height))


    font = pygame.font.Font('freesansbold.ttf', 32) 
    text = font.render('Solve Sudoku!', True, green, blue) 
    textRect = text.get_rect()  
    textRect.center = (240, width+50) 
    surface.blit(text, textRect) 

    pygame.display.update()




def main(inputGrid):
    """ This function runs the pygame functionality
    Args:
        inputGrid : grid the game is played on
    """

    pygame.display.set_caption('Sudoku') 

    global width, rows, height, values
    values = inputGrid
    width = 500 # this is width of window and it is also height and width of the grid 
    height = 600

    rows = 9
    cols = 9
    window = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock() # creating a clock object


    flag = True

    button = pygame.Rect(0, width, width, height)
  
    font = pygame.font.Font('freesansbold.ttf', 32) 
    text = font.render('Solve Sudoku!', True, green, blue) 
    textRect = text.get_rect()  
    textRect.center = (500, width+200) 
    
    


    while flag:
        
        for event in pygame.event.get():
            

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                
                # checks if mouse position is over the button - if true then start solving the sudoku puzzle
                if button.collidepoint(mouse_pos): 
                    solver = sudokuAlgo.Solver(grid)
                    solver.solveSudoku(values, window)

        
        
        clock.tick(500) 
        window.blit(text, textRect) 
        redrawWindow(width, rows, window)

    

    
    


    