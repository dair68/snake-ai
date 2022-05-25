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
        