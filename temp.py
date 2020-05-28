#!/usr/bin/python

import RPi.GPIO as gpio
import time
import psutil

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
pin = 13
gpio.setup(pin, gpio.OUT)
fan = gpio.PWM(pin, 50)
fan.start(0)

out_min = 0    # min speed
in_min = 25    # temperature min
out_max = 100  # max speed
in_max = 65    # temperature max

while True:
	tempC = psutil.sensors_temperatures()['cpu-thermal'][0][1]
	calc = (tempC - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	if calc > 100:
		calc = 100
	fan.ChangeDutyCycle(calc)
	time.sleep(0.5)
