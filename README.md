# pwmPiFanControl
With this simple script you can control the speed of a fan according to the cpu temperature of your Raspberry. By default I use pin 13 (BCM), the fan will start to turn on when the Raspberry is at 25 ° C to reach the maximum speed when the temperature rises to 65 ° C. The fan I used is that of an old 12V fixed PC, follow the circuit below for the connections

## Wirings

![wirings](https://i.stack.imgur.com/rSeVt.png)

## How to install
**Note:** To use the program you must have installed and started the pigpio daemon. To install it type `sudo apt install pigpiod` while to start it type `sudo systemctl start pigpiod` and finally `sudo systemctl enable pigpiod` to start it automatically at boot.
Place the `temp.py` script on your raspberry desktop, move the `fan.service` file to `/etc/systemd/system/` and give the command `sudo systemctl daemon-reload`. 
To start the newly installed service, type: `sudo systemctl start fan`, to stop it instead type `sudo systemctl stop fan`. 
You can also start it automatically at boot by typing `sudo systemctl enable fan`, You can also start it automatically at boot by typing or `sudo systemctl disable fan` to disable it.