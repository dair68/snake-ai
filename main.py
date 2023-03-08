# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from tkinter import *
import ai.snakeAnalysis as a
import ai.dumbAI as ai

root = Tk()
root.title("Snake")
root.resizable(False, False)
#game = SnakeGame(root)
game = SnakeGame(root, (3,3))
#root.mainloop()

analyzer = a.SnakeGameAnalyzer(game)
game.grid = [["#", "#", "#", "#", "#"], 
             ["#", "o", "H", "o", "#"], 
             ["#", "o", "S", "T", "#"],
             ["#", "o", "o", "o", "#"],
             ["#", "#", "#", "#", "#"]]
hashMap = analyzer.inboundGridAdjacencyList()
print(hashMap)
root.mainloop()