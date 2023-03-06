#module which a variety of graph traversal functions

from collections import deque
from queue import Queue

#finds the path between two vertices that traverses the fewest number of edges
#@param startVertex - integer id number of start vertex
#@param targetVertex - integer id number of targaet vertex
#@param graphAdjList - dict mapping node integer ids to set of node integer ids of neighboring vertices
#returns deque of vertex ids representing shortest path from startVertex to targetVertex, if it exists
def shortestPath(startVertex, targetVertex, graphAdjList):
    visitStatus = {v: False for v in graphAdjList}
    parentIDs = {startVertex: -1}
    nextNodes = Queue(maxsize=len(graphAdjList))
    nextNodes.put_nowait(startVertex)
    
    #exploring nodes
    while not nextNodes.empty():
        node = nextNodes.get_nowait()
        visitStatus[node] = True
        
        #checking if node is the targetVertex
        if node == targetVertex:
            break
        
        #adding unexplored neighbors to queue
        for vertex in graphAdjList[node]:
            #vertex unexplored
            if visitStatus[vertex] == False:
                parentIDs[vertex] = node
                nextNodes.put_nowait(vertex)
                
    path = deque()
    nodeID = targetVertex
    
    #assembling path
    while nodeID in parentIDs:
        path.appendleft(nodeID)
        nodeID = parentIDs[nodeID]
        
    return path