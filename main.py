# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.analyzer as a
import ai.basicAI as ai
import graphtheory.path as path
from graphtheory.sampleGraphs import graphs

root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#game = SnakeGame(root, 6, 6)
root.mainloop()

'''
#game.snakeCoords = [(1,1),(1,2),(2,2),(3,2),(3,1),(4,1)]
#game.snakeCoords = [(1,1),(1,2),(2,2),(3,2),(4,2),(4,1)]
#game.snakeCoords = [(1,1), (1,2), (2,2), (2,1)]
#game.snakeCoords = [(1,1), (2,1)]
game.snakeCoords = [(1,1), (1,2), (2,2), (2,1),(3,1)]
game.pelletCol = 3
game.pelletRow = 3
(game.cols, game.rows) = (4, 3)
game.grid = game.createGrid(game.cols, game.rows, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
analyzer = a.SnakeAnalyzer(game)
#analyzer = a.SnakeAnalyzer(game, matrix)
analyzer.reset()
print(analyzer.graph)
print(analyzer.pelletPath())
root.mainloop()
'''