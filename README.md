# Hörmann UAP1 MQTT with RaspberryPi

Requirements:
 - RaspberryPi Zero W
 - Hormann UAP1 module
 - 4 Relays

Dependencies:
```
sudo apt-get install python-pip
sudo python -m pip install --upgrade pip setuptools wheel
sudo pip install paho-mqtt
git clone git://git.drogon.net/wiringPi
cd wiringPi && cat INSTALL
```

## Reading Outputs

 - Ground pin (e.g. Board GPIO 34) of the Raspberry Pi should be connected to the UAP1 connectors S0{1,2,3}.5
 - The Board GPIO number 36 is connected to the UAP1 connector S01.8 (light on)
 - The Board GPIO number 38 is connected to the UAP1 connector S02.8 (door closed)
 - The Board GPIO number 40 is connected to the UAP1 connector S03.8 (door open)

Launch alone UAP1States.py to monitor the states of your door during 60 secondes.

## Actions

 - Raspberry Pi GPIO 29 to a relay connecting ground (0V) and S5 of the UAP1 together
 - Raspberry Pi GPIO 31 to a relay connecting ground (0V) and S4 of the UAP1 together
 - Raspberry Pi GPIO 33 to a relay connecting ground (0V) and S2 of the UAP1 together
 - Raspberry Pi GPIO 35 to a relay connecting ground (0V) and S3 of the UAP1 together

Launch alone UAP1Actions.py to switch on the light, then slightly open the door.

## Openhab icons

Copy folder "icons/classic" into "/etc/openhab2/icons/classic"
