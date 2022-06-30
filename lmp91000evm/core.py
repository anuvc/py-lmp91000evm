
from typing import Dict
import spidev
import smbus
import time
import numpy as np

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 1
spi.max_speed_hz=1000000

bus = smbus.SMBus(1)
address = 0x48

def write_to_register(value, register):
    bus.write_byte_data(address, register, value)


vref = 2.5


def decimal_range(start, stop, increment):
    while start <= stop:
        yield start
        start += increment
        
def decimal_range2(stop, start, decrement):
    while stop >= start:
        yield stop
        stop -= decrement 

register = {
    'BIAS': 17
}

def set_voltage(voltage: float) -> None:
    REFCN = volt_dicc[voltage]
    write_to_register(REFCN, register['BIAS'])

def sweep(start_volt:float, stop_volt:float, scan_rate:float, TIAG: int) -> Dict[float:float]:
    readings = {}
    step = 0.05
    wait_time = step/scan_rate
    for voltage in np.arange(start_volt, stop_volt, scan_rate):
        # Start timer
        start_time = time.time()
        # Set voltage and read current
        set_voltage(voltage)
        aux, volts, current = read_current(TIAG)
        # Store reading
        readings[voltage] = current

        # Print output 
        print (" Step: %5.3f\n  Voltage: %5.3f V\m ; Current: %5.3f uA" %(start+k*sweep,volts,current))
        # Stop timer
        time.sleep(wait_time-(time.time() - start_time))
        print("--- %s seconds ---" % (time.time() - start_time))

    
def read_current(TIAG):
    r = spi.readbytes(8)
    # print(r)
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
    return aux,volts,current


def cyclic_voltammetry(min, max, scan_rate):
    if((stop>start) and sweep<stop-start):
        k=0
        l=0
    # forward sweep
    sweep(min, max, scan_rate)
    # backward sweep
    sweep(max, min, scan_rate)

def startCV():
    w.delete("1.0","end")
    w.insert('1.0', ">> Transimpedance value selected: {}".format(variable_TIA.get())+'\n'+'\n')
    w.insert('1.0', ">> Operation mode selected: {}".format(variable_OPMODE.get())+'\n'+'\n')
    w.insert('1.0', ">> Starting sweep..."+'\n'+'\n')
    print (">> Transimpedance value selected: {}".format(variable_TIA.get())) 
    print (">> Operation mode selected: {}".format(variable_OPMODE.get()))
    print (">> Starting cyclic voltammetry...")
    
    TIA = TIA_dicc["{}".format(variable_TIA.get())]
    TIAG = TIA_values["{}".format(variable_TIA.get())]
    
    LOCK = int('00000000',2)
    TIACN = int(TIA,2)
    REFCN = int('10110000',2)
    MODECN = int('00000011',2)

    write(LOCK,1)
    write(TIACN,16)
    write(REFCN,17)
    write(MODECN,18)
    print(output(-0.2,0.6,0.05,TIAG))
    
def main():
    pass

if __name__ == "__main__":
    main()
