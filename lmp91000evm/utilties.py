import csv
from tkinter import *

root = Tk()

variable_TIA = StringVar(root)
variable_TIA.set("Default")

variable_OPMODE = StringVar(root)
variable_OPMODE.set("Default")

w = Text(root, width='60', height='12', bg='yellow', relief = 'groove')

def exportCSV():
    str = "cv"+".csv"
    csv_out = open(str, 'wb')
    mywriter = csv.writer(csv_out)
    for row in zip(t_cv, DATA_cv):
        mywriter.writerow(row)
    csv_out.close()
    w.insert('1.0', "Data exported to .csv succesfully!"+'\n'+'\n')