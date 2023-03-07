#module that hosts SnakeGameAnalyzer class and randElement function
import random

#obtains random element from a list
#@param elements - list of elements
#returns random element from elements
def randElement(elements):
    #checking if list is nonempty
    if len(elements) == 0:
        print("Error. Empty list inputted.")
        return None
    
    i = random.randrange(len(elements))
    return elements[i]

#class with a bunch of functions that obtain data from a particular snake game
class SnakeGameAnalyzer:
    #constructor
    #@param game - SnakeGame object that this object will analyze
    def __init__(self, game):
        self.game = game
        
    #reports all possible moves the snake can make it's current state
    #returns list of space coords of form (colNum, rowNum). includes game over moves
    def possibleMoves(self):
        moves = self.adjacentSpaces(self.game.headCoords())
        
        #all adjacent moves are valid if snake is stationary
        if self.game.headXVel == 0 and self.game.headYVel == 0:
            return moves

        filteredMoves = []
        
        #filtering out impossible moves
        for (col, row) in moves:
            xChange = col - self.game.headCol()
            yChange = row - self.game.headRow()
            
            #found possible move
            if xChange == 0 and yChange != -self.game.headYVel:
                filteredMoves.append((col, row))
            elif xChange != -self.game.headXVel and yChange == 0:
                filteredMoves.append((col, row))  
            
        return filteredMoves
    
    #finds all spaces adjacent to a given space
    #@param spaceCoords - tuple of form (colNum, rowNum) for space in question
    #returns list of space coords of form (colNum, rowNum) for all spaces adjacent to spaceCoords.
    #       includes game over moves
    def adjacentSpaces(self, spaceCoords):
        #checking if valide coordinates
        if not self.validCoords(spaceCoords):
            print("Error. Invalid coordinates inputted.")
            return []
        
        shifts = ((1, 0), (-1, 0), (0, 1), (0, -1))
        (x, y) = spaceCoords
        return [(x+u, y+v) for (u,v) in shifts if self.validCoords((x+u, y+v))]
    
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