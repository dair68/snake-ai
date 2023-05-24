# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:29:28 2022

@author: grant
"""

import sys
import os
import tkinter as tk
from snake import SnakeGame

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)
icon = "snakeicon.ico"
iconPath = ""

try:
    basePath = sys._MEIPASS
except Exception:
    basePath = os.path.abspath(".")
finally:
    iconPath = os.path.join(basePath, icon)
    
root.iconbitmap(iconPath)
game = SnakeGame(root)
root.mainloop()