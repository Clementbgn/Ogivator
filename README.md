# Ogivator Project
## Purpose
  
Ogivator is a little program developed in Python to generate a 2d profile of a rocket nosecone for Solidworks XYZ curve (txt file) for differents types of nosecone types

## Functions explanation

**generatefile(dataframe_xyz)** is used to generate a txt file based on a dataframe  

**openwiki()** is used to open the wikipedia page of nosecone design

**Conic(precision, length, diameter)** is used to generate the XYZ coordinates of a conic profile bases on the parameters

**Spherically_blunted_conic(precision, length, diameter, radius)** Idem with spherically blunted conic

**Bi_conic(precision, length1, length2, diameter1, diameter2)** Idem with Bi conic 

**Spherically_blunted_tangent_ogive(precision, length, diameter, radius)** Idem with spherically blunted tangent ogive

**Tangent_ogive(precision, length, diameter)** Idem

**Secant_ogive(precision, length, diameter)** Idem

**Elliptical(precision, length, diameter)** Idem

**Parabolic(precision, length, diameter, Kp)** Idem

**Power_series(precision, length, diameter, nparam)** Idem

**Haack_series(precision, length, diameter, Cp)** Idem

## Choix_type

Each function is used for the calculation of the xyz txt file and for the GUI, is define a Choix_() function, it is used to generate a new window and let you chose the parameters.

Here they are:

Choix_Conic()

Choix_Spherically_blunted_conic()

Choix_Bi_conic()

Choix_Tangent_ogive()

Choix_Spherically_blunted_tangent_ogive()

Choix_Secant_ogive()

Choix_Elliptical()

Choix_Parabolic()

Choix_Power_series()

Choix_Haack_series()
