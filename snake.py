# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:48:01 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk
import random
import tkinter.font as tkFont
from queue import Queue
from queue import LifoQueue
import math

#prints a 2d array to the console
#@param matrix - a 2d array
#prints array elements to console, with 1st index interpreted as column, 2nd index interpreted as row.
# 0th column is leftmost column, 0th row is topmost row with element printed left to right, top to bottom
def printMatrix(matrix):
    #printing rows one by one
    for y in range(len(matrix[0])):
        row = [matrix[x][y] for x in range(len(matrix))]
        rowString = "".join(row)
        print(rowString)
        
#obtains a random element from a list
#@param elements - list in question. must have at least one element
#returns random element from list. 
def randomElement(elements):
    #checking if list is non empty
    if len(elements) == 0:
        print("Error. Nonempty list inputted.")
        return None
    
    randIndex = random.randrange(len(elements))
    return elements[randIndex]

#reverses the direction of a vector
#@param vect - vector represented by tuple of numbers
#returns tuple representing vector with same magnitude but opposite direction acorss origin
def reverseVector(vect):
    return tuple(-k for k in vect)

#rotates a 2d vector a certain number of radians counterclockwise
#@param vect - 2d vector represented by tuple of numbers
#@param angle - angle in radians
#returns tuple representing resulting vector after rotating around origin
def rotateVector(vect, angle):
    x1 = vect[0]
    x2 = vect[1]
    y1 = x1*math.cos(angle) - x2*math.sin(angle)
    y2 = x1*math.sin(angle) + x2*math.cos(angle)
    return (y1, y2)

