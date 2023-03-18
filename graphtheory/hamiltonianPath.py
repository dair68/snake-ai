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
    
    #forming path from table data
    while mask > 0:
        #examining vertices within mask
        for j in range(len(pathData[0])):
            #no hamiltonian path ending in vertex j
            if pathData[mask][j] == False:
                continue
            
            lastVertexID = vertexIDs[lastVertex]
            vertexjID = vertexIDs[j]
            
            #adding vertex to path
            if lastVertex == -1 or graph.adjacent(lastVertexID, vertexjID):
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
    numVertices = len(graph.getVertices())
    vertexIDs = list(graph.getVertices())
    #print(vertexIDs)
    #pathData[i][j] is bool for whether mask i is h path containing vertex j at end
    pathData = hamiltonianPathMatrix(graph, vertexIDs)
    
    v1 = vertexIDs.index(startVertex)
    v2 = vertexIDs.index(finishVertex)
    
    #checking if there exists hamiltonian path with v2 as final vertex
    if pathData[-1][v2] == False:
        return deque()
    
    path = deque([v2])
    mask = len(pathData) - 1 - 2**v2
    lastVertex = v2
    
    #forming path from table data
    while mask > 0:
        #checking for penultimate iteration
        if len(path) == numVertices - 1:
            if mask == 2**v1:
                path.appendleft(v1)
                break
            else:
                return deque()
        
        lastMask = mask
        
        #examining vertices within mask
        for j in range(len(pathData[0])):
            #checking if j is equal to v1
            if j == v1:
                continue
            
            #no hamiltonian path ending in vertex j
            if pathData[mask][j] == False:
                continue
            
            lastVertexID = vertexIDs[lastVertex]
            vertexjID = vertexIDs[j]
            
            #adding vertex to path
            if lastVertex == -1 or graph.adjacent(lastVertexID, vertexjID):
                path.appendleft(j)
                lastVertex = j
                mask -= 2**j
                break
            
        #checking if mask has decreased
        if mask == lastMask:
            return deque()
        
    return deque([vertexIDs[mask] for mask in path])
    
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
                
                #analyzing path data for subset without node j
                for k in range(len(jCData)):
                    #checking there exists hamiltonian path with k as end node
                    if jCData[k] == False:
                        continue
                        
                    #checking if vertex k and j are adjacent
                    if graph.adjacent(vertexList[k], vertexList[j]):
                        pathData[i][j] = True
                        break
                    
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