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

def openwiki(): #Function to open the wikipedia page of the nose cone design
    webbrowser.open('https://en.wikipedia.org/wiki/Nose_cone_design')

def Conic(precision, length, diameter): #Function to generate a 2d profile of a Conic nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = x * R / L
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Spherically_blunted_conic(precision, length, diameter, radius): #Function to generate a 2d profile of a Spherically blunted conic nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    rn = float(radius)
    xt = np.power(L, 2) / R * np.sqrt(np.power(rn, 2) / (np.power(R, 2) + np.power(L, 2)))
    yt = xt * R / L
    x0 = xt + np.sqrt(np.power(rn, 2) - np.power(yt, 2))
    xa = x0 - rn
    y1 = []
    y2 = []
    for x in np.arange(xa, xt, precision_mm):
        y1.append(np.sqrt(np.power(rn, 2) - np.power(x - x0, 2)))
    for x in np.arange(xt, L, precision_mm):
        y2.append(x * R / L)
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = np.arange(xa, L + precision_mm, precision_mm)
    df1 = pl.DataFrame(y1)
    df2 = pl.DataFrame(y2)
    x = pl.DataFrame(x)
    y = pl.concat([df1, df2], how='vertical')
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Bi_conic(precision, length1, length2, diameter1, diameter2): #Function to generate a 2d profile of a BiConic nose cone based on the input parameters
    precision_mm = float(precision)
    L1 = float(length1)
    L2 = float(length2)
    L = L1 + L2
    R1 = 0.5 * float(diameter1)
    R2 = 0.5 * float(diameter2)
    y1 = []
    y2 = []
    for x in np.arange(0, L1, precision_mm):
        y1.append(x * R1 / L1)
    for x in np.arange(L1, L + precision_mm, precision_mm):
        y2.append(R1 + (x - L1) * (R2 - R1) / L2)
    z = np.zeros((int(L / precision_mm) + 1, 1))
    df1 = pl.DataFrame(y1)
    df2 = pl.DataFrame(y2)
    x = np.arange(0, L + precision_mm, precision_mm)
    x = pl.DataFrame(x)
    y = pl.concat([df1, df2], how='vertical')
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Spherically_blunted_tangent_ogive(precision, length, diameter, radius): #Function to generate a 2d profile of a Spherically blunted tangent ogive nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    rn = float(radius)
    p = (np.power(R, 2) + np.power(L, 2)) / (2 * R)
    x0 = L - np.sqrt(np.power(p - rn, 2) - np.power(p - R, 2))
    yt = rn * (p - R) / (p - rn)
    xt = x0 - np.sqrt(np.power(rn, 2) - np.power(yt, 2))
    xa = x0 - rn
    x = np.arange(0, L + precision_mm, precision_mm)
    y1 = []
    y2 = []
    for x in np.arange(xa, xt, precision_mm):
        y1.append(np.sqrt(np.power(rn, 2) - np.power(x - x0, 2)))
    for x in np.arange(xt, L - precision_mm, precision_mm):
        y2.append(np.sqrt(np.power(p, 2) - np.power(L - x, 2)) + R - p)
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = np.arange(xa, L + precision_mm, precision_mm)
    df1 = pl.DataFrame(y1)
    df2 = pl.DataFrame(y2)
    x = pl.DataFrame(x)
    y = pl.concat([df1, df2], how='vertical')
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Tangent_ogive(precision, length, diameter): #Function to generate a 2d profile of a tangent ogive nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    p = (np.power(R, 2) + np.power(L, 2)) / (2 * R)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = np.sqrt(np.power(p, 2) - np.power(L - x, 2)) + R - p
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Secant_ogive(precision, length, diameter): #Function to generate a 2d profile of a Secant ogive nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    p = (np.power(R, 2) + np.power(L, 2)) / (2 * R)
    alpha = np.arccos(np.sqrt(np.power(L, 2) + np.power(R, 2)) / (2 * p)) - np.arctan(R / L)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = np.sqrt(np.power(p, 2) - np.power(p * np.cos(alpha) - x, 2)) - p * np.sin(alpha)
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Elliptical(precision, length, diameter): #Function to generate a 2d profile of a Elliptical nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = R * np.sqrt(1 - np.power(x, 2) / np.power(L, 2))
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    y = y.reverse()
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Parabolic(precision, length, diameter, Kp): #Function to generate a 2d profile of a Parabolic nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    K = float(Kp)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = R * ((2 * (x / L) - K * np.power(x / L, 2)) / (2 - K))
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Power_series(precision, length, diameter, nparam): #Function to generate a 2d profile of a Power Series nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    n = float(nparam)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = R * np.power(x / L, n)
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)

def Haack_series(precision, length, diameter, Cp): #Function to generate a 2d profile of a Haack Series nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    C = float(Cp)
    x = np.arange(0, L + precision_mm, precision_mm)
    theta = np.arccos(1 - 2 * x / L)
    y = R / np.sqrt(np.pi) * np.sqrt(theta - 0.5 * np.sin(2 * theta) + C * np.power(np.sin(theta), 3))
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat([x.rename({'column_0': 'x_column_0'}), y.rename({'column_0': 'y_column_0'}), z.rename({'column_0': 'z_column_0'})], how='horizontal')
    generatefile(df)