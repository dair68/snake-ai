#module that hosts SnakeGameAnalyzer class
import graphtheory.path as g
from collections import deque

#class with a bunch of functions that obtain data from a particular snake game
class SnakeAnalyzer:
    #constructor
    #@param game - SnakeGame object that this object will analyze
    #@param moveMatrix - matrix where arr[i][j] is set of all spaces snake can
    #   move to from coordinate (i,j). optional.
    def __init__(self, game, moveMatrix=None):
        self.game = game
        self.graph = {}
        r = game.rows + 2
        c = game.cols + 2
        
        #checking if moveMatrix inputted
        if not moveMatrix:
            moveMatrix = [[set() for j in range(r)] for i in range(c)]
            
            #iterating over every pair of coordinates
            for i in range(c):
                for j in range(r):
                    #checking if out of bounds game over space
                    if not self.coordsInBounds(i,j):
                        continue
                    
                    shift = {(1,0), (-1,0), (0,1), (0,-1)}
                    spaces = {(i+x, j+y) for (x,y) in shift}
                    moveMatrix[i][j] = spaces
            
        self.moveMap = {}
            
        #iterating over every pair of coordinates
        for i in range(c):
            for j in range(r):
                space = self.spaceID((i,j))
                moves = {self.spaceID(s) for s in moveMatrix[i][j]}
                self.moveMap[space] = moves
        
    #changes game being analyzed
    #@param game - SnakeGame object
    def setGame(self, game):
        self.game = game
        
    #obtains game being analyzed
    #returns reference to game attached to analyzer
    def getGame(self):
        return self.game
    
    #reports all possible moves the snake can make it's current state
    #returns set of space coords of form (col, row). includes game over moves
    def moveCoords(self):
        moves = self.moveMap[self.headID()]
        coords = {self.spaceCoords(m) for m in moves}
        
        #all adjacent moves are valid if snake is stationary
        if self.game.headXVel == 0 and self.game.headYVel == 0:
            return coords

        filteredMoves = set()
        
        #filtering out impossible moves
        for (col, row) in coords:
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
    def moveIDs(self):
        return {self.spaceID(coords) for coords in self.moveCoords()}
    
    #reports all possible moves not in out of bounds game over zone
    #returns set of space coords of form (colNum, rowNum)
    def possibleInboundMoveCoords(self):
        return {s for s in self.possibleMoveCoords() if self.coordsInBounds(*s)}
    
    #reports all possible moves not in out of bounds game over zone snake can make
    #returns set of space ids
    def possibleInboundMoveIDs(self):
        return {s for s in self.possibleMoveIDs() if self.idInBounds(s)}
    
    #finds all spaces adjacent to a given space
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in question
    #returns set of space coords of form (colNum, rowNum) for all spaces adjacent to spaceCoords.
    #       includes game over moves
    def adjacentSpaceCoords(self, spaceCoords):
        self.assertValidCoords(spaceCoords)
        
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
        self.assertValidCoords(spaceCoords)
        
        neighbors = self.adjacentSpaceCoords(spaceCoords)
        return {space for space in neighbors if self.coordsInBounds(*space)}
    
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
        self.assertValidCoords(spaceCoords1)
        self.assertValidCoords(spaceCoords2)
        
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
     
    #rebuilds self.graph to represent current state of game grid
    #@param snakeSegs - deque of space coords making up snake.
    #   uses snake stored in game attached to analyzer by default
    #graph does not include spaces within game over zone or occupied by snake
    def createGraph(self, snakeSegs=None):
        #populating snakeCoords if needed
        if snakeSegs == None:
            snakeSegs = self.game.snakeCoords
        
        snakeIDs = {self.spaceID(coords) for coords in snakeSegs}
        cols = self.game.cols
        rows = self.game.rows
        self.graph = {v:set() for v in range(cols*rows) if v not in snakeIDs}
    
        #adding edges to graph
        for v in range(cols*rows):
            #checking if space is occupied
            if v in snakeIDs:
                continue
            
            neighbors = self.moveMap[v]
            
            #figuring out which neighboring spaces are accessible
            for neighbor in neighbors:
                #checking if space empty
                if neighbor not in snakeIDs:
                    self.graph[v].add(neighbor)
                    
    #removes a certain vertex from self.graph
    #@param vertex - space id of space to be removed from graph
    def removeVertex(self, vertex):
        del self.graph[vertex]
        neighbors = self.adjacentSpaceIDs(vertex)
        
        #removing edges from neighbors
        for n in neighbors:
            #checking if neighbor currently exists in graph
            if n in self.graph:
                self.graph[n].discard(vertex)
                
    #adds a certain vertex to self.graph
    #@param vertex - space id of space to be added to graph
    def addVertex(self, vertex):
        if vertex in self.graph:
            return
        
        self.graph[vertex] = set()
        neighbors = self.adjacentSpaceIDs(vertex)
            
        #figuring out which neighbors are present in graph
        for n in neighbors:
            #checking if node in graph
            if n not in self.graph:
                continue
            
            #checking if there's edge from vertex to n
            if n in self.moveMap[vertex]:
                self.graph[vertex].add(n)
            #checking if there's edge from n to vertex
            if vertex in self.moveMap[n]:
                self.graph[n].add(vertex)
    
    #creates adjacency list for every inbound space in game grid
    #returns dict adjacency list containing visitable adjacent spaces
    #   does not include spaces within game over zone. includes spaces with snake.
    def inboundSpaceGraph(self):
        graph = {v:set() for v in range(self.game.cols*self.game.rows)}
        
        #adding nodes to adjacency list
        for spaceID in range(self.game.cols*self.game.rows):
            for vertexID in self.adjacentInboundSpaceIDs(spaceID):
                graph[spaceID].add(vertexID)
                graph[vertexID].add(spaceID)
                
        return graph
                
    #checking if certain space in game grid contains snake segment
    #@param spaceCoords - tuple of form (colNum, rowNum) describing space coordinates
    #returns True is snake is currently occupying inputted space within grid
    def isSnakeSpaceCoords(self, spaceCoords):
        self.assertValidCoords(spaceCoords)
        
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
        self.assertValidCoords(spaceCoords)
        
        (col, row) = spaceCoords
        
        #finding id number depending on if space causes out of bounds game over
        if self.coordsInBounds(col, row):
            return (col - 1) % self.game.cols + self.game.cols*(row - 1)
        else:
            return self.__gameOverSpaceID(spaceCoords)
    
    #obtains space id for a pair of space coordinates in out of bounds game over area
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in grid
    #returns integer id corresponding to the space's id number
    def __gameOverSpaceID(self, spaceCoords):
        self.assertValidCoords(spaceCoords)
        assert not self.coordsInBounds(*spaceCoords)
            
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
    #@param col - col number of space
    #@param row - row number of space
    #returns True is space is in bounds, false otherwise
    def coordsInBounds(self, col, row):
        self.assertValidCoords((col, row))
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
    def assertValidCoords(self, spaceCoords):
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
        moveSet = self.moveIDs()
        
        self.createGraph()
        moves = {m for m in moveSet if m in self.graph and self.idInBounds(m)}
        
        #checking if tail ifsadjacent space
        if self.tailID() in moveSet:
            moves.add(self.tailID())
        
        self.removeVertex(self.pelletID())
        self.addVertex(self.tailID())
        
        target = self.tailID()
        
        #checking if snake has length 2
        if self.game.snakeLength() >= 2:
            penultimate = self.game.snakeCoords[-2]
            target = self.spaceID(penultimate)
            self.addVertex(target)
        
        #finding tail paths that do NOT involve pellet
        data = g.singleTargetPaths(self.graph, target, moves)
        self.addVertex(self.pelletID())
        
        #checking if penultimate vertex must be removed
        if self.game.snakeLength() >= 2:
            self.removeVertex(target)
        
        movesLeft = set(moves)
        moves = {m for m in data if data[m]}
        movesLeft -= moves
        
        #checking all spaces already accounted for
        if not movesLeft:
            self.removeVertex(self.tailID())
            return {self.spaceCoords(m) for m in moves}
        
        data = g.singleTargetPaths(self.graph, self.tailID(), movesLeft)
        newMoves = {m for m in data if data[m]}
        moves |= newMoves
        self.removeVertex(self.tailID())
        return {self.spaceCoords(m) for m in moves}
        
    #finds new snake coordinates after it has moved down a certain path
    #@param path - deque of space coords representing path snake will take.
    #@param snake - deque of space coords making up snake. uses self.game.snakeCoords by default
    #   0th element is snake head.
    #@param pelletCoords - coordinates of pellet. optional
    #returns deque coordinates snake will be at after moving down inputted path.
    def futureSnakeCoords(self, path, snake=None, pelletCoords=None):    
        futureSnake = deque(self.game.snakeCoords) if snake == None else deque(snake)
        #print(futureSnake)
        pathCopy = deque(path)
        finalPathSpace = ()
        
        #checking if snake will chomp pellet along the way
        if pelletCoords in path:
            finalPathSpace = pathCopy[-1]
            pathCopy.pop()
        
        #checking if path empty
        if len(pathCopy) == 0:
            return futureSnake
        
        currentSegs = set(futureSnake)
        pathCopy.popleft()
        
        #going down path
        for coords in pathCopy:
            #print(f"coords: {coords}")
            #print(f"futureSnake[0]: {futureSnake[0]}")
            assert self.spacesAreAdjacent(coords, futureSnake[0])
            
            currentSegs.remove(futureSnake[-1])
            futureSnake.pop()
            currentSegs.add(coords)
            futureSnake.appendleft(coords)
           
            #snake has reached game over
            if len(currentSegs) < len(futureSnake):
                return futureSnake
            if not self.coordsInBounds(*futureSnake[0]):
                return futureSnake
            
        #reattaching final space if needed
        if finalPathSpace != ():
            futureSnake.appendleft(finalPathSpace)
            
        return futureSnake
    
    #finds shortest path from pellet's current location to tail's current location
    #returns deque of space coords if path found
    def pelletTailPath(self):
        self.addVertex(self.tailID())
        path = g.shortestPath(self.graph, self.pelletID(), self.tailID())
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
        graph = self.freeInboundSpaceGraph(snakeSegs)
        headID = self.spaceID(snakeCoords[0])
        tailID = self.spaceID(snakeCoords[-1])
        
        graph[headID] = set()
        graph[tailID] = set()
        
        self.addAdjInboundFreeEdges(graph, headID, snakeSegs)
        self.addAdjInboundFreeEdges(graph, tailID, snakeSegs)
        
        headCoords = self.spaceCoords(headID)
        tailCoords = self.spaceCoords(tailID)
        
        #checking if head next to tail for snakes longer than 2
        if self.spacesAreAdjacent(headCoords, tailCoords) and len(snakeCoords) > 2:
            graph.addEdge(headID, tailID)
            
        path = g.shortestPath(graph, headID, tailID)
        return deque([self.spaceCoords(spaceID) for spaceID in path])
    
    #adds edges connecting space to adjacent inbound spaces not occupied by snake to a graph
    #@param graph - SimpleUndirectedGraph object representing state of game
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
                graph[vertex].add(spaceID)
                graph[spaceID].add(vertex)
                
    #finds shortest path from head's current location to pellet's current location
    #path does not account for snake moving body parts out of the way
    #returns path represented as deque of space coords. empty deque if no path found 
    def pelletPath(self):
       graph = self.freeInboundSpaceGraph()
       graph[self.headID()] = set()
       self.addAdjInboundFreeEdges(graph, self.headID())
       path = g.shortestPath(graph, self.headID(), self.pelletID())
       return deque([self.spaceCoords(spaceID) for spaceID in path])
   
    #finds absolutely shortest path from head's current location to pellet's current location
    #path found with knowledge that snake can move body parts out of the way
    #returns path represented as deque of space coords. empty deque if no path found 
    '''
    def fastPelletPath(self):
        graph = self.inboundSpaceGraph()
        
        #assigning value of 0 to each node in graph
        for vertex in graph:
            graph.setVertexValue(vertex, 0)
        
        #populating nodeValues with snake data
        for i in range(1, self.game.snakeLength()):
            coords = self.game.snakeCoords[i]
            segID = self.spaceID(coords)
            graph.setVertexValue(segID, self.game.snakeLength() - i)
            
        #adjusting number for special case of length 2 snakes
        if self.game.snakeLength() == 2:
            coords = self.game.snakeCoords[-1]
            segID = self.spaceID(coords)
            graph.setVertexValue(segID, 3)
            
        headID = self.headID()
        pelletID = self.pelletID()
        path = search.distanceGatedShortestPath(graph, headID, pelletID)
        
        return deque([self.spaceCoords(vertex) for vertex in path])
    '''
             
    #adds all edges within path to graph
    #@param graph - SimpleUndirectedGraph object
    #@param path - deque of vertex ids making up path. and edges in path added to graph
    def __addPathEdges(self, graph, path):
        pathList = list(path)
        
        #adding edges to graph
        for i in range(len(pathList)-1):
            v1 = pathList[i]
            v2 = pathList[i+1]
            graph.addEdge(v1,v2)
    
    #checks if a given snake can avoid inevitable game over down the line
    #@param snakeCoords - deque of snake space coordinates
    #returns True if snake can avert game over, False otherwise
    def snakeSafe(self, snakeCoords):
        return len(self.headTailPath(snakeCoords)) > 0