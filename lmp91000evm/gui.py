from tkinter import *
from .core import startCV, exportCSV

root = Tk()
root.wm_title("CVGIT")
root.geometry('880x500+100+100')

DATA_cv = [0]*33
t_cv={-0.2,-0.15,-0.1,-0.05,0,0.05,0.10,0.15,0.2,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.6,0.55,0.5,0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0,-0.05,-0.1,-0.15,-0.2}

TITLE = Label(root, text='Cyclic Voltammetry GIT Client Interface')
TITLE.grid(column='1',row='1',columnspan='3',rowspan='1',pady=20)

substance = Label(root, text='Substance: Pottasium ferrocyanide in KCl')
substance.grid(column='1',row='3',columnspan='1',rowspan='1')

variable_TIA = StringVar(root)
variable_TIA.set("Default")

TIA_label = Label(root,text='TIA gain')
TIA_label.grid(column='3',row='2',columnspan='1',rowspan='1')

TIA = OptionMenu(root, variable_TIA, "Default", "2.75 KOhms",
                 "3.5 KOhms", "7 KOhms", "14 KOhms",
                 "35 KOhms", "120 KOhms", "350 KOhms")
TIA.grid(column='3',row='3',columnspan='1',rowspan='1')

variable_OPMODE = StringVar(root)
variable_OPMODE.set("Default")


w = Text(root, width='60', height='12', bg='yellow', relief = 'groove')
w.grid(column='1',row='9',columnspan='3',rowspan='1',pady=50,padx=20)
w.insert('1.0','\n Welcome to Cyclic Voltammetry Client Interface.\n Please:\n 1) Insert the SPE in the adapters plug.\n 2) Choose your fit config\n    (TIA and OPMODE).\n 3) Click Start and save graph.\n'+'\n'+'\n'+'IISER Bhopal')



menubar = Menu(root)
menubar.add_command(label="Start",command=startCV)
menubar.add_command(label="Clear")
menubar.add_command(label="Save graph")
menubar.add_command(label="Export .csv",command=exportCSV)
menubar.add_command(label="Save data to DB")
menubar.add_command(label="Close")

root.config(menu=menubar)
root.mainloop()