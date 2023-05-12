#module hosting ai that will allow snake to win in reasonable timeframe
from ai.snakeAI import SnakeAI
from ai.advancedAnalyzer import AdvancedSnakeAnalyzer

class AdvancedAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        self.analyzer = AdvancedSnakeAnalyzer(game)
        c = game.cols
        r = game.rows
        self.moveMatrix = [[() for j in range(r+2)] for i in range(c+2)]
        self.condensedGrid = [[0 for j in range(r//2)] for i in range(c//2)]
        
    def refreshAI(self):
        g = self.getGame()
        (x,y) = self.__condensedCoords(g.headCol(), g.headRow())
        self.__createMiniCycle(x, y)
  
    def nextMove(self):
        print("advanced ai move")
        game = self.getGame()
        col = game.headCol()
        row = game.headRow()
        
        #checking if any paths marked at all
        if not self.moveMatrix[col][row]:
            self.refreshAI()
            
        return self.moveMatrix[col][row]
    
    #maps regular grid coordinates to condensed coordinates
    #@param col - column number in self.moveMatrix
    #@param row - row number in self.moveMatrix
    #returns coords of space in self.condensedGrid corresponding to inputs
    #   returns empty tuple if condesnedGrid does not have a match
    def __condensedCoords(self, col, row):
        self.analyzer.assertValidCoords((col, row))
        game = self.getGame()
        
        #checking if out of bounds space inputted
        if col == 0 or col == game.cols+1 or row == 0 or row == game.rows+1:
            return ()
        
        a = min(col, game.cols - 1)
        x = (a - 1)//2
        
        b = min(row, game.rows - 1)
        y = (b - 1)//2
        return (x, y)
    
    #creates tiny cycle within self.moveMatrix corresponding to spot 
    #   in condensed matrix
    #@param col - col num for self.condensedMatrix
    #@param row - row num for self.condensedMatrix
    def __createMiniCycle(self, col, row):
        game = self.getGame()
        shifts = []
        
        #determining what shifts look like
        if col == len(self.condensedGrid) - 1 and game.cols % 2 == 1:
            shifts = [(1,0), (1,0), (0,1), (-1,0), (-1,0), (0,-1)]
        elif row == len(self.condensedGrid[0]) - 1 and game.rows % 2 == 1:
            shifts = [(1,0), (0,1), (0,1), (-1,0), (0,-1), (0,-1)]
        else:
            shifts = [(1,0), (0,1), (-1,0), (0,-1)]
        
        x = 2*col + 1
        y = 2*row + 1
        
        #filling move matrix
        for shift in shifts:
            newCoords = (x + shift[0], y + shift[1])
            self.moveMatrix[x][y] = newCoords
            (x, y) = newCoords