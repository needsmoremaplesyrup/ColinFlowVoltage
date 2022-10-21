import pyvisa as visa
from datetime import datetime
import os
import time
import matplotlib.pyplot as plt

def namecheck(name,namelist,iter):
    iter+=1
    newname = name + f"({iter})"
    if newname+".csv" in namelist:
        return(namecheck(name,namelist,iter))
    else:
        return(newname)


def tracker():
    # data variables
    voltdata = []
    currdata = []
    timedata = []
    x, y, z, start = (0, 0, 0, 0)
    minsec = "sec"
    directory=f"C:\\Users\\{os.getlogin()}\\Documents\\VoltageDatafiles"
# check for datafile folder, if it doesn't exist make it
    try:
        os.chdir(directory)
    except:
        os.mkdir(directory)

# name data file, if no name entered use date and time
    namelist=os.listdir(directory)
    print(namelist)
    name = input("Type name of file: ")
    if name == "":
        name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    if name+".csv" in namelist:
        overwrite = input(f"File named {name} found. Overwrite?(Y/N): ")
        if overwrite == "Y" or "y" or "yes" or "YES":
            pass
        if overwrite == "N" or "n" or "no" or "NO" or "":
            name=namecheck(name,namelist,0)

# open data file and write headings
    datafile = open(f"{name}.csv", "w")
    datafile.write("Time(s), Voltage(V), Current(A)\n")

# Get time values for duration of run and interval between measurements
    duration = input("Duration (min): ")
    interval = input("Intervals (min): ")
    if duration == "":
        duration = 120
    if interval == "":
        interval = .25

# adjust values into seconds
    duration = float(duration)*60
    interval = float(interval)*60

# if duration is longer than 3 min use minutes rather than seconds in the graphing
    if duration > 180:
        minsec = "min"

#CURRENT OR VOLTAGE?
    dattype=input("V or C?")
    if dattype=="V":
        dattype=0
    elif dattype=="C":
        dattype=1
    else:
        print("only V or C please, defaulting to Voltage")
        dattype=0

    '''
# input voltage and currents
    voltage = input("Input voltage(V): ")
    current = input("Input current(A): ")
    if voltage == "":
        voltage = 30
    if current == "":
        current = .26
    voltage=float(voltage)
    current=float(current)
    '''
# Start communicating with device
    rm = visa.ResourceManager()
    Keithley = rm.open_resource('USB0::0x05E6::0x2280::4386872::INSTR')
    Keithley.read_termination = '\n'
    Keithley.write_termination = '\n'

# check connections
    print(Keithley.query("*IDN?"))
    print(duration,interval)


    try:
        # set parameters on device and turn device on
        #Keithley.write(f":VOLT {str(voltage)}")
        #Keithley.write(f":CURR {str(current)}")
        #Keithley.write(":INIT:CONT ON")
        for i in range(int(duration/interval+1)):
            plt.clf()
            time.sleep(1)
            x, y, z = Keithley.query(":MEAS:VOLT?").split(",")  # idk why i asks for VOLT and get TIME,VOLT,CURR
            # Remove + and unit from data
            x, y, z = (float(x[1:-1]), float(y[1:-1]), float(z[1:-1]))
            # adjusting time data to use it for timepoint from initial start
            if i == 0:
                start = z
            z = round(z-start, 5)
            # add to lists
            currdata.append(x)
            voltdata.append(y)
            timedata.append(z)
            # write data to file
            datafile.write(f"{timedata[-1]},{voltdata[-1]},{currdata[-1]}\n")
            # adjusts time units if duration is too long for seconds to make sense
            if duration >= 180:
                timedata[-1] = round(timedata[-1]/60, 1)
            if dattype:
                plt.plot(timedata, currdata)
            else:
                plt.plot(timedata, voltdata)
            plt.savefig(f"{name}.png")
            plt.pause(interval)

    except:
        # if error occurs, turn power supply off, save the graph
        '''
        Keithley.write(":OUTP OFF")
        Keithley.write(":VOLT 0")
        Keithley.write(":CURR 0")
        '''
        if dattype:
            plt.plot(timedata, currdata)
        else:
            plt.plot(timedata, voltdata)
        plt.savefig(f"{name}.png")

    datafile.close()
    # turn power supply off
    '''
    Keithley.write(":OUTP OFF")
    Keithley.write(":VOLT 0")
    Keithley.write(":CURR 0")
    '''
    if dattype:
        plt.plot(timedata, currdata)
        plt.title('Current')
        plt.ylabel('Current (A)')
    else:
        plt.plot(timedata, voltdata)
        plt.title('Voltage')
        plt.ylabel('Voltage (V)')
    plt.xlabel(f'Time ({minsec})')
    plt.savefig(f"{name}.png")
    # save graph as image
    plt.show()


tracker()
