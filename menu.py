# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 16:27:57 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk
import tkinter as tk
from snake import SnakeGame

#widget with menu options for snake game
class SnakeMenu:
    #constructor
    #@param root - parent tk widget
    def __init__(self, root):
        self.mainFrame = ttk.Frame(root)
        self.mainFrame.pack()
        self.menuFrame = ttk.Frame(self.mainFrame)
        self.menuFrame.pack()
        #self.frame.pack(fill=ttk.Y)
        
        self.titleLabel = ttk.Label(self.menuFrame, text="Snake")
        self.titleLabel.grid(column=0, row=0)
        #self.frame.columnconfigure(0, weight=1)
        
        self.playBtn = ttk.Button(self.menuFrame, text="Play Game")
        self.playBtn.grid(row=1)
        self.playBtn.bind("<Button-1>", self.startGame)
        
        self.aiBtn = ttk.Button(self.menuFrame, text="Run AI")
        self.aiBtn.grid(row=2)
        
        self.gameWidget = None
        
    #starts snake game
    #@param event - event object
    #changes contents of frame to game
    def startGame(self, event):
        self.menuFrame.pack_forget()
        self.gameWidget = SnakeGame(self.mainFrame)