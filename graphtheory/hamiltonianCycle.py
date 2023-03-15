# -*- coding: utf-8 -*-
from collections import deque
from graphtheory.gridGraph import GridGraph
from graphtheory.graph import SimpleUndirectedGraph

#searching for a hamiltonian cycle within a graph
#@param graph - SimpleUndirectedGraph or GridGraph object
#returns deque of vertex ids representing path, if it exists. 1st and last ids will be same.
def hamiltonianCycle(graph):
    return hamiltonianHelper(graph)
    
#helper function for findHamiltonianCycle()
#@param graph - SimpleUndirectedGraph object
#@param path - deque of current path formed. deque([0]) by default
#@param visitStatus - dict mapping node ids booleans indicating if they've been visited yet
#returns deque of vertex numbers representing path, if it exists. 1st and last ids will be same.
def hamiltonianHelper(graph, path=None, visitStatus=None):
    #addressing special cases for extreme path lengths
    if path == None:
        startVertex = next(iter(graph.getVertices()))
        path = deque([startVertex])
    elif len(path) > len(graph.getVertices()) + 1:
        return False
    elif len(path) == len(graph.getVertices()) + 1:
        return isHamiltonianCycle(path, graph)
        
    #setting visited to empty set if needed
    if visitStatus == None:
        visitStatus = {v: False for v in graph.getVertices()}
        
        #marking nodes already in path as visited
        for vertex in path:
            visitStatus[vertex] = True
        
    currentVertex = path[-1] if len(path) > 0 else 0
    neighbors = graph.neighbors(currentVertex)
    
    #exploring graph until cycle found
    for vertex in neighbors:
        #vertex hasn't been visited
        if visitStatus[vertex] == False:
            path.append(vertex)
            visitStatus[vertex] = True
            possiblePath = hamiltonianHelper(graph, path, visitStatus)
            
            #found cycle!
            if len(possiblePath) > 0:
                return possiblePath
            else:
                path.pop()
                visitStatus[vertex] = False
                
    #checking if final vertex leads back to the first
    if len(path) == len(graph.getVertices()) and path[0] in neighbors:
        path.append(path[0])
        return path
    else:
        return deque()
    
#checks if a path is a hamiltonian cycle for a given graph
#@param path - deque of vertex ids forming path. first and last ids in path expected to be same for a cycle
#@param graph - SimpleUndirectedGraph object
#returns True if the path is a hamiltonian cycle, false otherwise
def isHamiltonianCycle(path, graph):
    #checking if path is correct length to possibly touch every node
    if len(path) != len(graph.getVertices()) + 1:
        return False
    
    #checking if vertices at ends of path are the same
    if path[0] != path[-1]:
        return False
    
    pathList = list(path)
    
    #checking if all the vertices are adjacent and avoid revisiting except at ends
    for i in range(len(graph.getVertices())):
        vertex1 = pathList[i]
        vertex2 = pathList[i+1]
        
        #vertices not adjacent
        if vertex2 not in graph.neighbors(vertex1):
            return False
        
    return True

#obtains a hamiltonian cycle within a rectangular grid graph, if it exists
#@param graph - GridGraph object
#returns deque of vertex ids representing path, if it exists. 1st and last ids will be same.
def gridHamiltonianCycle(graph):
    (m,n) = graph.dimensions()
    
    #checking if graph has odd number of vertices
    if m*n % 2 == 1:
        return deque()
    
    #checking if graph has 1 for one of its dimensions
    if m == 1 or n == 1:
        return deque()
    
    squares = gridGraphSquares(graph)
    colorHamiltonianSquares(squares)
    print(squares)
    graphCopy = SimpleUndirectedGraph(graph.getVertices(), graph.getEdges())
    
    #removing unnecessary edges from graphCopy based on squares
    for i in range(m-1):
        for j in range(n-1):
            upperLeft = graph.vertexAt(i,j)
            upperRight = graph.vertexAt(i+1,j)
            lowerLeft = graph.vertexAt(i,j+1)
            lowerRight = graph.vertexAt(i+1,j+1)
            
            #index is not far right
            if i < m-2:
                #checking if square and square to right are both filled or both empty
                if squares[i][j] == squares[i+1][j]:
                    graphCopy.removeEdge(upperRight, lowerRight)
                
            #index not on bottom row
            if j < n-2:
                #checking if square and square below are both filled or both empty
                if squares[i][j] == squares[i][j+1]:
                    graphCopy.removeEdge(lowerLeft, lowerRight)
                    
            #square empty
            if squares[i][j] == 0:
                #removing edges at edge of grid
                if i == 0:
                    graphCopy.removeEdge(upperLeft, lowerLeft)
                if j == 0:
                    graphCopy.removeEdge(upperLeft, upperRight)
                if i == m-2:
                    graphCopy.removeEdge(upperRight, lowerRight)
                if j == n-2:
                    graphCopy.removeEdge(lowerLeft, lowerRight)
                
    return hamiltonianCycle(graphCopy)
    
#obtains unit squares formed by the vertices of an mxn grid graph 
#@param graph - GridGraph object
#returns 2d nested lists of dimension (m-1)x(n-1).
#   square at matrix[i][j] corresponds to the square surrounded by vertices 
#   (i,j), (i+1,j), (i,j+1), and (i+1,j+1) in grid graph
def gridGraphSquares(graph):
    (m, n) = graph.dimensions()
    assert m > 1
    assert n > 1
    return [[None for j in range(n - 1)] for i in range(m - 1)]

#paints the square representation of grid graph to indicate hamiltonian cycle
#@param squares - matrix for which each entry represents unit square 
#   surrounded by vertices in grid graph. must have an odd dimension.
#fills squares with 1's and 0's with 1 meaning filled and 0 meaning empty
#   the hamiltonian path is obtained by tracing the vertices around 
#   the "filled" squares
def colorHamiltonianSquares(squares):
    m = len(squares)
    n = len(squares[0])
    assert m % 2 == 1 or n % 2 == 1
    
    #m is odd dimension
    if m % 2 == 1:
        #coloring every square
        for i in range(m):
            for j in range(n):
                squares[i][j] = 0 if i % 2 == 1 and j > 0 else 1
    else:
        #coloring every square
        for i in range(m):
            for j in range(n):
                squares[i][j] = 0 if j % 2 == 1 and i > 0 else 1