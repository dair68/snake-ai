#module hosting sample graph objects
from graphtheory.graph import SimpleUndirectedGraph

vertices = {0, 1, 2, 3, 4}
edgeSet1 = {(0,1), (0,3), (1,2), (1,3), (1,4), (2,4), (3,4)}
graph1 = SimpleUndirectedGraph(vertices, edgeSet1)

edgeSet2 = {(0,1), (0,3), (1,2), (1,3), (1,4), (2,4)}
graph2 = SimpleUndirectedGraph(vertices, edgeSet2)
graphs = [graph1, graph2]