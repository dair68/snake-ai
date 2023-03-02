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
from collections import deque

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
        print("Error. Empty list inputted.")
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
        
        self.cols = 10
        self.rows = 10
        #self.cols = 9
        #self.rows = 10
        #self.cols = 9
        #self.rows = 9
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
        #self.aiBtn = ttk.Button(self.buttonFrame, text="Run AI", style="Bold.TButton",
        #                        command = lambda : self.startAI(2, 1))
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
        self.snakeSquares = deque()
        self.snakeCoords = deque()
        self.prevTailCol = -1
        self.prevTailRow = -1
        
        self.gameStarted = False
        self.aiMode = False
        self.steering = False
        
        self.pelletPath = deque()
        self.postPelletPath = deque()
        self.loopMoves = 0
        self.swirlNeighbors = {}
        self.borderIDs = set()
        
        self.__debugMode()
        
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
        
        self.grid = self.blankGrid()
        self.grid[col][row] = "H"
        self.snakeCoords = deque([(col, row)])
        #print(self.snakeCoords)
        
        self.canvas.delete("all")
        self.canvas.focus_set()
        self.playAgainBtn.grid_remove()
        self.aiBtn.grid_remove()
        
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
        self.pelletPath = deque()
        self.postPelletPath = deque()
        self.loopMoves = 0
        self.__createSwirlNeighborsMap("loose")
        self.borderIDs = self.getBorderIDs()
         
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
        self.steering = True
        self.mainFrame.after(3000, self.runTurn)
        
    #begins running the ai with snake starting in center space
    def startAICentered(self):
        self.startAI(self.cols//2, self.rows//2)
        
    #creates set of ints representing ids of all border spaces that don't result in game over
    #returns set of border ids
    def getBorderIDs(self):
        ids = set()
        
        #creating set of edge ids
        for col in range(1, self.cols+1):
            for row in range(1, self.rows+1):
                space = (col, row)
                
                #found edge space
                if col == 1 or col == self.cols or row == 1 or row == self.rows:
                    ids.add(self.spaceID(col, row))
                    
        return ids
        
    #runs app in debug mode
    def __debugMode(self):
        print("Entering debug mode!")
        self.playAgainBtn["state"] = "disable"
        self.aiBtn["state"] = "disable"
        
        self.cols = 7
        self.rows = 8
        self.squareLength = 30
        self.grid = self.blankGrid()
        
        #segments = deque([(2,1), (2,2), (2,3)])
        segments = deque([(2,1)])
        self.__buildSnake(segments)
        
        print(f"snake: {segments}")
        self.printGrid()
        self.__createSwirlNeighborsMap("loose")
        
        pathPart = deque(segments)
        pathPart.reverse()
        print(f"pathPart: {pathPart}")
        path = self.findHamiltonianCycle(pathPart)
        #path = self.__loopGridHelper(segs)
        #path = self.findLoopSpanningGrid()
        print(f"path: {path}")
        
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
    #returns coords of spaces left, right, above, and below inputted space, 
    #including ones that cause out of bounds game over
    def adjacentSpaceCoords(self, col, row):
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
    
    #finds spaces adjacent to a certain space
    #@param spaceID - spaceID of space for which adjacent neighbors are to be found
    #returns ids of spaces left, right, above, and below inputted space, 
    #including ones that cause out of bounds game over
    def adjacentSpaceIDs(self, spaceID):
        coords = self.spaceCoords(spaceID)
        (col, row) = coords
        spaces = self.adjacentSpaceCoords(col, row)
        return [self.spaceID(x, y) for (x, y) in spaces]
    
    #obtains all spaces next to given space that do not create over of bounds game over
    #@param col - column number
    #@param row - row number
    #returns list of all spaces next to inputted space that don't create out of bounds game over
    def adjacentInboundSpaces(self, col, row):
        spaces = []
        
        #evaluating nearby spaces
        for s in self.adjacentSpaceCoords(col, row):
            (x, y) = s
            
            #found a space within bounds
            if self.spaceInBounds(x, y):
                spaces.append(s)
            
        return spaces
    
    #figures out how two adjacent spaces are positioned relative to each other
    #@param space1Coords - space coords for first space
    #@param space2Coords - space coords for second space
    #returns "up", "down", "left", "right" or "none" to describe how to go from space1 to space2
    def adjacentSpaceDirection(self, space1Coords, space2Coords):
        (col1, row1) = space1Coords
        (col2, row2) = space2Coords
        
        #checking if space1 has valid coordinates
        if not self.validCoords(col1, row1):
            print("Error. Invalid value for space1Coords.")
            print(f"space1Coords {space1Coords}")
            
        #checking if space2 has valid coordinates
        if not self.validCoords(col2, row2):
            print("Error. Invalid value for space2Coords.")
            print(f"space2Coords {space2Coords}")
            
        xChange = col2 - col1
        yChange = row2 - row1
            
        #determining direction of space2 relative to space1
        if xChange == 1 and yChange == 0:
            return "right"
        elif xChange == -1 and yChange == 0:
            return "left"
        elif xChange == 0 and yChange == 1:
            return "down"
        elif xChange == 0 and yChange == -1:
            return "up"
        else :
            return "none"
        
    #converts a cardinal direction into a character symbol
    #@param direction - string of form "up", "down", "left", and "right"
    #returns "^" for "up", "v" for "down", "<" for "left", and ">" for "right", "" otherwise
    def directionSymbol(self, direction):
        #determining symbol based on direction string
        if direction == "up":
            return "^"
        elif direction == "down":
            return "v"
        elif direction == "left":
            return "<"
        elif direction == "right":
            return ">"
        else:
            return ""
    
    #finds spaces up, down, left, and right of head space that are within grid
    #returns list of space coordinates. may include game over edge spaces
    def headAdjacentSpaces(self):
        return self.adjacentSpaceCoords(self.getHeadCol(), self.getHeadRow())
    
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
    #returns true if coords describes space in grid, including game over edge spaces
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
    def gameOverEdgeSpace(self, space):
        #checking for valid space
        if not self.validSpace(space):
            print("Invalid space input")
            return False
        
        return self.edgeCol(space[0]) or self.edgeRow(space[1])
    
    #checks if a space is at the corner of grid
    #@param spaceCoords - pair of space coordinates
    #returns true if space is at corner of grid within area that wouldn't trigger
    #   out of bounds game over
    def isCornerSpace(self, spaceCoords):
        (col, row) = spaceCoords
        
        #checking if valid coordinates
        if not self.validCoords(col, row):
            print("Invalid space coordinates inputted.")
            return False
        
        #checking if space is at corner of grid
        if spaceCoords == (1,1):
            return True  
        elif spaceCoords == (1, self.rows):
            return True 
        elif spaceCoords == (self.cols, 1):
            return True 
        elif spaceCoords == (self.cols, self.rows):
            return True 
        else:
            return False
    
    #checks if space is in bounds of snake crawlspace
    #@param col - column number
    #@param row - row number
    #returns true if space within area that would not cause out of bounds game over
    def spaceInBounds(self, col, row):
        return 1 <= col and col <= self.cols and 1 <= row and row <= self.rows 
    
    #finds the shortest uninterrupted path between 2 spaces, if it exists
    #@param firstSpaceID - id number of first space
    #@param secondSpaceID - id number of second space
    #@params options - keyword arguments for optional parameters
    #   options[neighbors] - dictionary mapping space ids to neighboring space ids for directed graphs
    #   options[excludedSpaces] - set of space coordinates that are not allowed in middle of path
    #   options[snakeSeg] - deque of space coordinates making up snake
    #   options[pelletID] - id of pellet space
    #   options[snakeMove] - bool indicating whether path should account for snake movement, 
    #                           moving snake 1 space per path tile and possibly lengthened snake
    #                       after eating pellet
    #returns list of coordinates for shortest path connecting spaces. if no path exists, returns empty list.
    #endpoints of path can contain any symbols, but middle portions can't contain snake or wall
    def findPath(self, firstSpaceID, secondSpaceID, **options):
        return self.findSubgraphPath(firstSpaceID, {secondSpaceID}, **options)
    
    #finds shortest path from a certain space to a collection of spaces
    #@param spaceID - id number of start space
    #@param subgraphIDs - set of space ids
    #@param options - keyword arguments for the following optional parameters:
    #   options[neighbors] - dictionary mapping space ids to neighboring space ids for directed graphs
    #   options[excludedSpaces] - set of space coordinates that are not allowed make up middle of path 
    #   options[snakeSeg] - deque of space coordinates making up snake
    #   options[pelletID] - id of pellet space
    #   options[snakeMove] - bool indicating whether path should account for snake movement, 
    #                       moving snake 1 space per path tile and possibly lengthened snake
    #                       after eating pellet
    #returns shortest uninteruppted path from inputted space to any of the spaces in subgraph
    #if nonempty deque returned, it is a path with no snake spaces or game over edges
    #aside from those at endpoints and subgraph spaces
    def findSubgraphPath(self, spaceID, subgraphIDs, **options):
        space = self.spaceCoords(spaceID)
        (col, row) = space
        
        #ensuring valid column number
        if not self.validColumn(col):
            print("invalid column input")
            return deque()
        #ensuring valid row number
        if not self.validRow(row):
            print("invalid row input")
            return deque()
        
        #print(f"options: {options}")
        snakeSeg = deque(options.get("snakeSeg", self.snakeCoords))
        #print(f"snakeSeg: {snakeSeg}")
        grid = self.createGrid(snakeSeg)
        pelletID = options.get("pelletID", self.getPelletID())
        (pelletCol, pelletRow) = self.spaceCoords(pelletID)
        grid[pelletCol][pelletRow] = "P"
        startSpaceID = self.spaceID(col, row)
        
        #maps a space's id to the id of its parent space in bfs
        spaceParents = {startSpaceID: 0}
        nodeDist = {startSpaceID: 0}
        nextNodes = Queue(maxsize=(self.cols+2)*(self.rows+2))
        nextNodes.put_nowait(startSpaceID)
        currentDist = 0
        finalSpaceID = 0
        
        #visiting nodes one by one until target space found
        while not nextNodes.empty():
            nodeID = nextNodes.get_nowait()
            nodeCoords = self.spaceCoords(nodeID)
            #print(f"visiting node {nodeID}")
            #print(f"visiting space {nodeCoords}")
            
            #updating distance from start node
            if nodeDist[nodeID] > currentDist:
                currentDist = nodeDist[nodeID]
                #print(f"now at radius {currentDist}")
                move = options.get("snakeMove")
                
                #shifting snake by one
                if move == True and len(snakeSeg) > 0:
                    #print("shifting snake 1 space")
                    tailCoords = snakeSeg[-1]
                    (tailCol, tailRow) = tailCoords
                    grid[tailCol][tailRow] = "X" if len(snakeSeg) == 2 else "o"
                    snakeSeg.pop()
                    #print(f"snakeSeg: {snakeSeg}")
            
            #found member of subgraph!
            if nodeID in subgraphIDs:
                finalSpaceID = nodeID
                break    
            
            (nodeCol, nodeRow) = nodeCoords
            symbol = grid[nodeCol][nodeRow]
            excludedSpaces = options.get("excludedSpaces", set())
            #print(f"excludedSpaces: {excludedSpaces}")
            #print(f"visiting {nodeCoords}")
            #print(f"symbol: {symbol}")
            goodSpaces = {"o", "P"}
            
            #checking if space has neighbors worth exploring
            if nodeID == startSpaceID or (symbol in goodSpaces and nodeID not in excludedSpaces):        
                nearbySpaces = []
                
                #determining nearby spaces based on if neighbors were inputted
                if "neighbors" in options and len(options["neighbors"]) > 0:
                    neighborsMap = options["neighbors"]
                    nearbySpaces = neighborsMap[nodeID]
                else:
                    nearbySpaces = self.adjacentSpaceIDs(nodeID)
            
                #recording adjacent spaces for later visit
                for spaceID in nearbySpaces:
                    #space not yet visited. adding info
                    if spaceID not in spaceParents:
                        spaceParents[spaceID] = nodeID
                        nodeDist[spaceID] = nodeDist[nodeID] + 1
                        nextNodes.put_nowait(spaceID)  
        
        path = deque()
        spaceID = finalSpaceID
        
        #creating path to target space
        while spaceID in spaceParents:
            coords = self.spaceCoords(spaceID)
            path.appendleft(coords)
            spaceID = spaceParents[spaceID]
        
        #print(f"distances: {nodeDist}")
        #print(f"parents: {spaceParents}")
        return path
    
    #searches for a loop that covers every non-gameover grid space
    #@param pathSegs - deque of spaces coords. searches for path that starts
    #                  at element 0 goes thru pathSegs to element -1, then rest of board
    #                   optional
    #returns deque of space coords for grid spanning loop, if it exists
    def findHamiltonianCycle(self, pathSegs=None):
        #using (1,1) as pathSeg if none provided
        if pathSegs == None:
            return self.__hamiltonianHelper(deque([(1,1)]))
        else:
            return self.__hamiltonianHelper(deque(pathSegs))
    
    #helper function for self.findHamiltonianCycle(pathSegs)
    #@param pathSegs - deque of space coords making up path. will be changed in function
    #@param grid - grid representing current state of pathSegs. optional
    #returns path that covers every non-game over grid space within loop if possible
    def __hamiltonianHelper(self, pathSegs, grid=None):
        #converting pathSegs to set if needed
        if grid == None:
            grid = self.__createHamiltonianGrid(pathSegs)
            
        #analyzing paths that are as long as number of grid spaces
        if len(pathSegs) == self.cols*self.rows:
            #checking hamiltonian found
            if self.isHamiltonianCycle(pathSegs):
                direction = self.adjacentSpaceDirection(pathSegs[-1], pathSegs[0])
                symbol = self.directionSymbol(direction)
                (col, row) = pathSegs[-1]
                grid[col][row] = symbol
                self.printGrid(grid)
                return pathSegs
            else:
                return deque()

        nextSpaces = self.__possibleHamiltonianMoves(pathSegs, grid)
        
        #searching for rest of path spanning grid
        for coords in nextSpaces:   
            self.__addHamiltonianPathSeg(coords, pathSegs, grid)
            possiblePath = self.__hamiltonianHelper(pathSegs, grid)
            
            #found path!
            if len(possiblePath) > 0:
                return possiblePath
            
            self.__removeHamiltonianPathSeg(pathSegs, grid)
        
        return deque()
    
    #creates a grid representing existing hamiltonian path
    #@param pathSegs - deque of space coordinates for current path part
    #returns grid with "^", "<", ">", "v" representing directions to travel
    def __createHamiltonianGrid(self, pathSegs):
        grid = self.blankGrid()
        
        #filling grid with * representing a path segment
        for i in range(len(pathSegs)):
            space = pathSegs[i]
            (col, row) = space
            grid[col][row] = "*"
            
            #previous space exists
            if i > 0:
                prevSpace = pathSegs[i-1]
                direction = self.adjacentSpaceDirection(prevSpace, space)
                symbol = self.directionSymbol(direction)
                (prevCol, prevRow) = prevSpace
                grid[prevCol][prevRow] = symbol
                
        return grid
        
    #updates pathSegs and grid from self.__hamiltonianHelper() with a new path part
    #@param spaceCoords - spaceCoords of newest path segment to be added
    #@param pathSegs - deque of space coordinates of current path segments
    #@param grid - grid of current hamiltonian path in the making
    def __addHamiltonianPathSeg(self, spaceCoords, pathSegs, grid):
        pathSegs.append(spaceCoords)
        grid[spaceCoords[0]][spaceCoords[1]] = "*"
        #print(f"path: {pathSegs}")
        
        #checking if there's a penultimate space to update
        if len(pathSegs) >= 2:
            prevSpace = pathSegs[-2]
            direction = self.adjacentSpaceDirection(prevSpace, spaceCoords)
            grid[prevSpace[0]][prevSpace[1]] = self.directionSymbol(direction)
            
    #removes most recent space in pathSegs for self.__hamiltonianHelper() and updates grid
    #@param pathSegs - deque of space coordinates representing current hamiltonian path
    #@param grid - grid representing current path progress. updated in function
    def __removeHamiltonianPathSeg(self, pathSegs, grid):
        newestSeg = pathSegs[-1]
        (col, row) = newestSeg
        grid[col][row] = "o"
        pathSegs.pop()
        
        secondNewestSeg = pathSegs[-1]
        (col2, row2) = secondNewestSeg
        grid[col2][row2] = "*"
        
    #checks if a space in grid is surrounded by nonempty spaces
    #@param spaceCoords - space coordinates of space in question
    #@param grid - grid representing current state of game
    #returns True is space surrounded by symbols other than "o"
    def spaceSurrounded(self, spaceCoords, grid):
        (col, row) = spaceCoords
        neighbors = self.adjacentSpaceCoords(col, row)
        
        #examining neighboring spaces
        for neighbor in neighbors:
            (neighborCol, neighborRow) = neighbor
            
            #space is free
            if grid[neighborCol][neighborRow] == "o":
                return False
            
        return True
    
    #checks if next space would be a 90 degree bend if added to partial hamiltonian cycle
    #@param spaceCoords - space coordinates of possible space to be append to path 
    #@param pathSegs - deque of space coordinates for current path
    #@param grid - grid showcasing current path
    #returns True if space must be a 90 degree bend, False otherwise
    def __hamiltonianCornerSpace(self, spaceCoords, pathSegs, grid):
        neighbors = self.adjacentSpaceCoords(spaceCoords[0], spaceCoords[1])
        neighbors.remove(pathSegs[-1])
        
        inaccessibleSpaces = [s for s in neighbors if grid[s[0]][s[1]] != "o"]
        
        #must be 2 blocked spaces for corner to be possibe
        if len(inaccessibleSpaces) != 2:
            return False
        
        (blockedSpace1, blockedSpace2) = inaccessibleSpaces
        (col1, row1) = blockedSpace1
        (col2, row2) = blockedSpace2
        pathStartSpace = pathSegs[0]
        
        #checking if the blocked spaces form corner
        if col1 != col2 and row1 != row2 and pathStartSpace not in inaccessibleSpaces:
            return True
        
        return False
    
    #figures out which spaces could possibly lead to next path segment in hamiltonian cycle
    #@param pathSegs - deque of space coords making up current partial hamiltonian path
    #@param grid - grid representing current state of path
    #returns list of spaces coordinates for where path should check next
    def __possibleHamiltonianMoves(self, pathSegs, grid):
        recentSpace = pathSegs[-1]
        (col, row) = recentSpace
        neighbors = [s for s in self.adjacentInboundSpaces(col, row) if grid[s[0]][s[1]] == "o"]
        
        #searching for corner space
        for space in neighbors:
            #found corner space!
            if self.__hamiltonianCornerSpace(space, pathSegs, grid):
                return [space]
        
        filteredSpaces = list(neighbors)
        
        #seeing if any moves would leave the path end trapped
        for space in neighbors:
            (spaceCol, spaceRow) = space
            grid[spaceCol][spaceRow] = "*"
            threshold = self.cols*self.rows - 1
        
            #checking if new space would leave tail trapped
            if len(pathSegs) < threshold and self.spaceSurrounded(pathSegs[0], grid):
                #print("tail trapped!")
                filteredSpaces.remove(space)
                
            grid[spaceCol][spaceRow] = "o"
            
        return filteredSpaces
        
    #checks if a path covers every non-gameover grid space within a loop
    #@param pathSegs - deque of space coords
    #returns True if pathSegs covers every non-gameover grid space and is a loop
    def isHamiltonianCycle(self, pathSegs):
        #checking if number of segments matches number of grid spaces
        if len(pathSegs) != self.cols*self.rows:
            return False
        
        visitedSpaces = set()
        prevSpace = pathSegs[-1]
        
        #checking each space one by one
        for i in range(len(pathSegs)):
            coords = pathSegs[i]
            (col, row) = coords
            
            #checking if valid coordinates
            if not self.validCoords(col, row) or not self.spaceInBounds(col, row):
                print("Invalid coordinates found within pathSegs")
                return False
            
            #checking if space already visited
            if coords in visitedSpaces:
                return False
            
            #checking if space adjacent to previous space
            if not self.spacesAreAdjacent(prevSpace, coords):
                return False
            
            visitedSpaces.add(coords)
            prevSpace = coords
                
        return True
    
    #finds all vacant spaces reachable from a certain space
    #@param col - column number of space in question
    #@param row - row number of space in question
    #@discovered - set of vacant spaces discovered by previous iteration of function
    #returns set of all spaces reachable from inputted space using paths containing
    # no pellets, snake, or wall. set excludes inputted space
    def connectedVacantSpaces(self, col, row, discovered=set()):
        neighbors = self.adjacentSpaceCoords(col, row)
        
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
        
        neighbors = self.adjacentSpaceCoords(self.getHeadCol(), self.getHeadRow())
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
    #@param neighbors - dictionary mapping space ids to lists of space ids for neighboring nodes. for directed graphs
    #returns list of adjacent spaces snake can travel to without inevitable game over
    def safeMoves(self, neighbors=None):
        adjacent = self.freeMoves()
        safeMoves = []
        tailAccessibleSpaces = {self.getTailID()}
        pelletTailPath = deque()
        
        #finding path depending on if neighbors are needed
        if neighbors == None:
            pelletTailPath = self.findPath(self.getPelletID(), self.getTailID())
        else:
            pelletTailPath = self.findPath(self.getPelletID(), self.getTailID(), neighbors=neighbors)
        
        #adding path from pellet to tail as subgraph if it exists
        if len(pelletTailPath) > 0:
            tailAccessibleSpaces = set(self.pathIDs(pelletTailPath))
        
        #adding penultimate segment as future tail location, if it exists
        if self.snakeLength() > 1:
            penultSeg = self.snakeCoords[-2]
            tailAccessibleSpaces.add(self.spaceID(penultSeg[0], penultSeg[1]))
        
        #print(f"tail accessible spaces: {tailAccessibleSpaces}")
        
        #deducing spaces that can be safely entered
        for coords in adjacent:
            col = coords[0]
            row = coords[1]
            
            #skipping space if it contains a pellet and no pellet to tail path exists
            if self.grid[col][row] == "P" and len(pelletTailPath) == 0:
                continue
            
            spaceID = self.spaceID(col, row)
            tailPath = deque()
            
            #finding path depending on if neighbors are needed
            if neighbors == None:
                tailPath = self.findSubgraphPath(spaceID, tailAccessibleSpaces)
            else:
                tailPath = self.findSubgraphPath(spaceID, tailAccessibleSpaces, neighbors=neighbors)
            
            
            #space is safe!
            if len(tailPath) > 0:
                safeMoves.append(coords)
                tailAccessibleSpaces = tailAccessibleSpaces.union(tailPath)
                
        if self.snakeLength() == self.cols*self.rows - 1:
            pelletCoords = (self.pelletCol, self.pelletRow)
            
            #checking if pellet space near head
            if abs(self.pelletCol - self.getHeadCol()) == 1 and pelletCoords not in safeMoves:
                safeMoves.append(pelletCoords)
            elif abs(self.pelletRow - self.getHeadRow()) == 1 and pelletCoords not in safeMoves:
                safeMoves.append(pelletCoords)
             
        return safeMoves
    
    #looks for a path from snake head to tail
    #@param snakeSeg - deque of space coordinates representing snake. self.snakeCoords by default
    #returns deque of space coordinates representing path, if it exists
    #   path may go through pellets. does not return paths that require snake to
    #   move out of the way first
    def findTailPath(self, snakeSeg=None):
        #using self.snakeCoords if needed
        if snakeSeg == None:
            snakeSeg = self.snakeCoords
            
        #searching for path to tail
        path = self.findPath(self.getHeadID(snakeSeg), 
                             self.getTailID(snakeSeg),
                             snakeSeg=snakeSeg
                             )
        
        return path
    
    #checks if a path to tail exists from snake head
    #@param snakeSeg - deque of space coords representing snake. self.snakeCoords by default
    #returns True if there's a path that doesn't touch snake or go out of bounds
    def tailPathExists(self, snakeSeg=None):
        #using self.snakeCoords if needed
        if snakeSeg == None:
            snakeSeg = self.snakeCoords
            
        return len(self.findTailPath(snakeSeg)) > 0
        
    #finds a path from the head to the pellet
    #@param pelletPathNeighbors - dictionary mapping neighbors for path to adhere to
    #returns deque of space coords of path found. path may endanger snake in the future
    def findPelletPath(self, pelletPathNeighbors=None):
        n = {} if pelletPathNeighbors == None else pelletPathNeighbors
        
        return self.findPath(self.getHeadID(), 
                             self.getPelletID(), 
                             neighbors=n,
                             snakeMove=True)
    
    #finds info about a possible pellet path under certain neighbor parameters
    #@param pelletPathNeighbors - dictionary mapping neighbors for path to adhere to
    #@param tailPathNeighbors - dictionary mapping neighbors for head to tail to adhere to
    #returns dictionary of form {pelletPath: deque(), futureSnake: deque()}. path may endanger snake in future
    def findPelletPathInfo(self, pelletPathNeighbors={}, tailPathNeighbors={}):
        #print(f"head id: {self.getHeadID()}")
        path = self.findPelletPath()
        
        #found no path to pellet
        if len(path) == 0:
            return {"pelletPath": deque(), "futureSnake": deque()}
    
        #print(path1[1])
        futureSnake = deque(self.snakeCoords)
        a = path[0]
        path.popleft()
        futureSnake = self.futureSnakeCoords(futureSnake, path, self.getPelletCoords())
        #print(f"future snake3: {futureSnake}")

        path.appendleft(a)
        return {"pelletPath": path, "futureSnake": futureSnake}
    
    
    #finds a safe path to the pellet that abides by the swirl movement philosophy
    #returns list of space coords for path found with first elem being head. 
    #empty list if no path found
    def findSwirlPelletPath(self):
        return self.findPelletPath({}, self.swirlNeighbors)
    
    #finds a path to the pellet and paths that allows the snake to readjust itself afterwards
    #returns dict of form {pelletPath: deque(), tailPath: deque(), untanglePath: deque()}
    def findSafePelletPathInfo(self):
        pathInfo = self.findPelletPathInfo()
        pelletPath = pathInfo["pelletPath"]
        
        #checking if pellet path was found
        if len(pelletPath) == 0:
            return {"pelletPath": deque(), 
                    "tailPath": deque(), 
                    "untanglePath": deque(),
                    "futureSnake": deque()}
       
        tailPath = deque(pathInfo["pelletTailPath"])
        #tailPath.popleft()
        #print(f"tailPath: {tailPath}")
        snake = deque(pathInfo["futureSnake"])
        #print(f"future snake {snake}")
        testedTailSeg = deque()
        #print(f"snake: {snake}")
        
        #seeing if pellet to tail segments allow snake to reorient itself in spiral
        for k in range(len(tailPath)):
            untanglePath = self.__quickUntanglePath(snake)
            
            #found an escape route!
            if len(untanglePath) > 0:
                #print("untangle path found!")
                #print(f"path 1: {testedTailSeg}")
                #print(f"path 2: {untanglePath}")
                escapePath = testedTailSeg
                #untanglePath.popleft()
                
                #forming escape path
                for space in untanglePath:
                    escapePath.append(space)
                
                return {"pelletPath": pathInfo["pelletPath"], 
                        "tailPath": tailPath,
                        "untanglePath": escapePath,
                        "futureSnake": pathInfo["futureSnake"]}
            
            testedTailSeg.append(tailPath[0])
            tailPath.rotate(-1)
            snake.appendleft(tailPath[0])
            snake.pop()
            
        return {"pelletPath": pathInfo["pelletPath"], 
                "tailPath": tailPath,
                "untanglePath": deque(),
                "futureSnake": pathInfo["futureSnake"]}
    
    #checks if a path exists from a snake's head to tail.
                
    #sees if snake can immediately "untangle" itself into a swirl formation
    #@param snakeSeg - deque of snake coordinates of form (col, row)
    #returns deque of path snake can follow to reshape into a comb formation
    def __quickUntanglePath(self, snakeSeg):
        #print("\nrunning self.__quickUntanglePath")
        #print(f"snakeSeg: {snakeSeg}")
        currentSegs = set(snakeSeg)
        #print(f"currentSegs: {currentSegs}")
        untanglePath = deque([snakeSeg[0]])
        rotations = 0
        
        #seeing if snake can be quickly untangled
        for k in range(len(snakeSeg)):
            #print(f"snakeSeg: {snakeSeg}")
            #print(f"currentSegs: {currentSegs}")
            currentSegs.remove(snakeSeg[-1])
            (headCol, headRow) = untanglePath[-1]
            nextSpace = self.nextCombSpace(headCol, headRow)
            #print(f"next space: {nextSpace}")
            #print(f"updated currentSets: {currentSegs}")
            
            #space already recorded. snake would chomp itself if it kept going
            if nextSpace in currentSegs:
                #print("snake will chomp itself!")
                snakeSeg.rotate(-rotations)
                return deque()
            
            currentSegs.add(nextSpace)
            snakeSeg.rotate()
            rotations += 1
            untanglePath.append(nextSpace)
            
        snakeSeg.rotate(-rotations)
        return untanglePath
        
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
    def basicAISteer(self):
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
        self.pelletPath.popleft()
            
        xVelocity = space[0] - self.getHeadCol()
        yVelocity = space[1] - self.getHeadRow()
        self.steerSnake(xVelocity, yVelocity)
    
    #provides the direction the snake should move next to produce a loop
    #@param spaceCoords - tuple of form (col, row). head space by default
    #returns tuple of form (xVelocity, yVelocity)
    def loopAIDirection(self, spaceCoords=None):
        velocities = ()
        
        #using head values
        if spaceCoords == None:
            spaceCoords = self.getHeadCoords()
            
        (col, row) = spaceCoords
    
        #steer snake based on grid dimensions
        if self.rows == 2 or self.cols == 2:
            velocities = self.rectLoopDirection(col, row)
        elif self.cols % 2 == 0:
            velocities = self.__combLoopHelper(col, row, self.cols, self.rows)
        else:
            velocities = self.tongLoopDirection(spaceCoords)
            
        return velocities
                
    #moves snake a space to allow it to move in loop that covers most of game area
    def loopAiSteer(self):
        velocities = self.loopAIDirection()
        self.steerSnake(velocities[0], velocities[1])
                
    #finds direction that helps snake move in rectangle shape spanning board edges
    #@param col - column number
    #@param row - row number
    #returns tuple of form (xVelocity, yVelocity) of where snake should go next
    def rectLoopDirection(self, col, row):
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
    #@param spaceCoords - tuple of form (col, row). head space by default
    #returns tuple of form (xVelocity, yVelocity) that point to where snake should go next
    def combLoopAIDirection(self, spaceCoords=None):
        #using head
        
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
            #top right corner
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
    
    #finds space after inputted space in loop formation
    #@param col - column number
    #@param row - row number
    #returns space coords of form (col, row) after inputted space under comb loop
    def nextCombSpace(self, col, row):
        velocities = self.__combLoopHelper(col, row, self.cols, self.rows)
        (xVelocity, yVelocity) = velocities
        return (col + xVelocity, row + yVelocity)
    
    #finds space after inputted space in loop formation
    #@param col - column number
    #@param row - row number
    #returns space coords of form (col, row) after inputted space under comb loop
    def nextSwirlSpace(self, col, row):
        velocities = self.loopAIDirection((col, row))
        (xVelocity, yVelocity) = velocities
        return (col + xVelocity, row + yVelocity)
    
    #finds space before inputted space in loop formation
    #@param col - column number
    #@param row - row number
    #returns space coords of form (col, row) for space that occurs before in swirl
    def prevSwirlSpace(self, col, row):
        spaces = self.adjacentInboundSpaces(col, row)
        #print(f"adjacent inbound spaces: {spaces}")
        
        #finding previous swirl space
        for space in spaces:
            (x, y) = space
            
            #found previous swirl space
            if self.nextSwirlSpace(x, y) == (col, row):
                return space
    
    #finds space after inputted space in rectangle formation
    #@param col - column number
    #@param row - row number
    #returns space coords form (col, row) after inputted space under rect loop
    def nextRectSpace(self, col, row):
        velocities = self.rectLoopDirection(col, row)
        (xVelocity, yVelocity) = velocities
        return (col + xVelocity, row + yVelocity)
    
    #chooses direction that will allow snake to move about grid in tong shaped loop
    #@param spaceCoords - tuple of form (col, row). head space by default
    #returns tuple of (xVelocity, yVelocity) indicating how snake should move next
    def tongLoopDirection(self, spaceCoords=None):
        #using head space
        if spaceCoords == None:
            spaceCoords = self.getHeadCoords()
        
        (col, row) = spaceCoords
        xVelocity = 0
        yVelocity = 0
        
        #moving snake based on where it lies in grid
        if col > 2:
            return self.__combLoopHelper(col - 1, row, self.cols - 1, self.rows)
        elif col == 2:
            #taking care of movement for second column from left
            if row == 1:
                xVelocity = 1
            elif row % 2 == self.rows % 2:
                xVelocity = -1
            else:
                yVelocity = -1
        else:
            #taking care of movement in far left column
            if row == 1:
                xVelocity = 1
            elif row == 2:
                #choosing velocity based on number of rows
                if self.rows % 2 == 0:
                    yVelocity = -1
                else:
                    randNum = random.randrange(2)
                    
                    #randomly choosing up or right
                    if randNum == 1:
                        yVelocity = -1
                    else:
                        xVelocity = 1
            elif row % 2 == self.rows % 2:
                yVelocity = -1
            else:
                xVelocity = 1
        return (xVelocity, yVelocity)
    
    #steers the snake to gun for pellets if it's absolutely safe to do so
    #steers snake to an adjacent space for that turn.
    def safeWinAISteer(self):
        #searching for pellet path
        if len(self.pelletPath) == 0:
            self.pelletPath = self.findSafeWinPelletPath()
            
            #found a pellet path!
            if len(self.pelletPath) > 0:
                self.pelletPath.popleft()
                print("pellet path: ")
                print(self.pelletPath)
                
        #moving snake depending on if pellet path found
        if len(self.pelletPath) > 0:
            print("going down pellet path")
            self.moveDownPath(self.pelletPath)
        else:
            safeMoves = self.safeMoves()
            swirlMove = self.nextSwirlSpace(self.getHeadCol(), self.getHeadRow())
            
            #having snake go down swirl if safe, other choosing randomly
            if swirlMove in safeMoves:
                print("going down swirl path")
                self.loopAiSteer()
            else:
                print("safe move")
                self.surviveAISteer()
            
    #steers snake in direction that will allow snake to win quickly
    #steers snake to an adjacent space for that turn
    def fastWinAISteer(self):
        #searching for pellet path
        if len(self.pelletPath) == 0:
            possiblePelletPath = deque()
            escapeRoute = deque()
            
            #searching for path depending on phase of game
            if self.snakeLength() < 5:
                possiblePelletPath = self.findPelletPath()
            else:
                pathInfo = self.fastWinPelletPathInfo()
                possiblePelletPath = pathInfo["pelletPath"]
                escapeRoute = pathInfo["escapePath"]
            
            #found a pellet path!
            if len(possiblePelletPath) > 0:
                possiblePelletPath.popleft()
                self.pelletPath = possiblePelletPath
                print("pellet path: ")
                print(self.pelletPath)
                
                #trimming escape path if needed
                if len(escapeRoute) > 0:
                    escapeRoute.popleft()
                    
                self.postPelletPath = escapeRoute
                print("escape route: ")
                print(self.postPelletPath)
                
        #moving snake depending on if pellet path found
        if len(self.pelletPath) > 0:
            print("going down pellet path")
            self.moveDownPath(self.pelletPath)
        elif len(self.postPelletPath) > 0:
            print("going down escape route:")
            print(self.postPelletPath)
            self.moveDownPath(self.postPelletPath)
        else:
            possiblePath = self.longestSafeSwirlPath()
            
            #found path
            if len(possiblePath) > 0:
                self.postPelletPath = possiblePath
                self.postPelletPath.popleft()
                print(f"swirl safe path found: {possiblePath}")
                print("going down escape route:")
                self.moveDownPath(self.postPelletPath)
                return
            else:
                print("safe move")
                self.surviveAISteer()
            
    #looks for a pellet path that the snake can then escape to readopt swirl formation
    #returns dict of form {pelletPath": deque(), "futureSnake":deque(), "escapePath": deque()}
    def fastWinPelletPathInfo(self):
        pathInfo = self.findPelletPathInfo()
        futureSnake = pathInfo["futureSnake"]
        possiblePelletPath = pathInfo["pelletPath"]
        print(f"possible path: {possiblePelletPath}")
        print(f"future snake: {futureSnake}")
        
        #no path found
        if len(possiblePelletPath) == 0:
            pathInfo["escapePath"] = deque()
            return pathInfo
        
        swirlTailSpaces = self.tailAccessibleSwirlIDs(futureSnake)
        #print(f"tail swirl spaces: {swirlTailSpaces}")
        
        headSpace = futureSnake[0]
        (headCol, headRow) = headSpace
        nextSwirlSpace = self.nextSwirlSpace(headCol, headRow)
        #print(f"next swirl space: {nextSwirlSpace}")
        nextSwirlID = self.spaceID(nextSwirlSpace[0], nextSwirlSpace[1])
        #print(f"next swirl id: {nextSwirlID}")
        
        #snake can start swirling immediately
        if nextSwirlID in swirlTailSpaces:
            pathInfo["escapePath"] = deque()
            return pathInfo
       
        headID = self.spaceID(headCol, headRow)
        tailSpace = futureSnake[-1]
        tailID = self.spaceID(tailSpace[0], tailSpace[1])
        #print(f"head id: {headID}"
        
        #searching for path to swirl tail spaces
        while len(swirlTailSpaces) > 0:
            spaceID = swirlTailSpaces[-1]
            swirlTailSpaces.pop()
            remainingSpaces = set(swirlTailSpaces)
            escapePath = self.findPath(headID, 
                                       spaceID, 
                                       neighbors=self.swirlNeighbors, 
                                       excludedSpaces=remainingSpaces, 
                                       snakeSeg=futureSnake)
            
            #found escape route!
            if len(escapePath) > 0:
                pathInfo["escapePath"] = escapePath
                return pathInfo
        
        return {"pelletPath": deque(), "futureSnake": deque(), "escapePath": deque()}
    
    #finds all spaces that can reach snake's tail thru swirl path
    #@param snakeSeg - deque of snake space coords
    #returns deque of space ids that can follow swirl path to reach tail
    def tailAccessibleSwirlIDs(self, snakeSeg):
        #spaceList = []
        spaces = deque()
        snakeSegSet = set(snakeSeg)
        tailSpace = snakeSeg[-1]
        space = self.prevSwirlSpace(tailSpace[0], tailSpace[1])
        
        #finding all spaces that lead to tail under swirl formation
        while space not in snakeSegSet:
            (col, row) = space
            spaces.append(self.spaceID(col, row))
            #spaceList.append(space)
            space = self.prevSwirlSpace(space[0], space[1])
            
        #print("spaces that can reach tail thru swirl: ")
        #print(spaceList)
        return spaces
    
    #finds a swirl path from a snake's given position that won't create game over
    #@param snake - deque of space coords for snake's starting position. self.snakeCoords by default
    #@param pelletCoords - location of pellet of form (col, row). 
    #   (self.pelletCol, self.pellletRow by default
    #returns deque of space coords for path, if it exists. 
    #   path will be not longer than number of tiles in grid
    def longestSafeSwirlPath(self, snakeSegs=None, pelletCoords=None):
        #using self.snakeCoords if needed
        if snakeSegs == None:
            snakeSegs = self.snakeCoords
        
        #using (self.pelletCol, self.pelletRow) for pellet coords if needed
        if pelletCoords == None:
            pelletCoords = self.getPelletCoords()
            
        print(f"pelletCoords: {pelletCoords}")
            
        #checking if pelletCoords are valid coordinates
        if not self.validCoords(pelletCoords[0], pelletCoords[1]):
            print("Error. pelletCoords has invalid coordinates.")
            print(f"pelletCoords: {pelletCoords}")
            return deque()
        
        snakeCoords = deque(snakeSegs)
        coordSet = set(snakeCoords)
        snakeLength = len(snakeCoords)
        path = deque([snakeCoords[0]])
        
        #seeing how far the snake can go
        for k in range(self.cols*self.rows):
            head = snakeCoords[0]
            (col, row) = head
            space = self.nextSwirlSpace(col, row)
            tail = snakeCoords[-1]
            
            #next space will make snake chomp itself
            if space != tail and space in coordSet:
                return path if len(path) > 1 and self.tailPathExists(snakeCoords) else deque()
            
            #next space will have snake eat pellet
            if (col, row) == pelletCoords:
                return path if len(path) > 1 and self.tailPathExists(snakeCoords) else deque()
            
            snakeCoords = self.futureSnakeCoords(snakeCoords, deque([space]), pelletCoords)
           
            coordSet.remove(tail)
            coordSet.add(space)
            path.append(space)
        
        return path if self.tailPathExists(snakeCoords) else deque()
    
    #finds pellet path that allows snake to then resume swirl formation without issues
    #returns deque of space coords for path if it exists.
    def findSafeWinPelletPath(self):
        pathInfo = self.findPelletPathInfo()
        futureSnake = pathInfo["futureSnake"]
        possiblePelletPath = pathInfo["pelletPath"]
        print(f"possible path: {possiblePelletPath}")
        print(f"future snake: {futureSnake}")
        
        #no path found
        if len(possiblePelletPath) == 0:
            return deque()
        
        headSpace = futureSnake[0]
        space = self.nextSwirlSpace(headSpace[0], headSpace[1])
        firstSpace = space
        snakeSeg = set(futureSnake)
        
        #seeing if following swirl path leads back to tail
        while space not in futureSnake:
            (col, row) = space
            space = self.nextSwirlSpace(col, row)
          
        tailSpace = futureSnake[-1]    
          
        #found swirl path to tail!
        if space == tailSpace and firstSpace != tailSpace:
            return possiblePelletPath
            
        return deque()
    
    #checks if spaces at edge of grid are vacant
    #@param returns true if no snake parts at edge of game area right next to game over zone
    def emptyEdgeSpaces(self):
        snakeSymbols = {"H", "S", "T"}
        
        #checking top and bottom rows
        for col in range(1, self.cols + 1):
            #print(f"col: {col}")
            
            #found nonempty space
            if self.grid[col][1] in snakeSymbols:
                return False
            if self.grid[col][self.rows] in snakeSymbols:
                return False
        
        #checking left and right columns
        for row in range(1, self.rows + 1):
            #found nonempty space
            if self.grid[1][row] in snakeSymbols:
                return False
            if self.grid[self.cols][row] in snakeSymbols:
                return False
        
        return True
    
    #moves snake one space down inputted path
    #@param path - deque of space coordinates
    #shifts snake down leftmost space in path. will popleft() path in process
    def moveDownPath(self, path):
        #path has no spaces
        if len(path) == 0:
            print("Error. Path has length of 0.")
            return
    
        space = path[0]
        xVelocity = space[0] - self.getHeadCol()
        yVelocity = space[1] - self.getHeadRow()
        self.steerSnake(xVelocity, yVelocity)
        path.popleft()
        
    #updates self.pelletPath with a path if a better one exists
    def __updatePelletPath(self):
        possiblePelletPath = self.findPelletPath()
        
        #updating pellet path if needed
        if len(possiblePelletPath) > 0:
            #updating pellet path
            if len(self.pelletPath) == 0 or len(possiblePelletPath) < len(self.pelletPath):
                possiblePelletPath.popleft()
                self.pelletPath = possiblePelletPath
                print("updating pellet path")
                print(f"pellet path: {self.pelletPath}")
        
    #checks if there is enough room for snake to travel rectangle path
    #returns true if there is enough room for snake to go down rectangle route with entirety of body
    def __rectTraversable(self):
        return len(self.__rectUnwindPath()) > 0
        
    #finds path that lets snake unwind in a rectangle formation
    #returns deque of space coords for path found. empty deque if no path found
    def __rectUnwindPath(self):
        #print(self.getHeadID())
        #print(self.borderIDs)
        borderPath = self.findSubgraphPath(self.getHeadID(), self.borderIDs)
        #print(f"border path: {borderPath}")
        
        #no edge path found
        if len(borderPath) == 0:
            return deque()
        
        borderPath.popleft()
        futureSnake1 = self.futureSnakeCoords(self.snakeCoords, borderPath)
        #print(f"futureSnake1: {futureSnake1}")
        
        #border path exceeds snake length. snake is safe
        if len(borderPath) >= self.snakeLength():
            return borderPath
        
        rectPath = deque()
        pathSeg = futureSnake1[0]
        
        #forming rectangle path
        for k in range(self.snakeLength() - len(borderPath)):
            (col, row) = pathSeg
            nextSeg = self.nextRectSpace(col, row)
            rectPath.append(nextSeg)
            pathSeg = nextSeg
            
        #print(f"rectPath: {rectPath}")
        futureSnake2 = self.futureSnakeCoords(futureSnake1, rectPath)
        #print(f"futureSnake2: {futureSnake2}")
        
        #snake is able to go down path without chomping itself
        if futureSnake2[0] == rectPath[-1]:
            borderPath.extend(rectPath)
            return borderPath
        
        return deque()
        
    #finds path that allows snake to unwind in swirl formation if possible
    #returns deque of space coords for path found. empty deque if no path found
    def __swirlUnwindPath(self):
        swirlPath = deque()
        pathSeg = self.getHeadCoords()
        
        #forming rectangle path
        for k in range(self.snakeLength()):
            (col, row) = pathSeg
            nextSeg = self.nextSwirlSpace(col, row)
            swirlPath.append(nextSeg)
            pathSeg = nextSeg
            
        print(f"swirlPath: {swirlPath}")
        futureSnake = self.futureSnakeCoords(self.snakeCoords, swirlPath)
        print(f"futureSnake: {futureSnake}")
        
        #snake is able to go down path without chomping itself
        if futureSnake2[0] == swirlPath[-1]:
            return swirlPath
        
        return deque()
    
    #determines velocities at space that allow snake's next move to stay within a strict swirl
    #velocities determined regardless of snake's current velocity
    #@param col - column number
    #@parma row - row number
    #returns list of tuples of form (xVelocity, yVelocity)
    def strictSwirlDirections(self, col, row):
        velocities = set()
        rightVel = (1, 0)
        
        #seeing if space allows snake to move right
        if row == 1 and col != self.cols:
            velocities.add(rightVel)
        if self.cols % 2 == 1 and col == 1:
            #adding addition spaces where snake can move right depending on rows
            if self.rows % 2 == 0 and row % 2 == 1:
                velocities.add(rightVel)
            elif self.rows % 2 == 1 and row % 2 == 0:
                velocities.add(rightVel)
                
        leftVel = (-1, 0)       
                
        #seeing if space allows snake to move left
        if row >= 2 and col > 2:
            velocities.add(leftVel)
        if row >= 2 and col == 2:
            #checking if number of columns is even
            if self.cols % 2 == 0:
                velocities.add(leftVel)
            elif self.rows % 2 == 0 and row % 2 == 0:
                velocities.add(leftVel)
            elif self.rows % 2 == 1 and row % 2 == 1:
                velocities.add(leftVel)
        
        downVel = (0, 1)
                
        #seeing if space allows snake to move down
        if row < self.rows and self.cols % 2 == col % 2 and col > 1:
            velocities.add(downVel)
            
        upVel = (0, -1)
        
        #seeing if space allows snake to move up
        if row > 1:
            #finding situations where up is permitted
            if self.cols % 2 == 0 and col % 2 == 1:
                velocities.add(upVel)
            elif self.cols % 2 == 1 and col > 2 and col % 2 == 0:
                velocities.add(upVel)
            elif col == 1 and row == 2:
                velocities.add(upVel)
            elif col == 1 and row % 2 == self.rows % 2:
                velocities.add(upVel)
            elif col == 2 and self.cols % 2 == 1 and self.rows % 2 != row % 2:
                velocities.add(upVel)
        
        return list(velocities)
    
    #determines velocities at space that allow snake's next move to stay within a loose swirl
    #velocities determined regardless of snake's current velocity
    #@param col - column number
    #@parma row - row number
    #returns list of tuples of form (xVelocity, yVelocity)
    def looseSwirlDirections(self, col, row):
        directions = set(self.strictSwirlDirections(col, row))
        
        #adding right directions if needed
        if 2 < row and row < self.rows and col < self.cols:
            directions.add((1,0))
            
        #adding up direction if needed
        if row > 1 and col < self.cols:
            directions.add((0,-1))
            
        #adding down directions if needed
        if row < self.rows and col > 1:
            directions.add((0,1))
            
        return list(directions)
    
    #finds spaces near given space that allow it to move in swirl on next turn
    #@param col - column number
    #@param row - row number
    #@param swirlType - "loose" or "strict". determines whether to use loose or strict swirl
    #returns list of space coordinates
    def swirlSpaces(self, col, row, swirlType="strict"):
        #returning velocities based on type of swirl
        if swirlType == "strict":
            velocities = self.strictSwirlDirections(col, row)
        elif swirlType == "loose":
            velocities = self.looseSwirlDirections(col, row)
        else:
            print("Error. Invalid swirlType inputted.")
            return []
        
        return [(col + v[0], row + v[1]) for v in velocities]
    
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
        if not self.gameOverEdgeSpace((col, row)):
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
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns coordinates in form (col, row). if head doesn't exist returns empty tuple.
    def getHeadCoords(self, snakeSeg = None):
        #using self.snakeCoords if needed
        if snakeSeg is None:
            #print("using self.snakeCoords")
            snakeSeg = self.snakeCoords
        
        #print(self.snakeCoords)
        return snakeSeg[0]
    
    #gets column snake head is in
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns grid column number of head. if no head returns -1
    def getHeadCol(self, snakeSeg = None):
        return self.getHeadCoords(snakeSeg)[0]
    
    #gets row snake head is in
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #return grid row number of head
    def getHeadRow(self, snakeSeg = None):
        return self.getHeadCoords(snakeSeg)[1]
    
    #obtains head square
    #returns reference to head unit square. if none returns None
    def getHead(self):
        return self.snakeSquares[0] if self.snakeLength() > 0 else None
    
    #obtains id of space head segment is occupying
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns integer representing space id of head space
    def getHeadID(self, snakeSeg = None):
        return self.spaceID(self.getHeadCol(snakeSeg), self.getHeadRow(snakeSeg))
    
    #obtains id of space pellet is occupying
    #returns integer representing space id of pellet space
    def getPelletID(self):
        return self.spaceID(self.pelletCol, self.pelletRow)
    
    #obtains space coords of the space pellet is occupying
    #returns tuple of form (pelletCol, pelletRow)
    def getPelletCoords(self):
        return (self.pelletCol, self.pelletRow)
    
    #obtains tail square
    #returns reference to tail unit square
    def getTail(self):
        return self.snakeSquares[-1] if self.snakeLength() > 0 else None
    
    #obtains tail coordinates
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns tail grid coordinates as (col, row). if no tail returns empty tuple
    def getTailCoords(self, snakeSeg = None):
        #using self.snakeCoords if needed
        if snakeSeg is None:
            snakeSeg = self.snakeCoords
        
        return snakeSeg[-1]
    
    #obtains tail column
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns tail grid column number. if no tail returns -1
    def getTailCol(self, snakeSeg = None):
        return self.getTailCoords(snakeSeg)[0]
    
    #obatins tail row
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns tail grid row number. if no tail returns -1
    def getTailRow(self, snakeSeg = None):
        return self.getTailCoords(snakeSeg)[1]
    
    #obtains id of space tail is occupying
    #@param snakeSeg - list of snake coords. self.snakeCoords by default
    #returns id of space tail of occupying
    def getTailID(self, snakeSeg = None):
        return self.spaceID(self.getTailCol(snakeSeg), self.getTailRow(snakeSeg))
    
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
            print(f"x velocity: {xVelocity}")
            print(f"y velocity: {yVelocity}")
            print(f"snake head velocity: ({self.headXVelocity}, {self.headYVelocity})")
            
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
            #self.basicAISteer()
            #self.loopAiSteer()
            #self.safeWinAISteer()
            self.fastWinAISteer()
        
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
        if self.snakeLength() == self.cols*self.rows:
            self.win()
            self.printGrid()
            print("\n")
            return
        
        #drawing extra pellet if needed
        if self.pellet == None:
            self.drawPelletRandom()
           
        #printing grid if there was a change in snake's position
        if prevHeadCol != self.getHeadCol() or prevHeadRow != self.getHeadRow():
            self.printGrid()
            print("\n")
        
        #milliseconds = 1000
        milliseconds = 100
        self.canvas.after(milliseconds, self.runTurn)
        
    #shift the snake one spot
    def moveSnake(self):
        #snakeLength = len(self.snakeSquares)
        snakeLength = self.snakeLength()
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
            self.snakeSquares.popleft()
            rect = self.drawRect(prevHeadCol, prevHeadRow, headCol, headRow)
            self.snakeSquares.appendleft(rect)
        
        #drawing head block with blue unit square
        self.snakeCoords.appendleft(headCoords)
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
        
    #prints a game grid to the console
    #@param grid - 2 by 2 list representing game grid. self.grid by default
    def printGrid(self, grid=None):
        #using self.grid if grid not provided
        if grid == None:
            grid = self.grid
        
        printMatrix(grid)
        
    #obtains a copy of the game grid
    #returns 2d array of game grid. Edges of grid represent out of bounds game over zones
    def getGridCopy(self):
        return [[self.grid[x][y] for y in range(self.rows+2)] for x in range(self.cols+2)]
    
    #creates dictionary mapping space ids to ids of neighboring spaces under swirl paths
    #@param swirlType - "loose" or "strict". determines map form
    #neighbors found regardless of snake's position or velocity
    def __createSwirlNeighborsMap(self, swirlType="strict"):
        self.swirlNeighbors = {}
        
        #reporting neighbors for each space in grid
        for x in range(1, self.cols + 1):
            for y in range(1, self.rows + 1):
                spaceID = self.spaceID(x, y)
                neighborSpaces = self.swirlSpaces(x, y, swirlType)
                neighborIDs = [self.spaceID(s[0], s[1]) for s in neighborSpaces]
                self.swirlNeighbors[spaceID] = neighborIDs
                
    #replaces and creates a snake within memory composed in inputted segments
    #@param segments - list of snake coordinates. 0th element is snake head
    #does not replicate snake in gui
    def __buildSnake(self, segments):
        self.snakeCoords = deque([(seg[0], seg[1]) for seg in segments])
        self.fillGridWithSnake(self.grid, self.snakeCoords)
                
    #prints a certain path onto a copy of the grid
    #@param path - list of space coords forming path
    #prints grid to console with path represented by *. stars will not replace snake or pellet spaces
    def __printGridPath(self, path):
        gridCopy = self.getGridCopy()
        
        #updating grid copy with path
        for space in path:
            col = space[0]
            row = space[1]
            
            #not updating snake segments of pellet with path marks
            if gridCopy[col][row] not in {"H", "S", "T", "P"}:
                gridCopy[col][row] = "*"
                
        printMatrix(gridCopy)
        
    #obtains a list of space ids for a path of space coordinates
    #@param path - list of space coordinates
    #returns list of space ids corresponding to the coordinates in path in that order
    def pathIDs(self, path):
        return [self.spaceID(coord[0], coord[1]) for coord in path]
    
    #produces 2 by 2 nested lists that represent a blank game grid
    #returns 2 by 2 lists that allow for blank grid to be modified
    def blankGrid(self):
        grid = [["o" for y in range(self.rows + 2)] for x in range(self.cols + 2)]
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
    
    #updates a grid matrix with snake symbols
    #@param grid - 2 by 2 nested lists representing grid
    #@param snakeSeg - deque of space coordinates making up snake. 0th element is head
    #filled inputted grid with snake coordinates. "H" for head, "T" for tail, "S" otherwise
    def fillGridWithSnake(self, grid, snakeSeg):
        labeledSeg = set()
        
        #copying snake over to grid
        for i in range(len(snakeSeg) - 1, -1, -1):
            seg = snakeSeg[i]
            col = seg[0]
            row = seg[1]
            
            #chooseing grid symbol based on snake segment
            if i == 0:
                #snake has chomped itself
                if self.gameOverEdgeSpace(seg) or seg in labeledSeg:
                    grid[col][row] = "X"
                else:
                    grid[col][row] = "H"
            elif i == len(snakeSeg) - 1:
                grid[col][row] = "T"
            else:
                grid[col][row] = "S"
                
            labeledSeg.add(seg)
            
    #creates new grid object with inputted snake coordinates
    #@param snakeSeg - deque of space coordinates making up snake. 0th element is head
    #returns 2 by 2 nested lists grid with snake coordinates. "H" for head, "T" for tail, "S" otherwise
    def createGrid(self, snakeSeg = deque()):
        grid = self.blankGrid()
        self.fillGridWithSnake(grid, snakeSeg)
        return grid         
    
    #checks if two spaces are adjacent to each other in grid
    #@param space1 - tuple of form (col#, row#)
    #@param space2 - tuple of form (col#, row#)
    #returns True if spaces are next to each other in grid
    def spacesAreAdjacent(self, space1Coords, space2Coords):
        (col1, row1) = space1Coords
        (col2, row2) = space2Coords
        
        #checking if spaces next to each other
        if col1 == col2 and abs(row1 - row2) == 1:
            return True
        elif row1 == row2 and abs(col1 - col2) == 1:
            return True
        else:
            return False
                
    #finds new snake coordinates after it has moved down a certain path
    #@param snakeSeg - deque of space coordinates making up snake. 0th element is head
    #@param path - list of space coordinates representing path snake will take. 0th element is space adjacent to snake head.
    #@param pelletCoords - space coords for where pellet is located 
    #returns list coordinates snake will be at after moving down inputted path.
    #   assumes snake will eat no more than 1 pellet along the way
    def futureSnakeCoords(self, snakeSeg, path, pelletCoords=None):
        futureSnake = deque(snakeSeg)
        currentSegs = set(futureSnake)
        prevTail = futureSnake[-1]
        
        #going down path
        for coords in path:
            #print(f"coords: {coords}")
            
            #next path coordinates are invalid
            if not self.spacesAreAdjacent(futureSnake[0], coords):
                print("Error. Bad path input.")
                print(f"snakeSeg: {snakeSeg}")
                print(f"path: {path}")
                return deque()
            
            currentSegs.remove(futureSnake[-1])
            prevTail = futureSnake[-1]
            futureSnake.pop()
            currentSegs.add(coords)
            futureSnake.appendleft(coords)
            
            #snake is eating pellet!
            if coords == pelletCoords:
                futureSnake.append(prevTail)
                currentSegs.add(prevTail)
           
            #snake has reached game over
            if len(currentSegs) < len(futureSnake) or self.gameOverEdgeSpace(coords):
                #print("future snake is a game over!")
                return futureSnake
            
        return futureSnake