#module hosting DumbAI class
from ai.snakeAI import SnakeAI
from randomElement import randElement

#class that recommends suboptimal moves for a given snake game
class DumbAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object
    def __init__(self, game):
        SnakeAI.__init__(self, game)
        
    #reports random move for the snake to make next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    def nextMove(self):
        moves = self.possibleMoves()
        return randElement(moves)