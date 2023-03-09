#module hosting DumbAI class
from ai.snakeAI import SnakeAI
import randomElement as r

#class that recommends suboptimal moves for a given snake game
class DumbAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object
    def __init__(self, game):
        super().__init__(game)
        
    #reports random space for the snake to make next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    def nextMove(self):
        print("dumb ai move")
        moves = self.analyzer.possibleMoves()
        #print(f"moves: {moves}")
        return r.randElement(moves)