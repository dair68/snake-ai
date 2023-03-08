#module for hosting the snakeAI class
from ai.snakeAnalysis import SnakeGameAnalyzer
from randomElement import randElement

#base class for all snake game ai classes
class SnakeAI(SnakeGameAnalyzer):
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    def __init__(self, game):
        SnakeGameAnalyzer.__init__(self, game)
        
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses first accessible space it finds
    def nextMove(self):
        print("snake ai move")
        moves = self.possibleMoves()
        iterator = iter(moves)
        return next(iterator)