#module with SimpleUndirectedGraph class

#class for creating simple undirected graphs. best used for sparse graphs
class SimpleUndirectedGraph:
    #constructor
    #@param vertices - set of vertex ids to be added to graph. optional
    #@param edges - set of tuples of form (vertexID1, vertexID2) indicating desired edges
    #   each vertex must be included somewhere within the "vertices" parameter. optional
    def __init__(self, vertices=None, edges=None):
        self.adjacencyList = {}
        self.vertexValues = {}
        
        #checking if vertices inputted
        if vertices != None:
            self.adjacencyList = {vertex:set() for vertex in vertices}
            self.vertexValues = {vertex:None for vertex in vertices}
        
        self.edgeValues = {}
        
        #checking if edges inputted
        if edges != None:
            self.addEdges(*tuple(edges))
                
    #obtains all vertices in graph
    #returns set of vertex ids for all vertices within graph
    def getVertices(self):
        return set(self.adjacencyList.keys())
    
    #obtains all edges in graph
    #returns set of edges with each edge being tuple of form (vertex1ID, vertex2ID)
    def getEdges(self):
        return set(self.edgeValues.keys())
    
    #obtains values attached to every vertex in graph
    #returns dict mapping vertex id to value stored in that vertex
    def getVertexValues(self):
        return self.vertexValues
    
    #obtains values attached to every edge in graph
    #returns dict mapping edge tuples of form (vertex1ID, vertex2ID) to value at edge
    def getEdgeValues(self):
        return self.edgeValues
    
    #adds vertices to graph
    #@param *args - arbitrary amount of id numbers for each vertex to be added
    #   vertex not added if vertex with that id already in graph
    def addVertices(self, *args):
        #adding vertices
        for vertex in args:
            self.addVertex(vertex)
                
    #adds edges to graph
    #@param *args - arbitray amount of edge tuples of form (vertex1ID, vertex2ID)
    #   edge not added if it is already in graph.
    #   raises error is vertex not already in graph is listed within edge
    def addEdges(self, *args):
        #adding edge data
        for edge in args:
            assert self.validEdge(edge)
            (vertex1, vertex2) = edge
            self.addEdge(vertex1, vertex2)
    
    #checks if a tuple represents a valid edge for a simple graph
    #@param edge - tuple
    #returns True if tuple has 2 integer elements that are not the same
    def validEdge(self, edge):
        return len(edge) == 2 and edge[0] != edge[1]
    
    #checks if 2 vertices within graph have edge connecting them
    #@param vertex1 - integer id number of 1st vertex
    #@param vertex2 - integer id number of 2nd vertex
    #returns True is vertex1 and vertex2 have an edge between them, False otherwise
    def adjacent(self, vertex1, vertex2):
        assert self.vertexIncluded(vertex1)
        assert self.vertexIncluded(vertex2)
        return vertex2 in self.adjacencyList[vertex1]
    
    #checks if a vertex of a certain id is within graph
    #@param vertex - integer vertex id
    #returns True is vertex if within graph, False otherwise
    def vertexIncluded(self, vertex):
        return vertex in self.adjacencyList
    
    #finds all adjacent vertices to to a certain vertex
    #@param vertex - integer vertex id
    #returns set of vertex ids for all vertices with an edge between
    def neighbors(self, vertex):
        assert self.vertexIncluded(vertex)
        return self.adjacencyList[vertex]
    
    #adds a vertex to the graph
    #@param vertex - integer vertex id. vertex not added if one with that id already exists
    def addVertex(self, vertex):
        #checking if vertex already exists in graph
        if not self.vertexIncluded(vertex):
            self.adjacencyList[vertex] = set()
            self.vertexValues[vertex] = None
            
    #removes a vertex and all edges connected to it from graph
    #@param vertex - integer vertex id. removes vertex if it exists.
    def removeVertex(self, vertex):
        #checking if vertex exists in graph
        if self.vertexIncluded(vertex):
            neighbors = set(self.neighbors(vertex))
            
            #removing all edges attached to vertex
            for v in neighbors:
                self.removeEdge(vertex, v)
            
            self.adjacencyList.pop(vertex)
            self.vertexValues.pop(vertex)
            
    #adds edge to a graph, if it does not already exist
    #@param vertex1 - integer id of vertex making up one end of edge
    #@param vertex2 - integer id of vertex making up other end of edge
    def addEdge(self, vertex1, vertex2):
        edge = (vertex1, vertex2) if vertex1 < vertex2 else (vertex2, vertex1)
        assert vertex1 != vertex2
        assert self.vertexIncluded(vertex1)
        assert self.vertexIncluded(vertex2)
        
        #checking if edge already present
        if edge not in self.edgeValues:
            self.adjacencyList[vertex1].add(vertex2)
            self.adjacencyList[vertex2].add(vertex1)
            self.edgeValues[edge] = None
        
    #removes an edge from a graph, if it exists
    #@param vertex1 - integer id of vertex making up one end of edge
    #@param vertex2 - integer id of vertex making up other end of edge
    def removeEdge(self, vertex1, vertex2):
        edge = (vertex1, vertex2) if vertex1 < vertex2 else (vertex2, vertex1)
        assert self.validEdge(edge)
        
        #checking if edge exists
        if self.adjacent(vertex1, vertex2):
            self.adjacencyList[vertex1].discard(vertex2)
            self.adjacencyList[vertex2].discard(vertex1)
            self.edgeValues.pop(edge)
            
    #obtains value stored in a specific vertex
    #@param vertex - integer id of vertex
    #returns value stored at inputted vertex
    def getVertexValue(self, vertex):
        assert self.vertexIncluded(vertex)
        return self.vertexValues[vertex]
    
    #assigns value to a particular vertex
    #@param vertex - integer id of vertex
    #@param value - data to be stored in vertex
    def setVertexValue(self, vertex, value):
        assert self.vertexIncluded(vertex)
        self.vertexValues[vertex] = value
        
    #obtains value stored in specific edge
    #@param vertex1 - integer id of vertex making up one end of edge
    #@param vertex2 - integer id of vertex making up other end of edge
    #returns value stored in inputted edge
    def getEdgeValue(self, vertex1, vertex2):
        assert self.adjacent(vertex1, vertex2)
        edge = (vertex1, vertex2) if vertex1 < vertex2 else (vertex2, vertex1)
        assert self.validEdge(edge) 
        return self.edgeValues[edge]
    
    #assigns value to specific edge
    #@param vertex1 - integer id of vertex making up one end of edge
    #@param vertex2 - integer id of vertex making up other end of edge
    #@param value - data to be stored in edge
    def setEdgeValue(self, vertex1, vertex2, value):
        assert self.adjacent(vertex1, vertex2)
        edge = (vertex1, vertex2) if vertex1 < vertex2 else (vertex2, vertex1)
        assert self.validEdge(edge)
        self.edgeValues[edge] = value