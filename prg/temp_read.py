






import RPi.GPIO as GPIO
import time

# Use the pin numbers from the ribbon cable board. 
GPIO.setmode(GPIO.BCM)
#PIN Setup
# Set up the pin you are using (24 for Temp Valve 1 and 18 for valve 2) as output. 
GPIO.setup(24, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#procedures
def read_tmp1()
	# Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before. 
	tfile = open("/sys/bus/w1/devices/28-0000061542c0/w1_slave") 
	# Read all of the text in the file. c
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

def read_tmp2()
        # Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before. 
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





# Main Code
read_tmp1()
read_tmp2()
while True:
    input_state = GPIO.input(23)
    if input_state == False:
        print('shower ON')
        time.sleep(0.2)

# Turn on the pin and see the LED light up. 
GPIO.output(24, GPIO.HIGH)
#Turn off the pin to turn off the LED. 
time.sleep(5)
GPIO.output(24, GPIO.LOW)
GPIO.output(18, GPIO.HIGH)
time.sleep(5)

