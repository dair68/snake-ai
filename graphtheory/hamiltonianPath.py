#module with functions for finding hamiltonian paths
import bitmask as bm

#checks if graph has a hamiltonian path
#@param graph - UndirectedSimpleGraph object
#returns True if hamiltonian path exists, False otherwise
def hasHamiltonianPath(graph):
    numVertices = len(graph.getVertices())
    vertexMap = {}
    vertices = graph.getVertices()
    iterator = iter(vertices)
    
    #assigning each vertex a mark from 0 to numVertices - 1.
    #in vertexMap entries are mark:vertexID
    for n in range(numVertices):
        vertex = next(iterator)
        vertexMap[n] = vertex
        
    print(vertexMap)
    #pathData[i][j] is bool for whether mask i is h path containing vertex j at end
    pathData = [[None for j in range(numVertices)] for i in range(2**numVertices)]
    #print(pathData)
    
    iterations = len(pathData)
    #iterations = 12
    
    #filling in path table
    for i in range(iterations):
        for j in range(len(pathData[0])):
            #filling table for different situations
            if bm.count(i) == 1:
                oneIndex = bm.first(i)
                pathData[i][j] = (oneIndex == j)
            elif bm.bit(j, i) == 1:
                jMark = 1 << j
                jCMark = i - jMark
                jCData = pathData[jCMark]
                
                #analyzing path data for subset without node j
                for k in range(len(jCData)):
                    #checking there exists hamiltonian path with k as end node
                    if jCData[k] == False:
                        continue
                        
                    #checking if vertex k and j are adjacent
                    if graph.adjacent(vertexMap[k], vertexMap[j]):
                        pathData[i][j] = True
                        break
                    
            #checking if path data still not assigned
            if pathData[i][j] == None:
                pathData[i][j] = False
                
    #printPathTable(pathData)
    
    #analyzing final row of table to figure out if there's a hamiltonian path
    for j in range(len(pathData[0])):
        #hamiltonian path ending in j exists!
        if pathData[-1][j] == True:
            return True
        
    return False
    
#prints table storing hamiltonian path info
#@param table - 2**n by n table storing info about hamiltonian paths in graph
#prints entries of table[i][j] with i being row, j being column
#None=-1, True=1, False=0
def printPathTable(table):
    symbols = {None:"-1", True:" 1", False:" 0"}
    
    #printing each row 1 by 1
    for i in range(len(table)):
        row = table[i]
        rowNum = [symbols[row[j]] for j in range(len(row))]
        rowStr = "".join(rowNum)
        print(rowStr)