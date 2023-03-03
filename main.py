# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
from hamiltonianCycles import findHamiltonianCycle

root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
root.mainloop()

'''
graph1 = [[0, 1, 0, 1, 0],
          [1, 0, 1, 1, 1],
          [0, 1, 0, 0, 1],
          [1, 1, 0, 0, 1],
          [0, 1, 1, 1, 0]]

graph2 = [[0, 1, 0, 1, 0],
          [1, 0, 1, 1, 1],
          [0, 1, 0, 0, 1],
          [1, 1, 0, 0, 0],
          [0, 1, 1, 0, 0]]

graph = graph2
graphName = "graph1" if graph == graph1 else "graph2"
path = findHamiltonianCycle(graph)
print(f"{graphName} hamiltonian cycle: ")
print(path)
'''