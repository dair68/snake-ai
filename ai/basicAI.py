#module hosting BasicAI class
from ai.snakeAI import SnakeAI
from collections import deque
from ai.surviveAI import SurviveAI

#class for ai that causes snake to pursue pellets while maintaining safety
class BasicAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        self.pelletPath = deque()
        
    #computes a path to the pellet from snake's current state
    #returns deque of space coords for path from snake head to pellet
    def findPelletPath(self):
        #return self.getAnalyzer().pelletPath()
        return self.getAnalyzer().safePelletPath()
    
    #has ai search the grid once more to recalibrate movement recommendations
    #run this if the game hasn't been following all the previously recommended 
    #   moves since the last refresh
    def reset(self):
        print("reinitializing ai")
        self.getAnalyzer().reset()
        self.pelletPath = deque()
    
    #updates game data stored in ai
    #run this after following a move recommended by self.nextMove()
    def update(self):
        self.getAnalyzer().update()
        
    #recommends a space for snake to visit next.
    #move chosen based on pellet proximity and safety
    #returns tuple of from (colNum, rowNum) 
    #   run self.update() after following move returned by function
    def nextMove(self):
        print("basic ai move")
         
        #checking if pellet path exists
        if len(self.pelletPath) <= 1:
             self.pelletPath = self.findPelletPath()
        
        print("pellet path: ")
        print(self.pelletPath)
        
        #recommending move
        if self.pelletPath:
            self.pelletPath.popleft()
            return self.pelletPath[0]
        else:
            ai = SurviveAI(self.getGame())
            return ai.nextMove()