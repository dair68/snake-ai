# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.analyzer as a
import ai.advancedAI as ai
from graphtheory.sampleGraphs import graphs
import graphtheory.graphPath as path

root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#game = SnakeGame(root, 4, 4)
root.mainloop()

'''
#game.snakeCoords = [(1,1)]
#game.snakeCoords = [(1,1), (1,2), (2,2), (2,1)]
#game.snakeCoords = [(1,1), (1,2), (2,2), (2,1), (3,1)]
#game.snakeCoords = [(3,2),(3,3),(2,3),(1,3),(1,2),(1,1),(2,1),(3,1),(4,1),(4,2)]
#game.snakeCoords = [(2,2),(1,2),(1,3),(2,3),(3,3),(4,3),(4,2),(4,1),(3,1)]
#game.snakeCoords = [(2,2),(1,2),(1,3),(2,3),(3,3),(4,3),(4,2),(4,1),(3,1),(2,1)]
game.snakeCoords = [(1,2),(1,3), (2,3), (2,2), (2,1), (1,1)]
game.pelletCol = 3
game.pelletRow = 3
(game.cols, game.rows) = (4, 4)
game.grid = game.createGrid(game.cols, game.rows, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
analyzer = a.SnakeAnalyzer(game)
#analyzer = a.SnakeAnalyzer(game, matrix)
analyzer.reset()
artificialIntelligence = ai.AdvancedAI(game)
root.mainloop()
'''