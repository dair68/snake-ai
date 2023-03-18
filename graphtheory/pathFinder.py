#module which a variety of graph traversal functions
from graphtheory.graph import SimpleUndirectedGraph
from collections import deque
from queue import Queue

#finds the path between two vertices that traverses the fewest number of edges
#@param graph - SimpleUndirectedGraph object
#@param startVertex - integer id number of start vertex
#@param targetVertex - integer id number of targaet vertex
#returns deque of vertex ids representing shortest path from startVertex to targetVertex, if it exists
def shortestPath(graph, startVertex, targetVertex):
    pathData = singleSourceShortestPaths(graph, startVertex, {targetVertex})
    return pathData[targetVertex]

#finds paths between one vertex and other vertices that contains fewest number of edges
#@param graph - SimpleUndirectedGraph object
#@param startVertex - integer id number of start vertex
#@param targetVertices - set of vertex ids for which paths are to end.
#   chooses set of all vertices in graph by default
#returns dict mapping vertex ids to deques of ids making up shortest path to them
def singleSourceShortestPaths(graph, startVertex, targetVertices=None):
    #initializing targetVertices if needed
    if targetVertices == None:
        targetVertices = graph.getVertices()
    
    visitStatus = {v:False for v in graph.getVertices()}
    visitStatus[startVertex] = True
    remainingTargets = set(targetVertices)
    remainingTargets.discard(startVertex)
    parentIDs = {startVertex: -1}
    nextNodes = Queue(maxsize=len(graph.getVertices()))
    nextNodes.put_nowait(startVertex)
    
    #exploring nodes
    while not nextNodes.empty():
        #checking if all targets have been found
        if len(remainingTargets) == 0:
            break
        
        node = nextNodes.get_nowait()
        
        #adding unexplored neighbors to queue
        for vertex in graph.neighbors(node):
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

#finds paths leading to one vertex that contains fewest number of edges
#@param graph - SimpleUndirectedGraph object
#@param targetVertex - vertex id for which all paths end
#@param startVertices - integer id numbers of vertices for which paths begin
#   chooses set of all vertices in graph by default
#returns dict mapping vertex ids to deques of ids making up shortest path from them
def singleDestinationShortestPaths(graph, targetVertex, startVertices=None):
    pathData = singleSourceShortestPaths(graph, targetVertex, startVertices)
    
    #reversing the paths in path dictionary
    for path in pathData.values():
        path.reverse()
    
    return pathData

#finds the path between two vertices that traverses the fewest number of edges
#for a graphs where nodes have values indicating min number of edges from start 
#node they must be to be accessed
#@param graph - SimpleUndirectedGraph object.
#   each node within graph has integer value indicating number of edges that must
#   be traversed before it can be reached
#   many edges must be touches before node becomes accessible
#@param startVertex - integer id number of start vertex
#@param targetVertex - integer id number of targaet vertex
#returns deque of vertex ids representing shortest path from startVertex to targetVertex, if it exists
def distanceGatedShortestPath(graph, startNode, targetNode): 
    visitStatus = {v:False for v in graph.getVertices()}
    nextNodes = Queue(maxsize=len(graph.getVertices()))
    nodeDist = {}
    parentIDs = {}
    
    #checking if start node can be visited
    if graph.getVertexValue(startNode) == 0:
        visitStatus[startNode] = True
        parentIDs = {startNode: -1}
        nextNodes.put_nowait(startNode)
        nodeDist[startNode] = 0
    
    #exploring nodes
    while not nextNodes.empty():
        node = nextNodes.get_nowait()
        
        #checking if target has been found
        if node == targetNode:
            break
        
        #adding unexplored neighbors to queue
        for v in graph.neighbors(node):
            #checking if unexplored accessible vertex
            if visitStatus[v] == False and nodeDist[node]+1 >= graph.getVertexValue(v):
                visitStatus[v] = True
                parentIDs[v] = node
                nodeDist[v] = nodeDist[node] + 1
                nextNodes.put_nowait(v)
                
    path = deque()
    vertex = targetNode
    
    #assembling path
    while vertex in parentIDs:
        path.appendleft(vertex)
        vertex = parentIDs[vertex]
        
    return path