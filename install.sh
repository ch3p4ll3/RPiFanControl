if ! [ -x "$(command -v pigpiod)" ]; then
  echo 'pigpiod was not found in the system.'
  sudo apt install pigpiod
fi

echo 'Copying the python file to the desktop'
cp temp.py ~/Desktop/
echo 'Copying the systemd file to /etc/systemd/system'
sudo cp fan.service /etc/systemd/system/
echo 'Reloading the systemd services'
sudo systemctl daemon-reload
echo 'Starting and enabling the script'
sudo systemctl enable fan.service
sudo systemctl start fan.service