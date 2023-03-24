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

button_up = Pin(17, Pin.IN, Pin.PULL_UP)
button_down = Pin(16, Pin.IN, Pin.PULL_UP)
button_left = Pin(18, Pin.IN, Pin.PULL_UP)
button_right = Pin(19, Pin.IN, Pin.PULL_UP)
led = Pin(13, Pin.OUT)


snake = snake.Snake()


def draw_board():
    lcd.hline(0, 0, 84, 1)
    lcd.hline(0, 1, 84, 1)
    lcd.hline(0, 46, 84, 1)
    lcd.hline(0, 47, 84, 1)
    lcd.vline(0, 0, 48, 1)
    lcd.vline(1, 0, 48, 1)
    lcd.vline(83, 0, 48, 1)
    lcd.vline(82, 0, 48, 1)


def draw_snake():
    for segment in snake.segments:
        lcd.fill_rect(segment.x, segment.y, segment.size, segment.size, 1)


def draw_food():
    lcd.fill_rect(snake.food.x, snake.food.y, snake.food.size, snake.food.size, 1)


def check_win():
    end_game = False

    if snake.head.x < 2 or snake.head.x > 78 or snake.head.y < 2 or snake.head.y > 42:
        end_game = True

    for snake_segment in snake.segments[1:]:
        if snake_segment.x == snake.head.x and snake_segment.y == snake.head.y:
            end_game = True

    return end_game


def food_has_been_eaten():
    if snake.head.x == snake.food.x and snake.head.y == snake.food.y:
        generate_snake_food()
        return True


def generate_snake_food():
    random_x = random.randrange(2, 82, 4)
    random_y = random.randrange(2, 42, 4)

    snake.food.x = random_x
    snake.food.y = random_y


game_is_end = False
previous_time = time.ticks_ms()
while not game_is_end:
    time_passed = time.ticks_diff(time.ticks_ms(), previous_time)
    if time_passed >= 500:
        lcd.fill(0)
        lcd.show()

        x, y = snake.move_snake()
        if food_has_been_eaten():
            snake.add_segment(x, y)

        draw_board()
        draw_snake()
        draw_food()

        game_is_end = check_win()
        lcd.show()
        previous_time = time.ticks_ms()

    if not button_up.value():
        snake.move_up()
    elif not button_down.value():
        snake.move_down()
    elif not button_left.value():
        snake.move_left()
    elif not button_right.value():
        snake.move_right()
