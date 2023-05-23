# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:48:01 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from collections import deque
#from ai.snakeAI import SnakeAI
#from ai.dumbAI import DumbAI
#from ai.surviveAI import SurviveAI
#from ai.basicAI import BasicAI
from ai.advancedAI import AdvancedAI
from randomElement import randElement

#widget with a game of snake contained within
class SnakeGame:
    #constructor
    #@param root - parent tk widget
    #@param cols - number of columns in grid. must be >= 2. 10 by default
    #@param rows - number of rows in grid. must be >= 2. 10 by default
    def __init__(self, root, cols=10, rows=10):
        assert cols >= 2
        assert rows >= 2
        self.cols = cols
        self.rows = rows
        
        self.mainFrame = ttk.Frame(root)
        self.mainFrame.pack()
    
        self.labelFont = tkFont.Font(family="Small Fonts", size=14)
        self.labelStyle = ttk.Style(root)
        self.labelStyle.configure("Bold.TLabel", font=self.labelFont)
        
        self.buttonFont = tkFont.Font(family="Andalus", size=11)
        self.buttonStyle = ttk.Style(root)
        self.buttonStyle.configure("Bold.TButton", font=self.buttonFont)
        
        self.score = 0
        self.scoreLabel = ttk.Label(self.mainFrame, style="Bold.TLabel")
        self.scoreLabel["text"] = f"Score: {self.score}"
        self.scoreLabel.grid(column=0, row=0)
        
        self.gameFrame = ttk.Frame(self.mainFrame)
        self.gameFrame.grid(column=0, row=1)
        
        self.gameMsgLabel = ttk.Label(self.mainFrame, style="Bold.TLabel")
        self.gameMsgLabel["text"] = "Select mode below"
        self.gameMsgLabel.config(wraplength=200, justify="center")
        self.gameMsgLabel.grid(column=0, row=2)
        self.mainFrame.grid_rowconfigure(2, minsize=48, weight=1)
        
        self.squareLength = 30
        self.grid = []
        
        self.buttonFrame = ttk.Frame(self.mainFrame)
        self.buttonFrame.grid(column=0, row=3) 
        self.playBtn = ttk.Button(self.buttonFrame, style="Bold.TButton")
        self.playBtn["text"] = "Play"
        self.playBtn["command"] = self.startCentered
        self.mainFrame.grid_rowconfigure(3, minsize=30, weight=1)
        self.playBtn.grid(column=0, row=0)
        
        self.aiBtn = ttk.Button(self.buttonFrame, style="Bold.TButton")
        self.aiBtn["text"] = "Run AI"
        self.aiBtn["command"] = self.startAICentered
        self.aiBtn.grid(column=1, row=0)
        
        self.aiEnd = False
        self.stopBtn = ttk.Button(self.buttonFrame, style="Bold.TButton")
        self.stopBtn["text"] = "Stop"
        self.stopBtn["command"] = self.stopAI
        self.stopBtn.grid(column=0, row=0)
        self.stopBtn.grid_remove()
        
        h = self.squareLength*self.rows
        w = self.squareLength*self.cols
        self.canvas = Canvas(self.gameFrame, height=h, width=w)
        self.canvas.configure(bg="black", borderwidth=0)
        self.canvas.configure(highlightthickness=0)
        self.canvas.focus_set()
        self.canvas.pack()
        
        self.snakeMoving = False
        self.headXVel = 0
        self.headYVel = 0
        self.pellet = None
        self.pelletCol = -1
        self.pelletRow = -1
        self.snakeSquares = deque()
        self.snakeCoords = deque()
        self.prevTailCol = -1
        self.prevTailRow = -1
        
        self.gameStarted = False
        self.aiMode = False
        self.ai = None
        self.steering = False
        
        self.pelletPath = deque()
        self.postPelletPath = deque()
        self.loopMoves = 0
        
    #begins new game with start snake at a certain position
    #@param col - column number of start snake segment
    #@param row - row number of start snake segment
    def start(self, col=1, row=1):
        self.score = 0
        self.updateScoreDisplay()
        print(col)
        print(row)
        self.snakeMoving = False
        self.headXVel = 0
        self.headYVel = 0
        self.pellet = None
        self.pelletCol = -1
        self.pelletRow = -1
        
        self.grid = self.blankGrid(self.cols, self.rows)
        self.grid[col][row] = "H"
        self.snakeCoords = deque([(col, row)])
        #print(self.snakeCoords)
        
        self.canvas.delete("all")
        self.canvas.focus_set()
        self.playBtn.grid_remove()
        self.aiBtn.grid_remove()
        self.stopBtn.grid_remove()
        
        startSquare = self.drawUnitSquare(col, row, "blue", "white")
        self.gameMsgLabel["text"] = "Move the blue square with the arrow keys!"
        
        self.snakeSquares = deque([startSquare])
        self.prevTailCol = col
        self.prevTailRow = row
        self.drawPelletRandom()
        self.printGrid()
        self.gameStarted = True
        self.bindArrowKeys()
        self.aiMode = False
        self.ai = None
        self.aiEnd = False
        self.pelletPath = deque()
        self.postPelletPath = deque()
        self.loopMoves = 0
         
    #starts player controlled game with snake in middle of screen
    def startCentered(self):
        self.start(self.cols//2, self.rows//2)
        
    #begins running the ai with snake starting at certain position
    #@param col - starting column of snake
    #@param row - starting row of snake
    def startAI(self, col=1, row=1):
        print("starting ai")
        self.start(col, row)
        self.aiMode = True
        self.aiEnd = False
        #self.ai = SnakeAI(self)
        #self.ai = DumbAI(self)
        #self.ai = SurviveAI(self)
        #self.ai = BasicAI(self)
        self.ai = AdvancedAI(self)
        
        self.unbindArrowKeys()
        self.gameMsgLabel["text"] = "Witness the AI guide the snake!"
        self.stopBtn.grid()
        self.steering = True
        self.mainFrame.after(3000, self.runTurn)
        
    #begins running the ai with snake starting in center space
    def startAICentered(self):
        self.startAI(self.cols//2, self.rows//2)
        
    #has the ai input the direction it wants snake to move next
    def aiSteer(self):
        self.steering = True
        space = self.ai.nextMove()
        (col, row) = space
        print(f"ai move: {space}")
        xShift = col - self.headCol()
        yShift = row - self.headRow()
        
        #determining which direction to move snake in
        if xShift == 1 and yShift == 0:
            self.right()
        elif xShift == -1 and yShift == 0:
            self.left()
        elif xShift == 0 and yShift == 1:
            self.down()
        elif xShift == 0 and yShift == -1:
            self.up()
        else:
            print("Error. Invalid ai coordinates.")
            print("snake head: " + str(self.headCoords()))
            print("xShift: " + str(xShift))
            print("yShift: " + str(yShift))
           
    #allows game to respond to arrow key inputs
    def bindArrowKeys(self):
        self.canvas.bind("<Up>", self.up)
        self.canvas.bind("<Down>", self.down)
        self.canvas.bind("<Right>", self.right)
        self.canvas.bind("<Left>", self.left)
        self.steering = True
        
    #stops game from responding to arrow key inputs
    def unbindArrowKeys(self):
        self.canvas.unbind("<Up>")
        self.canvas.unbind("<Down>")
        self.canvas.unbind("<Right>")
        self.canvas.unbind("<Left>")
        self.steering = False
        
    #draw unit square in game area of certain color
    #@param col - column number from 1 to 10
    #@param row - row number from 1 to 10
    #@param fill - color string. "white" by default.
    #@param outline - color string. "white" by default.
    #returns reference to square drawn
    def drawUnitSquare(self, col, row, fill="white", outline="white"):
        return self.drawRect(col, row, col, row, fill, outline)
    
    #draws rectangle with 2 particular spaces at its corners
    #@param col1 - column number from 1 to 10
    #@param row1 - row number from 1 to 10
    #@param col2 - column number from 1 to 10
    #@param row2 - row number from 1 to 10
    #@param fill - color string. "white" by default.
    #@param outline - color string. "white" by default.
    #returns reference to rectangle drawn
    def drawRect(self, col1, row1, col2, row2, fill="white", outline="white"):
        #ensuring that col2 is to the right of col1
        if col2 < col1:
            return self.drawRect(col2, row1, col1, row2, fill, outline)
        
        #ensuring that row1 is above row2
        if row1 > row2:
            return self.drawRect(col1, row2, col2, row1, fill, outline)
            
        k = self.squareLength*0.60
        margin = (self.squareLength - k)/2
        x = (col1 - 1)*self.squareLength + margin
        y = (row1 - 1)*self.squareLength + margin
        width = (col2 - col1)*self.squareLength + k
        height = (row2 - row1)*self.squareLength + k
        rect = self.canvas.create_rectangle(x, y, x + width, y + height)
        self.canvas.itemconfig(rect, fill=fill, outline=outline)
        self.canvas.pack()
        return rect
        
    #counts segments in snake
    #returns numbers of squares making up snake
    def snakeLength(self):
        return len(self.snakeCoords)
    
    #gets coordinates of head square
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns coordinates in form (col, row). if head doesn't exist returns empty tuple.
    def headCoords(self, snakeSeg=None):
        #using self.snakeCoords if needed
        if snakeSeg is None:
            snakeSeg = self.snakeCoords
        
        return snakeSeg[0]
    
    #gets column snake head is in
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns grid column number of head. if no head returns -1
    def headCol(self, snakeSeg=None):
        return self.headCoords(snakeSeg)[0]
    
    #gets row snake head is in
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #return grid row number of head
    def headRow(self, snakeSeg=None):
        return self.headCoords(snakeSeg)[1]
    
    #obtains head square in canvas
    #returns reference to head unit square in canvas. if none returns None
    def headSquare(self):
        return self.snakeSquares[0] if self.snakeLength() > 0 else None
    
    #obtains space coords of the space pellet is occupying
    #returns tuple of form (pelletCol, pelletRow)
    def pelletCoords(self):
        return (self.pelletCol, self.pelletRow)
    
    #obtains tail square in canvas
    #returns reference to tail unit square
    def tailSquare(self):
        return self.snakeSquares[-1] if self.snakeLength() > 0 else None
    
    #obtains tail coordinates
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns tail grid coordinates as (col, row). if no tail returns empty tuple
    def tailCoords(self, snakeSeg=None):
        #using self.snakeCoords if needed
        if snakeSeg is None:
            snakeSeg = self.snakeCoords
        
        return snakeSeg[-1]
    
    #obtains tail column
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns tail grid column number. if no tail returns -1
    def tailCol(self, snakeSeg=None):
        return self.tailCoords(snakeSeg)[0]
    
    #obatins tail row
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns tail grid row number. if no tail returns -1
    def tailRow(self, snakeSeg=None):
        return self.tailCoords(snakeSeg)[1]
    
    #draws pellet unit square
    #@param col - column number from 1 to 10
    #@param row - row number from 1 to 10
    def drawPellet(self, col, row):
        self.pelletCol = col
        self.pelletRow = row
        self.grid[col][row] = "P"
        self.pellet = self.drawUnitSquare(col, row, "yellow", "yellow")
        self.canvas.pack()
        
    #spawns pellet in random vacant location on grid
    def drawPelletRandom(self):
        emptySpaces = set()
        
        #compiling all empty spaces
        for x in range(1, self.cols + 1):
            for y in range(1, self.rows + 1):
                #found empty space
                if self.grid[x][y] == "o":
                    emptySpaces.add((x, y))
                
        pelletCoords = randElement(emptySpaces)
        pelletCol = pelletCoords[0]
        pelletRow = pelletCoords[1]
                
        self.drawPellet(pelletCol, pelletRow)
        
    #updates the score label to display the current score
    def updateScoreDisplay(self):
        self.scoreLabel.config(text=f"Score: {self.score}")
        
    #has the snake eat the pellet currently on screen to elongate it
    def eatPellet(self):
        print("eating pellet")
        prevCol = self.prevTailCol 
        prevRow = self.prevTailRow
        self.grid[prevCol][prevRow] = "T"
        
        col = self.tailCol()
        row = self.tailRow()
        
        #changing tail of multilength snake to S before it extends.
        if not self.grid[col][row] == "H":
            self.grid[col][row] = "S"
     
        tail = self.drawRect(prevCol, prevRow, col, row)
        self.canvas.tag_lower(tail)
        self.snakeSquares.append(tail)
        self.snakeCoords.append((prevCol, prevRow))
        
        self.score += 1
        self.updateScoreDisplay()
       
        self.canvas.delete(self.pellet)
        self.pellet = None
        self.pelletCol = -1
        self.pelletRow = -1
        self.canvas.pack()
        
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
       
    #begins the snake movement loop
    #causes the snake to start moving while adjusting game to accomodate
    def startMovement(self):
        print("starting movement")
        self.snakeMoving = True
        self.steering = True
        
        #removing text for player controlled game
        if not self.aiMode:
            self.gameMsgLabel["text"] = ""
            self.runTurn()
       
    #sets movement direction of snake to up
    #@param event - event object
    def up(self, event=None):
        print("up arrow key pressed")
        #moving snake up if it's not moving down
        if not self.headYVel == 1 and self.steering == True:
            self.unbindArrowKeys()
            self.headYVel = -1
            self.headXVel = 0
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #sets movement direction of snake to down
    #@param event - event object
    def down(self, event=None):
        print("down arrow key pressed")
        #moving snake down if it's not moving up
        if not self.headYVel == -1 and self.steering == True:
            self.unbindArrowKeys()
            self.headYVel = 1
            self.headXVel = 0
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #sets movement direction of snake to right
    #@param event - event object
    def right(self, event=None):
        print("right arrow key pressed")
        #moving snake right if it's not going left
        if not self.headXVel == -1 and self.steering == True: 
            self.unbindArrowKeys()
            self.headYVel = 0
            self.headXVel = 1
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #sets movement direction of snake to left
    #@param event - event object
    def left(self, event=None):
        print("left arrow key pressed")
        #moving snake left if it's not going right
        if not self.headXVel == 1 and self.steering == True:
            self.unbindArrowKeys()
            self.headYVel = 0
            self.headXVel = -1
         
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #steers snake based inputted velocities. snake can't turn 180 degrees.
    #@param xVelocity - -1, 0, or 1
    #@param yVelocity - -1, 0, or 1
    #steers snake based on x and y velocities. if parameters are invalid, snake persists in current direction
    def steerSnake(self, xVelocity, yVelocity):
        #selecting arrow key direction that leads to chosen space
        if xVelocity == 1 and yVelocity == 0:
            self.right()
        elif xVelocity == -1 and yVelocity == 0:
            self.left()
        elif yVelocity == 1 and xVelocity == 0:
            self.down()
        elif yVelocity == -1 and xVelocity == 0:
            self.up()
        else:
            print("Error. Invalid x and/or y velocities inputed.")
            print(f"x velocity: {xVelocity}")
            print(f"y velocity: {yVelocity}")
            print(f"snake head velocity: ({self.headXVel}, {self.headYVel})")
                    
    #shifts the snake one spot based on arrow keys pressed
    #makes new pellet if needed
    def runTurn(self):
        prevHeadCol = self.headCol()
        prevHeadRow = self.headRow()
        
        #having ai choose direction in ai mode
        if self.aiMode:
            self.aiSteer()
            self.moveSnake()
            self.ai.update()
        else:
            self.moveSnake()
            
        self.steering = True
        
        #returning arrow key movement for player control
        if not self.aiMode:
            self.bindArrowKeys()
          
        #ending ai if needed
        if self.aiEnd:
            self.restoreModeButtons()
            self.playBtn.config(text="Play")
            self.gameMsgLabel["text"] = "Select mode below"
            return
          
        #game over if snake touches edge or itself
        if self.grid[self.headCol()][self.headRow()] == "X":
            self.gameOver()
            self.printGrid()
            print("\n")
            return
        
        #checking if game has been won
        if self.snakeLength() == self.cols*self.rows:
            self.win()
            self.printGrid()
            print("\n")
            return
        
        #drawing extra pellet if needed
        if self.pellet == None:
            self.drawPelletRandom()
           
        #printing grid if there was a change in snake's position
        if prevHeadCol != self.headCol() or prevHeadRow != self.headRow():
            self.printGrid()
            print("\n")
        
        #milliseconds = 1000
        milliseconds = 100
        self.canvas.after(milliseconds, self.runTurn)
            
    #shift the snake one spot based on x and y velocities recorded by game
    def moveSnake(self):
        snakeLength = self.snakeLength()
   
        #turning previous head square to normal body square
        prevHeadCol = self.headCol()
        prevHeadRow = self.headRow()
        self.grid[prevHeadCol][prevHeadRow] = "S"
        
        #removing snake's old tail square
        self.prevTailCol = self.tailCol()
        self.prevTailRow = self.tailRow()
        self.grid[self.tailCol()][self.tailRow()] = "o"
        self.canvas.delete(self.tailSquare())
    
        self.snakeCoords.pop()
        self.snakeSquares.pop()
        
        #marking tail with "T" on grid if snake has multiple segments
        if snakeLength > 1:
            self.grid[self.tailCol()][self.tailRow()] = "T"
        
        #inserting block at snake's new head destination
        headCol = prevHeadCol + self.headXVel
        headRow = prevHeadRow + self.headYVel
        headCoords = (headCol, headRow)
        
        #replacing old head with rectangle block for snakes length > 1
        if snakeLength > 1:
            #print("replacing head with rectangle")
            oldHead = self.snakeSquares.popleft()
            self.canvas.delete(oldHead)
            rect = self.drawRect(prevHeadCol, prevHeadRow, headCol, headRow)
            self.snakeSquares.appendleft(rect)
        
        #drawing head block with blue unit square
        self.snakeCoords.appendleft(headCoords)
        head = self.drawUnitSquare(headCol, headRow)
        self.snakeSquares.appendleft(head)
        headDestination = self.grid[headCol][headRow]
        
        #affecting game based on space head touches
        if headDestination == "#" or headDestination == "S":
            self.grid[headCol][headRow] = "X"
            self.canvas.itemconfig(head, fill="red", outline="white")
        else:
            self.grid[headCol][headRow] = "H"
            self.canvas.itemconfig(head, fill="blue", outline="white")
            
            #snake has eaten pellet
            if headDestination == "P":
                self.eatPellet()
                
        self.canvas.pack()
        
    #stops ai from running game
    def stopAI(self):
        print("terminating ai")
        self.aiEnd = True
        
    #displays game over
    def gameOver(self):
        loseText = "Game Over!"
        print(loseText)
        self.gameMsgLabel["text"] = loseText
        self.restoreModeButtons()
        self.playBtn.config(text="Play Again")
        
    #displays that the user has won
    def win(self):
        winText = "Congratulations. You won!"
        print(winText)
        self.gameMsgLabel["text"] = winText
        self.restoreModeButtons()
        self.playBtn.config(text="Play Again")
        
    #restores the mode selection buttons to screen
    def restoreModeButtons(self):
        self.stopBtn.grid_remove()
        self.playBtn.grid()
        self.aiBtn.grid()
        
    #prints a game grid to the console
    #@param grid - 2 by 2 list representing game grid. self.grid by default
    def printGrid(self, grid=None):
        #using self.grid if grid not provided
        if grid == None:
            grid = self.grid
        
        #printing rows one by one
        for y in range(len(grid[0])):
            row = [grid[x][y] for x in range(len(grid))]
            rowString = "".join(row)
            print(rowString)
                   
    #produces 2 by 2 nested lists that represent a blank game grid
    #@param cols - number of column in grid
    #@param rows - number of rows in grid
    #returns 2 by 2 lists that allow for blank grid to be modified
    def blankGrid(self, cols, rows):
        grid = [["o" for y in range(rows + 2)] for x in range(cols + 2)]
        borderChar = "#"
        
        #labeling top and bottom borders of grid
        for x in range(len(grid)):
            grid[x][0] = borderChar
            grid[x][-1] = borderChar
        
        #labeling left and right borders of grid
        for y in range(len(grid[0])):
            grid[0][y] = borderChar
            grid[-1][y] = borderChar
            
        return grid