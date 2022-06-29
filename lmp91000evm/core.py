from tkinter import*
import spidev
import smbus
import time
#import math

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 1
spi.max_speed_hz=1000000

bus = smbus.SMBus(1)
address = 0x48

def write(value,reg):
    bus.write_byte_data(address,reg,value)
    
LOCK = int('00000000',2)
TIACN = int('00010000',2)
REFCN = int('10110000',2)
MODECN = int('00000011',2)

write(LOCK,1)
write(TIACN,16)
write(REFCN,17)
write(MODECN,18)

DATA_cv = [0]*25
            
#TIAG = TIA_values["{}".format(variable_TIA.get())]
TIAG=14000
vref = 2.5
volt_dicc={
           '-0.05':'10100010',
           '-0.10':'10100011',
           '-0.15':'10100100',
           '-0.20':'10100101',
           '-0.00':'10110000',
           '0.00':'10110000',
           '0.025':'10110001',
           '0.05':'10110010',
           '0.10':'10110011',
           '0.15':'10110100',
           '0.20':'10110101',
           '0.25':'10110110',
           '0.30':'10110111',
           '0.35':'10111000',
           '0.40':'10111001',
           '0.45':'10111010',
           '0.50':'10111011',
           '0.55':'10111100',
           '0.60':'10111101'        
          }
def decimal_range(start, stop, increment):
    while start <= stop:
        yield start
        start += increment
        
def decimal_range2(stop, start, decrement):
    while stop >= start:
        yield stop
        stop -= decrement 
        
def output(start:float,stop:float,sweep:float)->None:
    if((stop>start) and sweep<stop-start):
        k=0
        
        for x in decimal_range(start,stop,sweep):
            REFCN = int(volt_dicc["{:0.2f}".format(x)],2)
            #print(REFCN)
            bus.write_byte_data(address,17,REFCN)
            start_time = time.time()
            r = spi.readbytes(8)
            bin_r = r
            bin_r[0] = "{0:08b}".format(r[0])
            bin_r[1] = "{0:08b}".format(r[1])
            bin_r[2] = "{0:08b}".format(r[2])
            bin_r = bin_r[0] + bin_r[1] + bin_r[2]
            bin_r = bin_r[2:18]
            if bin_r[0] == '1':
                aux = bin_r.replace('1', '2').replace('0', '1').replace('2', '0')
                value = -int(aux,2)-1
            else:
                value = int(bin_r,2)

            vmax = 5-(vref/(2**16))
            binmax = ((2**16)-1)
            volts = (vmax*value)/(binmax)+vref
            current = ((volts-(vref/2))/(TIAG))*1000000
            print (" Step: %5.3f\n  Voltage: %5.3f V\m ; Current: %5.3f uA" %(start+k*sweep,volts,current))
            DATA_cv[k] = aux[0]
            k=k+1
            
            time.sleep(1-(time.time() - start_time))
            print("--- %s seconds ---" % (time.time() - start_time))
            
        k=1
        for x in decimal_range2(stop-sweep,start,sweep):
            REFCN = int(volt_dicc["{:0.2f}".format(x)],2)
            print(REFCN)
            bus.write_byte_data(address,17,REFCN)
            start_time = time.time()
            r = spi.readbytes(8)
            bin_r = r
            bin_r[0] = "{0:08b}".format(r[0])
            bin_r[1] = "{0:08b}".format(r[1])
            bin_r[2] = "{0:08b}".format(r[2])
            bin_r = bin_r[0] + bin_r[1] + bin_r[2]
            bin_r = bin_r[2:18]
            if bin_r[0] == '1':
                aux = bin_r.replace('1', '2').replace('0', '1').replace('2', '0')
                value = -int(aux,2)-1
            else:
                value = int(bin_r,2)

            vmax = 5-(vref/(2**16))
            binmax = ((2**16)-1)
            volts = (vmax*value)/(binmax)+vref
            current = ((volts-(vref/2))/(TIAG))*1000000
            print (" Step: %5.3f\n  Voltage: %5.3f V\m ; Current: %5.3f uA" %(stop-k*sweep,volts,current))
            DATA_cv[k] = aux[0]
            k=k+1
            
            time.sleep(1-(time.time() - start_time))
            print("--- %s seconds ---" % (time.time() - start_time))
    else:
            return 0


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



def startCV():
    
    w.delete("1.0","end")
    w.insert('1.0', ">> Transimpedance value selected: {}".format(variable_TIA.get())+'\n'+'\n')
    w.insert('1.0', ">> Operation mode selected: {}".format(variable_OPMODE.get())+'\n'+'\n')
    w.insert('1.0', ">> Starting sweep..."+'\n'+'\n')
    print (">> Transimpedance value selected: {}".format(variable_TIA.get())) 
    print (">> Operation mode selected: {}".format(variable_OPMODE.get()))
    print (">> Starting cyclic voltammetry...")
    print(output(-0.2,0.6,0.05))

menubar = Menu(root)
menubar.add_command(label="Start",command=startCV)
menubar.add_command(label="Clear")
menubar.add_command(label="Save graph")
menubar.add_command(label="Export .csv")
menubar.add_command(label="Save data to DB")
menubar.add_command(label="Close")

root.config(menu=menubar)
root.mainloop()