#!/usr/bin/python3

import pigpio
import time
import psutil


GPIO = 13  # GPIO pin (BCM) of the transistor that controls the fan

pi = pigpio.pi()

if not pi.connected:
    exit(0)

pi.set_mode(GPIO, pigpio.OUTPUT)
pi.set_PWM_frequency(GPIO, 20000)  # Set frequency at 20KHz
pi.set_PWM_range(GPIO, 100)   # Now  25 = 1/4,   50 = 1/2,   75 = 3/4 on
pi.set_PWM_dutycycle(GPIO, 0)

out_min = 30  # min speed
out_max = 100  # max speed
in_min = 25  # temperature min
in_max = 65  # temperature max

while True:
    try:
        tempC = psutil.sensors_temperatures()['cpu-thermal'][0][1]
        calc = (tempC - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        if calc > out_max:
            calc = out_max

        elif calc < out_min:
            calc = out_min

        pi.set_PWM_dutycycle(GPIO, calc)

        time.sleep(.5)

    except KeyboardInterrupt:
        pi.set_PWM_dutycycle(GPIO, 0)
        pi.stop()
