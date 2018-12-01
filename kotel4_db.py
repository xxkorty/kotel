#!/usr/bin/env python3



from __future__ import division
import spidev
import time
import RPi.GPIO as GPIO
import datetime
import pytz
import sqlite3
#preparing the GPIO for manuall switch
GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)
#GPIO.setup(22, GPIO.OUT)
#GPIO.setup(24, GPIO.OUT)
#GPIO.setup(25, GPIO.OUT)
#setting PWM
p = GPIO.PWM(18,100)          #GPIO19 as PWM output, with 100Hz frequency
p.start(50)                   #generate PWM signal with default 50% duty cycle

#procedures
def read_tmp1():
#    outside temp;
#    return tmp01;
    tfile = open("/sys/bus/w1/devices/28-0000061542c0/w1_slave")
# Read all of the text in the file. 
    text = tfile.read()
# Close the file now that the text has been read. 
    tfile.close()
# Split the text with new lines (\n) and select the second line. 
    secondline = text.split("\n")[1]
# Split the line into words, referring to the spaces, and select the 10th word (counting from 0). 
    temperaturedata = secondline.split(" ")[9]
# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number. 
    temperature = float(temperaturedata[2:])
# Put the decimal point in the right place and display it. 
    tmp01 = temperature / 1000
    return tmp01;

def read_tmp2():
#    temp on output line;
#    return tmp02;
    tfile = open("/sys/bus/w1/devices/28-0000061572da/w1_slave")
# Read all of the text in the file. 
    text = tfile.read()
# Close the file now that the text has been read. 
    tfile.close()
# Split the text with new lines (\n) and select the second line. 
    secondline = text.split("\n")[1]
# Split the line into words, referring to the spaces, and select the 10th word (counting from 0). 
    temperaturedata = secondline.split(" ")[9]
# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number. 
    temperature = float(temperaturedata[2:])
# Put the decimal point in the right place and display it. 
    tmp02 = temperature / 1000
    return tmp02;
# define target temp for output line based on outside temp compentsation
# to be finished later



def get_tmp3():
    if day_night():
        tmp03n = 55
    else: 
        tmp03n = 40
    if -1 < read_tmp1() < 5:
        tmp03 = tmp03n + 5
    elif -6 < read_tmp1() <-1:
        tmp03 = tmp03n + 10
    elif read_tmp1() < -6:
        tmp03 = tmp03n + 15
    else:
        tmp03 = tmp03n 
    return tmp03

def temp_dif():
	tmpdiff = get_tmp3() - read_tmp2();
	return tmpdiff;


#save temp in SQL database

def log_temperature(tmp02):

    conn=sqlite3.connect('templog.db')
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (tmp02,))

    # commit the changes
    conn.commit()

    conn.close()



# Determine night or day

def day_night(tz='Europe/Prague'):
    tz = pytz.timezone(tz)
    time_now = datetime.datetime.now(tz).time()

    #here we could apply any timezone according shop geo location
    time_day = datetime.time(5, 10, tzinfo=tz)
    time_night = datetime.time(22, 30, tzinfo=tz)

    is_day = False

    if time_now >= time_day and time_now <= time_night:
        is_day = True
#       print ("day")
        return is_day

#Main code
a = 0

while (a is 0): 
    if temp_dif() > 20:   
        print ("switching to full heat") 
        time.sleep(2)
        p.ChangeDutyCycle(100)
    elif temp_dif() > 10:
        print ("switching to 2/3 heat")
        time.sleep(2);
        p.ChangeDutyCycle(80)
    elif temp_dif() > 5:
        print ("switching to 1/3 heat")
        time.sleep(2)
        p.ChangeDutyCycle(50)
    elif temp_dif() > 2:
        print ("switchiong to holding heat 10%")
        time.sleep(2)
        p.ChangeDutyCycle(10) 
    else: 
        print ("switching heat off")
        p.ChangeDutyCycle(0)
    print ("outputline temp is %d" % read_tmp2())
    print ("outside temp is %d" % read_tmp1())
    print ("desired temp is %d" % get_tmp3())
    print ("diff temp is %d" % temp_dif())
    log_temperature(read_tmp2())
    time.sleep(120)
