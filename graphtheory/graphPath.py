#module which a variety of graph traversal functions
from collections import deque
from queue import Queue

#finds the path between two vertices that traverses the fewest number of edges
#@param graph - dict containing graph adjacency list
#@param start - integer id number of start vertex
#@param end - integer id number of targaet vertex
#returns deque of vertex ids representing shortest path from startVertex to targetVertex, if it exists
def shortestPath(graph, start, end):
    pathData = singleSourcePaths(graph, start, {end})
    return pathData[end]

#finds paths between one vertex and other vertices that contains fewest number of edges
#@param graph - dict containing graph adjacency list
#@param start - nonnegative integer id number of start vertex
#@param targets - set of vertex ids for which paths are to end.
#   chooses set of all vertices in graph by default
#returns dict mapping vertex ids to deques of ids making up shortest path to them
def singleSourcePaths(graph, start, targets=None):
    #initializing targetVertices if needed
    if targets == None:
        targets = graph.keys()
    
    parents = {start: -1}
    targetsLeft = set(targets)
    targetsLeft.discard(start)
    
    nextNodes = Queue(maxsize=len(graph))
    nextNodes.put_nowait(start)
    
    #exploring nodes
    while not nextNodes.empty():
        #checking if all targets have been found
        if not targetsLeft:
            break
        
        node = nextNodes.get_nowait()
        
        #adding unexplored neighbors to queue
        for neighbor in graph[node]:
            #vertex unexplored
            if neighbor not in parents:
                parents[neighbor] = node
                targetsLeft.discard(neighbor)
                nextNodes.put_nowait(neighbor)
                
    paths = {v:deque() for v in targets}
    
    #assembling paths
    for end in targets:
        node = end
        
        #forming path for certain end node
        while node in parents:
            paths[end].appendleft(node)
            node = parents[node]
        
    return paths

#finds paths leading to one vertex that contains fewest number of edges
#@param graph - dict containing graph adjacency list
#@param target - vertex id for which all paths end
#@param startNodes - nonnegative integer id numbers of vertices for which paths begin. chooses set of all vertices in graph by default
#returns dict mapping vertex ids to deques of ids making up shortest path from them
def singleTargetPaths(graph, target, startNodes=None):
    reverseGraph = {v:set() for v in graph}
    
    #reversing edge directions in graph
    for v in graph:
        #analyzing neighbors
        for neighbor in graph[v]:   
            reverseGraph[neighbor].add(v)
    
    paths = singleSourcePaths(reverseGraph, target, startNodes)
    
    #reversing the paths in path dictionary
    for path in paths.values():
        path.reverse()
    
    return paths

#finds the path between two vertices that traverses the fewest number of edges
#for a graphs where nodes have values indicating min number of edges from start 
#node they must be to be accessed
#@param graph - dict containing graph adjacency list
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