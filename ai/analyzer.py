#module that hosts SnakeGameAnalyzer class
import graphtheory.graphPath as g
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
        self.prevTailID = self.tailID()
            
        #iterating over every pair of coordinates
        for i in range(c):
            for j in range(r):
                space = self.spaceID((i,j))
                moves = {self.spaceID(s) for s in moveMatrix[i][j]}
                self.moveMap[space] = moves
                
        #print(self.moveMap)
        
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
    #graph includes spaces within game over zone. 
    # does not include spaces occupied by snake
    def __createGraph(self, snakeSegs=None):
        #populating snakeCoords if needed
        if snakeSegs == None:
            snakeSegs = self.game.snakeCoords
        
        snakeIDs = {self.spaceID(coords) for coords in snakeSegs}
        c = self.game.cols + 2
        r = self.game.rows + 2
        self.graph = {v:set() for v in range(c*r) if v not in snakeIDs}
    
        #adding edges to graph
        for v in range(c*r):
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
    def __removeVertex(self, vertex):
        del self.graph[vertex]
        neighbors = self.adjacentSpaceIDs(vertex)
        
        #removing edges from neighbors
        for n in neighbors:
            #checking if neighbor currently exists in graph
            if n in self.graph:
                self.graph[n].discard(vertex)
                
    #adds a certain vertex to self.graph
    #@param vertex - space id of space to be added to graph
    def __addVertex(self, vertex):
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
              
    #refreshes analyzer's fields. after each snake move.
    def update(self):
        prev = self.prevTailID
        
        #deleting head space if needed
        if self.headID() != prev:
            self.__removeVertex(self.headID())
     
        #checking if snake tail moved
        if prev != self.tailID() and prev != self.headID():
            self.__addVertex(self.prevTailID)
            
        self.prevTailID = self.tailID()
        #assert self.__correctGraph()
                    
    #checks if graph correctly matches current state of game grid
    #returns True if graph is correct, False otherwise
    def __correctGraph(self):
        snake = self.game.snakeCoords
        
        for i in range(self.game.cols + 2):
            for j in range(self.game.rows + 2):
                s = self.spaceID((i,j))
                if (i,j) in snake and s in self.graph:
                    print(f"Error. Vertex {s} should have been deleted")
                    return False
                if (i,j) not in snake and s not in self.graph:
                    print(f"Error. Vertex {s} should be present.")
                    return False
                    
        return True
            
    #completely reinitializes analyzer. run when move recs not followed. 
    def reset(self):
        self.__createGraph()
    
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
    #@param snakeCoords - deque of snake space coords. optional
    #returns integer id number of space occupied by snake head
    def headID(self, snakeCoords=None):
        return self.spaceID(self.game.headCoords(snakeCoords))
    
    #obtains spaceID for snake's tail space
    #@param snakeCoords - deque of snake space coords. optional
    #returns integer id number of space occupied by snake tail
    def tailID(self, snakeCoords=None):
        return self.spaceID(self.game.tailCoords(snakeCoords))
    
    #obtains spaceID for pellet space
    #returns integer id number of space occupied by pellet
    def pelletID(self):
        return self.spaceID(self.game.pelletCoords())
    
    #finds spaces snake can safely move to next turn
    #returns set of space coords that snake can move next without game over
    def safeMoves(self):
        #assert self.__correctGraph()
        #self.createGraph()
        moveSet = self.moveIDs()
        moves = {m for m in moveSet if m in self.graph and self.idInBounds(m)}
        
        #checking if tail is adjacent space
        if self.game.snakeLength() > 2 and self.tailID() in moveSet:
            moves.add(self.tailID())
        
        assert self.pelletID() in self.graph
        self.__removeVertex(self.pelletID())
        self.__addVertex(self.tailID())
        
        target = self.tailID()
        
        #checking if snake has length 2
        if self.game.snakeLength() > 2:
            penultimate = self.game.snakeCoords[-2]
            target = self.spaceID(penultimate)
            self.__addVertex(target)
        
        #finding tail paths that do NOT involve pellet
        data = g.singleTargetPaths(self.graph, target, moves)
        self.__addVertex(self.pelletID())
        
        #checking if penultimate vertex must be removed
        if self.game.snakeLength() > 2:
            self.__removeVertex(target)
        
        movesLeft = set(moves)
        moves = {m for m in data if data[m]}
        movesLeft -= moves
        
        #checking all spaces already accounted for
        if not movesLeft:
            self.__removeVertex(self.tailID())
            return {self.spaceCoords(m) for m in moves}
        
        data = g.singleTargetPaths(self.graph, self.tailID(), movesLeft)
        newMoves = {m for m in data if data[m]}
        moves |= newMoves
        self.__removeVertex(self.tailID())
        #assert self.__correctGraph()
        return {self.spaceCoords(m) for m in moves}
        
    #finds new snake coordinates after it has moved down a certain path
    #@param path - deque of space coords representing path snake will take.
    #@param pelletCoords - (col, row) coordinates of pellet. optional.
    #@param snake - deque of space coords making up snake. optional.
    #returns deque coordinates snake will be at after moving down path
    #   assumes no pellets on route
    def futureSnake(self, path, snake=None):
        originalSnake = self.game.snakeCoords if snake == None else snake
        future = deque(originalSnake)
        #print(futureSnake)
        pathCopy = deque(path)
        finalPathSpace = ()
        
        #checking if path empty
        if len(pathCopy) == 0:
            return future
        
        currentSegs = set(future)
        pathCopy.popleft()
        
        #going down path
        for coords in pathCopy:
            #print(f"coords: {coords}")
            #print(f"futureSnake[0]: {futureSnake[0]}")
            assert self.spacesAreAdjacent(coords, future[0])
            
            finalSeg = future.pop()
            currentSegs.remove(finalSeg)
            currentSegs.add(coords)
            future.appendleft(coords)
           
            #snake has reached game over
            if len(currentSegs) < len(future):
                return future
            if not self.coordsInBounds(*future[0]):
                return future
            
        return future
    
    #finds new snake coordinates after it has moved down a certain path
    #@param path - deque of space coords representing path snake will take.
    #@param snake - deque of space coords making up snake. optional.
    #returns deque coordinates snake will be at after moving down path
    #   assumes snake will eat exactly one pellet somewhere along path
    def elongatedFutureSnake(self, path, snake=None):
        originalSnake = self.game.snakeCoords if snake == None else snake
        
        #checking if path empty
        if not path:
            return originalSnake
        
        finalSpace = path.pop()
        future = self.futureSnake(path, originalSnake)
        path.append(finalSpace)
        future.appendleft(finalSpace)
        return future
    
    #finds shortest path from pellet's current location to tail's current location
    #returns deque of space coords if path found
    def pelletTailPath(self):
        self.__addVertex(self.tailID())
        path = g.shortestPath(self.graph, self.pelletID(), self.tailID())
        return deque([self.spaceCoords(spaceID) for spaceID in path])
    
    #finds shortest path from snake's head to tail
    #@param snakeCoords - deque of space coords making up snake. optional
    def headTailPath(self, snakeCoords=None):
        #populating snakeCoords if needed
        if snakeCoords == None:
            snakeCoords = deque(self.game.snakeCoords)
            
        head = self.headID(snakeCoords)
        tail = self.tailID(snakeCoords)
        
        self.__addVertex(head)
        self.__addVertex(tail)
        path = g.shortestPath(self.graph, head, tail)
        self.__removeVertex(head)
        
        #checking if tail and head are same
        if tail != head:
            self.__removeVertex(tail)
        
        return deque([self.spaceCoords(s) for s in path])
    
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
                
    #finds shortest path from snake head to pellet
    #path does not require snake to move itself out of the way
    #returns path represented as deque of space coords
    #   path returned may cause game over down the line
    def pelletPath(self):
       self.__addVertex(self.headID())
       path = g.shortestPath(self.graph, self.headID(), self.pelletID())
       self.__removeVertex(self.headID())
       #assert self.__correctGraph()
       return deque([self.spaceCoords(spaceID) for spaceID in path])
   
    #finds shortest safe path from snake head to pellet
    #path does not require snake to move itself out of the way
    #returns path represented as deque of space coords
    #   path will avoid inevitable game over
    def safePelletPath(self):
        path = self.pelletPath()
        return path if self.__pathSafe(path) else deque()
    
    #checks if a given path is safe for snake to follow
    #@param path - deque of space coords
    #returns True if snake can follow path without game over, false otherwise
    def __pathSafe(self, path):
        #checking if pellet path found
        if not path:
            return True
        
        future = self.elongatedFutureSnake(path)
        addedVertices = set()
        
        #adjusting graph to match future snake
        for space in reversed(self.game.snakeCoords):
            #checking if space is in future snake
            if space in future:
                #break
                continue
            
            v = self.spaceID(space)
            self.__addVertex(v)
            addedVertices.add(v)
            
        removedVertices = set()
        
        #adjusting graph to match future snake
        for space in future:
            #checking if space is in original
            if space in self.game.snakeCoords:
                #break
                continue
            
            v = self.spaceID(space)
            self.__removeVertex(v)
            removedVertices.add(v)
        
        result = self.__snakeSafe(future)
        
        #restoring graph
        for v in removedVertices:
            self.__addVertex(v)
        for v in addedVertices:
            self.__removeVertex(v)
        
        #assert self.__correctGraph()
        return result
   
    #finds absolute shortest path from head to pellet
    #path found with knowledge that snake can move body parts out of the way
    #returns path represented as deque of space coords
    #   path may endanger snake down the line
    def fastPelletPath(self):
        #checking if snake has no more 2 segments
        if self.game.snakeLength() <= 2:
            return self.pelletPath()
            
        graph = dict(self.moveMap)
        thres = {v:0 for v in graph}
        i = 1
        
        #recording distance data from snake segments
        for space in reversed(self.game.snakeCoords):
            v = self.spaceID(space)
            thres[v] = i
            i += 1
        
        thres[self.headID()] = 0
        path = g.distGatedPath(graph, self.headID(), self.pelletID(), thres)
        #assert self.__correctGraph()
        return deque([self.spaceCoords(spaceID) for spaceID in path])
    
    #finds absolute shortest path from head to pellet that's also safe
    #path found with knowledge that snake can move body parts out of the way
    #returns path represented as deque of space coords
    #   path will avoid leading to inevitable game over
    def fastSafePelletPath(self):
        path = self.fastPelletPath()
        return path if self.__pathSafe(path) else deque()
             
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
    #@param snakeCoords - deque of snake space coordinates. optional.
    #returns True if snake can avert game over, False otherwise
    def __snakeSafe(self, snakeCoords=None):
        return bool(self.headTailPath(snakeCoords))