import pyvisa as visa
from datetime import datetime
import os
import matplotlib.pyplot as plt


def tracker(interval, duration):
    #min,min
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
    name=input("Type name of file: ")
    if(name==""):
        name=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    else:
        pass
    #timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    datafile = open(f"{name}.csv", "w")
    datafile.write("Time(s), Voltage(V), Current(A)\n")

    #Start communicating with device
    rm = visa.ResourceManager()
    Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    Keithley.read_termination = '\n'
    Keithley.write_termination = '\n'
    Keithley.query("*IDN?")

    try:
        for i in range(int(duration/interval+1)):
            plt.clf()
            x, y, z = Keithley.query(":MEAS:VOLT?").split(",")  #idk why i asks for VOLT and get TIME,VOLT,CURR
            #Remove + and unit from data
            x, y, z = (float(x[1:-1]), float(y[1:-1]), float(z[1:-1]))
            #adjusting time data to use it for timepoint from initial start
            if i == 0:
                start = z
            z = round(z-start, 5)
            #add to lists
            currdata.append(x)
            voltdata.append(y)
            timedata.append(z)
            #write data to file
            datafile.write(f"{timedata[-1]},{voltdata[-1]},{currdata[-1]}\n")
            #adjusts time units if duration is too long for seconds to make sense
            if duration >= 180:
                timedata[-1] = round(timedata[-1]/60, 1)
            plt.plot(timedata, voltdata)
            plt.pause(interval)

    except:
        datafile.close()
        plt.plot(timedata, voltdata)
        plt.title('Voltage')
        plt.xlabel(f'Time ({minsec})')
        plt.ylabel('Voltage (V)')
        plt.savefig(f"{name}.png")
        plt.show()
    else:
        datafile.close()
        #select V or A, or have both as subplots side by side
        plt.title('Voltage')
        plt.xlabel(f'Time ({minsec})')
        plt.ylabel('Voltage (V)')
        #save graph as image
        plt.savefig(f"{name}.png")
        plt.show()



tracker(.25, 10)#Interval length(X), Duration(X)
