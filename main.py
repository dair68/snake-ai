# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.snakeAnalysis as a
import ai.basicAI as ai
import graphtheory.pathFinder as path
import graphtheory.sampleGraphs as sg


root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#game = SnakeGame(root, (3,3))
root.mainloop()

'''
artificialIntelligence = ai.BasicAI(game)
analyzer = a.SnakeGameAnalyzer(game)
game.snakeCoords = [(5,1),(4,1),(3,1),(3,2),(4,2),(5,2),(6,2)]
game.pelletCol = 1
game.pelletRow = 1
(game.cols, game.rows) = (6, 6)
game.grid = game.createGrid(6, 6, game.snakeCoords)
game.drawPellet(game.pelletCol, game.pelletRow)
game.printGrid()
foundPath = analyzer.fastPelletPath()
print(foundPath)
root.mainloop()
'''