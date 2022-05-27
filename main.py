import pyvisa as visa
import time
from matplotlib.pyplot import ylabel, plot, show, xlabel

def voltagetracker(interval,duration):#min,min
    print("hi")
    x = []
    data = []
    print(interval,duration)
    rm = visa.ResourceManager()
    print(rm.list_resources())
    #Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    for i in range(int(duration/interval)+1):
        x.append(interval*i)
        data.append(i)#Keithley.query('V?'))
        time.sleep(interval)
    plot(x, data)
    xlabel('time (min)')
    ylabel('voltage (V)')
    show()
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
print("run")
voltagetracker(1,6)