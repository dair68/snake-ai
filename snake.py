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
        #root.resizable(False, False)
        
        scoreText = ttk.Label(root, text="scores")
        scoreText.grid(column=0, row=0)
        
        gameFrame = ttk.Frame(root)
        gameFrame.grid(column=0, row=1)
        
        self.cols = 10
        self.rows = 10
        self.squareLength = 15
        self.grid = []
        
        canvasHeight = self.squareLength*self.rows
        canvasWidth = self.squareLength*self.cols
        self.outlineColor = "gray"
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
        self.start(self.cols//2, self.rows//2)
        
    #begins new game of snake with start snake segment at a certain position
    #@param col - column number of start snake segment. number from 1-20.
    #@param row - row number of start snake segment. number from 1-20
    def start(self, col=1, row=1):
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
        
        #labeling border of grid
        for x in range(len(self.grid)):
            self.grid[x][0] = borderChar
            self.grid[x][-1] = borderChar
            
        for y in range(len(self.grid[0])):
            self.grid[0][y] = borderChar
            self.grid[-1][y] = borderChar
        
        self.grid[col][row] = "H"
        
        self.snakeCoords = []
        self.snakeCoords.append((col, row))
        
        startSquare = self.drawUnitSquare(col, row)
        self.snakeSquares = []
        self.snakeSquares.append(startSquare)
        self.prevTailCol = col
        self.prevTailRow = row
        self.printGrid()
        self.drawPelletRandom()
        self.gameStarted = True
        
    #draw white unit square in game area
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    #returns reference to square drawn
    def drawUnitSquare(self, col, row):
        k = self.squareLength
        x = (col - 1)*k
        y = (row - 1)*k
        square = self.canvas.create_rectangle(x, y, x + k, y + k)
        self.canvas.itemconfigure(square, fill="white", outline=self.outlineColor)
        self.canvas.pack()
        
        return square
    
    #moves an existing white unit square to a particular place in game area
    #@param square - reference to square drawn
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    def moveUnitSquare(self, square, col, row):
        k = self.squareLength
        x = (col - 1)*k
        y = (row - 1)*k
        self.canvas.coords(square, x, y, x + k, y + k)
        
    #draws a white unit square that will be treated as pellet for snake to eat
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    def drawPellet(self, col, row):
        self.pelletCol = col
        self.pelletRow = row
        self.grid[col][row] = "P"
        self.pellet = self.drawUnitSquare(col, row)
        self.canvas.itemconfigure(self.pellet, fill="yellow", outline=self.outlineColor)
        self.canvas.pack()
        
    #spawns pellet in random vacant location on grid
    def drawPelletRandom(self):
        col = random.randint(1, self.cols)
        row = random.randint(1, self.rows)
        
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
        
        self.canvas.itemconfigure(self.pellet, fill="white", outline=self.outlineColor)
        self.moveUnitSquare(self.pellet, self.prevTailCol, self.prevTailRow)
    
        self.drawPelletRandom()
        self.canvas.pack()
        
    #removes white unit square from game area
    #@param col - column number from 0 to 19
    #@param row - row number from 0 to 19
    def eraseSnakeSquare(self, col, row):
        pass
        
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
        if not self.headYVelocity == 1:
            self.headYVelocity = -1
            self.headXVelocity = 0
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #sets movement direction of snake to down
    #@param event - event object
    def down(self, event):
        print("down arrow key pressed")
        #moving snake down if it's not moving up
        if not self.headYVelocity == -1:
            self.headYVelocity = 1
            self.headXVelocity = 0
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #sets movement direction of snake to right
    #@param event - event object
    def right(self, event):
        print("right arrow key pressed")
        #moving snake right if it's not going left
        if not self.headXVelocity == -1: 
            self.headYVelocity = 0
            self.headXVelocity = 1
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #sets movement direction of snake to left
    #@param event - event object
    def left(self, event):
        print("left arrow key pressed")
        #moving snake left if it's not going right
        if not self.headXVelocity == 1:
            self.headYVelocity = 0
            self.headXVelocity = -1
         
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.snakeMoving = True
            self.runTurn()
            
    #checks if snake has bumped into the edge
    def snakeTouchingEdge(self):
        headCoords = self.snakeCoords[0]
        col = headCoords[0]
        row = headCoords[1]
        
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
        
        #extends snake if eating pellet
        if self.headTouchingPellet():
            print("Pellet eaten!")
            self.eatPellet()
            
        print("\n")
        self.printGrid()
        
        #game over if snake touches edge
        if self.snakeTouchingEdge():
            self.end()
            return
        
        milliseconds = 1000
        self.canvas.after(milliseconds, self.runTurn)
        
    #shift the snake one spot
    def moveSnake(self):
        headCoords = self.snakeCoords[0]
        prevHeadCol = headCoords[0]
        prevHeadRow = headCoords[1]
        self.grid[prevHeadCol][prevHeadRow] = "S"
        headCoords = (prevHeadCol + self.headXVelocity, prevHeadRow + self.headYVelocity)
        headCol = headCoords[0]
        headRow = headCoords[1]
        self.snakeCoords.insert(0, headCoords)
        self.grid[headCol][headRow] = "H"
 
        tailCoords = self.snakeCoords[-1]
        self.prevTailCol = tailCoords[0]
        self.prevTailRow = tailCoords[1]
        self.grid[self.prevTailCol][self.prevTailRow] = "o"
        self.snakeCoords.pop()
        tailCoords = self.snakeCoords[-1]
        tailCol = tailCoords[0]
        tailRow = tailCoords[1]
        
        tail = self.snakeSquares[-1]
        self.moveUnitSquare(tail, headCol, headRow)
        self.snakeSquares.insert(0, tail)
        self.snakeSquares.pop()
        self.canvas.pack()
        
    #stops the game and displays the result
    def end(self):
        print("Game over!")
        x = 0.5*self.canvas.winfo_width()
        y = 0.5*self.canvas.winfo_height()
        self.canvas.create_text(x, y, text="Game Over", fill="white")
        
    #prints the game grid to the console. 1 means white square, 0 means vacant
    def printGrid(self):
        #printing rows one by one
        for y in range(len(self.grid)):
            row = [str(self.grid[x][y]) for x in range(len(self.grid[0]))]
            rowString = "".join(row)
            print(rowString)
                