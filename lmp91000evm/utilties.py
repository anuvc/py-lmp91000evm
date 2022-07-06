import csv
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

readings = []

DATA_cv = [0]*33
t_cv=[-0.2,-0.15,-0.1,-0.05,0,0.05,0.10,0.15,0.2,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.6,0.55,0.5,0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0,-0.05,-0.1,-0.15,-0.2]

root = Tk()

variable_TIA = StringVar(root)
variable_TIA.set("Default")

variable_OPMODE = StringVar(root)
variable_OPMODE.set("Default")

variable_scan_rate = StringVar(root)
variable_scan_rate.set("0.05")

w = Text(root, width='60', height='12', bg='yellow', relief = 'groove')

f = Figure(figsize=(4,3), dpi=120, facecolor='white', frameon=False,tight_layout=True)
a = f.add_subplot(111,title='CV 50mV/s - CVGIT',xlabel='v, V',
                  ylabel='i,'+ u"\u00B5"+'A',autoscale_on=True)
dataPlot = FigureCanvasTkAgg(f, master=root)
dataPlot.draw()
dataPlot.get_tk_widget().grid(column='5',row='3', columnspan='2', rowspan='10')



def exportCSV():
    str = "cv"+".csv"
    csv_out = open(str, 'w')
    mywriter = csv.writer(csv_out)
    for row in zip(t_cv, readings):
        mywriter.writerow(row)
    csv_out.close()
    w.delete("1.0","end")
    w.insert('1.0', "Data exported to .csv succesfully!"+'\n'+'\n')