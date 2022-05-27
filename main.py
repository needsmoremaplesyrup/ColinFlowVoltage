import pyvisa as visa
import time
import numpy
import matplotlib.pyplot as plt
'''
x=10
y=66

for i in range(int(y/x)):
    print(i)

'''
def voltagetracker(interval,duration):#min,min
    x = []
    data = []
    print(interval,duration)
    rm = visa.ResourceManager()
    rm.list_resources()
    #Keithley = rm.open_resource('GPIB0::xx::INSTR')

    for i in range(int(duration/interval)+1):
        x.append(interval*i)
        data.append(i)#Keithley.query('V?'))
        time.sleep(interval)
    plt.plot(x,data)
    plt.xlabel('time (min)')
    plt.ylabel('voltage (V)')
    plt.show()
'''
class voltagetracker:#min,min
    def __init__(self,interval,duration,x,data):
        print(interval,duration)
        interval=interval
        duration=duration
        x = []
        data = []
    print(self.interval,self.duration)
    rm = visa.ResourceManager()
    rm.list_resources()
    #Keithley = rm.open_resource('GPIB0::xx::INSTR')

    for i in (self.duration/interval):
        time.sleep(interval*60)
        self.x.append(interval*i)
        self.data.append(Keithley.query('V?'))
    plt.plot(self.time,self.data)
    plt.xlabel('time (min)')
    plt.ylabel('voltage (V)')
    plt.show()
'''

voltagetracker(1,6)