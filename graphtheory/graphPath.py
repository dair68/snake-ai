#module which a variety of graph traversal functions
from collections import deque

#finds the path between two vertices that traverses the fewest number of edges
#@param graph - dict containing graph adjacency list
#@param start - integer id number of start vertex
#@param end - integer id number of targaet vertex
#returns deque of vertex ids representing shortest path from start to target
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
    
    nodeQueue = deque()
    nodeQueue.append(start)
    
    #exploring nodes
    while nodeQueue:
        #checking if all targets have been found
        if not targetsLeft:
            break
        
        node = nodeQueue.popleft()
        
        #adding unexplored neighbors to queue
        for neighbor in graph[node]:
            #vertex unexplored
            if neighbor not in parents:
                parents[neighbor] = node
                targetsLeft.discard(neighbor)
                nodeQueue.append(neighbor)
                
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
#@param graph - dict containing graph adjacency list
#@param start - integer id number of start vertex
#@param end - integer id number of targaet vertex
#@param nodeThres - dict mapping node ids to integer representing distance from start the path must traverse before node can be visited
#returns deque of vertex ids representing shortest path from start to target
def distGatedPath(graph, start, end, nodeThres):
    #checking if start node can be visited
    if nodeThres[start] > 0:
        return deque()
    
    parents = {start: -1}  
    nodeQueue = deque()
    nodeQueue.append((start, 0))
    
    #exploring nodes
    while nodeQueue:
        data = nodeQueue.popleft()
        (node, dist) = data
        
        #checking if target found
        if node == end:
            break
        
        #adding unexplored neighbors to queue
        for neighbor in graph[node]:
            #vertex unexplored
            if neighbor not in parents and dist + 1 >= nodeThres[neighbor]:
                parents[neighbor] = node
                nodeQueue.append((neighbor, dist + 1))
                
    path = deque()
    node = end

    #forming path for certain end node
    while node in parents:
        path.appendleft(node)
        node = parents[node]
        
    return path