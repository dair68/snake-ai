# -*- coding: utf-8 -*-

from collections import deque

#searching for a hamiltonian cycle within a graph
#@param graph - SimpleUndirectedGraph object
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

#searching for a hamiltonian cycle within a rectangular grid graph
#@param graphAdjList - dict mapping node integer ids to set of node integer ids of neighboring vertices
#returns deque of vertex numbers representing path, if it exists. 1st and last ids will be same.
def rectGridHamiltonianCycle(graphAdjList):
    return hamiltonianHelper(graphAdjList)