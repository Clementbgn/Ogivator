import numpy as np
import polars as pl
import webbrowser
from tkinter import *
import os


def resource_path(relative_path):  # Function to define the relative paths
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./src/Ogivator")  # Path of the Script and pictures
    return os.path.join(base_path, relative_path)


def generatefile(
    dataframe_xyz,
):  # Function to generate a txt file with the XYZ coordinates
    df = dataframe_xyz.drop_nulls()  # Drop empty values from the dataframe
    if (
        os.path.isfile("nosecone.txt") == True
        and os.path.isfile("noseconeold.txt") == False
    ):
        os.rename(
            "nosecone.txt", "noseconeold.txt"
        )  # If a file nosecone.txt already exists rename it noseconeold.txt
    if (
        os.path.isfile("nosecone.txt") == True
        and os.path.isfile("noseconeold.txt") == True
    ):
        os.remove("noseconeold.txt")
        os.rename(
            "nosecone.txt", "noseconeold.txt"
        )  # If nosecone.txt and noseconeold.txt already exists remove the old one, rename nosecone.txt to noseconeold.txt
    path = "nosecone.txt"
    with open(path, "a") as f:
        df_string = df.write_csv(
            include_header=False, separator=" "
        )  # Write the dataframe as csv format to nosecone.txt
        f.write(df_string)


def openwiki():  # Function to open the wikipedia page of the nose cone design
    webbrowser.open("https://en.wikipedia.org/wiki/Nose_cone_design")


def Conic(
    precision, length, diameter
):  # Function to generate a 2d profile of a Conic nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    x = np.arange(0, L + precision_mm, precision_mm)
    y = x * R / L
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Spherically_blunted_conic(
    precision, length, diameter, radius
):  # Function to generate a 2d profile of a Spherically blunted conic nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    rn = float(radius)
    xt = (
        np.power(L, 2)
        / R
        * np.sqrt(np.power(rn, 2) / (np.power(R, 2) + np.power(L, 2)))
    )
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
    y = pl.concat([df1, df2], how="vertical")
    z = pl.DataFrame(z)
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Bi_conic(
    precision, length1, length2, diameter1, diameter2
):  # Function to generate a 2d profile of a BiConic nose cone based on the input parameters
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
    y = pl.concat([df1, df2], how="vertical")
    z = pl.DataFrame(z)
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Spherically_blunted_tangent_ogive(
    precision, length, diameter, radius
):  # Function to generate a 2d profile of a Spherically blunted tangent ogive nose cone based on the input parameters
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
    y = pl.concat([df1, df2], how="vertical")
    z = pl.DataFrame(z)
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Tangent_ogive(
    precision, length, diameter
):  # Function to generate a 2d profile of a tangent ogive nose cone based on the input parameters
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
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Secant_ogive(
    precision, length, diameter
):  # Function to generate a 2d profile of a Secant ogive nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    p = (np.power(R, 2) + np.power(L, 2)) / (2 * R)
    alpha = np.arccos(np.sqrt(np.power(L, 2) + np.power(R, 2)) / (2 * p)) - np.arctan(
        R / L
    )
    x = np.arange(0, L + precision_mm, precision_mm)
    y = np.sqrt(np.power(p, 2) - np.power(p * np.cos(alpha) - x, 2)) - p * np.sin(alpha)
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Elliptical(
    precision, length, diameter
):  # Function to generate a 2d profile of a Elliptical nose cone based on the input parameters
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
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Parabolic(
    precision, length, diameter, Kp
):  # Function to generate a 2d profile of a Parabolic nose cone based on the input parameters
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
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Power_series(
    precision, length, diameter, nparam
):  # Function to generate a 2d profile of a Power Series nose cone based on the input parameters
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
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Haack_series(
    precision, length, diameter, Cp
):  # Function to generate a 2d profile of a Haack Series nose cone based on the input parameters
    precision_mm = float(precision)
    L = float(length)
    R = 0.5 * float(diameter)
    C = float(Cp)
    x = np.arange(0, L + precision_mm, precision_mm)
    theta = np.arccos(1 - 2 * x / L)
    y = (
        R
        / np.sqrt(np.pi)
        * np.sqrt(theta - 0.5 * np.sin(2 * theta) + C * np.power(np.sin(theta), 3))
    )
    z = np.zeros((int(L / precision_mm) + 1, 1))
    x = pl.DataFrame(x)
    y = pl.DataFrame(y)
    z = pl.DataFrame(z)
    df = pl.concat(
        [
            x.rename({"column_0": "x_column_0"}),
            y.rename({"column_0": "y_column_0"}),
            z.rename({"column_0": "z_column_0"}),
        ],
        how="horizontal",
    )
    generatefile(df)


