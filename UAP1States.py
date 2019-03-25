import threading
import time

import RPi.GPIO as GPIO #WirePI

GPIO.setwarnings(False)

# See https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
GPIO_MODE = GPIO.BOARD # GPIO.BCM

DOOR_MAX_MOVING_TIME = 30

STATE_UNKNOWN, STATE_CLOSED, STATE_OPEN, STATE_SLIGHTLY_OPEN, STATE_MOVING = range(5)
DOOR_STATE_TO_STR = { STATE_UNKNOWN: 'Unknown',
              STATE_CLOSED: 'Closed',
              STATE_OPEN: 'Open',
              STATE_SLIGHTLY_OPEN: 'Slightly',
              STATE_MOVING: 'Moving'}
OFF = False
ON = True
LIGHT_STATE_TO_STR = { ON: 'ON', OFF: 'OFF', None: 'Unknown' }

class UAP1States:
    def __init__(self, GPIO_light, GPIO_down, GPIO_up):
        """ Get the state of the door by checking the GPIOs of the Raspberry Pi connected to the Hormann UAP1.

        The GPIO_light is the GPIO number of the board connected to the UAP1 connector S03.8
        The GPIO_down is the GPIO number of the board connected to the UAP1 connector S02.8
        The GPIO_up is the GPIO number of the board connected to the UAP1 connector S01.8

        Note: Ground pin should be connected to the UAP1 connectors S0{1,2,3}.5
        """
        self.door_state = STATE_UNKNOWN
        self.light_state = None
        self.last_door_move = None
        self.execute = True
        self.GPIO_light = GPIO_light
        self.GPIO_down = GPIO_down
        self.GPIO_up = GPIO_up

        #GPIO Pin Setup
        GPIO.setmode(GPIO_MODE)
        GPIO.setup(GPIO_light, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIO_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GPIO_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)


        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while self.execute:
            light = GPIO.input(self.GPIO_light) == 0
            down = GPIO.input(self.GPIO_down) == 0
            up = GPIO.input(self.GPIO_up) == 0

            self.light_state = light

            if not down and not up and self.door_state != STATE_SLIGHTLY_OPEN :
                if self.door_state == STATE_MOVING:
                    if time.time() - self.last_door_move > DOOR_MAX_MOVING_TIME :
                        self.door_state = STATE_SLIGHTLY_OPEN
                else:
                    self.last_door_move = time.time()
                    self.door_state = STATE_MOVING

            if down:
                self.door_state = STATE_CLOSED

            if up:
                self.door_state = STATE_OPEN

            # Check every 0.2s after new states
            time.sleep(0.2) 

    def get_door(self):
        return self.door_state

    def get_light(self):
        return self.light_state

    def get_str_light(self):
        return LIGHT_STATE_TO_STR[self.light_state]

    def get_str_door(self):
        return DOOR_STATE_TO_STR[self.door_state]

    def get_str_states(self):
        return (self.get_str_light(), self.get_str_door())

    def finish(self):
        self.execute = False
        self.thread.join()
        GPIO.cleanup()


# Tests
if __name__ == '__main__':

    a = UAP1States(36, 38, 40)
    sec = time.time()
    
    # Monitor the states during 60 secondes
    while time.time() - sec < 60 :
        print(a.get_str_states())
        time.sleep(1)
    
    a.finish()

