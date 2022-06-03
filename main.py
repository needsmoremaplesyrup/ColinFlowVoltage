import pyvisa as visa
from datetime import datetime
import os
import matplotlib.pyplot as plt


def tracker(voltage, current, interval, duration):  #V,A,min,min
    voltdata = []
    currdata = []
    timedata = []
    x, y, z, start = (0, 0, 0, 0)
    minsec = "sec"

#Convert minutes into seconds
    duration = duration*60
    interval = interval*60

    #labels
    if duration > 180:
        minsec = "min"

    #check for file folder, if it doesn't exist make it
    try:
        os.chdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")
    except:
        os.mkdir(f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles")

    #find date & time then create file and write header in file
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    datafile = open(f"{timestamp}.csv", "w")
    datafile.write("Time(s), Current(A), Voltage(V)\n")

    #Start communicating with device
    rm = visa.ResourceManager()
    Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    Keithley.read_termination = '\n'
    Keithley.write_termination = '\n'
    Keithley.query("*IDN?")

    for i in range(int(duration/interval+1)):
        plt.clf()
        x, y, z = Keithley.query(":MEAS:VOLT?").split(",")  #idk why i asks for VOLT and get TIME,VOLT,CURR
        x, y, z = (float(x[1:-1]), float(y[1:-1]), float(z[1:-1]))
        if i == 0:
            start = z
        z = round(z-start, 5)
        currdata.append(x)
        voltdata.append(y)
        timedata.append(z)
        datafile.write(f"{timedata[-1]},{currdata[-1]},{voltdata[-1]}\n")
        if duration >= 180:
            timedata[-1] = round(timedata[-1]/60, 1)
        plt.plot(timedata, voltdata, "o-")
        plt.pause(interval)

    datafile.close()
    #select V or A, or have both as subplots side by side
    plt.title('Voltage')
    plt.xlabel(f'Time ({minsec})')
    plt.ylabel('Voltage (V)')
    #save graph as image
    plt.show()


tracker(30, .26, .1, 1)#Voltage(V),Current(A),Interval length(X), Duration(X)
