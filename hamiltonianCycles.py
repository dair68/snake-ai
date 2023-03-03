# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import deque

#searching for a hamiltonian cycle within a graph
#@param graphMatrix - 2 by 2  of integers describing which nodes have paths between them.
#   graphMatrix[v1][v2] = 1 if there's an edge between vertices v1 and v2, 0 otherwise
#returns list of vertex numbers representing path, if it exists
def findHamiltonianCycle(graphMatrix):
    return list(hamiltonianHelper(graphMatrix))
    
#helper function for findHamiltonianCycle()
#@param graphMatrix - 2 by 2  of integers describing which nodes have paths between them.
#   graphMatrix[v1][v2] = 1 if there's an edge between vertices v1 and v2, 0 otherwise
#@param path - deque of current path formed. deque([0]) by default
#@param visited - set of current nodes visited on current path. empty set by default
#returns deque of vertex numbers representing path, if it exists
def hamiltonianHelper(graphMatrix, path=None, visited=None):
    #setting path to empty list if needed
    if path == None:
        path = deque([0])
        
    #setting visited to empty set if needed
    if visited == None:
        visited = set()
        
    currentVertex = path[-1] if len(path) > 0 else 0
    neighbors = vertexNeighbors(currentVertex, graphMatrix) 
    
    #exploring graph until cycle found
    for vertex in neighbors:
        #vertex hasn't been visited
        if vertex not in visited:
            path.append(vertex)
            visited.add(vertex)
            possiblePath = hamiltonianHelper(graphMatrix, path, visited)
            
            #found cycle!
            if len(possiblePath) > 0:
                return possiblePath
            else:
                path.pop()
                visited.remove(vertex)
                
    #checking if final vertex leads back to the first
    if len(path) == len(graphMatrix) and path[0] in neighbors:
        path.append(path[0])
        return path
    else:
        return deque()
    
#finds all vertices adjacent to a given vertex
#@param vertexNum - integer representing the id number of vertex in question
#@param graphMatrix - 2 by 2  of integers describing which nodes have paths between them.
#   graphMatrix[v1][v2] = 1 if there's an edge between vertices v1 and v2, 0 otherwise
#returns set of vertex numbers repsenting all vertices adjacent to vertextNum
def vertexNeighbors(vertexNum, graphMatrix):
    return {v for v in range(len(graphMatrix)) if graphMatrix[vertexNum][v] == 1}