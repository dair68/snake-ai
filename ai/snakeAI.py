#module for hosting the snakeAI class
from ai.snakeAnalysis import SnakeGameAnalyzer
from randomElement import randElement

class SnakeAI(SnakeGameAnalyzer):
    #constructor
    #@param game - SnakeGame object
    def __init__(self, game):
        SnakeGameAnalyzer.__init__(self, game)
        
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   space chosen is random
    def nextMove(self):
        moves = self.possibleMoves()
        return randElement(moves)