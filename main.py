import pyvisa as visa
import time
from datetime import datetime
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import random

def voltagetracker(interval,duration):#min,min
    duration=duration*60
    interval=interval*60
    mins=[]
    data=[]

    try:
        os.chdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")
    except:
        os.mkdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")
    timestamp=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    rm = visa.ResourceManager()
    print(rm.list_resources())
    datafile=open(f"{timestamp}.csv","w")
    datafile.write("Time(X), Voltage(V) \n")
    Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    for i in range(int(duration/interval+1)):
        plt.clf()
        mins.append(interval*i)
        data.append(Keithley.query("V?"))
        datafile.write(f"{mins[-1]},{data[-1]}\n")
        plt.plot(mins,data)
        plt.pause(interval)
    datafile.close()
    plt.title('Voltage Tracker')
    plt.xlabel('Time (min)')
    plt.ylabel('Voltage (V)')
    plt.show()
voltagetracker(1/60,1)