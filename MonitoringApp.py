from gpiozero import Button, LED, RGBLED, DistanceSensor, PWMOutputDevice, PWMLED
from signal import pause
import time
from datetime import datetime
from datetime import date
import csv
import threading
import RPi.GPIO as gpio


# set ups
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(14, gpio.OUT, initial=gpio.LOW)    # for the led
light = gpio.PWM(14, 0.5)
led = LED(14)
button = Button(16)
RGB = RGBLED(red=5, green=6, blue=13)
sensor = DistanceSensor(24, 25, max_distance=100)

# *** mode MS: Monitor System ***
def MS():
       
    # showing in MS mode
    print("\n***** {In Monitor System Mode} *****")
    RGB.color = (.7,0,0)
    
    # getting continous distance data and changing LED accordingly
    while not(button.is_pressed):
        if (sensor.distance*100) > 20:
            gpio.output(14, 0)
            while (sensor.distance*100) > 20 and not(button.is_pressed):
                if (sensor.distance*100) >= 100:
                    print("100 cm - 0 Hz")
                    time.sleep(.1)
                else:
                    print(str(sensor.distance*100) + " cm - 0 Hz")
                    time.sleep(.1)
        elif (sensor.distance*100) >= 16 and (sensor.distance*100) <= 20:
            light.ChangeFrequency(0.5)
            light.start(50)
            while (sensor.distance*100) >= 16 and (sensor.distance*100) <= 20 and not(button.is_pressed):
                print(str(sensor.distance*100) + " cm - 0.5 Hz")
                time.sleep(.1)
            light.stop()
        elif (sensor.distance*100) >= 12 and (sensor.distance*100) < 16:
            light.ChangeFrequency(1)
            light.start(50)
            while (sensor.distance*100) >= 12 and (sensor.distance*100) < 16 and not(button.is_pressed):
                print(str(sensor.distance*100) + " cm - 1 Hz")
                time.sleep(.1)
            light.stop()
        elif (sensor.distance*100) >= 8 and (sensor.distance*100) < 12:
            light.ChangeFrequency(2)
            light.start(50)
            while (sensor.distance*100) >= 8 and (sensor.distance*100) < 12 and not(button.is_pressed):
                print(str(sensor.distance*100) + " cm - 2 Hz")
                time.sleep(.1)
            light.stop()
        elif (sensor.distance*100) >= 4 and (sensor.distance*100) < 8:
            light.ChangeFrequency(4)
            light.start(50)
            while (sensor.distance*100) >= 4 and (sensor.distance*100) < 8 and not(button.is_pressed):
                print(str(sensor.distance*100) + " cm - 4 Hz")
                time.sleep(.1)
            light.stop()
        elif (sensor.distance*100) < 4:
            light.ChangeFrequency(100)
            light.start(50)
            while (sensor.distance*100) < 4 and not(button.is_pressed):
                print(str(sensor.distance*100) + " cm - 100 Hz (or on)")
                time.sleep(.1)
            light.stop()
        else:
            print("Error")
    return("Out of MS")
          
# *** mode ORD: Only Record Data ***
def ORD():
    
    # showing in ORD mode
    print("\n***** {In Only Record Data Mode} *****")
    RGB.color = (0,.7,0)
    
    # creating a new file
    currentDate = date.today()
    currentMonth = str(currentDate.month).zfill(2)
    currentDay = str(currentDate.day)
    currentYear = (str(currentDate.year))[2:]
    currentTime = (datetime.now()).strftime("%H_%M_%S")
    print("Recording data to filename:", end=" ")
    print("Started_" + currentMonth + currentDay + currentYear + "_" + currentTime + ".csv")
    header = [["Date", "Time", "Distance"]]
    filepath = "/home/pi/Documents/Started_" + currentMonth + currentDay + currentYear + "_" + currentTime + ".csv"
    with open(filepath, 'w', newline='') as file:
        add = csv.writer(file)
        add.writerows(header)
    
    # collecting data to append to file
    temp1 = []
    while not(button.is_pressed):
        while len(temp1) <= 100 and not(button.is_pressed):
            dateNow = str(date.today())
            timeNow = str(datetime.now().time())
            if (sensor.distance*100) >= 100:
                distance = str(100)
            else:  
                distance = str(round(sensor.distance*100, 2))
            temp1.append([dateNow, timeNow[0:12], distance])
            time.sleep(.1)
        
        # putting 10 secs of info in file
        try:
            with open(filepath, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(temp1)
            temp1 = []
        except FileNotFoundError:
            print("The file is not found. Program is ending.")
            exit(0)
        
    # stopping collecting data
    print("Stopped Recording data to filename:", end=" ")
    print("Started_" + currentMonth + currentDay + currentYear + "_" + currentTime + ".csv")
    return("Out of ORD")

# *** function to direct mode ***
def to_func():
    while 1:
        while button.is_pressed:
            print("Button is pressed")
            time_count = 0
            while time_count < 5:
                time.sleep(0.1)
                time_count = time_count + 0.1
                
                # to star MS mode
                if time_count < 2 and not(button.is_pressed):
                    MS()
                    break
                
                # to start ORD mode
                if time_count >= 2 and not(button.is_pressed):
                    ORD()
                    break
                
            # to close program
            if time_count >= 5:
                RGB.color = (0,0,.7)
                not_valid = True
                while not_valid:
                    to_close = input("Do you want to close the program? (type 'y' or 'n'): ")
                    try:
                        if str(to_close) == "y":
                            not_valid = False
                            RGB.color = (0,0,0)
                            light.stop()
                            print("Program closing.")
                            exit(0)
                        elif str(to_close) == "n":
                            not_valid = False
                            print("The program will start In Monitor System Mode in 3 seconds.\n")
                            time.sleep(3)
                            MS()
                            break
                        else:
                            print("Need to enter 'y' or 'n', try again.\n")
                    except ValueError:
                        print("Need to enter 'y' or 'n', try again.\n")
        time.sleep(0.1)

# catching a keyboard interrupt
try:

    # asking user to install GPIO Zero
    print("Make sure to install GPIO Zero library to use this program.\n")
    print("NOTE: The Distance Sensor can't measure more than 100 cm.")
    print("To use this program:\n-  single click the button to start Monitor System Mode\n-  hold the button for 2 seconds to start Only Record Data\n-  hold the button for 5 seconds to close the program")
    print("Monitor System Mode will automatically start in 10 seconds unless a respective button press condition is made...")

    # when program runs first is on MS
    time_c = 0
    first_pressed = False
    while time_c < 10:
        time.sleep(0.1)
        time_c = time_c + 0.1
        if button.is_pressed:
            first_pressed = True
            time_c = 10
            to_func()
    if not(first_pressed):
        MS()
        to_func()

except KeyboardInterrupt:
    RGB.color = (0,0,0)
    light.stop()
    f.close()
    print("Program closing.")
    exit(0)
    


