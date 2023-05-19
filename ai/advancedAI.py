#module hosting ai that will allow snake to win in reasonable timeframe
from ai.snakeAI import SnakeAI
from collections import deque
import random

class AdvancedAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object this ai will recommend moves for
    #   game MUST have even number of columns and rows!
    def __init__(self, game):
        assert game.rows % 2 == 0
        assert game.cols % 2 == 0
        
        moveMatrix = []
        randNum = random.randrange(2)
        
        #checking which random number chosen
        if randNum == 1:
            moveMatrix = self.__clockwiseMoveMatrix(game)
        else:
            moveMatrix = self.__counterclockwiseMoveMatrix(game)
        
        #print(moveMatrix)
        super().__init__(game, moveMatrix)
        self.pelletPath = deque()
        
    #creates move matrix built from 2x2 clockwise squares
    #@param game - snake game
    #returns matrix mapping space coords to set of space coords to travel to
    def __clockwiseMoveMatrix(self, game):
        r = game.rows + 2
        c = game.cols + 2
        moveMatrix = [[set() for j in range(r)] for i in range(c)]
        
        #filling moveMatrix
        for i in range(1, game.cols + 1):
            for j in range(1, game.rows + 1):
                moveSet = moveMatrix[i][j]
                
                #assigning move based on col row pair
                if i % 2 == 1 and j % 2 == 1:
                    moveSet.add((i, j-1))
                    moveSet.add((i+1, j))
                elif i % 2 == 0 and j % 2 == 1:
                    moveSet.add((i+1, j))
                    moveSet.add((i, j+1))
                elif i % 2 == 0 and j % 2 == 0:
                    moveSet.add((i-1, j))
                    moveSet.add((i, j+1))
                else:
                    moveSet.add((i-1, j))
                    moveSet.add((i, j-1))
                    
        return moveMatrix
    
    #creates move matrix built from 2x2 counter-clockwise squares
    #@param game - snake game
    #returns matrix mapping space coords to set of space coords to travel to
    def __counterclockwiseMoveMatrix(self, game):
        r = game.rows + 2
        c = game.cols + 2
        moveMatrix = [[set() for j in range(r)] for i in range(c)]
        
        #filling moveMatrix
        for i in range(1, game.cols + 1):
            for j in range(1, game.rows + 1):
                moveSet = moveMatrix[i][j]
                
                #assigning move based on col row pair
                if i % 2 == 1 and j % 2 == 1:
                    moveSet.add((i-1, j))
                    moveSet.add((i, j+1))
                elif i % 2 == 0 and j % 2 == 1:
                    moveSet.add((i, j-1))
                    moveSet.add((i-1, j))
                elif i % 2 == 0 and j % 2 == 0:
                    moveSet.add((i+1, j))
                    moveSet.add((i, j-1))
                else:
                    moveSet.add((i, j+1))
                    moveSet.add((i+1, j))
                    
        return moveMatrix
        
    #computes a path to the pellet from snake's current state
    #returns deque of space coords for path from snake head to pellet
    def findPelletPath(self):
        #return self.getAnalyzer().safePelletPath()
        return self.getAnalyzer().fastSafePelletPath()
    
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
        print("advanced ai move")
         
        #checking if pellet path exists
        if not self.pelletPath:
             self.pelletPath = self.findPelletPath()
             self.pelletPath.popleft()
        
        return self.pelletPath.popleft()