from machine import Pin


class Keyboard:
    def __init__(self):

        # self.button_back = Pin(16, Pin.IN, Pin.PULL_UP)
        #
        # self.button_up = Pin(17, Pin.IN, Pin.PULL_UP)
        # self.button_not_used1 = Pin(18, Pin.IN, Pin.PULL_UP)
        # self.button_left = Pin(19, Pin.IN, Pin.PULL_UP)
        # self.button_not_used2 = Pin(20, Pin.IN, Pin.PULL_UP)
        # self.button_right = Pin(22, Pin.IN, Pin.PULL_UP)
        #    #10 self.button_not_used3 = Pin(26, Pin.IN, Pin.PULL_UP)
        #     #9 self.button_down = Pin(27, Pin.IN, Pin.PULL_UP)
        # self.button_not_used4 = Pin(28, Pin.IN, Pin.PULL_UP)
        #
        #
        # self.button_arrow_back = Pin(2, Pin.IN, Pin.PULL_UP)
        # self.button_arrow_left = Pin(1, Pin.IN, Pin.PULL_UP)
        # self.button_arrow_right = Pin(0, Pin.IN, Pin.PULL_UP)

        self.button_left = Pin(16, Pin.IN, Pin.PULL_UP)
        self.button_up = Pin(17, Pin.IN, Pin.PULL_UP)
        self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
        self.button_right = Pin(19, Pin.IN, Pin.PULL_UP)

        self.button_functional_left = Pin(20, Pin.IN, Pin.PULL_UP)
        self.button_functional_right = Pin(22, Pin.IN, Pin.PULL_UP)

        self.button_arrow_back = Pin(2, Pin.IN, Pin.PULL_UP)
        self.button_arrow_left = Pin(1, Pin.IN, Pin.PULL_UP)
        self.button_arrow_right = Pin(0, Pin.IN, Pin.PULL_UP)
