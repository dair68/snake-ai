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


root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
root.mainloop()

'''
artificialIntelligence = ai.LoopAI(game)
analyzer = a.SnakeGameAnalyzer(game)
game.snakeCoords = [(5,1),(4,1),(3,1),(3,2),(4,2),(5,2),(6,2),(6,3)]
#game.snakeCoords = [(2,1), (2,2)]
game.pelletCol = 1
game.pelletRow = 1
(game.cols, game.rows) = (6, 6)
game.grid = game.createGrid(game.cols, game.rows, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
rect = analyzer.smallestBoundingRect(game.snakeCoords)
print(rect)
root.mainloop()
'''