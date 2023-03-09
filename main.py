# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.snakeAnalysis as a
import ai.dumbAI as ai
import graphtheory.graphTraversal as g

root = Tk()
root.title("Snake")
root.resizable(False, False)
game = SnakeGame(root)
#game = SnakeGame(root, (3,3))
root.mainloop()

'''
print(game)
artificialIntelligence = ai.SnakeAI(game)
print(artificialIntelligence.getGame())
root.mainloop()
'''