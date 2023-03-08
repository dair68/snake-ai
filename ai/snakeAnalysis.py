#module that hosts SnakeGameAnalyzer class

#class with a bunch of functions that obtain data from a particular snake game
class SnakeGameAnalyzer:
    #constructor
    #@param game - SnakeGame object that this object will analyze
    def __init__(self, game):
        self.game = game
        
    #reports all possible moves the snake can make it's current state
    #returns set of space coords of form (colNum, rowNum). includes game over moves
    def possibleMoves(self):
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
        #checking if valid id
        if not self.validSpaceID(spaceID):
            print("Error. Invalid space id inputted.")
            return set()
        
        coords = self.spaceCoords(spaceID)
        return {self.spaceID(s) for s in self.adjacentSpaceCoords(coords)}
    
    #finds all spaces adjacent to given space that is in area that 
    #   won't result in out of bounds game over
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in question
    #returns set of space coords for adjacent spaces not within game over zone
    def adjacentInboundSpaceCoords(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        neighbors = self.adjacentSpaceCoords(spaceCoords)
        return {space for space in neighbors if self.spaceInBounds(space)}
    
    #finds all space adjacent to given space that is in area that 
    #   won't result in out of bounds game over
    #@param spaceID - integer id number for space in question
    #returns set of space ids for adjacent spaces not within game over zone
    def adjacentInboundSpaceIDs(self, spaceID):
        #checking if valid id inputted
        if not self.validSpaceID(spaceID):
            print("Error. Invalid space id inputted.")
            return set()
        
        coords = self.spaceCoords(spaceID)
        return {self.spaceID(s) for s in self.adjacentInboundSpaceCoords(coords)}
    
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
    #returns dict mapping space ids to set of space ids for visitable adjacent spaces
    #   does not include spaces within game over zone. snake spaces considered inaccessible
    def inboundGridAdjacencyList(self):
        vertexMap = {}
        
        #adding nodes to adjacency list
        for spaceID in range(self.game.cols*self.game.rows):
            coords = self.spaceCoords(spaceID)
         
            #checking if space is occupied
            if not self.snakeSpace(coords):
                vertexMap[spaceID] = set()
                neighbors = self.adjacentInboundSpaceCoords(coords)
            
                #figuring out which neighboring spaces are accessible
                for (x, y) in neighbors:
                    #checking if space empty
                    if not self.snakeSpace((x, y)):
                        vertexMap[spaceID].add(self.spaceID((x, y)))
                
        return vertexMap
                
    #checking if certain space in game grid contains snake segment
    #@param spaceCoords - tuple of form (colNum, rowNum) describing space coordinates
    #returns True is snake is currently occupying inputted space within grid
    def snakeSpace(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        snakeSymbols = {"H", "S", "T"}
        (col, row) = spaceCoords
        
        return self.game.grid[col][row] in snakeSymbols
    
    #obtains space id for a pair of space coordinates
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in grid
    #returns integer corresponding to the space's id number
    def spaceID(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        (col, row) = spaceCoords
        
        #finding id number depending on if space causes out of bounds game over
        if self.spaceInBounds(spaceCoords):
            return (col - 1) % self.game.cols + self.game.cols*(row - 1)
        else:
            return self.__gameOverSpaceID(spaceCoords)
        
        return -1
    
    #obtains space id for a pair of space coordinates in out of bounds game over area
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in grid
    #returns integer id corresponding to the space's id number
    def __gameOverSpaceID(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        assert not self.spaceInBounds(spaceCoords)
            
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
        #checking if space id is valid
        if not self.validSpaceID(spaceID):
            print("Error. Invalid spaceID inputted.")
            return ()
         
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
        #checking if valid space id
        if not self.validSpaceID(spaceID):
            print("Error. Invalid space id inputted.")
            return ()
        elif spaceID < self.game.cols*self.game.rows:
            print("Error. Inbound space id inputted.")
            return ()
        else:
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
    def spaceInBounds(self, spaceCoords):
        self.assertValidSpaceCoords(spaceCoords)
        
        (col, row) = spaceCoords
        
        return self.columnInBounds(col) and self.rowInBounds(row)
        
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