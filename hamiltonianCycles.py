# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import deque

#searching for a hamiltonian cycle within a graph
#@param graphHashMap - dict mapping node integer ids to set of node integer ids of neighboring vertices
#returns deque of vertex numbers representing path, if it exists. 1st and last ids will be same.
def findHamiltonianCycle(graphHashMap):
    return hamiltonianHelper(graphHashMap)
    
#helper function for findHamiltonianCycle()
#@param graphHashMap - dict mapping node integer ids to set of node integer ids of neighboring vertices
#@param path - deque of current path formed. deque([0]) by default
#@param visited - set of current nodes visited on current path. empty set by default
#returns deque of vertex numbers representing path, if it exists. 1st and last ids will be same.
def hamiltonianHelper(graphHashMap, path=None, visited=None):
    #setting path to empty list if needed
    if path == None:
        startVertex = next(iter(graphHashMap))
        path = deque([startVertex])
        
    #setting visited to empty set if needed
    if visited == None:
        visited = set(path)
        
    currentVertex = path[-1] if len(path) > 0 else 0
    neighbors = graphHashMap[currentVertex]
    
    #exploring graph until cycle found
    for vertex in neighbors:
        #vertex hasn't been visited
        if vertex not in visited:
            path.append(vertex)
            visited.add(vertex)
            possiblePath = hamiltonianHelper(graphHashMap, path, visited)
            
            #found cycle!
            if len(possiblePath) > 0:
                return possiblePath
            else:
                path.pop()
                visited.remove(vertex)
                
    #checking if final vertex leads back to the first
    if len(path) == len(graphHashMap) and path[0] in neighbors:
        path.append(path[0])
        return path
    else:
        return deque()