#module hosting AdvancedSnakeAnalyzer class
from ai.analyzer import SnakeAnalyzer

#class that incorporates hamiltonian cycles into analysis
class AdvancedSnakeAnalyzer(SnakeAnalyzer):
    #constructor
    #@param game - SnakeGame object that this object will analyze
    def __init__(self, game):
        super().__init__(game)
    
    #finds rect bounding specific point in grid that allows for hamiltonian cycle
    #@param col - column number of coordinate
    #@param row - row number of coordinate
    #returns rectangle as tuple of form (x1, y1, x2, y2) 
    #   where (x1,y1) is upper left coord and (x2,y2) is bottom right coord
    def coordBoundingRect(self, col, row):
        game = self.getGame()
        assert game.snakeLength() == 1
        (col, row) = game.headCoords()
        cols = game.cols
        rows = game.rows
        rect = [col, row, col, row]
    
        #analyzing squares bounding snake square
        if self.coordsInBounds(col-1, row-1) and self.coordsInBounds(col, row):
            rect[0] = col - 1 
            rect[1] = row - 1
        elif self.coordsInBounds(col, row-1) and self.coordsInBounds(col+1, row):
            rect[1] = row - 1 
            rect[2] = col + 1
        elif self.coordsInBounds(col-1, row) and self.coordsInBounds(col, row+1):
            rect[0] = col - 1 
            rect[3] = row + 1
        else:
            rect[2] = col + 1
            rect[3] = row + 1
        
        self.__adjustRect(rect)
        return rect

    #adjusts dimensions of rectangle to ensure hamiltonian cycle could occur
    #@param rect - list of form [x1, y1, x2, y2]
    #   (x1, y1) is upper corner, (x2, y2) is lower corner
    def __adjustRect(self, rect):
        self.__createEvenMargins(rect)
        self.__createEvenRect(rect)

    #adjust dimensions of rectangle to ensure surround rectangles are even
    #@param rect - list of form [x1, y1, x2, y2]
    #   (x1, y1) is upper corner, (x2, y2) is lower corner
    def __createEvenMargins(self, rect):
        x1, y1, x2, y2 = rect
        game = self.getGame()
    
        leftMargin = x1 - 1
        rightMargin = game.cols  - x2
        upperMargin = y1 - 1
        lowerMargin = game.rows - y2
    
        #ensuring even margins
        if leftMargin*game.rows % 2 == 1 or leftMargin == 1:
            rect[0] -= 1
        if rightMargin*game.rows % 2 == 1 or rightMargin == 1:
            rect[2] += 1
        if upperMargin*game.cols % 2 == 1 or upperMargin == 1:
            rect[1] -= 1
        if lowerMargin*game.cols % 2 == 1 or lowerMargin == 1:
            rect[3] += 1

    #adjust dimensions of rectangle to ensure rectangle (and margins) even
    #@param analyzer - SnakeGameAnalyzer for a given snake game
    #@param rect - list of form [x1, y1, x2, y2]
    #   (x1, y1) is upper corner, (x2, y2) is lower corner
    def __createEvenRect(self, rect):
        x1, y1, x2, y2 = rect
        game = self.getGame()
    
        #checking if rectangle has even area
        if not self.__evenRect(x1, y1, x2, y2):
            #ensuring rectangle has even area
            if x1 > 3 and (x1 - 2)*game.rows % 2 == 0:
                rect[0] -= 1
            elif x2 < game.cols - 3 and (game.cols - x2 - 1)*game.rows % 2 == 0:
                rect[1] += 1
            elif y1 > 3 and (y1 - 2)*game.cols % 2 == 0:
                rect[2] -= 1
            else:
                rect[3] += 1
    
    #checks if a given rectangle has even area
    #@param x1 - upper left column number
    #@param y1 - upper left row number
    #@param x2 - lower right column number
    #@param y2 - lower right row number
    def __evenRect(self, x1, y1, x2, y2):
        m = x2 - x1 + 1
        n = y2 - y1 + 1
        return m*n % 2 == 0