# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.snakeAnalysis as a
import ai.surviveAI as ai
import graphtheory.pathFinder as path
import graphtheory.sampleGraphs as sg

root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#game = SnakeGame(root, (3,3))
root.mainloop()

'''
artificialIntelligence = ai.SurviveAI(game)
game.snakeCoords = [(2,2), (2,3),(3,3)]
(game.cols, game.rows) = (6, 6)
game.grid = game.createGrid(6, 6, game.snakeCoords)
game.printGrid()
move = artificialIntelligence.nextMove()
print(move)
root.mainloop()
'''