def Choix_Conic():  # Function that generates the interface after clicking on Conic
    Fenetre_Conic = Tk()
    Fenetre_Conic.title("Ogivator | Conic")
    Fenetre_Conic.geometry("1280x720")
    Fenetre_Conic.minsize(1280, 720)
    Fenetre_Conic.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_Conic.config(background="#252526")
    Frame_Conique = Frame(Fenetre_Conic, bg="#252526")
    text_info = Label(
        Frame_Conique,
        text="Conic ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_Conique,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_Conique, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_Conique,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_Conique, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_Conique,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_Conique, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_Conique,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Conic(precision_entry.get(), L_entry.get(), D_entry.get()),
    )
    Generate_button.grid(row=7, column=0, sticky=N + S + E + W, pady=10)
    Frame_Conique.pack(expand=YES)


def Choix_Spherically_blunted_conic():  # Function that generates the interface after clicking on Spherically blunted conic
    Fenetre_SBC = Tk()
    Fenetre_SBC.title("Ogivator | Spherically blunted conic")
    Fenetre_SBC.geometry("1280x720")
    Fenetre_SBC.minsize(1280, 720)
    Fenetre_SBC.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_SBC.config(background="#252526")
    Frame_SBC = Frame(Fenetre_SBC, bg="#252526")
    text_info = Label(
        Frame_SBC,
        text="Spherically blunted conic ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_SBC,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_SBC, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_SBC,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_SBC, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_SBC,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_SBC, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    text_SR = Label(
        Frame_SBC,
        text="Radius of the blunted nose (mm): \\ Rayon de l'arrondissement de l'ogive (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_SR.grid(row=7, column=0, sticky=N)
    SR_entry = Entry(Frame_SBC, bg="#252526", fg="white")
    SR_entry.grid(row=8, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_SBC,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Spherically_blunted_conic(
            precision_entry.get(), L_entry.get(), D_entry.get(), SR_entry.get()
        ),
    )
    Generate_button.grid(row=9, column=0, sticky=N + S + E + W, pady=10)
    Frame_SBC.pack(expand=YES)


def Choix_Bi_conic():  # Function that generates the interface after clicking on Bi conic
    Fenetre_BC = Tk()
    Fenetre_BC.title("Ogivator | Bi-Conic")
    Fenetre_BC.geometry("1280x720")
    Fenetre_BC.minsize(1280, 720)
    Fenetre_BC.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_BC.config(background="#252526")
    Frame_BC = Frame(Fenetre_BC, bg="#252526")
    text_info = Label(
        Frame_BC,
        text="Bi-Conic ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L1 = Label(
        Frame_BC,
        text="Length 1 (mm): \\ Longueur 1 (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L1.grid(row=1, column=0, sticky=N)
    L1_entry = Entry(Frame_BC, bg="#252526", fg="white")
    L1_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R1 = Label(
        Frame_BC,
        text="Diameter 1 (mm): \\ Diamètre 1 (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R1.grid(row=3, column=0, sticky=N)
    D1_entry = Entry(Frame_BC, bg="#252526", fg="white")
    D1_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_L2 = Label(
        Frame_BC,
        text="Length 2 (mm): \\ Longueur 2 (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L2.grid(row=5, column=0, sticky=N)
    L2_entry = Entry(Frame_BC, bg="#252526", fg="white")
    L2_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    text_R2 = Label(
        Frame_BC,
        text="Diameter 2 (mm): \\ Diamètre 2 (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R2.grid(row=7, column=0, sticky=N)
    D2_entry = Entry(Frame_BC, bg="#252526", fg="white")
    D2_entry.grid(row=8, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_BC,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=9, column=0, sticky=N)
    precision_entry = Entry(Frame_BC, bg="#252526", fg="white")
    precision_entry.grid(row=10, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_BC,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Bi_conic(
            precision_entry.get(),
            L1_entry.get(),
            L2_entry.get(),
            D1_entry.get(),
            D2_entry.get(),
        ),
    )
    Generate_button.grid(row=11, column=0, sticky=N + S + E + W, pady=10)
    Frame_BC.pack(expand=YES)


def Choix_Tangent_ogive():  # Function that generates the interface after clicking on Tangent ogive
    Fenetre_TO = Tk()
    Fenetre_TO.title("Ogivator | Tangent ogive")
    Fenetre_TO.geometry("1280x720")
    Fenetre_TO.minsize(1280, 720)
    Fenetre_TO.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_TO.config(background="#252526")
    Frame_TO = Frame(Fenetre_TO, bg="#252526")
    text_info = Label(
        Frame_TO, text="Tangent ogive", font=("Helvetica", 30), bg="#252526", fg="white"
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_TO,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_TO, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_TO,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_TO, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_TO,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_TO, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_TO,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Tangent_ogive(
            precision_entry.get(), L_entry.get(), D_entry.get()
        ),
    )
    Generate_button.grid(row=7, column=0, sticky=N + S + E + W, pady=10)
    Frame_TO.pack(expand=YES)


def Choix_Spherically_blunted_tangent_ogive():  # Function that generates the interface after clicking on Spherically blunted tangent ogive
    Fenetre_SBTO = Tk()
    Fenetre_SBTO.title("Ogivator | Spherically blunted tangent ogive")
    Fenetre_SBTO.geometry("1280x720")
    Fenetre_SBTO.minsize(1280, 720)
    Fenetre_SBTO.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_SBTO.config(background="#252526")
    Frame_SBTO = Frame(Fenetre_SBTO, bg="#252526")
    text_info = Label(
        Frame_SBTO,
        text="Spherically blunted tangent ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_SBTO,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_SBTO, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_SBTO,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_SBTO, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_SBTO,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_SBTO, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    text_SR = Label(
        Frame_SBTO,
        text="Radius of the blunted nose (mm): \\ Rayon de l'arrondissement de l'ogive (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_SR.grid(row=7, column=0, sticky=N)
    SR_entry = Entry(Frame_SBTO, bg="#252526", fg="white")
    SR_entry.grid(row=8, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_SBTO,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Spherically_blunted_tangent_ogive(
            precision_entry.get(), L_entry.get(), D_entry.get(), SR_entry.get()
        ),
    )
    Generate_button.grid(row=9, column=0, sticky=N + S + E + W, pady=10)
    Frame_SBTO.pack(expand=YES)


def Choix_Secant_ogive():  # Function that generates the interface after clicking on Secant ogive
    Fenetre_SO = Tk()
    Fenetre_SO.title("Ogivator | Secant ogive")
    Fenetre_SO.geometry("1280x720")
    Fenetre_SO.minsize(1280, 720)
    Fenetre_SO.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_SO.config(background="#252526")
    Frame_SO = Frame(Fenetre_SO, bg="#252526")
    text_info = Label(
        Frame_SO, text="Secant ogive", font=("Helvetica", 30), bg="#252526", fg="white"
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_SO,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_SO, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_SO,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_SO, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_SO,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_SO, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_SO,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Secant_ogive(
            precision_entry.get(), L_entry.get(), D_entry.get()
        ),
    )
    Generate_button.grid(row=7, column=0, sticky=N + S + E + W, pady=10)
    Frame_SO.pack(expand=YES)


def Choix_Elliptical():  # Function that generates the interface after clicking on Elliptical
    Fenetre_E = Tk()
    Fenetre_E.title("Ogivator | Elliptical")
    Fenetre_E.geometry("1280x720")
    Fenetre_E.minsize(1280, 720)
    Fenetre_E.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_E.config(background="#252526")
    Frame_E = Frame(Fenetre_E, bg="#252526")
    text_info = Label(
        Frame_E,
        text="Elliptical ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_E,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_E, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_E,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_E, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_E,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_E, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_E,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Elliptical(precision_entry.get(), L_entry.get(), D_entry.get()),
    )
    Generate_button.grid(row=7, column=0, sticky=N + S + E + W, pady=10)
    Frame_E.pack(expand=YES)


def Choix_Parabolic():  # Function that generates the interface after clicking on Parabolic
    Fenetre_P = Tk()
    Fenetre_P.title("Ogivator | Parabolic")
    Fenetre_P.geometry("1280x720")
    Fenetre_P.minsize(1280, 720)
    Fenetre_P.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_P.config(background="#252526")
    Frame_P = Frame(Fenetre_P, bg="#252526")
    text_info = Label(
        Frame_P,
        text="Parabolic ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_P,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_P, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_P,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_P, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_P,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_P, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    text_Np = Label(
        Frame_P,
        text="Parabolic parameter K (mm): \\ Paramètre parabolique K (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_Np.grid(row=7, column=0, sticky=N)
    K_entry = Entry(Frame_P, bg="#252526", fg="white")
    K_entry.grid(row=8, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_P,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Parabolic(
            precision_entry.get(), L_entry.get(), D_entry.get(), K_entry.get()
        ),
    )
    Generate_button.grid(row=9, column=0, sticky=N + S + E + W, pady=10)
    Frame_P.pack(expand=YES)


def Choix_Power_series():  # Function that generates the interface after clicking on Power series
    Fenetre_PS = Tk()
    Fenetre_PS.title("Ogivator | Power series")
    Fenetre_PS.geometry("1280x720")
    Fenetre_PS.minsize(1280, 720)
    Fenetre_PS.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_PS.config(background="#252526")
    Frame_PS = Frame(Fenetre_PS, bg="#252526")
    text_info = Label(
        Frame_PS,
        text="Power series ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_PS,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_PS, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_PS,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_PS, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_PS,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_PS, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    text_Np = Label(
        Frame_PS,
        text="Power parameter n: \\ Paramètre de puissance n: ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_Np.grid(row=7, column=0, sticky=N)
    Np_entry = Entry(Frame_PS, bg="#252526", fg="white")
    Np_entry.grid(row=8, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_PS,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Power_series(
            precision_entry.get(), L_entry.get(), D_entry.get(), Np_entry.get()
        ),
    )
    Generate_button.grid(row=9, column=0, sticky=N + S + E + W, pady=10)
    Frame_PS.pack(expand=YES)


def Choix_Haack_series():  # Function that generates the interface after clicking on haack Series
    Fenetre_HS = Tk()
    Fenetre_HS.title("Ogivator | Haack series")
    Fenetre_HS.geometry("1280x720")
    Fenetre_HS.minsize(1280, 720)
    Fenetre_HS.iconbitmap(resource_path("ICONE.ico"))
    Fenetre_HS.config(background="#252526")
    Frame_HS = Frame(Fenetre_HS, bg="#252526")
    text_info = Label(
        Frame_HS,
        text="Haack series ogive",
        font=("Helvetica", 30),
        bg="#252526",
        fg="white",
    )
    text_info.grid(row=0, column=0, sticky=N, pady=(0, 20))
    text_L = Label(
        Frame_HS,
        text="Length of the nose cone (mm): \\ Longueur de l'ogive(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_L.grid(row=1, column=0, sticky=N)
    L_entry = Entry(Frame_HS, bg="#252526", fg="white")
    L_entry.grid(row=2, column=0, sticky=N + S + E + W, pady=10)
    text_R = Label(
        Frame_HS,
        text="Diameter of the base(mm): \\ Diamètre de la base(mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_R.grid(row=3, column=0, sticky=N)
    D_entry = Entry(Frame_HS, bg="#252526", fg="white")
    D_entry.grid(row=4, column=0, sticky=N + S + E + W, pady=10)
    text_P = Label(
        Frame_HS,
        text="Precision of the x values (mm): \\ Précision des valeurs de x (mm): ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_P.grid(row=5, column=0, sticky=N)
    precision_entry = Entry(Frame_HS, bg="#252526", fg="white")
    precision_entry.grid(row=6, column=0, sticky=N + S + E + W, pady=10)
    text_C = Label(
        Frame_HS,
        text="Haack parameter C: \\ Paramètre de Haack C: ",
        font=("Helvetica", 20),
        bg="#252526",
        fg="white",
    )
    text_C.grid(row=7, column=0, sticky=N)
    C_entry = Entry(Frame_HS, bg="#252526", fg="white")
    C_entry.grid(row=8, column=0, sticky=N + S + E + W, pady=10)
    Generate_button = Button(
        Frame_HS,
        text="Generate XYZ file",
        font=("Helvetica", 25),
        fg="#ffc600",
        bg="#01193b",
        command=lambda: Haack_series(
            precision_entry.get(), L_entry.get(), D_entry.get(), C_entry.get()
        ),
    )
    Generate_button.grid(row=9, column=0, sticky=N + S + E + W, pady=10)
    Frame_HS.pack(expand=YES)


# MAIN PART OF THE CODE

home = Tk()  # Definition of the home window
home.title("Ogivator LightEdition")  # Add title to the window
home.geometry("1280x720")  # Define the size of the window
home.minsize(1280, 720)  # Define the min size of the window
home.iconbitmap(resource_path("ICONE.ico"))  # Define the icon of the program
home.config(background="#252526")  # Define the color of the background
cadre = Frame(home, bg="#252526")  # Definition of a frame to contain all buttons
credit = Frame(home, bg="#252526")  # Definition of a frame to contain credits
logo_Eso = PhotoImage(file=resource_path("Logo_Eso.png")).subsample(
    9
)  # Addition of the picture of the ESO organization
canvas = Canvas(cadre, width=250, height=250, bg="#252526", bd=0, highlightthickness=0)
canvas.create_image(125.0, 125.0, image=logo_Eso)
canvas.grid(row=0, column=0, sticky=W)
developper = Label(
    credit,
    text="Developped by Clément Bouguyon 4th year Aersopace Engineering student at ESTACA in November 2023",
    font=("Helvetica", 10),
    bg="#252526",
    fg="white",
)
developper.grid(row=0, column=0, sticky=N)
cadre.pack(expand=YES)
credit.pack(expand=YES)
C = Button(
    cadre,
    text="Conic ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Conic,
)
C.grid(row=2, column=0, sticky=N + S + E + W, pady=(50, 5))
SBC = Button(
    cadre,
    text="Spherically blunted conic ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Spherically_blunted_conic,
)
SBC.grid(row=3, column=0, sticky=N + S + E + W, pady=5)
BC = Button(
    cadre,
    text="Bi-conic ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Bi_conic,
)
BC.grid(row=4, column=0, sticky=N + S + E + W, pady=5)
TO = Button(
    cadre,
    text="Tangent ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Tangent_ogive,
)
TO.grid(row=5, column=0, sticky=N + S + E + W, pady=5)
SBTO = Button(
    cadre,
    text="Spherically blunted tangent ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Spherically_blunted_tangent_ogive,
)
SBTO.grid(row=6, column=0, sticky=N + S + E + W, pady=5)
SO = Button(
    cadre,
    text="Secant ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Secant_ogive,
)
SO.grid(row=7, column=0, sticky=N + S + E + W, pady=5)
Ell = Button(
    cadre,
    text="Elliptical ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Elliptical,
)
Ell.grid(row=8, column=0, sticky=N + S + E + W, pady=5)
P = Button(
    cadre,
    text="Parabolic ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Parabolic,
)
P.grid(row=9, column=0, sticky=N + S + E + W, pady=5)
PS = Button(
    cadre,
    text="Power series ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Power_series,
)
PS.grid(row=10, column=0, sticky=N + S + E + W, pady=5)
HS = Button(
    cadre,
    text="Haack series ogive",
    font=("Helvetica", 12),
    fg="#252526",
    bg="white",
    command=Choix_Haack_series,
)
HS.grid(row=11, column=0, sticky=N + S + E + W, pady=5)
Wiki = Button(
    cadre,
    text="SHOW WIKIPEDIA PAGE FOR NOSE CONE INFORMATIONS",
    font=("Helvetica", 7),
    fg="#ffc600",
    bg="#01193b",
    command=openwiki,
)
Wiki.grid(row=12, column=0, sticky=N + S + E + W, pady=5)
home.mainloop()
