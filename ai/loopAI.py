#module hosting the LoopAI class
from ai.snakeAI import SnakeAI
from collections import deque
import graphtheory.hamiltonianCycle as h
from graphtheory.gridGraph import GridGraph

#class that has snake move around board in a loop
class LoopAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        self.loop = deque()
        
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
            
    #finds and removes next recommended move from queue
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses move that allows snake to move around board in infinite loop
    def nextMove(self):
        print("loop move")
        #checking if loop found
        if len(self.loop) == 0:
            self.refreshAI()
            
        self.loop.rotate(-1)
        return self.loop[0]