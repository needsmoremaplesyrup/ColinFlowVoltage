import pyvisa as visa
from datetime import datetime
import os
import matplotlib.pyplot as plt

def voltagetracker(voltage,current,interval,duration):#V,A,min,min
    voltdata = []
    currdata = []
    timedata = []
    x, y, z, start = (0, 0, 0, 0)

    #Convert minutes into seconds
    duration=duration*60
    interval=interval*60

    #check for file folder, if it doesn't exist make it
    try:
        os.chdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")
    except:
        os.mkdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")

    #find date & time then create file and write header in file
    timestamp=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    datafile=open(f"{timestamp}.csv","w")
    datafile.write("Time(s), Current(A), Voltage(V)\n")

    #Start communicating with device
    rm = visa.ResourceManager()
    Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    Keithley.read_termination = '\n'
    Keithley.write_termination = '\n'
    Keithley.query("*IDN?")

    for i in range(int(duration/interval+1)):
        plt.clf()
        x,y,z=Keithley.query(":MEAS:VOLT?").split(",")
        x,y,z=(float(x[1:-1]),float(y[1:-1]),float(z[1:-1]))
        if i==0:
            start=z
        z=z-start
        currdata.append(x)
        voltdata.append(y)
        timedata.append(z)
        datafile.write(f"{timedata[-1]},{currdata[-1]},{voltdata[-1]}\n")
        if interval>=60:
            timedata[-1]=round(timedata[-1]/60)
        plt.plot(timedata,voltdata)
        plt.pause(interval)

    datafile.close()
    plt.title('Voltage Tracker')
    plt.xlabel('Time (sec)')
    plt.ylabel('Voltage (V)')
    plt.show()

voltagetracker(30,.26,1/60,1/6)#Voltage(V),Current(A),Interval length(X), Duration(X)