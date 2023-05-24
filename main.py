# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

import tkinter as tk
from snake import SnakeGame

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)
root.iconbitmap("snakeicon.ico")
game = SnakeGame(root)
root.mainloop()