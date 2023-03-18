#module hosting sample graph objects
from graphtheory.graph import SimpleUndirectedGraph

vertices1 = {0, 1, 2, 3, 4}
edgeSet1 = {(0,1), (0,3), (1,2), (1,3), (1,4), (2,4), (3,4)}
graph1 = SimpleUndirectedGraph(vertices1, edgeSet1)

vertices2 = {0, 1, 2, 3, 4}
edgeSet2 = {(0,1), (0,3), (1,2), (1,3), (1,4), (2,4)}
graph2 = SimpleUndirectedGraph(vertices2, edgeSet2)

vertices3 = {0, 1, 2, 3, 4} 
edgeSet3 = {(0,1),(0,2),(0,3),(1,2),(1,4),(2,3),(2,4)}
graph3 = SimpleUndirectedGraph(vertices3, edgeSet3)

vertices4 = {0, 1, 2, 3}
edgeSet4 = {(0,1),(1,2),(1,3)}
graph4 = SimpleUndirectedGraph(vertices4, edgeSet4)

graphs = [graph1, graph2, graph3, graph4]