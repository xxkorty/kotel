import RPi.GPIO as GPIO 
import time
# Use the pin numbers from the ribbon cable board. 
GPIO.setmode(GPIO.BCM) 
# Set up the pin you are using ("18" is an example) as output. 
GPIO.setup(18, GPIO.OUT) 
GPIO.setup(22, GPIO.OUT) 
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)



a = 0

while (a is 0): 
	GPIO.output(24, GPIO.HIGH) 
	print "green ON" 
	time.sleep(1)
	GPIO.output(24, GPIO.LOW)
	GPIO.output(18, GPIO.HIGH)
	print "Yellow ON"
	time.sleep(1) 
	GPIO.output(18, GPIO.LOW)
	GPIO.output(22, GPIO.HIGH)
	print "White ON"
	time.sleep(1)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(25, GPIO.HIGH)
	print "Red ON"
	time.sleep(1)
	GPIO.output(25, GPIO.LOW)
	print "All OFF"
	time.sleep(1)

