import pyvisa as visa
import time
from datetime import datetime
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import random

def voltagetracker(voltage,current,interval,duration):#min,min
    duration=duration*60
    interval=interval*60
    mins=[]
    voltdata=[]
    currdata=[]
    timedata=[]

    try:
        os.chdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")
    except:
        os.mkdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")

    timestamp=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    rm = visa.ResourceManager()
    datafile=open(f"{timestamp}.csv","w")
    datafile.write("Time(X), Current(A), Voltage(V), Time(s)\n")
    Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    Keithley.read_termination = '\n'
    Keithley.write_termination = '\n'
    for i in range(int(duration/interval+1)):
        x=0
        y=0
        z=0
        plt.clf()
        mins.append(interval*i)
        #hold=Keithley.query(":MEAS:VOLT?")
        x,y,z=Keithley.query(":MEAS:VOLT?").split(",")
        x=float(x[1:-1])
        y=float(y[1:-1])
        z=float(z[1:-1])
        currdata.append(x)
        voltdata.append(y)
        timedata.append(z)
        #stagger time based on initial timepoint
        datafile.write(f"{mins[-1]},{currdata[-1]},{voltdata[-1]},{timedata[-1]}\n")
        plt.plot(mins,voltdata)
        plt.pause(interval)
    datafile.close()
    plt.title('Voltage Tracker')
    plt.xlabel('Time (sec)')
    plt.ylabel('Voltage (V)')
    plt.show()

voltagetracker(0,.26,1/60,1/6)#Voltage(V),Current(A),Interval length(X), Duration(X)