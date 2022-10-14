# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

from snake import SnakeGame
from menu import SnakeMenu
from tkinter import *

#root = Tk()
#root.resizable(False, False)
#game = SnakeGame(root)
#root.mainloop()

root = Tk()
snakeWindow = SnakeMenu(root)
root.mainloop()