from __future__ import division
import time
import spidev
import RPi.GPIO as GPIO
#preparing the GPIO for manuall switch
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)


#procedures
def read_tmp1():
#    tmp01 = 60;
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
#    tmp02= 50;
#    return tmp02;
    tfile = open("/sys/bus/w1/devices/28-000006156bc6/w1_slave")
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

def read_tmp3():
#    tmp03= 70;
#    return tmp03;
    def bitstring(n):
        s = bin(n)[2:]
        return '0'*(8-len(s)) + s

    def read(adc_channel=0, spi_channel=0):
        conn = spidev.SpiDev(0, spi_channel)
        conn.max_speed_hz = 1200000 # 1.2 MHz
        cmd = 128
        if adc_channel:
            cmd += 32
        reply_bytes = conn.xfer2([cmd, 0])
        reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
        reply = reply_bitstring[5:15]
        return int(reply, 2) / 2**10

    if __name__ == '__main__':
        tmp03 = read() * 100
        return tmp03;

def read_switch():
#    sw23 = 1;
#    return sw23;
    input_state = GPIO.input(23)
    if input_state == False:
            sw23 = 1;
    else:
            sw23 = 0;
            
    return sw23;



# Main code
a = 0

while (a is 0): 
    if read_tmp1() > read_tmp2():  
        print "exchanger warm - go to next check"
        time.sleep(2)
        if read_tmp2() < read_tmp3():
            print "switching water pump"
            GPIO.output(25, GPIO.HIGH)
            time.sleep(2)
            if read_switch() is 1 :
                print "switching shower"
                GPIO.output(24, GPIO.HIGH)
                time.sleep(2)
            else:
                print "shower switch OFF"
                GPIO.output(24, GPIO.LOW)                
        else:
            print "set temp lower than tank - cancel"
            GPIO.output(25, GPIO.LOW)  
            GPIO.output(24, GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)            
    elif read_switch() is 1 :
        print "switch water pump / all valves for shower"
        GPIO.output(25, GPIO.HIGH)  
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(2)
    else:
        print "switch water pump OFF"
        GPIO.output(25, GPIO.LOW)      
    time.sleep(5)
