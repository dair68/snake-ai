#module that hosts SurviveAI class
from ai.snakeAI import SnakeAI

#ai class that focuses on having the snake not die
class SurviveAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        SnakeAI.__init__(self, game)
        
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses space that will prevent game over both short and long term
    def nextMove(self):
        pass