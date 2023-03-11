#module hosting GreedyAI class
from ai.snakeAI import SnakeAI
from collections import deque
from ai.surviveAI import SurviveAI

#class for ai that causes snake to gun for pellets impulsively
class GreedyAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        self.pelletPath = deque()
        
    #obtains path to pellet currently recorded by ai
    #returns deque of space coords for path from snake head to pellet. may be empty.
    def getPelletPath(self):
        return deque(self.pelletPath)
    
    #has ai search the grid once more to recalibrate movement recommendations
    #run this if the game hasn't been following all the previous recommended moves
    def refreshAI(self):
        self.pelletPath = self.getAnalyzer().fastPelletPath()
        
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses space that will bring snake closer to pellet, regardless of safety
    #   assumes game has been following previously recommened moves.
    #   if game has not been following every previous move, run self.refreshAI()
    #   to update move recommendations.
    def nextMove(self):
        print("greedy ai move")
        
        #checking if pellet path exists
        if len(self.pelletPath) <= 1:
            self.refreshAI()
            
        #recommending move
        if len(self.pelletPath) > 0:
            self.pelletPath.popleft()
            return self.pelletPath[0]
        else:
            ai = SurviveAI(self.getGame())
            return ai.nextMove()