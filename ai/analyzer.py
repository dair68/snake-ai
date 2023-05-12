#module that hosts SnakeGameAnalyzer class
import graphtheory.pathFinder as search
import graphtheory.graph as g
from collections import deque
import graphtheory.gridGraph as grid

#adds padding to outside of rectangle within matrix
#@param rectCoords - tuple of form ((x1,y1), (y1,y2)) 
#   where (x1,y1) are col/row numbers for upper left corner 
#   and (x2,y2) are col/row numbers for lower right corner
#@param left - number of columns to be added to left side of rectangle
#@param right - number of columnts to be added to right side of rectangle
#@param up - number of rows to be added to upper side of rectangle
#@param down - number of rows to be added to lower side of rectangle
#returns new rectangle coordinates of form (u1,v1,u2,v2)
#   where (u1, v2) is upper left coordinates and (u2, v2) is lower right
def padRectangle(rectCoords, left, right, up, down):
    (x1,y1,x2,y2) = rectCoords
    
    x1 -= left
    x2 += right
    y1 -= up
    y2 += down
     
    return (x1,y1,x2,y2)

#class with a bunch of functions that obtain data from a particular snake game
class SnakeAnalyzer:
    #constructor
    #@param game - SnakeGame object that this object will analyze
    def __init__(self, game):
        self.game = game
        
        vertexIDs = [[-1 for j in range(self.game.rows+2)] for i in range(self.game.cols+2)]
        
        #recording ids of each vertex in grid
        for i in range(self.game.cols+2):
            for j in range(self.game.rows+2):
                vertexID = self.spaceID((i,j))
                vertexIDs[i][j] = vertexID
        
        #print(vertexIDs)
        self.wholeGridGraph = grid.GridGraph(self.game.cols+2, self.game.rows+2, vertexIDs)
        
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
     
    #creates graph representing current state of game grid
    #@param snakeSegs - set of space coordinates making up snake.
    #   uses snake stored in game attached to analyzer by default
    #returns SimpleUndirectedGraph object with space ids corresponding to vertex numbers
    #   does not include spaces within game over zone or occupied by snake
    def freeInboundSpaceGraph(self, snakeSegs=None):
        #populating snakeCoords if needed
        if snakeSegs == None:
            snakeSegs = set(self.game.snakeCoords)
        
        vertices = set()
        edges = set()
        
        #adding nodes to adjacency list
        for spaceID in range(self.game.cols*self.game.rows):
            #checking if space is occupied
            if not self.spaceCoords(spaceID) in snakeSegs:
                vertices.add(spaceID)
                neighbors = self.adjacentInboundSpaceIDs(spaceID)
            
                #figuring out which neighboring spaces are accessible
                for vertexID in neighbors:
                    #checking if space empty
                    if not self.spaceCoords(vertexID) in snakeSegs:
                        #figuring out which id number if smaller
                        if spaceID < vertexID:
                            edges.add((spaceID, vertexID))
                        else:
                            edges.add((vertexID, spaceID))
                
        return g.SimpleUndirectedGraph(vertices, edges)
    
    #creates adjacency list for every inbound space in game grid
    #returns SimpleUndirectedGraph object containing visitable adjacent spaces
    #   does not include spaces within game over zone. includes spaces with snake.
    def inboundSpaceGraph(self):
        vertices = set()
        edges = set()
        
        #adding nodes to adjacency list
        for spaceID in range(self.game.cols*self.game.rows):
            vertices.add(spaceID)
            
            for vertexID in self.adjacentInboundSpaceIDs(spaceID):
                edge = (spaceID, vertexID) if spaceID < vertexID else (vertexID, spaceID)
                edges.add(edge)
                
        return g.SimpleUndirectedGraph(vertices, edges)
                
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
    
    #finds spaces snake can safely move to next turn
    #returns set of space coords that snake can move next without game over
    #   or messing up endgame
    def extraSafeMoves(self):
        moves = self.safeMoves()
        safestMoves = set()
        
        #determining which moves won't mess up endgame
        for move in moves:
            headCoords = self.game.headCoords
            futureSnake = self.futureSnakeCoords(deque([headCoords, move]))
            spaces = self.badVacantSpaces(futureSnake)
            
            #checking if there are no singular empty spaces
            if spaces == 0:
                safestMoves.add(move)
                
        return safestMoves
        
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
        graph = self.freeInboundSpaceGraph()
        graph.addVertex(self.tailID())
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
        graph = self.freeInboundSpaceGraph(snakeSegs)
        headID = self.spaceID(snakeCoords[0])
        tailID = self.spaceID(snakeCoords[-1])
        
        graph.addVertex(headID)
        graph.addVertex(tailID)
        
        self.addAdjInboundFreeEdges(graph, headID, snakeSegs)
        self.addAdjInboundFreeEdges(graph, tailID, snakeSegs)
        
        headCoords = self.spaceCoords(headID)
        tailCoords = self.spaceCoords(tailID)
        
        #checking if head next to tail for snakes longer than 2
        if self.spacesAreAdjacent(headCoords, tailCoords) and len(snakeCoords) > 2:
            graph.addEdge(headID, tailID)
            
        path = search.shortestPath(graph, headID, tailID)
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
                graph.addEdge(vertex, spaceID)
                
    #finds shortest path from head's current location to pellet's current location
    #path does not account for snake moving body parts out of the way
    #returns path represented as deque of space coords. empty deque if no path found 
    def pelletPath(self):
       graph = self.freeInboundSpaceGraph()
       graph.addVertex(self.headID())
       self.addAdjInboundFreeEdges(graph, self.headID())
       path = search.shortestPath(graph, self.headID(), self.pelletID())
       return deque([self.spaceCoords(spaceID) for spaceID in path])
   
    #finds absolutely shortest path from head's current location to pellet's current location
    #path found with knowledge that snake can move body parts out of the way
    #returns path represented as deque of space coords. empty deque if no path found 
    def fastPelletPath(self):
        graph = self.inboundSpaceGraph()
        
        #assigning value of 0 to each node in graph
        for vertex in graph.getVertices():
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
    
    #finds smallest rectangle that bounds snake coordinates
    #@param snakeCoords - deque of space coordinates making up snake
    #return tuple of form (i, j, u, v) 
    #   where (i,j) are coordinates of upper left corner and 
    #   (u, v) are coordinates of bottom right corner
    def smallestBoundingRect(self, snakeCoords):
        initialSpace = snakeCoords[0]
        (minX, minY) = initialSpace
        (maxX, maxY) = initialSpace
        
        #searching for rectangle boundaries
        for coords in snakeCoords:
            (x, y) = coords
            
            #found new dimension
            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y
                
        return (minX, minY, maxX, maxY)
    
    #finds largest rectangle within region that doesn't contain snake coordinates
    #@param snakeCoords - deque of space coordinates making up snake
    #@param region - rectangle of form (x1, y1, x2, y2) where (x1,y1) is upper left, (x2, y2) is lower right
    #   searches for larest empty rectangle within rect
    #return tuple of form (i, j, u, v) 
    #   where (i,j) are coordinates of upper left corner and 
    #   (u, v) are coordinates of bottom right corner
    def __largestEmptyRect(self, snakeCoords, region):
        (x1, y1, x2, y2) = region
        m = x2 - x1 + 1
        n = y2 - y1 + 1
        rectData = [[() for j in range(n)] for i in range(m)]
        
        #filling data with snake coordinates
        for coord in snakeCoords:
            (col, row) = coord
            rectData[col-x1][row-y1] = (-1,-1)
            
        largestArea = 0
        largestRectCoords = ()
        
        #filling matrix with data on possible rectangles
        for i in range(m):
            for j in range(n):
                #checking column or row
                if i == 0:
                    data = ()
                    
                    #filling space based on row data
                    if j == 0 and rectData[0][0] == ():
                        data = (0,0)
                    elif rectData[0][j] == ():
                        data = (i,j) if rectData[0][j-1] == (-1,-1) else rectData[0][j-1]
                    else:
                        data = (-1,-1)
                        
                    rectData[0][j] = data
                elif j == 0 and rectData[i][0] == ():    
                    rectData[i][0] = (i,j) if rectData[i-1][0] == (-1,-1) else rectData[i-1][0]
                elif rectData[i][j] == ():
                    upperSpace = rectData[i][j-1]
                    leftSpace = rectData[i-1][j]
                    data = (-2,-2)
                    
                    #checking adjacent spaces
                    if upperSpace == (-1,-1) and leftSpace == (-1,-1):
                        data = (i,j)
                    elif upperSpace == (-1,-1):
                        data = (leftSpace[0], j)
                    elif leftSpace == (-1,-1):
                        data = (i, upperSpace[1])
                    else:
                        (u1,v1) = upperSpace
                        (u2,v2) = leftSpace
                        
                        #checking dimensions relative to each other
                        if u1 < u2 or v1 > v2:
                            data = (u2, max(v1,v2))
                        else:
                            area1 = (i-u1+1)*(j-v1+1)
                            area2 = (i-u2+1)*(j-v2+1)
                            data = upperSpace if area1 > area2 else leftSpace 
                            
                    rectData[i][j] = data
                    
                #checking area of rectangle just found
                if rectData[i][j] != (-1,-1):
                    (i2,j2) = rectData[i][j]
                    area = (i-i2+1)*(j-j2+1)
                    
                    #found larger area
                    if area > largestArea:
                        largestArea = area
                        largestRectCoords = (i,j)
        
        #print(largestArea)
        #print(largestRectCoords)
        (col2, row2) = largestRectCoords
        oppositeCorner = rectData[col2][row2]
        (col1, row1) = oppositeCorner
        return (col1 + x1, row1 + y1, col2 + x1, row2 + y1)
    
    #adds padding to a rectangle s.t. edge of rect and edge of grid have 
    #   even distance
    #@param rectCoords - tuple of form ((x1,y1), (y1,y2)) 
    #   where (x1,y1) are col/row numbers for upper left corner 
    #   and (x2,y2) are col/row numbers for lower right corner
    #adds columns and rows until distance from rect edge to grid edge is even, if possible
    #   ensures rectangle within grid bounds
    #   returns rectangle as (u1,v1,u1,v2) if found, empty tuple otherwise
    #   where (u1,v1) are col/row numbers for upper left corner 
    #   and (u2,v2) are col/row numbers for lower right corner
    def padRectEvenMargins(self, rectCoords):
        (x1,y1,x2,y2) = rectCoords
        m = x2 - x1 + 1
        n = y2 - y1 + 1
        rect = rectCoords
        
        #ensuring margins have even distance
        if x1 % 2 == 0:
            rect = padRectangle(rect, 1, 0, 0, 0)
        if (self.game.cols - x2) % 2 == 1:
            rect = padRectangle(rect, 0, 1, 0, 0)
        if y1 % 2 == 0:
            rect = padRectangle(rect, 0, 0, 1, 0)
        if (self.game.rows - y2) % 2 == 1:
            rect = padRectangle(rect, 0, 0, 0, 1)
            
        return rect
    
    #finds rectangle surrounding snake that could maybe hold hamiltonian cycle
    #@param snakeCoords - deque of space coords representing snake
    #returns rectangle as (u1,v1,u1,v2) if found, empty tuple otherwise
    #   (u1,v1) is (colNum, rowNum) for upper left corner 
    #   and (u2,v2) is (colNum, rowNum) for lower right corner
    def snakeRectangle(self, snakeCoords):
        rect = self.smallestBoundingRect(snakeCoords)
        (u1, v1, u2, v2) = rect
        
        #print(rect)
        rect = self.padRectEvenMargins(rect)
        #print(rect)
        
        (x1,y1,x2,y2) = rect
        m = x2 - x1 + 1
        n = y2 - y1 + 1
        
        #checking if rectangle has even number of spaces
        if m*n % 2 == 1:
            return ()
        
        #adding extra padding to increase chance of hamiltonian cycle
        if x1 > 2 and x1 == u1:
            rect = padRectangle(rect, 2, 0, 0, 0)
        if self.game.cols - x2 >= 2 and x2 == u2:
            rect = padRectangle(rect, 0, 2, 0, 0)    
        if y1 > 2 and y1 == v1:
            rect = padRectangle(rect, 0, 0, 2, 0)
        if self.game.rows - y2 >= 2 and y2 == v2:
            rect = padRectangle(rect, 0, 0, 0, 2)
        
        return rect
    
    #finds rectangle within snake rectangle that doesn't contain snake spaces
    #@param snakeCoords - deque of space coords representing snake
    #@param rect - rectangle containing all of snake
    #returns rectangle as (u1,v1,u1,v2) if found, empty tuple otherwise
    #   (u1,v1) is (colNum, rowNum) for upper left corner 
    #   and (u2,v2) is (colNum, rowNum) for lower right corner
    def snakeExcludedRectangle(self, snakeCoords, rect):
        emptyRect = self.__largestEmptyRect(snakeCoords, rect)
        #print(emptyRect)
        (u1, v1, u2, v2) = emptyRect
        width = u2 - u1 + 1
        height = v2 - v1 + 1
        
        #checking if rectangle at least 2 by 2
        if width < 6 or height < 6:
            print("rectangle too small")
            return ()
            
        (x1, y1, x2, y2) = rect
        
        #checking if empty rectangle has odd number of entries
        if width*height % 2 == 1:
            #shrinking rectangle down to even dimensions
            if u1 != x1:
                emptyRect = (u1+1, v1, u2, v2)
            elif u2 != x2:
                emptyRect = (u1, v1, u2-1, v2)
            elif v1 != y1:
                emptyRect = (u1, v1+1, u2, v2)
            elif v2 != y2:
                emptyRect = (u1, v1, u2, v2-1)
                
        #further trimming rectangle
        if u1 != x1 and u1 == emptyRect[0] and emptyRect[2] - emptyRect[0] > 2:
            emptyRect = (u1+2, emptyRect[1], emptyRect[2], emptyRect[3])
        if u2 != x2 and u2 == emptyRect[2] and emptyRect[2] - emptyRect[0] > 2:
            emptyRect = (emptyRect[0], emptyRect[1], u2-2, emptyRect[3])
        if v1 != y1 and v1 == emptyRect[1] and emptyRect[3] - emptyRect[1] > 2:
            emptyRect = (emptyRect[0], v1+2, emptyRect[2], emptyRect[3])
        if v2 != y2 and v2 == emptyRect[3] and emptyRect[3] - emptyRect[1] > 2:
            emptyRect = (emptyRect[0], emptyRect[1], emptyRect[2], v2-2)
                
        return emptyRect
    
    #searches for a pellet path and an escape route for current snake position
    #returns dict of form {pelletPath:deque(), escapePath:deque()}
    #   escape path allows snake to survive indefinitely after completing pellet path
    def pelletPathInfo(self):
        pelletPath = self.fastPelletPath()
        #print(pelletPath)
        
        #checks if pellet path found
        if len(pelletPath) == 0:
            return {"pelletPath": deque(), "escapePath": deque()}
        
        futureSnake = self.futureSnakeCoords(pelletPath, pelletPath[-1])
        print(futureSnake)
        rect = self.snakeRectangle(futureSnake)
        print(rect)
        
        #checking if rectangle found successfully
        if rect == ():
            return {"pelletPath": deque(), "escapePath": deque()}
        
        emptyRect = self.snakeExcludedRectangle(futureSnake, rect)
        print(emptyRect)
        
        sub = grid.GridGraph(1,1)
        innerGraph = grid.GridGraph(1,1)
        
        #determining subgraph surround snake
        if emptyRect == ():
            sub = self.wholeGridGraph.gridSubgraph(*rect)
        else:
            innerGraph = self.wholeGridGraph.gridSubgraph(*emptyRect)
            #print(innerGraph.getVertices())
            #print(innerGraph.getEdges())
            outerGraph = self.wholeGridGraph.gridSubgraph(*rect)
            sub = g.SimpleUndirectedGraph(outerGraph.getVertices(), outerGraph.getEdges())
            
            #removing unneeded vertices
            for v in outerGraph.getVertices():
                #vertex not in inner graph
                if v in innerGraph.getVertices():
                    sub.removeVertex(v)
            
        #print(sub.getVertices())
        #print(sub.getEdges())
        futureSnakeIDs = deque([self.spaceID(coords) for coords in futureSnake])
        futureSnakeIDs.reverse()
        
        print("finding hamiltonian cycle")
        rectCycle = h.fastFinishHamiltonianCycle(sub, futureSnakeIDs)
        #print(rectCycle)
        
        #checking if hamiltonian cycle found
        if len(rectCycle) == 0:
            return {"pelletPath": deque(), "escapePath": deque()}
        
        m = self.game.cols
        n = self.game.rows
        pathGraph = g.SimpleUndirectedGraph({v for v in range((m+2)*(n+2))})
        self.__addPathEdges(pathGraph, rectCycle)
        #print(pathGraph.getVertices())
        #print(pathGraph.getEdges())
        
        #adding previously cut away rectangle to existing cycle
        if emptyRect != ():
            cycle = h.gridHamiltonianCycle(innerGraph)
            #print(cycle)
            self.__addPathEdges(pathGraph, cycle)
            
            (x1, y1, x2, y2) = emptyRect
            combining = False
            combining = self.__combineCyclesHorizontal(pathGraph, x1, x2, y1-1)
            
            #checking if rectangles combined successfully
            if combining == False:
                print("combining")
                combining = self.__combineCyclesVertical(pathGraph, x2, y1, y2)    
            if combining == False:
                print("combining")
                combining = self.__combineCyclesHorizontal(pathGraph, x1, x2, y2)
            if combining == False:
                print("combining")
                combining = self.__combineCyclesVertical(pathGraph, x1-1, y1, y2)
        
        '''
        print("forming partial path")
        path = deque()
        prevSpaces = set()
        vertex = rectCycle[0]
         
        while vertex != -1:
            #print(vertex)
            path.append(self.spaceCoords(vertex))
            prevSpaces.add(vertex)
            neighbors = pathGraph.neighbors(vertex)
            vertex = -1
         
            for v in neighbors:
                if v not in prevSpaces:
                    vertex = v
                    break
                 
        print(path)
        '''
        
        rectangles = self.inboundComplementRects(rect)
        #print(rectangles)
        
        cycles = [deque() for i in range(len(rectangles))]
        
        #finding hamiltonian cycles for each rectangular subgraph
        for i in range(len(rectangles)):
            r = rectangles[i]
            
            #checking if valid rectangle
            if len(r) > 0:
                graph = self.wholeGridGraph.gridSubgraph(*r)
                cycle = h.gridHamiltonianCycle(graph)
                cycles[i] = cycle
                self.__addPathEdges(pathGraph, cycle)
                #print(cycle)
      
        #print(cycles)
        #print(pathGraph.getVertices())
        #print(pathGraph.getEdges())
        (x1, y1, x2, y2) = rect
        self.__combineCyclesHorizontal(pathGraph, x1, x2, y1-1)
        self.__combineCyclesVertical(pathGraph, x2, y1, y2)
        self.__combineCyclesHorizontal(pathGraph, x1, x2, y2)
        self.__combineCyclesVertical(pathGraph, x1-1, y1, y2)
    
        '''
        print("forming partial path")
        path = deque()
        prevSpaces = set()
        vertex = 0
        
        while vertex != -1:
            #print(vertex)
            path.append(self.spaceCoords(vertex))
            prevSpaces.add(vertex)
            neighbors = pathGraph.neighbors(vertex)
            vertex = -1
            
            for v in neighbors:
                if v not in prevSpaces:
                    vertex = v
                    break
                
        print(path)
        '''
        
        
        #removing edge vertices from pathGraph
        for k in range(m*n, (m+2)*(n+2)):
            pathGraph.removeVertex(k)
        
        finalPath = h.hamiltonianCycle(pathGraph)
        print(f"current pellet path: {pelletPath}")
        finalPath.pop()
        finalPath = deque([self.spaceCoords(v) for v in finalPath])
        print(f"final path: {finalPath}")
        space1Index = finalPath.index(pelletPath[0])
        finalPath.rotate(-space1Index)
        space2Index = finalPath.index(pelletPath[1])
        
        #reversing path elements if needed
        if space2Index != 1:
            finalPath.rotate(-1)
            #print("reversing path")
            finalPath.reverse()
        
        pelletIndex = finalPath.index(pelletPath[-1])
        finalPath.rotate(-pelletIndex)
        finalPath.append(finalPath[0])
        print(f"final path: {finalPath}")
        return {"pelletPath": pelletPath, "escapePath": finalPath}
        
            
    #checks whether a rectangle lies within inbound spaces of game grid
    #@param rectCoords - tuple of form ((x1,y1), (y1,y2)) 
    #   where (x1,y1) are col/row numbers for upper left corner 
    #   and (x2,y2) are col/row numbers for lower right corner
    #returns true is rectangle doesn't touch out of bounds game over spaces, false otherwise
    def rectInBounds(self, rectCoords):
        (i1, j1, i2, j2) = rectCoords
        s1 = (i1, j1)
        s2 = (i2, j2)
        return self.coordsInBounds(i1, j1) and self.coordsInBounds(i2, j2)
    
    #obtains rectangle surround rectangle within inbound grid spaces
    #@param rectCoords - tuple of form (x1,y1,y1,y2) 
    #   where (x1,y1) are col/row numbers for upper left corner 
    #   and (x2,y2) are col/row numbers for lower right corner
    #returns list of rect tuples. rect list plus inputted rect will span
    #   every inbound grid space without overlapping
    def inboundComplementRects(self, rectCoords):
        (i1, j1, i2, j2) = rectCoords
        
        rect1 = (1,1,self.game.cols,j1-1)
        rect2 = (i2+1,j1,self.game.cols,self.game.rows)
        rect3 = (1,j2+1,i2,self.game.rows)
        rect4 = (1,j1,i1-1, j2)
        
        rectangles = [rect1, rect2, rect3, rect4]
        filteredRect = [i for i in range(4)]
        
        #marking rectangles that are inbounds
        for i in range(len(rectangles)):
            r = rectangles[i]
            
            #checking if rectangle inbounds
            if self.rectInBounds(r):
                filteredRect[i] = r
            else:
                filteredRect[i] = ()
        
        return filteredRect
    
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

    #combines adjacent hamiltonian cycles within grid along horizontal boundary
    #@param graph - graph with each edge being part of hamiltonian cycle for subgraph
    #   graph based on game grid
    #@param x1 - col number of leftmost space in horizontal boundary between cycles
    #@param x2 - col number of rightmost space in horizontal boundary between cycles
    #@param y - row number
    #analyzes spaces for x in [x1-x2], y in [y, y+1] for possible way to join
    #   both surround hamiltonian cycles into 1. if cycles joined successfully
    #   somewhere across horizontal boundary, returns True, else returns False
    def __combineCyclesHorizontal(self, graph, x1, x2, y):
        #exploring top edge of central rectangle
        for i in range(x1, x2):
            v1 = self.spaceID((i, y))
            v2 = self.spaceID((i+1, y))
            v3 = self.spaceID((i, y+1))
            v4 = self.spaceID((i+1, y+1))
            
            #found parallel edges!
            if graph.adjacent(v1, v2) and graph.adjacent(v3, v4):
                graph.addEdge(v1, v3)
                graph.addEdge(v2, v4)
                graph.removeEdge(v1, v2)
                graph.removeEdge(v3, v4)
                return True
            
        return False
    
    #combines adjacent hamiltonian cycles within grid along vertical boundary
    #@param graph - graph with each edge being part of hamiltonian cycle for subgraph
    #   graph based on game grid
    #@param x - col number of boundary between cycles
    #@param y1 - row number of uppermost space in vertical boundary between cycles
    #@param y2 - row number of lowermost space in verticl boundary between cycles
    #analyzes spaces for x in [x, x+1], y in [y1, y2] for possible way to join
    #   both surround hamiltonian cycles into 1. if cycles joined successfully
    #   somewhere across vertical boundary, returns True, else returns False
    def __combineCyclesVertical(self, graph, x, y1, y2):
        #exploring top edge of central rectangle
        for j in range(y1, y2):
            v1 = self.spaceID((x, j))
            v2 = self.spaceID((x, j+1))
            v3 = self.spaceID((x+1, j))
            v4 = self.spaceID((x+1, j+1))
            
            #found parallel edges!
            if graph.adjacent(v1, v2) and graph.adjacent(v3, v4):
                graph.addEdge(v1, v3)
                graph.addEdge(v2, v4)
                graph.removeEdge(v1, v2)
                graph.removeEdge(v3, v4)
                return True
            
        return False
                        
    #counts number of empty spaces that can hurt endgame for given snake
    #@param snakeCoords - deque of snake space coordinates
    #returns integer number of vacant spaces considered unfriendly for engame
    def badVacantSpaces(self, snakeCoords):
        grid = self.game.blankGrid(self.game.cols, self.game.rows)
        self.game.fillGridWithSnake(grid, snakeCoords)
        #self.game.printGrid(grid)
        count = 0
        
        #examining spaces 1 by 1
        for i in range(1, self.game.cols+1):
            for j in range(1, self.game.rows+1):
                #checking if space is in 1x1 vacant zone
                if self.badVacantSpace(i, j, grid):
                    count += 1
                
        return count
    
    #checks if a space is empty and surrounded by occupied spaces
    #@param col - column number of space
    #@param row - row number of space
    #@param grid - game grid. uses current game state by default.
    #returns True if space is empty and surrounded by occupied spaces
    def unitVacantSpace(self, col, row, grid=None):
        #checking if grid inputted
        if grid == None:
            grid = self.game.grid
            
        #checking if space empty
        if grid[col][row] != "o":
            return False
        
        neighbors = self.adjacentInboundSpaceCoords((col, row))
        symbols = {grid[s[0]][s[1]] for s in neighbors}
        
        return "o" not in symbols 
    
    #checks if a space is empty and could lead to issues with endgame later
    #@param col - column number of space
    #@param row - row number of space
    #@param grid - game grid. uses current game state by default.
    #returns True if space is empty and surrounded by occupied spaces,
    #   with the exception of a head AND tail space
    def badVacantSpace(self, col, row, grid=None):
        #checking if grid inputted
        if grid == None:
            grid = self.game.grid
        
        #checking if space if empty and surrounded by occupied spaces
        if not self.unitVacantSpace(col, row, grid):
            return False
        
        neighbors = self.adjacentInboundSpaceCoords((col, row))
        symbols = {grid[s[0]][s[1]] for s in neighbors}
        
        return "H" not in symbols or "T" not in symbols
    
    #checks if a given snake can avoid inevitable game over down the line
    #@param snakeCoords - deque of snake space coordinates
    #returns True if snake can avert game over, False otherwise
    def snakeSafe(self, snakeCoords):
        return len(self.headTailPath(snakeCoords)) > 0