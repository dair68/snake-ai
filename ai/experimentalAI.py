#module for hosting experimental ai
from ai.snakeAI import SnakeAI
from collections import deque
from ai.surviveAI import SurviveAI
import randomElement as r

#ai that attempts to win game in timely manner while taking into account endgame
class ExperimentalAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        self.pelletPath = deque()
        
    #has ai search the grid once more to recalibrate movement recommendations
    #run this if the game hasn't been following all the previous recommended moves
    def refreshAI(self):
        pass
        
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses space that will bring snake closer to pellet, while maintaining safety
    #   assumes game has been following previously recommended moves.
    #   if game has not been following every previous move, run self.refreshAI() first
    def nextMove(self):
        print("experimental ai move")
        pass