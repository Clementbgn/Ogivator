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

def generatefile(dataframe_xyz): #Function to generate a txt file with the XYZ coordinates
    df = dataframe_xyz.drop_nulls() #Drop empty values from the dataframe
    if os.path.isfile('nosecone.txt') == True and os.path.isfile('noseconeold.txt') == False:
        os.rename('nosecone.txt', 'noseconeold.txt') #If a file nosecone.txt already exists rename it noseconeold.txt
    if os.path.isfile('nosecone.txt') == True and os.path.isfile('noseconeold.txt') == True:
        os.remove('noseconeold.txt')
        os.rename('nosecone.txt', 'noseconeold.txt') #If nosecone.txt and noseconeold.txt already exists remove the old one, rename nosecone.txt to noseconeold.txt
    path = 'nosecone.txt'
    with open(path, 'a') as f:
        df_string = df.write_csv(include_header=False, separator=' ') #Write the dataframe as csv format to nosecone.txt
        f.write(df_string)