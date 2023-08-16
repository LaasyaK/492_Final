"""
Author: Laasya Kallepalli
Date: 7/27/2023
Purpose: Reads Distance Sensor Data collected from MonitoringApp.py to generate a scatter plot of Distance versus time.
Input(s): needs 1 commandline argument, inputted as an example 'Started_072723_20_25_43.csv' as the file name made
from the MonitoringApp.py file
Output(s): creates a scatter plot of all the Data in the file of Distance in cm vs time in sec
"""
import sys
import platform
import re
import os
import csv
from matplotlib import pyplot as plt
import numpy as np
import math



# before running
print("Make sure to install the math, matplotlib, and numpy libraries to use this program.\n")

# ***** checking everything with the fileName given *****
# checking if too arguments are given
if len(sys.argv) > 2:
    print("\nToo many arguments given. Needs to be inputted in the format for example: python ViewData.py"
          " Started_072723_20_25_43.csv")
    print("Try again.")
    exit(0)

# checking if filename argument given
if len(sys.argv) < 2:
    print("\nToo little arguments given. Needs to be inputted in the format for example: python ViewData.py"
          " Started_072723_20_25_43.csv")
    print("This is the directory of the subfolder 'DataFiles': ")
    currentDir = os.getcwd()
    newDir = os.path.join(currentDir, "DataFiles")
    print(newDir)
    print("Try again.")
    exit(0)

# checking file type
file = sys.argv[1]
fileTypeGroup = re.split(r'\.', file)
startedGroup = re.match(r'^.{7}', file)
try:
    fileType = fileTypeGroup[1]
    fileCorrect = startedGroup.group()
    if not(fileType == "csv"):
        print("\nThe file inputted in the argument does not have the right file type to find data from. File type "
              "'csv' is only allowed. Try again.")
        exit(0)
    elif not(fileCorrect == "Started"):
        print("\nThe file inputted in the argument is not made for this program, Try again.")
        exit(0)
except IndexError:
    print("\nThe file inputted in the argument does not have a file type or it's not a file that is made for "
          "this program, Try again.")
    exit(0)

# checking if file exists
try:
    operating_system = platform.system()
    folder_path = os.path.abspath("DataFiles")
    if operating_system == "Windows":
        filename = folder_path + "\\" + file
    else:
        filename = folder_path + "/" + file
except FileNotFoundError:
    print("\nThe file inputted into the argument does not exist, Try again.")
    exit(0)
except FileExistsError:
    print("\nThe file inputted into the argument does not exist, Try again.")
    exit(0)

# ***** plotting the data from the file *****
# open csv file and take info in 2 arrays for x and y-axis
xAxis = np.array([])
yAxis = np.array([])
startTime = ""
date = ""
try:
    with open(filename, 'r', newline='') as f:
        csvData = csv.reader(f)
        firstRow = True
        secondRow = True
        count = 0
        for row in csvData:
            if firstRow:
                firstRow = False
                continue
            else:
                if secondRow:
                    secondRow = False
                    startTime = row[1][0:10]
                    date = row[0]
                xAxis = np.append(xAxis, count)
                count = count + 0.1           # data for every ms
                yAxis = np.append(yAxis, float(row[2]))
except FileNotFoundError:
    print("The file is not in the DataFiles folder, Try again.")
    exit(0)

# making a plot
plt.scatter(xAxis, yAxis)
plt.xlabel('Time after the start time (sec)')
plt.ylabel('Distance from Sensor (cm)')
plt.title('Scatter Plot of Distance vs Time on ' + date + ' at ' + startTime)

# making the yticks on the axis
minY_tick = int(math.floor(np.min(yAxis)))
maxY_tick = int(math.ceil(np.max(yAxis)))
numOfY_ticks = (maxY_tick - minY_tick)

if not(numOfY_ticks < 21):
    to_skip = round((numOfY_ticks/20))
else:
    to_skip = 1
y_ticks = []
count = minY_tick
while count <= maxY_tick:
    y_ticks.append(count)
    count = count + to_skip
plt.yticks(y_ticks)

# making the xticks on the axis
minX_tick = xAxis[0]
maxX_tick = xAxis[-1]
numOfX_ticks = len(xAxis)
if not(numOfX_ticks < 11):
    to_skip = (round(numOfX_ticks//10)) * 0.1
else:
    to_skip = .1
x_ticks = []
count = minX_tick
while count <= maxX_tick:
    x_ticks.append(count)
    count = count + to_skip
plt.xticks(x_ticks)

# intructions to save
print("After the scatter plot is shown and exited out of, you have the option to save the plot.")
plt.grid(True)

# saves first then deletes
saveNameGroup = re.match(r'^.*?\.', file)
saveName = (saveNameGroup.group()) + "png"
if operating_system == "Windows":
    path = folder_path + "\\" + saveName
else:
    path = folder_path + "/" + saveName
plt.savefig(path)
plt.show()

to_save = input("Do you want to save this plot? (type 's' to save or any other key to close the program): ")
try:
    if to_save == "s":
        print("The plot is saved to: " + saveName + " in the DataFiles folder.\n")
    else:
        os.remove(path)
        plt.close()
        print("Program closing.")
        exit(0)
except KeyboardInterrupt:
    plt.close()
    print("Program closing.")
    exit(0)
