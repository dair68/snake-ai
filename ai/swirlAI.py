#module hosting SwirlAI class
from ai.snakeAI import SnakeAI
from ai.surviveAI import SurviveAI
from collections import deque
from graphtheory.gridGraph import GridGraph
import graphtheory.hamiltonianCycle as h
import randomElement as rand

#class that has snake chase pellets while conforming to swirl pattern
class SwirlAI(SnakeAI):
    #constructor
    #@param game - SnakeGame object that ai will recommend moves for
    def __init__(self, game):
        super().__init__(game)
        self.pelletPath = deque()
        self.swirlMap = {}
        self.escapePath = deque()
        
    #has ai search the grid once more to recalibrate movement recommendations
    #run this if the game hasn't been following all the previously recommended 
    #   moves since the last refresh
    def refreshAI(self):
        print("refreshing ai")
        self.__createSwirlMap()
        # print(self.loop)
    
    #creates swirl pattern.
    #returns deque of space coordinates forming swirl
    def __createLoop(self):
        m = self.getGame().cols
        n = self.getGame().rows
        assert m*n % 2 == 0
            
        graph = GridGraph(m, n)
        cycle = h.gridHamiltonianCycle(graph)
        cycleCoords = deque([graph.vertexIndices(v) for v in cycle])
        loop = deque([(x+1,y+1) for (x,y) in cycleCoords])
        loop.pop()
            
        headCoords = self.getGame().headCoords()
        headIndex = loop.index(headCoords)
        loop.rotate(-headIndex)
        return loop
            
    #initializes self.swirlMap with a swirl pattern.
    #self.swirlMap with be dict mapping space coords to space coords.
    #maps a space to next space in swirl
    def __createSwirlMap(self):
        loop = self.__createLoop()
        swirl = list(loop)
        
        #iterating over list
        for i in range(len(swirl)):
            key = swirl[i]
            value = swirl[(i+1) % len(swirl)]
            self.swirlMap[key] = value
            
        #print(self.swirlMap)
           
    #finds pellet path for current snake. 
    #stores path in self.pelletPath as deque of space coords
    def __updatePelletPath(self):
        analyzer = self.getAnalyzer()
        possiblePath = analyzer.fastPelletPath()
        
        #checking if path found
        if len(possiblePath) > 0:
            futureSnake = analyzer.futureSnakeCoords(possiblePath, None, possiblePath[-1])
            #print(futureSnake)
        
            #checking if future snake has route to tail
            if self.__swirlSafeSnake(futureSnake): 
                self.pelletPath = possiblePath
                return
        
        self.pelletPath = deque()
        
    #checks if a snake can safely follow swirl pattern from current position
    #@param snake - deque of space coords
    #returns True if snake can safely travel down a number of swirl spaces 
    #   at least size of it's body
    #   updates self.escapePath with escape path found
    def __swirlSafeSnake(self, snake):
        #print(f"snake: {snake}")
        swirlPath = deque([snake[0]])
        snakeSegs = set(snake)
        pathSpace = self.swirlMap[swirlPath[-1]]
        
        #constructing swirl path
        while pathSpace not in snakeSegs:
            swirlPath.append(pathSpace)
            pathSpace = self.swirlMap[swirlPath[-1]]
            
        print(f"swirlPath: {swirlPath}")
        
        #checking if post pellet path is helpful
        if len(swirlPath) < len(snake) and pathSpace != snake[-1]:
            return False
        
        pathCopy = deque(swirlPath)
        print(f"escapePath: {self.escapePath}")
        swirlPath.popleft()
        finalSnake = deque(snake)
        finalSnake.extendleft(swirlPath)
        #print(f"finalSnake: {finalSnake}")
        
        #the path is safe!
        if self.getAnalyzer().snakeSafe(finalSnake):
            self.escapePath = pathCopy
            return True
        else:
            return False
           
    #finds and removes next recommended move from queue
    #returns tuple of from (colNum, rowNum) for space that snake is to visit next
    #   chooses move that allows guides snake with swirl pattern
    def nextMove(self):
        print("swirl move")
        
        #checking if swirl has been initialized
        if len(self.swirlMap) == 0:
            self.refreshAI()
            
        #checking if pellet path exists
        if len(self.pelletPath) <= 1:
             self.__updatePelletPath()
             
        #checking if pellet path found
        if len(self.pelletPath) > 0:
            print("chasing pellet")
            self.pelletPath.popleft()
            return self.pelletPath[0]
        elif len(self.escapePath) > 1:
            print("escape path")
            self.escapePath.popleft()
            return self.escapePath[0]
        else:
            moves = self.getAnalyzer().safeMoves()
            head = self.getGame().headCoords()
            swirlMove = self.swirlMap[head]
            
            #checking if swirl move is safe
            if swirlMove in moves:
                print("going down swirl")
                return swirlMove
            else:
                print("safe move")
                return rand.randElement(moves)