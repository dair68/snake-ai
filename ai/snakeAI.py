#module for hosting the snakeAI class
from ai.analyzer import SnakeAnalyzer

#base class for all snake game ai classes
class SnakeAI():
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    #@param moveMatrix - matrix where arr[i][j] is set of all spaces snake can
    #   move to from coordinate (i,j). optional.
    def __init__(self, game, moveMatrix=None):
        self.analyzer = SnakeAnalyzer(game, moveMatrix)
        self.reset()
    
    #lets user change the game being analyzed by this ai
    #@param game - SnakeGame object that ai will recommend moves for
    def setGame(self, game):
        self.analyzer = SnakeAnalyzer(game)
        
    #obtains game being analyzed
    #returns reference to game attached to ai
    def getGame(self):
        return self.analyzer.getGame()
    
    #obtains analyzer used to obtain game data
    #returns SnakeGameAnalyzer object
    def getAnalyzer(self):
        return self.analyzer
    
    #reports all possible moves snake can make at the moment
    #returns set of space coords of form (col, row)
    def possibleMoves(self):
        return self.analyzer.moveCoords()
    
    #has ai search the grid to recalibrate move recommendations
    #run this if the game hasn't been following all the prev 
    #   move recs since last refresh
    def reset(self):
        print("reinitializing ai")
        
    #updates game data stored in ai
    #run this after following a move recommended by self.nextMove()
    def update(self):
        print("updating ai")
    
    #recommends a space for snake to visit next
    #returns tuple of from (colNum, rowNum) 
    #   chooses first accessible space it finds
    #   run self.update() after following move returned by function
    def nextMove(self):
        print("snake ai move")
        moves = self.possibleMoves()
        return next(iter(moves))