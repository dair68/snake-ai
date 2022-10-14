# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 16:27:57 2022

@author: grant
"""

from tkinter import *
from tkinter import ttk
import tkinter as tk

#widget with menu options for snake game
class SnakeMenu:
    #constructor
    #@param root - parent tk widget
    def __init__(self, root):
        self.frame = ttk.Frame(root)
        self.frame.pack()
        #self.frame.pack(fill=ttk.Y)
        
        self.titleLabel = ttk.Label(self.frame, text="Snake")
        self.titleLabel.grid(column=0, row=0)
        #self.frame.columnconfigure(0, weight=1)
        
        self.playBtn = ttk.Button(self.frame, text="Play Game")
        self.playBtn.grid(row=1)
        
        self.aiBtn = ttk.Button(self.frame, text="Run AI")
        self.aiBtn.grid(row=2)