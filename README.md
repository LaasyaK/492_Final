This Repository holds all the files needed to collect data from an ultrasonic sensor and other devices set up on a breadboard. This breadboard was connected to a RasberryPi (where MonitoringApp.py was run to collect data). The file made by the RasberryPi was then used to plot data with ViewData.py.
Each of the files have multiple functions:
  - Collecting data from the setup can be run as 'MonitoringApp.py' and it can run 2 modes according to the press of the button:
      - less than 2 second press of the button runs Monitor System:
          - the LED connected flashes at a frequency from 0.5Hz-4Hz respective to the distance measured by the ultrasonic sensor
          - the LED instantanous changes its flashing frequency from a distance of 0cm-100cm of the sensor
      - more than 2 second press of the button runs Only Record Data:
          - records the data collected from the sensor every 0.1 second and stores it in a csv file until the mode is changed
          - after a change in the mode, the file is named with the date and stored in the RasberryPi to use for the next file
      - more than 5 second press of the button shuts down the program
  - Plotting the data can be run as 'ViewData.py dataFile':
      - it plots Distance vs Time on a scatter plot
      - it asks if you want to save the plot and if yes, saves it as a png

This program was written for the ECE 492 Python in Engineering class. 
Author: Laasya Kallepalli, 
Date: 8/16/2023
