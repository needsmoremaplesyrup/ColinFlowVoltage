import pyvisa as visa
from datetime import datetime
import os
import matplotlib.pyplot as plt

def voltagetracker(voltage,current,interval,duration):#min,min
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
    print(Keithley.query("*IDN?"))
    Keithley.write(":SENSe:CURRent:RANGe:AUTO ON")
    #Keithley.write(":FORMat:ELEMents \"MODE, CC\"")
    #Keithley.write(f":VOLT {voltage}")
    #Keithley.write(f":CURR {current}")
    for i in range(int(duration/interval+1)):
        plt.clf()
        mins.append(interval*i)
        data.append(Keithley.query("SENS:FUNC \"VOLT\"?"))
        datafile.write(f"{mins[-1]},{data[-1]}\n")
        plt.plot(mins,data)
        plt.pause(interval)
    datafile.close()
    plt.title('Voltage Tracker')
    plt.xlabel('Time (min)')
    plt.ylabel('Voltage (V)')
    plt.show()

voltagetracker(30,.26,1/60,1)#Voltage(V),Current(A),Interval length(X), Duration(X)