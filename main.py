#   RST - Reset:                     Pico GP8 (11)     
#   CE - Chip Enable / Chip select : Pico GP5 ( 7)     
#   DC - Data/Command :              Pico GP4 ( 6)     
#   Din - Serial Input (Mosi):       Pico GP7 (10)
#   Clk - SPI Clock:                 Pico GP6 ( 9)
#   Vcc:                             Pico 3V3 (36)
#   BL :                             Pico GP9(12)
#   Gnd:                             Pico GND (38)

import random
from lib import pcd8544_fb
from machine import Pin, SPI, Timer
import time
from snake_files import snake


spi = SPI(0)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(5)
dc = Pin(4)
rst = Pin(8)


back_light = Pin(9, Pin.OUT, value=0)
lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)
lcd.contrast(0x3f, pcd8544_fb.BIAS_1_48, pcd8544_fb.TEMP_COEFF_0)

button = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin(13, Pin.OUT)


snake = snake.Snake()
headings = ["UP", "DOWN", "RIGHT", "LEFT"]


def draw_board():
    lcd.hline(0, 0, 84, 1)
    lcd.hline(0, 47, 84, 1)
    lcd.vline(0, 0, 48, 1)
    lcd.vline(83, 0, 48, 1)


def draw_snake():
    for segment in snake.segments:
        lcd.fill_rect(segment.x, segment.y, segment.size, segment.size, 1)


def check_win():
    pass


previous_time = time.ticks_ms()
while True:
    time_passed = time.ticks_diff(time.ticks_ms(), previous_time)
    if time_passed >= 1000:
        lcd.fill(0)
        lcd.show()
        snake.move_snake()
        draw_snake()
        draw_board()
        check_win()
        lcd.show()
        previous_time = time.ticks_ms()

    if not button.value():
        snake.heading = random.choice(headings)
