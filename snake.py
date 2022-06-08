# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:48:01 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk

#widget with a game of snake contained within
class SnakeGame:
    #constructor
    #@param root - parent tk widget
    def __init__(self, root):
        root.title("Snake")
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.resizable(False, False)
        
        scoreText = ttk.Label(root, text="scores")
        scoreText.grid(column=0, row=0)
        
        gameFrame = ttk.Frame(root)
        gameFrame.grid(column=0, row=1)
        
        self.cols = 20
        self.rows = 20
        self.squareLength = 15
        self.grid = [[0 for y in range(self.rows)] for x in range(self.cols)]
        
        canvasHeight = self.squareLength*self.rows
        canvasWidth = self.squareLength*self.cols
        self.canvas = Canvas(gameFrame, height=canvasHeight, width=canvasWidth)
        self.canvas.configure(bg="black")
        self.canvas.bind("<Up>", self.up)
        self.canvas.focus_set()
        self.canvas.pack()
        
        self.snakeMoving = False
        self.headXVelocity = 0
        self.headYVelocity = 0
        self.pellet = None
        self.pelletCol = 0
        self.pelletRow = 0
        self.snakeSquares = []
        self.snakeCoords = []
        
        self.start(10, 10)
        
    #begins new game of snake with start snake segment at a certain position
    #@param col - column number of start snake segment. number from 0-19.
    #@param row - row number of start snake segment. number from 0-19
    def start(self, col=0, row=0):
        self.snakeMoving = False
        self.headXVelocity = 0
        self.headYVelocity = 0
        self.pellet = None
        self.pelletCol = 0
        self.pelletRow = 0
        self.snakeSquares = []
        self.snakeCoords = []
        
        self.grid[col][row] = 1
        self.snakeCoords.append((col, row))
        
        startSquare = self.drawUnitSquare(col, row)
        self.snakeSquares.append(startSquare)
        self.printGrid()
        
    #draw white unit square in game area
    #@param col - column number from 0 to 19
    #@param row - row number from 0 to 19
    #returns reference to square drawn
    def drawUnitSquare(self, col, row):
        k = self.squareLength
        x = col*k
        y = row*k
        square = self.canvas.create_rectangle(x, y, x + k, y + k)
        self.canvas.itemconfigure(square, fill="white", outline="white")
        self.canvas.pack()
        
        return square
        
    #draws a white unit square that will be treated as pellet for snake to eat
    #@param col - column number from 0 to 19
    #@param row - row number from 0 to 19
    def drawPellet(self, col, row):
        self.pelletCol = col
        self.pelletRow = row
        self.grid[col][row] = 1
        self.pellet = self.drawUnitSquare(col, row)
        self.canvas.pack()
        
    #has the snake eat the pellet currently on screen to elongate it
    def eatPellet(self):
        self.grid[self.pelletCol][self.pelletRow] = 0
        self.pelletCol = -1
        self.pelletRow = -1
        self.pellet = None
        
        self.snake.append(self.pellet)
        self.grid[self.prevTailCol][self.prevTailRow] = 1
        self.tailCol = self.prevTailCol
        self.tailRow = self.prevTailRow
        
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
        self.headYVelocity = -1
        self.headXVelocity = 0
        
        #starting game if hasn't started yet
        if not self.snakeMoving:
            self.snakeMoving = True
            self.moveSnake()
            
    #moves the snake until game ends
    def moveSnake(self):
        headCoords = self.snakeCoords[0]
        headCol = headCoords[0]
        headRow = headCoords[1]
        
        newHeadCoords = (headCol + self.headXVelocity, headRow + self.headYVelocity)
        newHeadCol = newHeadCoords[0]
        newHeadRow = newHeadCoords[1]
        self.snakeCoords.insert(0, newHeadCoords)
        self.snakeCoords.pop()
  
        k = self.squareLength
        x = newHeadCol*k
        y = newHeadRow*k
 
        tail = self.snakeSquares[-1]
        self.canvas.coords(tail, x, y, x + k, y + k)
        self.grid[newHeadCol][newHeadRow] = 1
        self.grid[headCol][headRow] = 0
        self.snakeSquares.insert(0, tail)
        self.snakeSquares.pop()
        self.canvas.pack()
        self.printGrid()
        
        milliseconds = 1000
        self.canvas.after(milliseconds, self.moveSnake)
        
    #prints the game grid to the console. 1 means white square, 0 means vacant
    def printGrid(self):
        #printing rows one by one
        for y in range(self.rows):
            row = [str(self.grid[x][y]) for x in range(self.cols)]
            rowString = "".join(row)
            print(rowString)
                