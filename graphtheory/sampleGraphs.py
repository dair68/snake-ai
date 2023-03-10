#module hosting sample graphs stored as dict adjacency lists

graph1 = {0: {1, 3},
          1: {0, 2, 3, 4},
          2: {1, 4},
          3: {0, 1, 4},
          4: {1, 2, 3}
          }

graph2 = {0: {1, 3},
          1: {0, 2, 3, 4},
          2: {1, 4},
          3: {0, 1},
          4: {1, 2}
          }

graphs = [graph1, graph2]