import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

import random

def voltagetracker(interval,duration):#min,min
    duration=duration*60
    interval=interval*60
    mins=[]
    data=[]
    total={}
    #rm = visa.ResourceManager()
    #print(rm.list_resources())
    #Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    for i in range(int(duration/interval+1)):
        plt.clf()
        mins.append(interval*i)
        data.append(random.randint(1,100))
        #data[i]=random.randint(1,100)#Keithley.query('V?'))
        plt.plot(mins,data)
        plt.pause(interval)
    plt.title('Voltage Tracker')
    plt.xlabel('Time (min)')
    plt.ylabel('Voltage (V)')
    plt.show()
voltagetracker(1/60,1)