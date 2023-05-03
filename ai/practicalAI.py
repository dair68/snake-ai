#module hosting ai that will allow snake to win in reasonable timeframe
from ai.snakeAI import SnakeAI
from ai.advancedAnalyzer import AdvancedSnakeAnalyzer

class PracticalAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        self.analyzer = AdvancedSnakeAnalyzer(game)
        self.snakeRect = []
        cols = game.cols
        rows = game.rows
        self.moveMatrix = [[(-1,-1) for j in range(rows)] for i in range(cols)]          
        
    #has ai search the grid once more to recalibrate movement recommendations
    #run this if the game hasn't been following all the previous recommended moves
    def refreshAI(self):
        (col, row) = self.getGame().headCoords()
        a = self.getAnalyzer()
        self.snakeRect = a.coordBoundingRect(col, row)
        print(self.snakeRect)
        
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses space that will bring snake closer to pellet, while maintaining safety
    #   assumes game has been following previously recommended moves.
    #   if game has not been following every previous move, run self.refreshAI() first
    def nextMove(self):
        #checking if snake rect initialized
        if len(self.snakeRect) == 0:
            self.refreshAI()