#module with functions for manipulating graph adjacency lists

#adds a vertex to an existing graph. vertex not added if it already exists
#@param graphAdjList - dict mapping vertex ids to sets of adjacent vertex ids
#@param vertex - id of vertex to be added
def addVertex(graphAdjList, vertex):
    #checking if vertex already in adjacency list
    if vertex not in graphAdjList:
        graphAdjList[vertex] = set()
        
#adds edge to an existing graph. 
#edge not added if it already exists or if vertices at endpoints don't exist in graph
#@param graphAdjList - dict mapping vertex ids to sets of adjacent vertex ids
#@param vertex1 - id of vertex at one end of edge
#@param vertex2 - id of vertex at other end of edge
def insertEdge(graphAdjList, vertex1, vertex2):
    assert vertex1 in graphAdjList and vertex2 in graphAdjList
    graphAdjList[vertex1].add(vertex2)
    graphAdjList[vertex2].add(vertex1)
        
#adds edge to an existing graph. edge not added if it already exists
#if one or both vertices at endpoints don't exist in graph, they are added too
#@param graphAdjList - dict mapping vertex ids to sets of adjacent vertex ids
#@param vertex1 - id of vertex at one end of edge
#@param vertex2 - id of vertex at other end of edge
def addEdge(graphAdjList, vertex1, vertex2):
    #checking if vertices exist in graph
    if vertex1 not in graphAdjList:
        addVertex(graphAdjList, vertex1)
    if vertex2 not in graphAdjList:
        addVertex(graphAdjList, vertex2)
        
    graphAdjList[vertex1].add(vertex2)
    graphAdjList[vertex2].add(vertex1)