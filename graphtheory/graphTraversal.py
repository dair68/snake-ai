#module which a variety of graph traversal functions

from collections import deque
from queue import Queue

#finds the path between two vertices that traverses the fewest number of edges
#@param graphAdjList - dict mapping node integer ids to set of node integer ids of neighboring vertices
#@param startVertex - integer id number of start vertex
#@param targetVertex - integer id number of targaet vertex
#returns deque of vertex ids representing shortest path from startVertex to targetVertex, if it exists
def shortestPath(graphAdjList, startVertex, targetVertex):
    pathData = singleSourceShortestPaths(graphAdjList, startVertex, {targetVertex})
    return pathData[targetVertex]

#finds paths between one vertex and other vertices that contains fewest number of edges
#@param graphAdjList - dict mapping node integer ids to set of node integer ids of neighboring vertices
#@param startVertex - integer id number of start vertex
#@param targetVertices - set of vertex ids for which paths are to be found.
#   chooses set of all vertices in graph by default
#returns dict mapping vertex ids to deques of ids making up shortes path to them
def singleSourceShortestPaths(graphAdjList, startVertex, targetVertices=None):
    #initializing targetVertices if needed
    if targetVertices == None:
        targetVertices = {vertex for vertex in graphAdjList}
    
    visitStatus = {v:False for v in graphAdjList}
    visitStatus[startVertex] = True
    remainingTargets = set(targetVertices)
    remainingTargets.discard(startVertex)
    parentIDs = {startVertex: -1}
    nextNodes = Queue(maxsize=len(graphAdjList))
    nextNodes.put_nowait(startVertex)
    
    #exploring nodes
    while not nextNodes.empty():
        #checking if all targets have been found
        if len(remainingTargets) == 0:
            break
        
        node = nextNodes.get_nowait()
        
        #adding unexplored neighbors to queue
        for vertex in graphAdjList[node]:
            #vertex unexplored
            if visitStatus[vertex] == False:
                visitStatus[vertex] = True
                parentIDs[vertex] = node
                remainingTargets.discard(vertex)
                nextNodes.put_nowait(vertex)
                
    paths = {v:deque() for v in targetVertices}
    
    #assembling paths
    for pathEnd in targetVertices:
        node = pathEnd
        while node in parentIDs:
            paths[pathEnd].appendleft(node)
            node = parentIDs[node]
        
    return paths