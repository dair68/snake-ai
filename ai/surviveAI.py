#module that hosts SurviveAI class
from ai.snakeAI import SnakeAI
import randomElement as r

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
    
    #has ai search the grid once more to recalibrate move recommendations
    #run this if the game hasn't been following all the previous
    #   move recs since the last refresh
    def reset(self):
        print("setting up graph")
        self.getAnalyzer().reset()
    
    #updates game data stored in ai
    #run this after following a move recommended by self.nextMove()
    def update(self):
        self.getAnalyzer().update()
    
    #recommends a space for snake to visit next
    #returns tuple of from (colNum, rowNum) 
    #   chooses random space that avoids eventual game over
    #   run self.update() after following move returned by function
    def nextMove(self):
        print("survive move")
        moves = self.safeMoves() 
        return r.randElement(self.safeMoves())