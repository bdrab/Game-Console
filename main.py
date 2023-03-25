import time
from lib import pcd8544_fb
from machine import Pin, SPI
from snake_files import snake_game
from keyboard_files import keyboard
from lib import buzzer_music
from sound_files import sounds
from app_files import app

spi = SPI(0)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(5)
dc = Pin(4)
rst = Pin(8)

led = Pin(13, Pin.OUT)
buzzer = Pin(21)
back_light = Pin(9, Pin.OUT, value=0)

keyboard = keyboard.Keyboard()
lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)
lcd.contrast(0x3f, pcd8544_fb.BIAS_1_48, pcd8544_fb.TEMP_COEFF_0)
snake_sound = buzzer_music.music(sounds.song, pins=[buzzer])
snake_game = snake_game.SnakeGame(game_keyboard=keyboard, game_song=snake_sound, game_lcd=lcd)


def test_menu():
    lcd.fill(1)
    lcd.show()
    time.sleep(5)


def turn_on_led():
    led.value(1)


def turn_off_led():
    led.value(0)


menu_items = [
    ["Snake", snake_game.run_snake],
    ["Test", test_menu],
    ["Settings", [
        ["LED", [
            ["LED ON", turn_on_led],
            ["LED OFF", turn_off_led],
            ]],
    ]],
]

app = app.App(game_lcd=lcd, keyboard=keyboard, menu=menu_items)

app.run()



