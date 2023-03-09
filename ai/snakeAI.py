#module for hosting the snakeAI class
from ai.snakeAnalysis import SnakeGameAnalyzer

#base class for all snake game ai classes
class SnakeAI():
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    def __init__(self, game):
        self.analyzer = SnakeGameAnalyzer(game)
    
    #lets user change the game being analyzed by this ai
    #@param game - SnakeGame object that ai will recommend moves for
    def setGame(self, game):
        self.analyzer = SnakeGameAnalyzer(game)
        
    #obtains game being analyzed
    #returns reference to game attached ai
    def getGame(self):
        return self.analyzer.getGame()
    
    #finds a space for snake to move to next
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses first accessible space it finds
    def nextMove(self):
        print("snake ai move")
        moves = self.analyzer.possibleMoves()
        iterator = iter(moves)
        return next(iterator)