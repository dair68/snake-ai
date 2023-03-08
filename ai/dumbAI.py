#module hosting DumbAI class
from ai.snakeAI import SnakeAI
import random

#class that recommends suboptimal moves for a given snake game
class DumbAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object
    def __init__(self, game):
        SnakeAI.__init__(self, game)
        
    #reports random space for the snake to make next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    def nextMove(self):
        print("dumb ai move")
        moves = self.possibleMoves()
        #print(f"moves: {moves}")
        return random.sample(moves, 1)[0]