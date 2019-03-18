import threading
import time

import RPi.GPIO as GPIO #WirePI

GPIO.setwarnings(False)

# See https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
GPIO_MODE = GPIO.BOARD # GPIO.BCM

class UAP1Actions:
    def __init__(self, GPIO_light, GPIO_close, GPIO_open, GPIO_slightly_o):
        """ Trigger actions by relays connected between the Hormann door and GPIOs of the Raspberry Pi.

        The GPIO_light is the GPIO number of the board connected to a relay connected to UAP1 connector S5
        The GPIO_close is the GPIO number of the board connected to a relay connected to UAP1 connector S4
        The GPIO_open is the GPIO number of the board connected to a relay connected to UAP1 connector S2
        The GPIO_slightly_o is the GPIO number of the board connected to a relay connected to UAP1 connector S3

        Note: UAP1 connectors "0V" should be connected to the previous relays.
        """
        self.GPIO_light = GPIO_light
        self.GPIO_close = GPIO_close
        self.GPIO_open = GPIO_open
        self.GPIO_slight = GPIO_slightly_o

        #GPIO Pin Setup
        GPIO.setmode(GPIO_MODE)

        all_gpios = [GPIO_light, GPIO_close, GPIO_open, GPIO_slightly_o]
        GPIO.setup(all_gpios, GPIO.OUT, initial=GPIO.HIGH)

    def trigger(self, pin):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.HIGH)

    def slightly_open(self):
        self.trigger(self.GPIO_slight)

    def open(self):
        self.trigger(self.GPIO_open)

    def close(self):
        self.trigger(self.GPIO_close)

    def light(self):
        self.trigger(self.GPIO_light)

# Tests
if __name__ == '__main__':

    a = UAP1Actions(29, 31, 33, 35)
    a.light()
    time.sleep(5)
    a.slightly_open()
    time.sleep(20)
    a.close()
    time.sleep(5)
    a.light()
    
