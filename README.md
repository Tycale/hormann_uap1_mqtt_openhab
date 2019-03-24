# Hörmann UAP1 MQTT with RaspberryPi

This project works for any garage door compatible with the UAP1 module from Hörmann.

Requirements:
 - RaspberryPi (I am using a "Rpi Zero W")
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

## MQTT Controller

UAP1MQTT.py takes care of communicate the state of the door and of the
light of the motor via resp. MQTT topics:

 - `state/${MQTT_CLIENTID}/door`
 - `state/${MQTT_CLIENTID}/light`

Plus, it executes commands received on:

 - `command/${MQTT_CLIENTID}/door` allows messages: CLOSE, OPEN, SLIGHT
 - `command/${MQTT_CLIENTID}/light` allows messages : ON, OFF

Following parameters can be set via global environment variables :

 - `${MQTT_SERVER}` for the server URI (e.g. "mqtt://10.8.0.42:1883")
 - `${MQTT_USERNAME}` for authenticate on the MQTT\_SEVER, can be null
 - `${MQTT_PASSWORD}` for authenticate on the MQTT\_SEVER, can be null
 - `${MQTT_CLIENT_ID}` identifies the MQTT client and the door (part of the
topic)

UAP1MQTT.py is the main file to launch.

## SystemD integration

Modify the sample file with good path and global env. variables :
```
cp uap1.service.sample uap1.service
```

Copy the service to the systemd folder and activate it:
```
cp uap1.service /etc/systemd/system/
systemctl enable uap1
systemctl start uap1
systemctl status uap1
```

This piece of software will be launch at the boot time now.

## Openhab integration

Copy/modify files under the folder "openhab" inside your openhab installation. You will need the MQTT Openhab MQTT 1.x module and the translation module.

### Openhab icons

Copy folder "icons/classic" into "/etc/openhab2/icons/classic"
 
