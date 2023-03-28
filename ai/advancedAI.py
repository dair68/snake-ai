#module for hosting AdvancedAI class
from ai.snakeAI import SnakeAI
from collections import deque
from graphtheory.gridGraph import GridGraph
from graphtheory import hamiltonianCycle as h

#ai for snake game that accomplishes short pellet paths, safety, AND endgame movement
class AdvancedAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        self.loop = deque()
        self.pelletPath = deque()
        
    #has ai search the grid once more to recalibrate movement recommendations
    #run this if the game hasn't been following all the previously recommended 
    #   moves since the last refresh
    def refreshAI(self):
        print("refreshing ai")
        
        #checking if loop already found
        if len(self.loop) == 0:
            m = self.getGame().cols
            n = self.getGame().rows
            assert m*n % 2 == 0
            
            graph = GridGraph(m, n)
            cycle = h.gridHamiltonianCycle(graph)
            cycleCoords = deque([graph.vertexIndices(v) for v in cycle])
            self.loop = deque([(x+1,y+1) for (x,y) in cycleCoords])
            self.loop.pop()
            
            headCoords = self.getGame().headCoords()
            headIndex = self.loop.index(headCoords)
            self.loop.rotate(-headIndex)
           # print(self.loop)
           
    #finds information on path to pellet and updates self.pelletPath and self.loop
    def __updatePelletPathInfo(self):
        pathInfo = self.getAnalyzer().pelletPathInfo()
        pelletPath = pathInfo["pelletPath"] 
        escapePath = pathInfo["escapePath"]
        
        #checking if pellet path found
        if len(pelletPath) > 0:
            self.pelletPath = pelletPath
            self.loop = escapePath
            self.loop.pop()
            print("pellet path found: ")
            print(self.pelletPath)
            print("escape route found: ")
            print(self.loop)

    #finds and removes next recommended move from queue
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses move that allows snake to move around board in infinite loop
    def nextMove(self):
        print("advanced ai move")
        #checking if loop found
        if len(self.loop) == 0:
            self.refreshAI()
            
        #checking if pellet path exists
        if len(self.pelletPath) <= 1:
             self.__updatePelletPathInfo()
             
        #checking if pellet path found
        if len(self.pelletPath) > 1:
            print("chasing pellet")
            self.pelletPath.popleft()
            print("pellet path: ")
            print(self.pelletPath)
            return self.pelletPath[0]
        else:
            print("going down escape route")
            self.loop.rotate(-1)
            print("escape route: ")
            print(self.loop)
            return self.loop[0]