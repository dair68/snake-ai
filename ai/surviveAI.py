#module that hosts SurviveAI class
from ai.snakeAI import SnakeAI
import randomElement as r

#ai class that focuses on having the snake not die
class SurviveAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        
    #finds shortest paths to tail from spaces near head
    #returns list of tail paths found, each path being deque of space coords
    def tailPaths(self):
        return self.getAnalyzer().tailPaths()
    
    #finds spaces snake can safely move to next turn
    #returns set of space coords that snake can move next without game over
    def safeMoves(self):
        return {path[0] for path in self.tailPaths()}
    
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses random space that will prevent game over both short and long term
    def nextMove(self):
        print("survive move")
        return r.randElement(self.safeMoves())