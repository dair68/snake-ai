# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.analyzer as a
import graphtheory.pathFinder as path
import graphtheory.sampleGraphs as sg
import graphtheory.graph as g
import graphtheory.gridGraph as grid
import ai.practicalAI as ai


root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#root.mainloop()


#game.snakeCoords = [(5,1),(4,1),(3,1)
#game.snakeCoords = [(6,5)]
#game.snakeCoords = [(4,9),(5,9),(6,9),(7,9),(8,9),(8,8),(8,7),(8,6),(8,5),(8,4)]
#game.snakeCoords = [(1,1),(1,2),(2,2),(3,2),(3,1),(4,1)]
game.snakeCoords = [(3,1)]
game.pelletCol = 3
game.pelletRow = 9
(game.cols, game.rows) = (10, 10)
game.grid = game.createGrid(game.cols, game.rows, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
artificialIntelligence = ai.PracticalAI(game)
analyzer = a.SnakeAnalyzer(game)
artificialIntelligence.refreshAI()
root.mainloop()
