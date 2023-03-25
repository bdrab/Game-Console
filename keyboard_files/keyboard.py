from machine import Pin, SPI


class Keyboard:
    def __init__(self):
        self.button_up = Pin(17, Pin.IN, Pin.PULL_UP)
        self.button_down = Pin(16, Pin.IN, Pin.PULL_UP)
        self.button_left = Pin(18, Pin.IN, Pin.PULL_UP)
        self.button_right = Pin(19, Pin.IN, Pin.PULL_UP)
        self.button_back = Pin(20, Pin.IN, Pin.PULL_UP)

