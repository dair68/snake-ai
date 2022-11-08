# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:48:01 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk
import random
import tkinter.font as tkFont

#widget with a game of snake contained within
class SnakeGame:
    #constructor
    #@param root - parent tk widget
    def __init__(self, root):
        #root.title("Snake")
        #root.rowconfigure(0, weight=1)
        #root.rowconfigure(1, weight=5)
        
        self.mainFrame = ttk.Frame(root)
        self.mainFrame.pack()
    
        self.labelFont = tkFont.Font(family="Small Fonts", size=14)
        self.labelStyle = ttk.Style(root)
        self.labelStyle.configure("Bold.TLabel", font=self.labelFont)
        
        self.buttonFont = tkFont.Font(family="Andalus", size=11)
        self.buttonStyle = ttk.Style(root)
        self.buttonStyle.configure("Bold.TButton", font=self.buttonFont)
        
        self.score = 0
        self.scoreLabel = ttk.Label(self.mainFrame, text=f"Score: {self.score}", style="Bold.TLabel")
        self.scoreLabel.grid(column=0, row=0)
        
        self.gameFrame = ttk.Frame(self.mainFrame)
        self.gameFrame.grid(column=0, row=1)
        
        self.gameMsgLabel = ttk.Label(self.mainFrame, text="Select mode below", style="Bold.TLabel")
        self.gameMsgLabel.config(wraplength=200, justify="center")
        self.gameMsgLabel.grid(column=0, row=2)
        self.mainFrame.grid_rowconfigure(2, minsize=48, weight=1)
        
        #self.cols = 2
        #self.rows = 2
        self.cols = 10
        self.rows = 10
        self.squareLength = 30
        self.grid = []
        
        self.buttonFrame = ttk.Frame(self.mainFrame)
        self.buttonFrame.grid(column=0, row=3)
        self.playAgainBtn = ttk.Button(self.buttonFrame, text="Play", 
                                       command = self.startCentered, style="Bold.TButton")
        self.mainFrame.grid_rowconfigure(3, minsize=30, weight=1)
        self.playAgainBtn.grid(column=0, row=0)
        
        self.aiBtn = ttk.Button(self.buttonFrame, text="Run AI", style="Bold.TButton",
                                command= self.startAICentered)
        self.aiBtn.grid(column=1, row=0)
        
        canvasHeight = self.squareLength*self.rows
        canvasWidth = self.squareLength*self.cols
        self.canvas = Canvas(self.gameFrame, height=canvasHeight, width=canvasWidth)
        self.canvas.configure(bg="black", borderwidth=0, highlightthickness=0)
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
        self.aiMode = False
        self.steering = False
        
    #begins new game of player controlled snake with start snake segment at a certain position
    #@param col - column number of start snake segment. number from 1-20.
    #@param row - row number of start snake segment. number from 1-20
    def start(self, col=1, row=1):
        self.score = 0
        self.updateScoreDisplay()
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
        
        self.canvas.delete("all")
        self.canvas.focus_set()
        self.playAgainBtn.grid_remove()
        self.aiBtn.grid_remove()
        
        startSquare = self.drawUnitSquare(col, row, "blue", "white")
        self.gameMsgLabel["text"] = "Move the blue square with the arrow keys!"
        
        self.snakeSquares = [startSquare]
        self.prevTailCol = col
        self.prevTailRow = row
        self.drawPelletRandom()
        self.printGrid()
        self.gameStarted = True
        self.bindArrowKeys()
        self.aiMode = False
         
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
        self.unbindArrowKeys()
        self.gameMsgLabel["text"] = "Witness the AI guide the snake!"
        self.mainFrame.after(3000, self.randomAISteer)
        
    #begins running the ai with snake starting in center space
    def startAICentered(self):
        self.startAI(self.cols//2, self.rows//2)
        
    #has the ai choose which direction the snake will move next
    def aiSteer(self):
        self.steering = True
        forwardSpaceCol = self.headCol + self.headXVelocity
        forwardSpaceRow = self.headRow + self.headYVelocity
        forwardSpace = self.grid[forwardSpaceCol][forwardSpaceRow]
        
        #deciding whether or not snake should turn
        
        
    #determines whether it's safe for the snake to enter a certain space
    #@param col - column of space
    #@param row - row of space
    #returns true if snake can enter space without inevitable game over
    def spaceSafe(self, col, row):
        space = self.grid[col][row]
        
        #space not safe if it's a wall or snake segment other than tail
        if space == "#" or space == "S":
            return False
        
        return False
        
    #has ai move snake in random direction
    def randomAISteer(self):
        self.steering = True
        randNum = random.randrange(4)
        
        #moving snake depending on random number chosen
        if randNum == 0:
            self.up()
        elif randNum == 1:
            self.down()
        elif randNum == 2:
            self.left()
        elif randNum == 3:
            self.right()
        else:
            print("Invalid number chosen")
    
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
    #@param col - column number from 1 to 20
    #@param row - row number from 1 to 20
    #@param fillColor - color string
    #@param outlineColor - color string
    #returns reference to square drawn
    def drawUnitSquare(self, col, row, fillColor="white", outlineColor="white"):
        square = self.drawRect(col, row, col, row, fillColor, outlineColor)
        return square
    
    #draws rectangle with 2 particular spaces at its corners
    #@param col1 - column number from 1 to 20
    #@param row1 - row number from 1 to 20
    #@param col2 - column number from 1 to 20
    #@param row2 - row number from 1 to 20
    #@param fillColor - color string
    #@param outlineColor - color string
    #returns reference to rectangle drawn
    def drawRect(self, col1, row1, col2, row2, fillColor="white", outlineColor="white"):
        #ensuring that col2 is to the right of col1
        if col2 < col1:
            return self.drawRect(col2, row1, col1, row2, fillColor, outlineColor)
        
        #ensuring that row1 is above row2
        if row1 > row2:
            return self.drawRect(col1, row2, col2, row1, fillColor, outlineColor)
            
        k = self.squareLength*0.60
        margin = (self.squareLength - k)/2
        x = (col1 - 1)*self.squareLength + margin
        y = (row1 - 1)*self.squareLength + margin
        width = (col2 - col1)*self.squareLength + k
        height = (row2 - row1)*self.squareLength + k
        rect = self.canvas.create_rectangle(x, y, x + width, y + height)
        self.canvas.itemconfig(rect, fill=fillColor, outline=outlineColor)
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
        self.pellet = self.drawUnitSquare(col, row, "yellow", "yellow")
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
        
    #updates the score label to display the current score
    def updateScoreDisplay(self):
        self.scoreLabel.config(text=f"Score: {self.score}")
        
    #has the snake eat the pellet currently on screen to elongate it
    def eatPellet(self):
        print("eating pellet")
        self.grid[self.prevTailCol][self.prevTailRow] = "T"
        
        #changing tail of multilength snake to S before it extends.
        if not self.grid[self.getTailCol()][self.getTailRow()] == "H":
            self.grid[self.getTailCol()][self.getTailRow()] = "S"
        #print(f"prev tail: {self.prevTailCol}, {self.prevTailRow}")
        #print(f"current tail: {self.getTailCol()}, {self.getTailRow()}")
        tail = self.drawRect(self.prevTailCol, self.prevTailRow, self.getTailCol(), self.getTailRow())
        self.canvas.tag_lower(tail)
        #tail = self.drawUnitSquare(self.prevTailCol, self.prevTailRow)
        self.snakeSquares.append(tail)
        self.snakeCoords.append((self.prevTailCol, self.prevTailRow))
        
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
        if not self.headYVelocity == 1 and self.steering == True:
            self.unbindArrowKeys()
            self.headYVelocity = -1
            self.headXVelocity = 0
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #sets movement direction of snake to down
    #@param event - event object
    def down(self, event=None):
        print("down arrow key pressed")
        #moving snake down if it's not moving up
        if not self.headYVelocity == -1 and self.steering == True:
            self.unbindArrowKeys()
            self.headYVelocity = 1
            self.headXVelocity = 0
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #sets movement direction of snake to right
    #@param event - event object
    def right(self, event=None):
        print("right arrow key pressed")
        #moving snake right if it's not going left
        if not self.headXVelocity == -1 and self.steering == True: 
            self.unbindArrowKeys()
            self.headYVelocity = 0
            self.headXVelocity = 1
        
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
    #sets movement direction of snake to left
    #@param event - event object
    def left(self, event=None):
        print("left arrow key pressed")
        #moving snake left if it's not going right
        if not self.headXVelocity == 1 and self.steering == True:
            self.unbindArrowKeys()
            self.headYVelocity = 0
            self.headXVelocity = -1
         
        #starting game if hasn't started yet
        if self.gameStarted and not self.snakeMoving:
            self.startMovement()
            
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
        prevHeadCol = self.getHeadCol()
        prevHeadRow = self.getHeadRow()
        
        #having ai choose direction in ai mode
        if self.aiMode:
            self.randomAISteer()
        
        self.moveSnake()
        self.steering = True
        
        #returning arrow key movement for player control
        if not self.aiMode:
            self.bindArrowKeys()
        
        #printing grid if there was a change in snake's position
        if prevHeadCol != self.getHeadCol() or prevHeadRow != self.getHeadRow():
            self.printGrid()
            print("\n")
        
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
           # return
        
        milliseconds = 1000
        #milliseconds = 100
        self.canvas.after(milliseconds, self.runTurn)
        
    #shift the snake one spot
    def moveSnake(self):
        snakeLength = len(self.snakeSquares)
        #print(f"snakelength: {snakeLength}")
        
        #turning previous head square to normal body square
        prevHeadCol = self.getHeadCol()
        prevHeadRow = self.getHeadRow()
        self.grid[prevHeadCol][prevHeadRow] = "S"
        
        #removing snake's old tail square
        self.prevTailCol = self.getTailCol()
        self.prevTailRow = self.getTailRow()
        self.grid[self.getTailCol()][self.getTailRow()] = "o"
        self.canvas.delete(self.getTail())
        #snakeLength = len(self.snakeSquares)
        #print(f"snakelength: {snakeLength}")
        self.snakeCoords.pop()
        self.snakeSquares.pop()
        
        #marking tail with "T" on grid if snake has multiple segments
        if snakeLength > 1:
            self.grid[self.getTailCol()][self.getTailRow()] = "T"
        
        #inserting block at snake's new head destination
        headCol = prevHeadCol + self.headXVelocity
        headRow = prevHeadRow + self.headYVelocity
        headCoords = (headCol, headRow)
        
        #replacing old head with rectangle block for snakes of multiple segments
        if snakeLength > 1:
            print("replacing head with rectangle")
            oldHead = self.snakeSquares[0]
            self.canvas.delete(oldHead)
            self.snakeSquares.pop(0)
            rect = self.drawRect(prevHeadCol, prevHeadRow, headCol, headRow)
            self.snakeSquares.insert(0, rect)
        
        #drawing head block with blue unit square
        self.snakeCoords.insert(0, headCoords)
        head = self.drawUnitSquare(headCol, headRow)
        self.snakeSquares.insert(0, head)
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
        
    #displays game over
    def gameOver(self):
        loseText = "Game Over!"
        print(loseText)
        self.gameMsgLabel["text"] = loseText
        self.restoreModeButtons()
        
    #displays that the user has won
    def win(self):
        winText = "Congratulations. You won!"
        print(winText)
        self.gameMsgLabel["text"] = winText
        self.restoreModeButtons()
        
    #restores the mode selection buttons to screen
    def restoreModeButtons(self):
        self.playAgainBtn.config(text="Play Again")
        self.playAgainBtn.grid()
        self.aiBtn.grid()
        
    #prints the game grid to the console
    def printGrid(self):
        #printing rows one by one
        for y in range(len(self.grid[0])):
            row = [str(self.grid[x][y]) for x in range(len(self.grid))]
            rowString = "".join(row)
            print(rowString)