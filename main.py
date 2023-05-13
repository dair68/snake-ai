# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.analyzer as a
import ai.advancedAI as ai
import graphtheory.path as path
from graphtheory.sampleGraphs import graphs

root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
root.mainloop()

'''
#game.snakeCoords = [(1,1),(1,2),(2,2),(3,2),(3,1),(4,1)]
#game.snakeCoords = [(1,1),(1,2),(2,2),(3,2),(4,2),(4,1)]
game.snakeCoords = [(1,1), (1,2), (2,2), (2,1)]
game.pelletCol = 3
game.pelletRow = 1
(game.cols, game.rows) = (4, 3)
game.grid = game.createGrid(game.cols, game.rows, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
matrix = [[set() for j in range(game.rows+2)] for i in range(game.cols+2)]
matrix[1][1].add((2,1))
matrix[2][1].add((3,1))
matrix[3][1].add((3,2))
matrix[3][2].add((2,2))
matrix[2][2].add((1,2))
matrix[1][2].add((1,1))

analyzer = a.SnakeAnalyzer(game)
#analyzer = a.SnakeAnalyzer(game, matrix)
print(analyzer.safeMoves())
root.mainloop()
'''