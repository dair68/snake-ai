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
        
        self.cols = 20
        self.rows = 20
        self.squareLength = 15
        canvasHeight = self.squareLength*self.rows
        canvasWidth = self.squareLength*self.cols
        
        self.canvas = Canvas(gameFrame, bg="black", height=canvasHeight, width=canvasWidth)
        self.drawSnakeSquare(10, 10)
        self.canvas.pack()
        
    #draws a white snake unit square within game area
    #@param col - column number from 0 to 19
    #@param row - row number from 0 to 19
    def drawSnakeSquare(self, col, row):
        k = self.squareLength
        x = col*k
        y = row*k
        self.canvas.create_rectangle(x, y, x + k, y + k, fill="white")
        self.canvas.pack()
        

        
        
        
     