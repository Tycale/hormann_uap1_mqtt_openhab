# Hörmann UAP1 MQTT with RaspberryPi

Requirements:
 - RaspberryPi Zero W
 - Hormann UAP1 module
 - 4 Relays

##Reading Outputs

Ground pin (e.g. Board GPIO 34) of the Raspberry Pi should be connected to the UAP1 connectors S0{1,2,3}.5
The Board GPIO number 36 is connected to the UAP1 connector S01.8 (light on)
The Board GPIO number 38 is connected to the UAP1 connector S02.8 (door closed)
The Board GPIO number 40 is connected to the UAP1 connector S03.8 (door open)

Launch alone UAP1States.py to monitor the states of your door during 60 secondes.

