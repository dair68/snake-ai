#module with functions for finding hamiltonian paths
import bitmask as bm
from collections import deque

#finds hamiltonian path within graph
#@param graph - UndirectedSimpleGraph object
#returns deque of vertex ids forming path. return empty deque if no path.
def hamiltonianPath(graph):
    numVertices = len(graph.getVertices())
    vertexIDs = list(graph.getVertices())
    #print(vertexIDs)
    #pathData[i][j] is bool for whether mask i is h path containing vertex j at end
    pathData = hamiltonianPathMatrix(graph, vertexIDs)
    #printPathTable(pathData)
    
    path = deque()
    mask = len(pathData) - 1
    lastVertex = -1
    vertexIndices = {vertexIDs[i]:i for i in range(len(vertexIDs))}
    
    #forming path from table data
    while mask > 0:
        vertexMarks = {}
        
        #determining which vertices to examine for path end
        if lastVertex == -1:
            vertexMarks = range(len(vertexIDs))
        else:
            vertexID = vertexIDs[lastVertex]
            neighbors = graph.neighbors(vertexID)
            vertexMarks = {vertexIndices[v] for v in neighbors}
        
        #examining neighbors of last vertex in path
        for j in vertexMarks:
            #found hamiltonian path ending in vertex j
            if pathData[mask][j] == True:
                path.appendleft(j)
                lastVertex = j
                mask -= 2**j
                break
            
        #checking if mask has decreased
        if mask == len(pathData) - 1:
            break
        
    return deque([vertexIDs[mask] for mask in path])

#finds hamiltonian path within graph that has 2 specific vertices as endpoints
#@param graph - UndirectedSimpleGraph object
#@param startVertex - integer vertex id of 1st vertex in path
#@param finishVertex - integer vertex id of last vertex i path
#returns deque of vertex ids forming path. return empty deque if no path.
def connectingHamiltonianPath(graph, startVertex, finishVertex):
    return hamiltonianHelper(graph, startVertex, finishVertex)

#helper function for connectingHamiltonianPath()
#@param graph - SimpleUndirectedGraph object
#@param startVertex - integer vertex id of 1st vertex in path
#@param finishVertex - integer vertex id of last vertex i path
#@param path - deque of current path formed. deque([0]) by default
#@param visitStatus - dict mapping node ids booleans indicating if they've been visited yet
#returns deque of vertex numbers representing path, if it exists
def hamiltonianHelper(graph, startVertex, finishVertex, path=None, visitStatus=None):
    #addressing special cases for extreme path lengths
    if path == None:
        path = deque([startVertex])
    elif len(path) > len(graph.getVertices()):
        return deque()
    elif len(path) == len(graph.getVertices()):
        #print("checking path")
        
        #checking if path has correct endpoints
        if path[0] != startVertex or path[-1] != finishVertex:
            return deque()
            
        return path if isHamiltonianPath(graph, path) else deque()
        
    #setting visited to empty set if needed
    if visitStatus == None:
        visitStatus = {v: False for v in graph.getVertices()}
        
        #marking nodes already in path as visited
        for vertex in path:
            visitStatus[vertex] = True
        
    currentVertex = path[-1] if len(path) > 0 else 0
    neighbors = graph.neighbors(currentVertex)
    
    #exploring graph until path found
    for vertex in neighbors:
        #vertex hasn't been visited
        if visitStatus[vertex] == False:
            path.append(vertex)
            #print(path)
            visitStatus[vertex] = True
            possiblePath = hamiltonianHelper(graph, startVertex, finishVertex,
                                             path, visitStatus)
            
            #found hamiltonian path!
            if len(possiblePath) > 0:
                return possiblePath
            else:
                #print("popping")
                path.pop()
                visitStatus[vertex] = False
                
    return deque()
    
#checks if a sequece of vertices forms a hamiltonian path for a given graph
#@param graph - UndirectedSimpleGraph object
#@param path - deque of vertex ids
#returns True is path is hamiltonian, False otherwise
def isHamiltonianPath(graph, path):
   #checking if path is correct length to possibly touch every node
   if len(path) != len(graph.getVertices()):
       return False
   
   pathList = list(path)
   visitStatus = {v: False for v in graph.getVertices()}
   
   #checking if all the vertices are adjacent and avoid revisiting
   for i in range(len(graph.getVertices())):
       vertex1 = pathList[i]
       
       #checking that vertex is unvisited
       if visitStatus[vertex1] == True:
           return False
       
       visitStatus[vertex1] = True
       
       #checking if past first vertex
       if i > 0:
           vertex2 = pathList[i-1]
       
           #vertices not adjacent
           if not graph.adjacent(vertex1, vertex2):
               return False
       
   return True
    
#creates matrix with info on hamiltonian paths within a graph
#@param graph - UndirectedSimpleGraph object
#@param vertexList - list of vertex ids for all vertices in graph
#return 2**n by n matrix with path data for graph
#   matrix[i][j] is bool indicating whether there's a hamiltonian path
#   for mask i ending with vertex j. j corresponds to vertex vertexList[j].
def hamiltonianPathMatrix(graph, vertexList):
    numVertices = len(graph.getVertices())
    #pathData[i][j] is bool for whether mask i is h path containing vertex j at end
    pathData = [[None for j in range(numVertices)] for i in range(2**numVertices)]
    #print(pathData)
    vertexIndices = {vertexList[i]:i for i in range(len(vertexList))}

    #filling in path table
    for i in range(len(pathData)):
        for j in range(len(pathData[0])):
            #filling table for different situations
            if bm.count(i) == 1:
                oneIndex = bm.first(i)
                pathData[i][j] = (oneIndex == j)
            elif bm.bit(j, i) == 1:
                jMask = 1 << j
                jCMask = i - jMask
                jCData = pathData[jCMask]
                neighbors = graph.neighbors(vertexList[j])
                neighborMarks = {vertexIndices[v] for v in neighbors}
                
                #analyzing path data for subset without node j
                for k in neighborMarks:
                    #checking there exists hamiltonian path with k as end node
                    if jCData[k] == True:
                        pathData[i][j] = True
                    
            #checking if path data still not assigned
            if pathData[i][j] == None:
                pathData[i][j] = False
                
    return pathData

#prints table storing hamiltonian path info
#@param table - 2**n by n table storing info about hamiltonian paths in graph
#prints entries of table[i][j] with i being row, j being column
#None=-1, True=1, False=0
def printPathMatrix(table):
    symbols = {None:"-1", True:" 1", False:" 0"}
    
    #printing each row 1 by 1
    for i in range(len(table)):
        row = table[i]
        rowNum = [symbols[row[j]] for j in range(len(row))]
        rowStr = "".join(rowNum)
        print(rowStr)