# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:48:01 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk
import random

#widget with a game of snake contained within
class SnakeGame:
    #constructor
    #@param root - parent tk widget
    def __init__(self, root):
        root.title("Snake")
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        
        self.score = 0
        self.scoreText = ttk.Label(root, text=f"Score: {self.score}")
        self.scoreText.grid(column=0, row=0)
        
        gameFrame = ttk.Frame(root)
        gameFrame.grid(column=0, row=1)
        
        self.cols = 5
        self.rows = 5
        self.squareLength = 20
        self.grid = []
        
        canvasHeight = self.squareLength*self.rows
        canvasWidth = self.squareLength*self.cols
        self.canvas = Canvas(gameFrame, height=canvasHeight, width=canvasWidth)
        self.canvas.configure(bg="black", borderwidth=0, highlightthickness=0)
        self.canvas.bind("<Up>", self.up)
        self.canvas.bind("<Down>", self.down)
        self.canvas.bind("<Right>", self.right)
        self.canvas.bind("<Left>", self.left)
        self.canvas.focus_set()
        self.canvas.pack()
        
        self.snakeMoving = False
        self.headXVelocity = 0
        self.headYVelocity = 0
        self.pellet = None
        self.pelletCol = -1
        self.pelletRow = -1
        self.snakeSquares = []
        self.snakeCoords = []
        self.prevTailCol = -1
        self.prevTailRow = -1
        
        self.gameStarted = False
        self.keyboardInput = True
        self.start(self.cols//2, self.rows//2)
        
    #begins new game of snake with start snake segment at a certain position
    #@param col - column number of start snake segment. number from 1-20.
    #@param row - row number of start snake segment. number from 1-20
    def start(self, col=1, row=1):
        self.score = 0
        print(col)
        print(row)
        self.snakeMoving = False
        self.headXVelocity = 0
        self.headYVelocity = 0
        self.pellet = None
        self.pelletCol = -1
        self.pelletRow = -1
        
        self.grid = [["o" for y in range(self.rows + 2)] for x in range(self.cols + 2)]
        borderChar = "#"
        
        #labeling top and bottom borders of grid
        for x in range(len(self.grid)):
            self.grid[x][0] = borderChar
            self.grid[x][-1] = borderChar
        
        #labeling left and right borders of grid
        for y in range(len(self.grid[0])):
            self.grid[0][y] = borderChar
            self.grid[-1][y] = borderChar
        
        self.grid[col][row] = "H"
        self.snakeCoords = [(col, row)]
        
        startSquare = self.drawUnitSquare(col, row)
        #self.setUnitSquareColor(startSquare, "blue")
        
        self.snakeSquares = [startSquare]
        self.prevTailCol = col
        self.prevTailRow = row
        self.printGrid()
        self.drawPelletRandom()
        self.gameStarted = True
        self.keyboardInput = True
        
    #draw unit square in game area of certain color
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    #@param color - color string
    #returns reference to square drawn
    def drawUnitSquare(self, col, row, color="white"):
        square = self.drawRect(col, row, col, row)
        self.canvas.itemconfig(square, fill=color)
        return square
    
    #draws rectangle with 2 particular spaces as its corners
    #@param col1 - column number from 1 to 20
    #@param row1 - row number from 1 to 20
    #@param col2 - column number from 1 to 20
    #@param row2 - row number from 1 to 20
    #returns reference to rectangle drawn
    def drawRect(self, col1, row1, col2, row2):
        #ensuring that col2 is to the right of col1
        if col2 < col1:
            self.drawRect(col2, row1, col1, row2)
        
        #ensuring that row1 is above row2
        if row1 > row2:
            self.drawRect(col1, row2, col2, row1)
            
        k = self.squareLength*0.75
        margin = (self.squareLength - k)/2
        x = (col1 - 1)*self.squareLength + margin
        y = (row1 - 1)*self.squareLength + margin
        width = (col2 - col1)*self.squareLength + k
        height = (row2 - row1)*self.squareLength + k
        rect = self.canvas.create_rectangle(x, y, x + width, y + height)
        self.canvas.pack()
        return rect
    
    #moves an existing white unit square to a particular place in game area
    #@param square - reference to square drawn
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    def moveUnitSquare(self, square, col, row):
        k = self.squareLength*0.75
        margin = (self.squareLength - k)/2
        x = (col - 1)*self.squareLength + margin
        y = (row - 1)*self.squareLength + margin
        self.canvas.coords(square, x, y, x + k, y + k)
    
    #gets coordinates of head square
    #returns coordinates in form (col, row)
    def getHeadCoords(self):
        return self.snakeCoords[0]
    
    #gets column snake head is in
    #returns grid column number of head
    def getHeadCol(self):
        return self.getHeadCoords()[0]
    
    #gets row snake head is in
    #return grid row number of head
    def getHeadRow(self):
        return self.getHeadCoords()[1]
    
    #obtains head square
    #returns reference to head unit square
    def getHead(self):
        return self.snakeSquares[0]
    
    #obtains tail square
    #returns reference to tail unit square
    def getTail(self):
        return self.snakeSquares[-1]
    
    #obtains tail coordinates
    #returns tail grid coordinates as (col, row)
    def getTailCoords(self):
        return self.snakeCoords[-1]
    
    #obtains tail column
    #returns tail grid column number
    def getTailCol(self):
        return self.getTailCoords()[0]
    
    #obatins tail row
    #returns tail grid row number
    def getTailRow(self):
        return self.getTailCoords()[1]
    
    #draws a yellow unit square that will be treated as pellet for snake to eat
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    def drawPellet(self, col, row):
        self.pelletCol = col
        self.pelletRow = row
        self.grid[col][row] = "P"
        self.pellet = self.drawUnitSquare(col, row, "yellow")
        self.canvas.pack()
        
    #spawns pellet in random vacant location on grid
    def drawPelletRandom(self):
        emptySpaces = []
        
        #compiling all empty spaces
        for x in range(1, self.cols + 1):
            for y in range(1, self.rows + 1):
                #found empty space
                if self.grid[x][y] == "o":
                    emptySpaces.append((x, y))
                    
        randIndex = random.randrange(len(emptySpaces))
        pelletCoords = emptySpaces[randIndex]
        pelletCol = pelletCoords[0]
        pelletRow = pelletCoords[1]
                
        self.drawPellet(pelletCol, pelletRow)
        
    #has the snake eat the pellet currently on screen to elongate it
    def eatPellet(self):
        self.snakeSquares.append(self.pellet)
        self.grid[self.prevTailCol][self.prevTailRow] = "S"
        self.snakeCoords.append((self.prevTailCol, self.prevTailRow))
        
        self.setUnitSquareColor(self.pellet, "white")
        self.moveUnitSquare(self.pellet, self.prevTailCol, self.prevTailRow)
        
        connector = self.drawUnitSquare(self.prevTailCol, self.prevTailRow)
        self.setUnitSquareColor(connector, "white")
        xShift = (self.snakeCoords[-2][0] - self.snakeCoords[-1][0])/2
        yShift = (self.snakeCoords[-2][1] - self.snakeCoords[-1][1])/2
        self.canvas.move(connector, xShift, yShift)
        
        self.score += 1
        self.scoreText.config(text=f"Score: {self.score}")
        self.canvas.pack()
       
        self.pellet = None
        self.pelletCol = -1
        self.pelletRow = -1
        
    #redraws game area to match current progress
    def redrawGame(self):
       self.canvas.configure(bg="black")
       
       #drawing new white squares
       for i in range(self.cols):
           for j in range(self.rows):
               #drawing white square where there's a 1 in grid
               if self.grid[i][j] == 1:
                   self.drawPellet(i, j)
                   
       self.canvas.pack()
       
    #sets movement direction of snake to up
    #@param event - event object
    def up(self, event):
        print("up arrow key pressed")
        #moving snake up if it's not moving down
        if self.keyboardInput and not self.headYVelocity == 1:
            self.headYVelocity = -1
            self.headXVelocity = 0
            self.keyboardInput = False
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #sets movement direction of snake to down
    #@param event - event object
    def down(self, event):
        print("down arrow key pressed")
        #moving snake down if it's not moving up
        if self.keyboardInput and not self.headYVelocity == -1:
            self.headYVelocity = 1
            self.headXVelocity = 0
            self.keyboardInput = False
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #sets movement direction of snake to right
    #@param event - event object
    def right(self, event):
        print("right arrow key pressed")
        #moving snake right if it's not going left
        if self.keyboardInput and not self.headXVelocity == -1: 
            self.headYVelocity = 0
            self.headXVelocity = 1
            self.keyboardInput = False
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #sets movement direction of snake to left
    #@param event - event object
    def left(self, event):
        print("left arrow key pressed")
        #moving snake left if it's not going right
        if self.keyboardInput and not self.headXVelocity == 1:
            self.headYVelocity = 0
            self.headXVelocity = -1
            self.keyboardInput = False
         
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #checks if snake has bumped into the edge
    def snakeTouchingEdge(self):
        col = self.getHeadCol()
        row = self.getHeadRow()
        
        return col == 0 or col == self.cols + 1 or row == 0 or row == self.rows + 1   
    
    #checks if snake head is on same spot as pellet
    def headTouchingPellet(self):
        headCoords = self.snakeCoords[0]
        col = headCoords[0]
        row = headCoords[1]
        
        return col == self.pelletCol and row == self.pelletRow
            
    #shifts the snake one spot and makes new pellet if none on screen
    def runTurn(self):
        self.moveSnake() 
        self.keyboardInput = True
        print("\n")
        self.printGrid()
        
        #game over if snake touches edge or itself
        if self.grid[self.getHeadCol()][self.getHeadRow()] == "X":
            self.gameOver()
            return
        
        #checking if game has been won
        if len(self.snakeSquares) == self.cols*self.rows:
            self.win()
            return
        
        #drawing extra pellet if needed
        if self.pellet == None:
            self.drawPelletRandom()
        
        milliseconds = 1000
        self.canvas.after(milliseconds, self.runTurn)
        
    #shift the snake one spot
    def moveSnake(self):
        #turning previous head square to normal body square
        prevHeadCol = self.getHeadCol()
        prevHeadRow = self.getHeadRow()
        self.grid[prevHeadCol][prevHeadRow] = "S"
        
        #removing snake's old tail square
        self.prevTailCol = self.getTailCol()
        self.prevTailRow = self.getTailRow()
        self.grid[self.getTailCol()][self.getTailRow()] = "o"
        self.canvas.delete(self.getTail())
        self.snakeCoords.pop()
        self.snakeSquares.pop()
        
        #inserting block at snake's new head destination
        headCol = prevHeadCol + self.headXVelocity
        headRow = prevHeadRow + self.headYVelocity
        headCoords = (headCol, headRow)
        self.snakeCoords.insert(0, headCoords)
        head = self.drawUnitSquare(headCol, headRow)
        self.snakeSquares.insert(0, head)
        headDestination = self.grid[headCol][headRow]
        
        #affecting game based on space head touches
        if headDestination == "#" or headDestination == "S":
            self.grid[headCol][headRow] = "X"
            self.canvas.itemconfig(head, fill="red")
        else:
            self.grid[headCol][headRow] = "H"
            self.canvas.itemconfig(head, fill="white")
            
            #snake has eaten pellet
            if headDestination == "P":
                #self.eatPellet()
                pass
        self.canvas.pack()
        
    #displays game over
    def gameOver(self):
        print("Game over!")
        x = 0.5*self.canvas.winfo_width()
        y = 0.5*self.canvas.winfo_height()
        self.canvas.create_text(x, y, text="Game Over", fill="magenta")
        
    #displays that the user has won
    def win(self):
        print("Congratulations. You won!")
        x = 0.5*self.canvas.winfo_width()
        y = 0.5*self.canvas.winfo_height()
        self.canvas.create_text(x, y, text="Congratulations.\n   You won!", fill="green")
        
    #prints the game grid to the console
    def printGrid(self):
        #printing rows one by one
        for y in range(len(self.grid)):
            row = [str(self.grid[x][y]) for x in range(len(self.grid[0]))]
            rowString = "".join(row)
            print(rowString)