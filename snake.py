# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:48:01 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk

#widget with a game of snake contained within
class Snake:
    #constructor
    #@param root - parent tk widget
    def __init__(self, root):
        root.title("Snake")
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.resizable(False, False)
        
        scoreText = ttk.Label(root, text="scores")
        scoreText.grid(column=0, row=0)
        
        gameFrame = ttk.Frame(root, style="TFrame")
        gameFrame.grid(column=0, row=1)
        
        canvas = Canvas(gameFrame, bg="black", height=300, width=300)
        canvas.create_rectangle(0, 0, 15, 15, fill="white")
        canvas.pack()

        
        
        
     