#module hosting class for making rectangular grid graphs
from graphtheory.graph import SimpleUndirectedGraph

#class for making rectangular grid graphs
class GridGraph:
    #constructor for making mxn rectangular grid graph.
    #@param m - positive integer signifying length of 1st dimension of grid
    #@param n - positive integer signifying length of 2nd dimension of grid
    #@param vertexIDMatrix - mxn nested lists for which vertexIDArr[i][j] is the
    #   vertex id number of the vertex at location (i, j). id numbers must be unique.
    #   optional
    def __init__(self, m, n, vertexIDMatrix=None):
        assert m > 0
        assert n > 0
        self.vertexIDMatrix = [[]]
        vertices = set()
        
        #assigning self.vertexIDMatrix based on parameters
        if vertexIDMatrix != None:
            assert len(vertexIDMatrix) == m
            assert len(vertexIDMatrix[0]) == n
            self.vertexIDMatrix = vertexIDMatrix
            
            vertices = {self.vertexIDMatrix[i][j] for i in range(m) for j in range(n)}
            assert len(vertices) == m*n
        else:
            self.vertexIDMatrix = [[j for j in range(n)] for i in range(m)]
        
            #populating self.vertexIDs
            for v in range(m*n):
                i = v%m
                j = v//m
                self.vertexIDMatrix[i][j] = v
                vertices.add(v)
        
        self.vertexCoordMap = {}
        
        #populating self.vertexCoordMap
        for i in range(m):
            for j in range(n):
                v = self.vertexIDMatrix[i][j]
                self.vertexCoordMap[v] = (i, j)
        
        edges = set()
        
        #looping over grid to find edges
        for i in range(m):
            for j in range(n):
                #checking if i+1 index in range
                if 0 <= i+1 and i+1 < m:
                    v1 = self.vertexIDMatrix[i][j]
                    v2 = self.vertexIDMatrix[i+1][j]
                    edge = (v1, v2)
                    edges.add(edge)
                    
                #checking if j+1 index in range
                if 0 <= j+1 and j+1 < n:
                    v1 = self.vertexIDMatrix[i][j]
                    v2 = self.vertexIDMatrix[i][j+1]
                    edge = (v1, v2)
                    edges.add(edge)
        
        self.graph = SimpleUndirectedGraph(vertices, edges)
        
    #obtains all vertices in graph
    #returns set of vertex ids for all vertices within graph
    def getVertices(self):
        return self.graph.getVertices()
    
    #obtains all edges in graph
    #returns set of edges with each edge being tuple of form (vertex1ID, vertex2ID)
    def getEdges(self):
        return self.graph.getEdges()
    
    #obtains values attached to every vertex in graph
    #returns dict mapping vertex id to value stored in that vertex
    def getVertexValues(self):
        return self.graph.getVertexValues()
    
    #obtains values attached to every edge in graph
    #returns dict mapping edge tuples of form (vertex1ID, vertex2ID) to value at edge
    def getEdgeValues(self):
        return self.graph.getEdgeValues()
    
    #checks if 2 vertices within graph have edge connecting them
    #@param vertex1 - integer id number of 1st vertex
    #@param vertex2 - integer id number of 2nd vertex
    #returns True is vertex1 and vertex2 have an edge between them, False otherwise
    def adjacent(self, vertex1, vertex2):
        return self.graph.adjacent(vertex1, vertex2)
    
    #checks if a vertex of a certain id is within graph
    #@param vertex - integer vertex id
    #returns True is vertex if within graph, False otherwise
    def vertexIncluded(self, vertex):
        return self.graph.vertexIncluded(vertex)
    
    #finds all adjacent vertices to to a certain vertex
    #@param vertex - integer vertex id
    #returns set of vertex ids for all vertices with an edge between
    def neighbors(self, vertex):
        return self.graph.neighbors(vertex)
    
    #obtains value stored in a specific vertex
    #@param vertex - integer id of vertex
    #returns value stored at inputted vertex
    def getVertexValue(self, vertex):
        return self.graph.getVertexValue(vertex)
    
    #assigns value to a particular vertex
    #@param vertex - integer id of vertex
    #@param value - data to be stored in vertex
    def setVertexValue(self, vertex, value):
        self.graph.setVertexValue(vertex, value)
    
    #obtains value stored in specific edge
    #@param vertex1 - integer id of vertex making up one end of edge
    #@param vertex2 - integer id of vertex making up other end of edge
    #returns value stored in inputted edge
    def getEdgeValue(self, vertex1, vertex2):
        return self.graph.getEdgeValue(vertex1, vertex2)
    
    #assigns value to specific edge
    #@param vertex1 - integer id of vertex making up one end of edge
    #@param vertex2 - integer id of vertex making up other end of edge
    #@param value - data to be stored in edge
    def setEdgeValue(self, vertex1, vertex2, value):
        self.graph.setEdgeValue(vertex1, vertex2, value)
        
    #obtains vertex id for vertex at certain location in mxn grid
    #@param i - first index. int for which 0 <= i < m
    #@param j - second index. int for which 0 <= j < n
    #returns vertex id for vertex at graph[i][j]
    def vertexAt(self, i, j):
        return self.vertexIDMatrix[i][j]
    
    #obtains vertex value for vertex at certain location in mxn grid
    #@param i - first index. int for which 0 <= i < m
    #@param j - second index. int for which 0 <= j < n
    #returns value for vertex at graph[i][j]
    def vertexValueAt(self, i, j):
        return self.getVertexValue(self.vertexAt(i, j))
    
    #sets value of vertex at graph[i][j] in mxn grid
    #@param i - first index. int for which 0 <= i < m
    #@param j - second index. int for which 0 <= j < n
    #@param value - data to be assigned to vertex
    def setVertexValueAt(self, i, j, value):
        self.setVertexValue(self.vertexAt(i, j), value)
        
    #obtains the indices corresponding to specific vertex id in mxn grid
    #@param vertex - integer id of vertex in question
    #if vertex that of id exists, returns indices in form of (i, j)
    #   where 0 <= i < m, 0 <= j < n
    def vertexIndices(self, vertex):
        return self.vertexCoordMap[vertex]
    
    #obtains dimensions of grid
    #returns tuple of form (m, n) where m is int upper bound for first index,
    #   and n is int upper bound fro second index
    def dimensions(self):
        m = len(self.vertexIDMatrix)
        n = len(self.vertexIDMatrix[0])
        return (m, n)
    
    #obtains value of edge connecting certain vertex locations in mxn grid
    #@param i1 - 1st index of first vertex. 0 <= i1 < m
    #@param j1 - 2nd index of first vertex. 0 <= j1 < n
    #@param i2 - 1st index of second vertex. 0 <= i2 < m
    #@param j2 - 2nd index of second vertex. 0 <= j2 < n
    #obtains value of edge connecting vertices at graph[i1][j1] and graph[i2][j2]
    def getEdgeValueAt(self, i1, j1, i2, j2):
        return self.getEdgeValue(self.vertexAt(i1, j1), self.vertexAt(i2, j2))
    
    #sets value of edge connecting certain vertex locations in mxn grid
    #@param i1 - 1st index of first vertex. 0 <= i1 < m
    #@param j1 - 2nd index of first vertex. 0 <= j1 < n
    #@param i2 - 1st index of second vertex. 0 <= i2 < m
    #@param j2 - 2nd index of second vertex. 0 <= j2 < n
    #@param value - data to be stored in edge connecting graph[i1][j1] and graph[i2][j2]
    def setEdgeValueAt(self, i1, j1, i2, j2, value):
        self.setEdgeValue(self.vertexAt(i1, j1), self.vertexAt(i2, j2), value)