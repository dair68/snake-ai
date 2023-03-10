#module that hosts SurviveAI class
from ai.snakeAI import SnakeAI
import randomElement as r
from ai.dumbAI import DumbAI

#ai class that focuses on having the snake not die
class SurviveAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
    
    #finds spaces snake can safely move to next turn
    #returns set of space coords that snake can move next without game over
    def safeMoves(self):
        return self.getAnalyzer().safeMoves()
    
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses random space that will prevent game over both short and long term
    def nextMove(self):
        moves = self.safeMoves()
        
        #checking if safe moves exists
        if len(moves) > 0:
            print("survive move")
            return r.randElement(self.safeMoves())
        else:
            print("no safe moves found. :(")
            ai = DumbAI(self.getGame())
            return ai.nextMove()