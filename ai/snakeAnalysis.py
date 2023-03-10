#module that hosts SnakeGameAnalyzer class
import graphtheory.pathFinder as search
import graphtheory.graph as g
from collections import deque

#class with a bunch of functions that obtain data from a particular snake game
class SnakeGameAnalyzer:
    #constructor
    #@param game - SnakeGame object that this object will analyze
    def __init__(self, game):
        self.game = game
        
    #changes game being analyzed
    #@param game - SnakeGame object
    def setGame(self, game):
        self.game = game
        
    #obtains game being analyzed
    #returns reference to game attached to analyzer
    def getGame(self):
        return self.game
    
    #reports all possible moves the snake can make it's current state
    #returns set of space coords of form (colNum, rowNum). includes game over moves
    def possibleMoveCoords(self):
        moves = self.adjacentSpaceCoords(self.game.headCoords())
        
        #all adjacent moves are valid if snake is stationary
        if self.game.headXVel == 0 and self.game.headYVel == 0:
            return moves

        filteredMoves = set()
        
        #filtering out impossible moves
        for (col, row) in moves:
            xChange = col - self.game.headCol()
            yChange = row - self.game.headRow()
            
            #found possible move
            if xChange == 0 and yChange != -self.game.headYVel:
                filteredMoves.add((col, row))
            elif xChange != -self.game.headXVel and yChange == 0:
                filteredMoves.add((col, row))  
            
        return filteredMoves
    
    #reports all possible moves the snake can make it's current state
    #returns set of space ids. includes game over moves
    def possibleMoveIDs(self):
        return {self.spaceID(coords) for coords in self.possibleMoveCoords()}
    
    #reports all possible moves not in out of bounds game over zone snake can make
    #returns set of space coords of form (colNum, rowNum)
    def possibleInboundMoveCoords(self):
        return {s for s in self.possibleMoveCoords() if self.coordsInBounds(s)}
    
    #reports all possible moves not in out of bounds game over zone snake can make
    #returns set of space ids
    def possibleInboundMoveIDs(self):
        return {s for s in self.possibleMoveIDs() if self.idInBounds(s)}
    
    #finds all spaces adjacent to a given space
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in question
    #returns set of space coords of form (colNum, rowNum) for all spaces adjacent to spaceCoords.
    #       includes game over moves
    def adjacentSpaceCoords(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        shifts = ((1, 0), (-1, 0), (0, 1), (0, -1))
        (x, y) = spaceCoords
        return {(x+u, y+v) for (u,v) in shifts if self.validCoords((x+u, y+v))}
    
    #finds all spaces adjacent to a given space
    #@param spaceID - integer id number of space in question
    #returns set of space ids for all spaces adjacent to space spaceID.
    #       includes game over moves
    def adjacentSpaceIDs(self, spaceID):
        self.assertValidSpaceID(spaceID)
        
        coords = self.spaceCoords(spaceID)
        return {self.spaceID(s) for s in self.adjacentSpaceCoords(coords)}
    
    #finds all spaces adjacent to given space that is in area that 
    #   won't result in out of bounds game over
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in question
    #returns set of space coords for adjacent spaces not within game over zone
    def adjacentInboundSpaceCoords(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        neighbors = self.adjacentSpaceCoords(spaceCoords)
        return {space for space in neighbors if self.coordsInBounds(space)}
    
    #finds all space adjacent to given space that is in area that 
    #   won't result in out of bounds game over
    #@param spaceID - integer id number for space in question
    #returns set of space ids for adjacent spaces not within game over zone
    def adjacentInboundSpaceIDs(self, spaceID):
        self.assertValidSpaceID(spaceID)
        
        coords = self.spaceCoords(spaceID)
        return {self.spaceID(s) for s in self.adjacentInboundSpaceCoords(coords)}
    
    #finds all space adjacent to head that is in area that 
    #   won't result in out of bounds game over
    #returns set of space ids for head adjacent spaces not within game over zone
    def headAdjacentInboundIDs(self):
        return self.adjacentInboundSpaceIDs(self.headID())
    
    #checks if 2 spaces are adjacent to each each other
    #@param spaceCoords1 - space coordinates of first space. (colNum, rowNum)
    #@param spaceCoords2 - space coordinates of second space. (colNum, rowNum)
    #returns True if spaces are adjacent, False otherwise
    def spacesAreAdjacent(self, spaceCoords1, spaceCoords2):
        self.assertValidSpaceCoords(spaceCoords1)
        self.assertValidSpaceCoords(spaceCoords2)
        
        (x1, y1) = spaceCoords1
        (x2, y2) = spaceCoords2
        
        #checking if spaces are adjacent
        if x1 == x2 and abs(y1 - y2) == 1:
            return True
        elif y1 == y2 and abs(x1 - x2) == 1:
            return True
        else:
            return False
    
    #checks if tuple is a valid pair of coordinates for a space within game grid,
    #   including out of bounds game over spaces
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in question
    #returns True is spaceCoords is valid pair of coordinates, False otherwise
    def validCoords(self, spaceCoords):
        #checking if tuple has 2 entries
        if len(spaceCoords) != 2:
            return False
        
        (col, row) = spaceCoords
        return self.validCol(col) and self.validRow(row)
    
    #checks if an integer is a valid space id
    #@param spaceID - integer
    #returns True if there's a space with that id, False otherwise. includes game over zone.
    def validSpaceID(self, spaceID):
        totalCols = self.game.cols + 2
        totalRows = self.game.rows + 2
        return 0 <= spaceID and spaceID < totalCols*totalRows
            
    #checks if a number if a valid column number, including out of bounds game over spaces
    #@param colNum - column number
    #returns True if it's a valid column in game, False otherwise
    def validCol(self, colNum):
        return 0 <= colNum and colNum <= self.game.cols + 1
    
    #checks if a number if a valid row number, including out of bounds game over spaces
    #@param rowNum - row number
    #returns True if it's a valid row in game, False otherwise
    def validRow(self, rowNum):
        return 0 <= rowNum and rowNum <= self.game.rows + 1
     
    #creates adjacency list for current state of game grid
    #@param snakeSegs - set of space coordinates making up snake.
    #   uses snake stored in game attached to analyzer by default
    #returns dict mapping space ids to set of space ids for visitable adjacent spaces
    #   does not include spaces within game over zone or occupied by snake
    def inboundAdjacencyList(self, snakeSegs=None):
        #populating snakeCoords if needed
        if snakeSegs == None:
            snakeSegs = set(self.game.snakeCoords)
        
        vertexMap = {}
        
        #adding nodes to adjacency list
        for spaceID in range(self.game.cols*self.game.rows):
            #checking if space is occupied
            if not self.spaceCoords(spaceID) in snakeSegs:
                vertexMap[spaceID] = set()
                neighbors = self.adjacentInboundSpaceIDs(spaceID)
            
                #figuring out which neighboring spaces are accessible
                for vertex in neighbors:
                    #checking if space empty
                    if not self.spaceCoords(vertex) in snakeSegs:
                        vertexMap[spaceID].add(vertex)
                
        return vertexMap
                
    #checking if certain space in game grid contains snake segment
    #@param spaceCoords - tuple of form (colNum, rowNum) describing space coordinates
    #returns True is snake is currently occupying inputted space within grid
    def isSnakeSpaceCoords(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        snakeSymbols = {"H", "S", "T"}
        (col, row) = spaceCoords
        
        return self.game.grid[col][row] in snakeSymbols
    
    #checking if certain space in game grid contains snake segment
    #@param spaceID - integer space id number
    #returns True is snake is currently occupying inputted space within grid
    def isSnakeSpaceID(self, spaceID):
        self.assertValidSpaceID(spaceID)
        return self.isSnakeSpaceCoords(self.spaceCoords(spaceID))
    
    #obtains space id for a pair of space coordinates
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in grid
    #returns integer corresponding to the space's id number
    def spaceID(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        (col, row) = spaceCoords
        
        #finding id number depending on if space causes out of bounds game over
        if self.coordsInBounds(spaceCoords):
            return (col - 1) % self.game.cols + self.game.cols*(row - 1)
        else:
            return self.__gameOverSpaceID(spaceCoords)
        
        return -1
    
    #obtains space id for a pair of space coordinates in out of bounds game over area
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in grid
    #returns integer id corresponding to the space's id number
    def __gameOverSpaceID(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        assert not self.coordsInBounds(spaceCoords)
            
        (col, row) = spaceCoords
            
        #assigning id based on location in game over boundary
        if row == 0:
            return self.game.cols*self.game.rows + col
        elif col == self.game.cols + 1:
            return self.__gameOverSpaceID((col, 0)) + row
        elif row == self.game.rows + 1:
            cornerID = self.__gameOverSpaceID((self.game.cols + 1, row))
            n = cornerID + self.game.cols + 1
            return n - col
        else:
            cornerID = self.__gameOverSpaceID((0, self.game.rows + 1))
            n = cornerID + self.game.rows + 1
            return n - row
            
    #obtains corresponding space coordinate for a space id
    #@param spaceID - integer id number of space in question
    #returns space coordinates of from (colNum, rowNum) matching spaceID
    def spaceCoords(self, spaceID):
        self.assertValidSpaceID(spaceID)
         
        #figuring out space coordinates based on id
        if spaceID < self.game.cols*self.game.rows:
            col = spaceID % self.game.cols + 1
            row = spaceID // self.game.cols + 1
            return (col, row)
        else:
            return self.__gameOverSpaceCoords(spaceID)
    
    #obtains space coordinates for an id in the game over zone
    #@param spaceID - integer id of space in game over zone
    #returns coords in form (colNum, rowNum) for inputted id
    def __gameOverSpaceCoords(self, spaceID):
        self.assertValidSpaceID(spaceID)
        assert not self.idInBounds(spaceID)
        
        cols = self.game.cols
        rows = self.game.rows
        upperLeftID = cols*rows
        upperRightID = upperLeftID + cols + 1
        lowerRightID = upperRightID + rows + 1
        lowerLeftID = lowerRightID + cols + 1
        (col, row) = (-1, -1)
            
        #determining space coordinates
        if spaceID <= upperRightID:
            row = 0
            col = spaceID - upperLeftID
        elif spaceID <= lowerRightID:
            col = cols + 1
            row = spaceID - upperRightID
        elif spaceID <= lowerLeftID:
            row = rows + 1
            col = lowerLeftID - spaceID
        else:
            col = 0
            row = (rows + 1) - (spaceID - lowerLeftID)
                
        return (col, row)
        
    #checks if a space is in zone that won't result in out of bounds game over
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in grid
    #returns True is space is in bounds, false otherwise
    def coordsInBounds(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        (col, row) = spaceCoords
        return self.columnInBounds(col) and self.rowInBounds(row)
    
    #checks if a space is in zone that won't result in out of bounds game over
    #@param spaceID - integer id number of space in grid
    #returns True is space is in bounds, false otherwise
    def idInBounds(self, spaceID):
        self.assertValidSpaceID(spaceID)
        return spaceID < self.game.cols*self.game.rows
        
    #checks if a certain column is within grid that won't cause out of bounds game over
    #@param colNum - column number of column in question
    #returns True if column in bounds, False otherwise
    def columnInBounds(self, colNum):
        return 1 <= colNum and colNum <= self.game.cols
    
    #checks if a certain row is within grid that won't cause out of bounds game over
    #@param rowNum - row number of row in question
    #returns True if row in bounds, False otherwise
    def rowInBounds(self, rowNum):
        return 1 <= rowNum and rowNum <= self.game.rows
        
    #runs assert procedure to ensure a set of space coordinates is valid
    #@param spaceCoords - tuple of from (colNum, rowNum)
    #raises AssertionError if invalid coordinates inputted
    def assertValidSpaceCoords(self, spaceCoords):
        assert self.validCoords(spaceCoords), "Invalid space coordinates."
        
    #runs assert procedure to ensure a space id is valid
    #@param spaceID - integer space id
    #raises AssertionError if invalid space id inputted
    def assertValidSpaceID(self, spaceID):
        assert self.validSpaceID(spaceID), "Invalid space id"
        
    #obtains spaceID for snake's head space
    #returns integer id number of space occupied by snake head
    def headID(self):
        return self.spaceID(self.game.headCoords())
    
    #obtains spaceID for snake's tail space
    #returns integer id number of space occupied by snake tail
    def tailID(self):
        return self.spaceID(self.game.tailCoords())
    
    #obtains spaceID for pellet space
    #returns integer id number of space occupied by pellet
    def pelletID(self):
        return self.spaceID(self.game.pelletCoords())
    
    #finds spaces snake can safely move to next turn
    #returns set of space coords that snake can move next without game over
    def safeMoves(self):
        startSpaces = set()
        
        #filtering out desirable start positions
        for coords in self.possibleInboundMoveCoords():
            #checking if path should start from that space
            if not self.isSnakeSpaceCoords(coords):
                startSpaces.add(coords)
            elif coords == self.game.tailCoords() and self.game.snakeLength() > 2:
                startSpaces.add(coords)
                
        moves = set()        
        
        #checking if pellet is within adjacent head spaces
        if self.game.pelletCoords() in startSpaces:
            path = self.pelletTailPath()
            
            #checking if path found
            if len(path) > 0:
                moves.add(path[0])
                
            startSpaces.remove(self.game.pelletCoords())
            
        #searching for tail paths from rest of spaces
        for coords in startSpaces:
            headCoords = self.game.headCoords
            futureSnake = self.futureSnakeCoords(deque([headCoords, coords]))
            path = self.headTailPath(futureSnake)
            
            #checking if path found
            if len(path) > 0:
                moves.add(path[0])
        
        return moves
    
    #finds new snake coordinates after it has moved down a certain path
    #@param path - deque of space coords representing path snake will take. 
    #   0th element is snake head.
    #returns deque coordinates snake will be at after moving down inputted path.
    #   assumes no pellet along the way
    def futureSnakeCoords(self, path):    
        futureSnake = deque(self.game.snakeCoords)
        
        #checking if path empty
        if len(path) == 0:
            return futureSnake
        
        currentSegs = set(futureSnake)
        trimmedPath = deque(path)
        trimmedPath.popleft()
        
        #going down path
        for coords in trimmedPath:
            assert self.spacesAreAdjacent(coords, futureSnake[0])
            
            currentSegs.remove(futureSnake[-1])
            futureSnake.pop()
            currentSegs.add(coords)
            futureSnake.appendleft(coords)
           
            #snake has reached game over
            if len(currentSegs) < len(futureSnake):
                return futureSnake
            if not self.coordsInBounds(futureSnake[0]):
                return futureSnake
            
        return futureSnake
    
    #finds shortest path from pellet's current location to tail's current location
    #returns deque of space coords if path found
    def pelletTailPath(self):
        graph = self.inboundAdjacencyList()
        g.addVertex(graph, self.tailID())
        self.addAdjInboundFreeEdges(graph, self.tailID())
   
        path = search.shortestPath(graph, self.pelletID(), self.tailID())
        return deque([self.spaceCoords(spaceID) for spaceID in path])
    
    #finds shortest path from head's current location to tail's current location
    #@param snakeCoords - deque of space coordinates making up snake.
    #   uses snake stored in game attached to analyzer by default
    def headTailPath(self, snakeCoords=None):
        #populating snakeCoords if needed
        if snakeCoords == None:
            snakeCoords = deque(self.game.snakeCoords)
            
        #checking for nonempty snake
        if len(snakeCoords) == 0:
            return deque()
            
        snakeSegs = set(snakeCoords)
        graph = self.inboundAdjacencyList(snakeSegs)
        headID = self.spaceID(snakeCoords[0])
        tailID = self.spaceID(snakeCoords[-1])
        
        g.addVertex(graph, headID)
        g.addVertex(graph, tailID)
        
        self.addAdjInboundFreeEdges(graph, headID, snakeSegs)
        self.addAdjInboundFreeEdges(graph, tailID, snakeSegs)
        
        headCoords = self.spaceCoords(headID)
        tailCoords = self.spaceCoords(tailID)
        
        #checking if head next to tail for snakes longer than 2
        if self.spacesAreAdjacent(headCoords, tailCoords) and len(snakeCoords) > 2:
            g.addEdge(graph, headID, tailID)
            
        path = search.shortestPath(graph, headID, tailID)
        return deque([self.spaceCoords(spaceID) for spaceID in path])
    
    #adds edges connecting space to adjacent inbound spaces not occupied by snake to a graph
    #@param graphAdjList - dict mapping space ids to sets of adjacent space ids.
    #   represents state of game
    #@param spaceID - integer space id of space in question
    #@param snakeSegs - set of space coords making up current snake
    #   uses coordinates stored in current game by default
    #if adjacent inbound snake free space not already in graph, it is added
    def addAdjInboundFreeEdges(self, graph, spaceID, snakeSegs=None):
        #initializing snakeSegs if needed
        if snakeSegs == None:
            snakeSegs = set(self.game.snakeCoords)
            
        #adding edges
        for vertex in self.adjacentInboundSpaceIDs(spaceID):
            #checking if edges should be added
            if self.spaceCoords(vertex) not in snakeSegs:
                g.addEdge(graph, vertex, spaceID)