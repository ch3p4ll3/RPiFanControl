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
pi.set_PWM_dutycycle(GPIO, 0)

out_min = 77  # min speed -> 77 = 30%
out_max = 255  # max speed -> 255 = 100%
in_min = 25  # temperature min
in_max = 65  # temperature max

while True:
    try:
        tempC = psutil.sensors_temperatures()['cpu-thermal'][0][1]
        calc = (tempC - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        if calc > 255:
            calc = 255

        elif calc < 77:
            calc = 77

        print(calc, " - ", tempC)

        pi.set_PWM_dutycycle(GPIO, calc)

        time.sleep(.5)

    except KeyboardInterrupt:
        pi.stop()