#rotates 2d vector 90 degrees counterclockwise
#@param x - x-coordinate of 2d vector
#@param y - y-coorindate of 2d vector
#returns tuple representing vector after rotation after origin
def rotateVector90Deg(x, y):
    return (-y, x)

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
        
        #self.cols = 10
        #self.rows = 10
        self.cols = 9
        self.rows = 10
        self.squareLength = 30
        self.grid = []
        
        self.buttonFrame = ttk.Frame(self.mainFrame)
        self.buttonFrame.grid(column=0, row=3)
        self.playAgainBtn = ttk.Button(self.buttonFrame, text="Play", 
                                       command = self.startCentered, style="Bold.TButton")
        self.mainFrame.grid_rowconfigure(3, minsize=30, weight=1)
        self.playAgainBtn.grid(column=0, row=0)
        
        #self.aiBtn = ttk.Button(self.buttonFrame, text="Run AI", style="Bold.TButton",
        #                        command= self.startAICentered)
        self.aiBtn = ttk.Button(self.buttonFrame, text="Run AI", style="Bold.TButton",
                                command = lambda : self.startAI(1, 1))
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
        
        self.pelletPath = []
        
        #self.__debugMode()
        
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
        self.pelletPath = []
         
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
        #self.mainFrame.after(3000, self.randomAISteer)
        self.mainFrame.after(3000, self.loopAiSteer)
        
    #begins running the ai with snake starting in center space
    def startAICentered(self):
        self.startAI(self.cols//2, self.rows//2)
        
    #runs app in debug mode
    def __debugMode(self):
        print("Entering debug mode!")
        self.playAgainBtn["state"] = "disable"
        self.aiBtn["state"] = "disable"
        
        self.cols = 10
        self.rows = 10
        self.squareLength = 30
        self.grid = []
        
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
         
        '''    
        headCol = 5
        headRow = 5
        self.grid[headCol][headRow] = "X" if self.edgeSpace((headCol, headRow)) else "H"
        self.snakeCoords.append((headCol, headRow))
        '''
        
        #segCoords = [(5,4), (4,4), (4,5), (4,6), (5,6), (6,6), (7,6), (8,6), (9,6), (10,6)]
        #segCoords = []
        #segCoords = [(5,4), (4,4), (4,5), (4,6), (5,6), (6,6), (6,5)]
        #segCoords = [(5,4), (4,4), (4,5), (4,6), (5,6), (6,6), (6,5), (6,4)]
        #segCoords = [(5,6), (5,7), (5,8), (5,9), (5,10), (6,10), (6,9), (6,8), 
        #             (6,7), (6,6), (6,5), (6,4), (6,3), (6,2), (6,1)]
        
        #self.drawPellet(1, 1)
        #self.drawPellet(6, 2)
        #self.drawPellet(1, 8)
        
        #headCol = 5
        #headRow = 2
        #self.grid[headCol][headRow] = "X" if self.edgeSpace((headCol, headRow)) else "H"
        #self.snakeCoords.append((headCol, headRow))
        #segCoords = [(5,3), (4,3), (3,3), (2,3), (2,2), (2,1), (3,1), (4,1), (5,1),
        #             (6,1), (7,1), (8,1)]
        #segCoords = [(4,2), (4,3), (5,3), (6,3), (7,3), (7,2), (7,1), (6,1), (5,1)]

        self.drawPellet(6, 9)
        headCol = 7
        headRow = 9
        self.grid[headCol][headRow] = "X" if self.edgeSpace((headCol, headRow)) else "H"
        self.snakeCoords.append((headCol, headRow))
        segCoords = [(9, 9), (10, 9), (10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10), (4, 10), (4, 9), (5, 9), (5, 8), (6, 8), (6, 7), (6, 6), (7, 6), (8, 6), (8, 5), (8, 4), (7, 4), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (3, 2), (3, 3), (3, 4), (4, 4), (4, 3), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (4, 7), (4, 8), (3, 8), (2, 8), (2, 7), (3, 7), (3, 6), (3, 5), (2, 5), (2, 6), (1, 6), (1, 5), (1, 4), (2, 4), (2, 3), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (8, 3), (8, 2), (9, 2), (9, 3), (10, 3), (10, 4), (9, 4), (9, 5), (10, 5), (10, 6), (10, 7), (9, 7)]
        
        #adding segments to snake
        for i in range(len(segCoords)):
            coords = segCoords[i]
            segCol = coords[0]
            segRow = coords[1]
            self.grid[segCol][segRow] = "T" if i == len(segCoords) - 1 else "S"
            self.snakeCoords.append((segCol, segRow))
       
        self.printGrid()
        self.headXVelocity = 0
        self.headYVelocity = -1
        print(f"Snake moving {self.headDirection()}")
        neighbors = self.adjacentSpaces(self.getHeadCol(), self.getHeadRow())
        #print(f"Nearby spaces: {neighbors}")
        #print(f"Movable spaces: {self.possibleMoves()}")
        #print(f"Spaces without insta game over: {self.freeMoves()}")
        #print(f"Safe moves: {self.safeMoves()}")
        
        #connectedSpaces = self.connectedVacantSpaces(headCol, headRow)
        #print(f"Empty accesible spaces: {connectedSpaces}")
        #print(len(connectedSpaces))
        
        self.findPelletPath()
        
        '''
        startSpace = (5, 5)
        endSpace = (10, 7)
        print(f"searching for path between {startSpace} and {endSpace}")
        path = self.findPath(startSpace[0], startSpace[1], endSpace[0], endSpace[1])
        '''
        
        '''
        startSpace = (5, 5)
        targetSpaces = {(col + 1, 7) for col in range(self.cols)}
        
        #marking target spaces on grid
        for space in targetSpaces:
            self.grid[space[0]][space[1]] = "@"
        self.printGrid()
        
        print(f"searching for path between {startSpace} and targets")
        path = self.find(startSpace[0], startSpace[1], targetSpaces)
        '''
        '''
        path = self.findPelletPath()
    
        #updating grid with path
        for i in range(len(path)):
            space = path[i]
            self.grid[space[0]][space[1]] = "*"
        
        #print(f"connecting path: {path}")
        self.printGrid()
        '''
        
    #has the ai choose which direction the snake will move next
    def aiSteer(self):
        self.steering = True
        
        #deciding whether or not snake should turn
        
    #reports current movement of snake
    #returns "up", "down", "left", "right", or "none"
    def headDirection(self):
        #reporting direction of snake head
        if self.headXVelocity == 0 and self.headYVelocity == 0:
            return "none"
        elif self.headXVelocity == 0 and self.headYVelocity == 1:
            return "down"
        elif self.headXVelocity == 0 and self.headYVelocity == -1:
            return "up"
        elif self.headXVelocity == 1 and self.headYVelocity == 0:
            return "right"
        elif self.headXVelocity == -1 and self.headYVelocity == 0:
            return "left"
        else:
            print("Error. Invalid snake movement")
            return ""
        
    #obtains coordinates for a space adjacent to certain space
    #@param col - column number of space in question
    #@param row - row number of space in question
    #@param direction - string that says "up", "down", "left", or "right"
    #returns (col, row) of space above, below, left, or right of inputted space. 
    #() for bad input or no valid space in that direction
    def adjacentSpace(self, col, row, direction):
        #checking for valid col
        if not self.validColumn(col):
            print("Invalid column number")
            return ()
        
        #checking for valid row
        if not self.validRow(row):
            print("Invalid row number")
            return ()
        
        xChange = 0
        yChange = 0
        
        #finding the target space based on direction
        if direction == "up":
            yChange = -1
        elif direction == "down":
            yChange = 1
        elif direction == "left":
            xChange = -1
        elif direction == "right":
            xChange = 1
        else:
            print("Error. Invalid direction parameter.")
            return ()
        
        spaceCol = col + xChange
        spaceRow = row + yChange
        return (spaceCol, spaceRow) if self.validCoords(spaceCol, spaceRow) else ()
    
    #finds spaces adjacent to a certain space
    #@param col - column number of space in question
    #@param row - row number of space in question
    #returns spaces left, right, above, and below inputted space that are within grid
    def adjacentSpaces(self, col, row):
        #checking for valid column
        if not self.validColumn(col):
            print("Invalid column number")
            return []
        
        #checking for valid row
        if not self.validRow(row):
            print("Invalid row number")
            return []
        
        directions = ["up", "right", "left", "down"]
        neighbors = []
        
        #recording neighbors that are valid spaces
        for direction in directions:
            coords = self.adjacentSpace(col, row, direction)
            
            #found valid space
            if self.validSpace(coords):
                neighbors.append(coords)
        
        return neighbors
    
    #finds spaces up, down, left, and right of head space that are within grid
    #returns list of space coordinates
    def headAdjacentSpaces(self):
        return self.adjacentSpaces(self.getHeadCol(), self.getHeadRow())
    
    #checks if a space's column number is valid
    #@param col - column number
    #returns true if possible for space to exist at that column
    def validColumn(self, col):
        return 0 <= col and col <= self.cols + 1
    
    #checks if a space's row number is valid
    #@param row - row number
    #returns true if possible for space to exist at that row
    def validRow(self, row):
        return 0 <= row and row <= self.rows + 1
    
    #checks if a pair of coordinates describes a valid space
    #@param col - column number
    #@param row - row number
    #returns true if there exists space in game area
    def validCoords(self, col, row):
        return self.validColumn(col) and self.validRow(row)
    
    #checks if a space is valid
    #@param coords - tuple of the space's (col, row)
    #returns true if coords describes space in grid
    def validSpace(self, coords):
        return len(coords) == 2 and self.validCoords(coords[0], coords[1])
    
    #checks if a col is at the very edge of the grid
    #@param col - column number
    #returns true if col is at grid edge that would result in game over
    def edgeCol(self, col):
        #checking that column number is valid
        if not self.validColumn(col):
            print("invalid column input")
            return False
        
        return col == 0 or col == self.cols + 1
    
    #checks if a row is at the very edge of the grid that results in game over
    #@param row - row number
    #returns true if row is at grid edge that would result in game over
    def edgeRow(self, row):
        #checking that row number is valid
        if not self.validRow(row):
            print("invalid row input")
            return False
        
        return row == 0 or row == self.rows + 1
    
    #checks if space is at very edge of grid
    #@param space - pair of space coordinates
    #returns true if space is at edge of grid where game over would occur
    def edgeSpace(self, space):
        #checking for valid space
        if not self.validSpace(space):
            print("Invalid space input")
            return False
        
        return self.edgeCol(space[0]) or self.edgeRow(space[1])
    
    #finds the shortest uninterrupted path between 2 spaces, if it exists
    #@param col1 - column number of first space
    #@param row1 - row number of first space
    #@param col2 - column number of second space
    #@param row2 - row number of second space
    #@param excludedSpaces - set of space coordinates that are not allowed in middle of path
    #returns list of coordinates for shortest path connecting spaces. if no path exists, returns empty list.
    #endpoints of path can contain any symbols, but middle portions can't contain snake or wall
    def findPath(self, col1, row1, col2, row2, excludedSpaces={}):
        return self.findSubgraphPath(col1, row1, {(col2, row2)}, excludedSpaces)
    
    #finds shortest path from a certain space to a collection of spaces
    #@param col - column number of space in question
    #@param row - row number of space in question
    #@param subgraph - set of space coordinates
    #@param excludedSpaces - set of space coordinates that are not allowed make up middle of path 
    #returns shortest uninteruppted path from inputted space to any of the spaces in subgraph
    #if nonempty list returned, it is a path with no snake, wall, or pellet spaces 
    #aside from those at endpoints and subgraph spaces
    def findSubgraphPath(self, col, row, subgraph, excludedSpaces={}):
        #ensuring valid column number
        if not self.validColumn(col):
            print("invalid column input")
            return []
        #ensuring valid row number
        if not self.validRow(row):
            print("invalid row input")
            return []
        
        startSpaceID = self.spaceID(col, row)
        targetSpaceIDs = {self.spaceID(coords[0], coords[1]) for coords in subgraph}
        
        #maps a space's id to the id of its parent space in bfs
        spaceParents = {startSpaceID: 0}
        nextNodes = Queue(maxsize=(self.cols+2)*(self.rows+2))
        nextNodes.put_nowait(startSpaceID)
        finalSpaceID = 0
        
        #visiting nodes one by one until target space found
        while not nextNodes.empty():
            nodeID = nextNodes.get_nowait()
            nodeCoords = self.spaceCoords(nodeID)
            #print(f"visiting space {nodeCoords}")
            
            #found member of subgraph!
            if nodeID in targetSpaceIDs:
                finalSpaceID = nodeID
                break    
            
            nodeCol = nodeCoords[0]
            nodeRow = nodeCoords[1]
            symbol = self.grid[nodeCol][nodeRow]
            
            #checking if space has neighbors worth exploring
            if nodeID == startSpaceID or (symbol == "o" and nodeCoords not in excludedSpaces):    
                nearbySpaces = self.adjacentSpaces(nodeCol, nodeRow)
                #print(f"neighbors: {nearbySpaces}")
            
                #recording adjacent spaces for later visit
                for spaceCoords in nearbySpaces:
                    spaceCol = spaceCoords[0]
                    spaceRow = spaceCoords[1]
                    spaceID = self.spaceID(spaceCol, spaceRow)
                
                    #space not yet visited. adding to queue.
                    if spaceID not in spaceParents:
                        spaceParents[spaceID] = nodeID
                        nextNodes.put_nowait(spaceID)  
        
        path = []
        spaceID = finalSpaceID
        
        #creating path to target space
        while spaceID in spaceParents:
            coords = self.spaceCoords(spaceID)
            path.insert(0, coords)
            spaceID = spaceParents[spaceID]
        
        return path
    
    #checks if there exists a path between a space and subgraph
    #@param col - column number of space in question
    #@param row - row number of space in question
    #@param subgraph - set of space coordinates forming subgraph
    #returns true if there exists at least one uninterrupted path between space and
    # any space in the subgraph. path is uninterruped if it has no pellet, snake, or wall
    # in it except for endpoints
    def pathExists(self, col, row, subgraph):
        return len(self.findSubgraphPath(col, row, subgraph)) > 0
    
    #finds all vacant spaces reachable from a certain space
    #@param col - column number of space in question
    #@param row - row number of space in question
    #@discovered - set of vacant spaces discovered by previous iteration of function
    #returns set of all spaces reachable from inputted space using paths containing
    # no pellets, snake, or wall. set excludes inputted space
    def connectedVacantSpaces(self, col, row, discovered=set()):
        neighbors = self.adjacentSpaces(col, row)
        
        #exploring neighboring spaces
        for space in neighbors:
            symbol = self.grid[space[0]][space[1]]
            
            #found an empty space!
            if symbol == "o" and space not in discovered:
                discovered.add(space)
                self.connectedVacantSpaces(space[0], space[1], discovered)
                
        return discovered
    
    #finds spaces that head can move to on next turn
    #returns list of adjacent spaces head can move to, regardless of if they result in game over
    def possibleMoves(self):
        #head can't move if game over
        if self.grid[self.getHeadCol()][self.getHeadRow()] == "X":
            return []
        
        neighbors = self.adjacentSpaces(self.getHeadCol(), self.getHeadRow())
        destinations = []
        
        #finding spaces head can move to
        for space in neighbors:
            col = space[0]
            row = space[1]
            xChange = col - self.getHeadCol()
            yChange = row - self.getHeadRow()
            
            #snake can' make 180 degree turn
            if self.headXVelocity != 0 and xChange == -self.headXVelocity:
                continue
            if self.headYVelocity != 0 and yChange == - self.headYVelocity:
                continue
                
            destinations.append(space)
            
        return destinations
    
    #finds spaces that head can move to on next turn without immediate game over
    #returns list of adjacent spaces that do not result in immediate game over
    def freeMoves(self):
        neighbors = self.possibleMoves()
        occupiedSymbols = {"#", "H", "S"}
        return [space for space in neighbors if self.grid[space[0]][space[1]] not in occupiedSymbols]
    
    #determines which nearby spaces are safe for head to travel to next
    #returns list of adjacent spaces snake can travel to without inevitable game over
    def safeMoves(self):
        neighbors = self.freeMoves()
        safeMoves = []
        tailAccessibleSpaces = {self.getTailCoords()}
        pelletTailPath = self.findPath(self.pelletCol, self.pelletRow, self.getTailCol(), self.getTailRow())
        
        #adding path from pellet to tail as subgraph if it exists
        if len(pelletTailPath) > 0:
            tailAccessibleSpaces = set(pelletTailPath)
        
        #adding penultimate segment as future tail location, if it exists
        if len(self.snakeCoords) > 1:
            tailAccessibleSpaces.add(self.snakeCoords[-2])
        
        #print(f"tail accessible spaces: {tailAccessibleSpaces}")
        
        #deducing spaces that can be safely entered
        for coords in neighbors:
            col = coords[0]
            row = coords[1]
            
            #skipping space if it contains a pellet and no pellet to tail path exists
            if self.grid[col][row] == "P" and len(pelletTailPath) == 0:
                continue
            
            tailPath = self.findSubgraphPath(col, row, tailAccessibleSpaces)
            
            #space is safe!
            if len(tailPath) > 0:
                safeMoves.append(coords)
                tailAccessibleSpaces = tailAccessibleSpaces.union(tailPath)
             
        return safeMoves
        
    #finds a path from the head to the pellet that will avoid endangering the snake along the way
    #updates self.pelletPath with list of space coords of path found.
    def findPelletPath(self):
        spaces = self.freeMoves()
        path1 = self.findPath(self.getTailCol(), self.getTailRow(), self.pelletCol, self.pelletRow)
        #print("tail to pellet path:")
        #print(path1)
        
        #found no path between pellet and tail
        if len(path1) == 0:
            return []
        
        forbiddenMoves = set(self.headAdjacentSpaces()).difference(set(self.possibleMoves()))
        badSpaces = forbiddenMoves.union(set(path1))
        path2 = self.findPath(self.pelletCol, self.pelletRow, self.getHeadCol(), self.getHeadRow(), badSpaces)
        #print("head to pellet path:")
        #print(path2)
        
        #found no path between head and pellet
        if len(path2) == 0:
            return []
        
        '''
        gridCopy = self.getGrid()
        specialSpaces = {"T", "P", "H"}
        
        #copying paths to grid copy
        for space in path1:
            col = space[0]
            row = space[1]
            symbol = gridCopy[col][row]
            #replacing space with path symbol
            if symbol not in specialSpaces: 
                gridCopy[col][row] = "@"
            
        for space in path2:
            col = space[0]
            row = space[1]
            symbol = gridCopy[col][row]
            #replacing space with path symbol
            if symbol not in specialSpaces: 
                gridCopy[col][row] = "*"
            
        printMatrix(gridCopy)
        '''
        
        path2.pop()
        path2.reverse()
        return path2
    
    #has ai move snake in random direction
    def randomAISteer(self):
        print("random steer!")
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
            
    #has the ai move snake to space that will avoid resulting in inevitable game over
    #chooses random space if all options will result in a loss
    def surviveAISteer(self):
        goodSpaces = self.safeMoves()
        
        #no safe spaces found. choosing random move
        if len(goodSpaces) == 0:
            print("no safe moves found :(")
            self.randomAISteer()
            return
        print("Survive steer!")
        
        space = randomElement(goodSpaces)
        xVelocity = space[0] - self.getHeadCol()
        yVelocity = space[1] - self.getHeadRow()
        
        #selecting arrow key direction that leads to chosen space
        self.steerSnake(xVelocity, yVelocity)
            
    #has the ai choose next space snake will visit based on what's sensible
    #chooses random space if all available moves will result in a loss
    def smartAISteer(self):
        space = ()
        
        #path to pellet not yet charted out
        if len(self.pelletPath) == 0:
            self.pelletPath = self.findPelletPath()
            
            #no path found
            if len(self.pelletPath) == 0:
                self.surviveAISteer()
                return
         
        print("Smart steer!")
        space = self.pelletPath[0]
        self.pelletPath.pop(0)
            
        xVelocity = space[0] - self.getHeadCol()
        yVelocity = space[1] - self.getHeadRow()
        self.steerSnake(xVelocity, yVelocity)
                    
    #moves snake a space to allow it to move in loop that covers most of game area
    def loopAiSteer(self):
        velocities = ()
    
        #steer snake based on grid dimensions
        if self.rows == 2 or self.cols == 2:
            velocities = self.rectLoopDirection()
        elif self.cols*self.rows % 2 == 0:
            velocities = self.combLoopAIDirection()
        else:
            self.randomAISteer()
            return
        
        self.steerSnake(velocities[0], velocities[1])
                
    #finds direction that helps snake move in rectangle shape spanning board edges
    #returns tuple of form (xVelocity, yVelocity) of where snake should go next
    def rectLoopDirection(self):
        col = self.getHeadCol()
        row = self.getHeadRow()
        xVelocity = 0
        yVelocity = 0
        
        #moving snake based on edges of board
        if col == self.cols and row < self.rows:
            yVelocity = 1
        elif row == 1 and col < self.cols:
            xVelocity = 1
        elif col == 1 and row > 1:
            yVelocity = -1
        else:
            xVelocity = -1
            
        return (xVelocity, yVelocity)
            
    #steers snake in direction that forms comb shaped loop spanning board
    #returns tuple of form (xVelocity, yVelocity) that point to where snake should go next
    def combLoopAIDirection(self):
        col = 0
        row = 0
        cols = 0
        rows = 0
        
        #checking if even number of columns
        if self.cols % 2 == 0:
            col = self.getHeadCol()
            row = self.getHeadRow()
            cols = self.cols
            rows = self.rows
            return self.__combLoopHelper(col, row, cols, rows)
        else:
            col = self.getHeadRow()
            row = self.cols - self.getHeadCol() + 1
            cols = self.rows
            rows = self.cols
            
            velocities = self.__combLoopHelper(col, row, cols, rows)
            x = velocities[0]
            y = velocities[1]
            return (-y, x)
            
    #helper function for comb loop function
    #@param col - head's column number
    #@param row - head's row number
    #@param cols - number of columns in grid
    #@param rows - number of rows in grid
    #returns tuple representing (xVelocity, yVelocity) for where snake should move next
    def __combLoopHelper(self, col, row, cols, rows):
        xVelocity = 0
        yVelocity = 0
        
        #movement for top of screen
        if row == 1:
            #top left corner
            if col == cols:
                yVelocity = 1
            else:
                xVelocity = 1
        #movement in column numbers with same parity as far right column num
        elif col % 2 == cols % 2:
            #bottom row
            if row == rows:
                xVelocity = -1
            else:
                yVelocity = 1   
        else:
            #rows beneath top two rows
            if row > 2:
                yVelocity = -1
                
            #2nd row from the top
            if row == 2:
                #there exists a column to the left to enter
                if col > 1:
                    xVelocity = -1
                else:
                    yVelocity = -1
        return (xVelocity, yVelocity)
    
    #obtains id number assigned to a specific space on the grid
    #@param col - column number
    #@param row - row number
    #returns int corresponding to that space. returns -1 for invalid input.
    def spaceID(self, col, row):
        #ensuring valid col number
        if not self.validColumn(col):
            print("invalid column number")
            return -1
        #ensuring valid row number
        if not self.validRow(row):
            print("invalid row number")
            return -1
        
        #non-edge space
        if not self.edgeSpace((col, row)):
            return (row - 1)*self.cols + col
       
        #calculating id for edge spaces
        #edges are numbered -1 to -(numEdgeSpaces) with upper left -1 and numbering clockwise
        if row == 0:
            return -(col + 1)
        elif col == self.cols + 1:
            upperRightID = self.spaceID(self.cols + 1, 0)
            return upperRightID - row
        elif row == self.rows + 1:
            lowerRightID = self.spaceID(self.cols + 1, self.rows + 1)
            return lowerRightID - (self.cols + 1 - col)
        else:
            lowerLeftID = self.spaceID(0, self.rows + 1)
            return lowerLeftID - (self.rows + 1 - row)
        
    #checks if a spaceID is valid
    #@param spaceID - integer space id
    #returns true if there's a space in grid with that id
    def validSpaceID(self, spaceID):
        #space in middle of grid
        if 1 <= spaceID and spaceID <= self.cols*self.rows:
            return True
        
        edgeSpaces = 2*(self.cols + 1) + 2*(self.rows + 1)
        
        #space on edge of grid
        if -edgeSpaces <= spaceID and spaceID <= -1:
            return True
        
        return False
    
    #obtains coordinates for space of a certain id
    #@param spaceID - positive integer id of space
    #returns coordinates in form (col, row). returns () for invalid id
    def spaceCoords(self, spaceID):
        #ensuring valid id
        if not self.validSpaceID(spaceID):
            print("invalid space id")
            return ()
        
        #not edge space
        if spaceID > 0:
            col = (spaceID - 1)%self.cols + 1
            row = (spaceID - 1)//self.cols + 1 
            return (col, row)
        
        absoluteID = abs(spaceID)
        
        #dealing with edge space ids
        if 1 <= absoluteID and absoluteID <= self.cols + 2:
            return (absoluteID - 1, 0)
        elif absoluteID <= self.cols + 2 + self.rows + 1:
            return (self.cols + 1, absoluteID - (self.rows + 2))
        elif absoluteID <= 2*(self.cols + 2) + self.rows:
            absBottomLeftID = 2*(self.cols + 2) + self.rows
            return (absBottomLeftID - absoluteID, self.rows + 1)
        else:
            absBottomLeftID = 2*(self.cols + 2) + self.rows
            magicNum = absoluteID - absBottomLeftID
            return (0, self.rows + 1 - magicNum)
    
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
        
    #counts segments in snake
    #returns numbers of squares making up snake
    def snakeLength(self):
        return len(self.snakeCoords)
    
    #gets coordinates of head square
    #returns coordinates in form (col, row). if head doesn't exist returns empty tuple.
    def getHeadCoords(self):
        return self.snakeCoords[0] if self.snakeLength() > 0 else ()
    
    #gets column snake head is in
    #returns grid column number of head. if no head returns -1
    def getHeadCol(self):
        return self.getHeadCoords()[0] if self.snakeLength() > 0 else -1
    
    #gets row snake head is in
    #return grid row number of head
    def getHeadRow(self):
        return self.getHeadCoords()[1] if self.snakeLength() > 0 else -1
    
    #obtains head square
    #returns reference to head unit square. if none returns None
    def getHead(self):
        return self.snakeSquares[0] if self.snakeLength() > 0 else None
    
    #obtains tail square
    #returns reference to tail unit square
    def getTail(self):
        return self.snakeSquares[-1] if self.snakeLength() > 0 else None
    
    #obtains tail coordinates
    #returns tail grid coordinates as (col, row). if no tail returns empty tuple
    def getTailCoords(self):
        return self.snakeCoords[-1] if self.snakeLength() > 0 else ()
    
    #obtains tail column
    #returns tail grid column number. if no tail returns -1
    def getTailCol(self):
        return self.getTailCoords()[0] if self.snakeLength() > 0 else -1
    
    #obatins tail row
    #returns tail grid row number. if no tail returns -1
    def getTailRow(self):
        return self.getTailCoords()[1] if self.snakeLength() > 0 else -1
    
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
                
        pelletCoords = randomElement(emptySpaces)
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
            
    #steers snake based on velocities inputed. snake can't make 180 degree turn
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
            #self.randomAISteer()
            #self.surviveAISteer()
            #self.smartAISteer()
            self.loopAiSteer()
        
        self.moveSnake()
        self.steering = True
        
        #returning arrow key movement for player control
        if not self.aiMode:
            self.bindArrowKeys()
          
        #game over if snake touches edge or itself
        if self.grid[self.getHeadCol()][self.getHeadRow()] == "X":
            self.gameOver()
            self.printGrid()
            print("\n")
            return
        
        #checking if game has been won
        if len(self.snakeSquares) == self.cols*self.rows:
            self.win()
            self.printGrid()
            print("\n")
            return
        
        #drawing extra pellet if needed
        if self.pellet == None:
            self.drawPelletRandom()
           # return
           
        #printing grid if there was a change in snake's position
        if prevHeadCol != self.getHeadCol() or prevHeadRow != self.getHeadRow():
            self.printGrid()
            print("\n")
        
        #milliseconds = 1000
        milliseconds = 100
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
            #print("replacing head with rectangle")
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
        printMatrix(self.grid)
        
    #obtains a copy of the game grid
    #returns 2d array of game grid. Edges of grid represent out of bounds game over zones
    def getGrid(self):
        return [[self.grid[x][y] for y in range(self.rows+2)] for x in range(self.cols+2)]