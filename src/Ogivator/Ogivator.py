import numpy as np
import polars as pl
import webbrowser
from tkinter import *
import os

def resource_path(relative_path): #Function to define the relative paths
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('./src/Ogivator') #Path of the Script and pictures
    return os.path.join(base_path, relative_path)