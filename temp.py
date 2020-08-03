#!/usr/bin/python3

import pigpio
import time
import psutil
import signal
import subprocess
from shutil import which

run = True


def handler_stop_signals(signum, frame) -> None:
    global run
    run = False


def main() -> None:
    global run
    gpio = 13  # gpio pin (BCM) of the transistor that controls the fan

    pi = pigpio.pi()

    if not pi.connected:
        exit(0)

    pi.set_mode(gpio, pigpio.OUTPUT)  # Set gpio pin as OUTPUT
    pi.set_PWM_frequency(gpio, 20000)  # Set frequency at 20KHz
    pi.set_PWM_range(gpio, 100)  # Now  25 = 1/4,   50 = 1/2,   75 = 3/4 on
    pi.set_PWM_dutycycle(gpio, 0)  # Set PWM Duty Cycle to 0

    out_min = 30  # min speed
    out_max = 100  # max speed
    in_min = 25  # temperature min
    in_max = 65  # temperature max

    while run:
        try:
            tempC = psutil.sensors_temperatures()['cpu_thermal'][0].current
            calc = (tempC - in_min) * (out_max - out_min) / \
                   (in_max - in_min) + out_min

            if calc > out_max:
                calc = out_max

            elif calc < out_min:
                calc = out_min

            pi.set_PWM_dutycycle(gpio, calc)

            time.sleep(.5)

        except KeyboardInterrupt:
            pi.set_PWM_dutycycle(gpio, 0)
            pi.stop()

    pi.set_PWM_dutycycle(gpio, 0)
    pi.stop()


if __name__ == '__main__':
    if which("pigpiod") is None:
        print("The daemon is not installed, type "
              "'sudo apt install pigpiod' to install it")
        exit(0)
    elif "pigpiod" not in (p.name() for p in psutil.process_iter()):
        subprocess.Popen(f"sudo {which('pigpiod')} -s 2").wait(1)
    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)
    main()
