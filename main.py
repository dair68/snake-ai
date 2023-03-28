# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.snakeAnalysis as a
import ai.loopAI as ai
import graphtheory.pathFinder as path
import graphtheory.sampleGraphs as sg
import graphtheory.hamiltonianCycle as h
import graphtheory.hamiltonianPath as p
import graphtheory.graph as g
import graphtheory.gridGraph as grid


root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#root.mainloop()


#game.snakeCoords = [(5,1),(4,1),(3,1)
game.snakeCoords = [(6,5)]
#game.snakeCoords = [(2,1)]
game.pelletCol = 5
game.pelletRow = 5
(game.cols, game.rows) = (10, 10)
game.grid = game.createGrid(game.cols, game.rows, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
artificialIntelligence = ai.LoopAI(game)
analyzer = a.SnakeGameAnalyzer(game)
pathInfo = analyzer.pelletPathInfo()
print(pathInfo)
root.mainloop()
