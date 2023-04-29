import time

from machine import Pin, I2C
from snake_files import snake_game
from tetris_files import tetris_game
from keyboard_files import keyboard
from lib import buzzer_music
from sound_files import sounds
from app_files import app
from lib.ssd1306 import SSD1306_I2C
from settings import *


i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
lcd = SSD1306_I2C(SCREEN_RES_X, SCREEN_RES_Y, i2c_dev)

led = Pin(13, Pin.OUT)
buzzer = Pin(21)
back_light = Pin(9, Pin.OUT, value=0)

keyboard = keyboard.Keyboard()
snake_sound = buzzer_music.music(sounds.song_snake, pins=[buzzer])
snake_tetris = buzzer_music.music(sounds.song_tetris, pins=[buzzer])
snake_game = snake_game.SnakeGame(game_keyboard=keyboard, game_song=snake_sound, game_lcd=lcd)
tetris_game = tetris_game.TetrisGame(game_keyboard=keyboard, game_song=snake_tetris, game_lcd=lcd)


def turn_on_led():
    led.value(1)


def turn_off_led():
    led.value(0)


def turn_on_sounds():
    pass


def turn_off_sounds():
    pass


menu_items = [
    ["Snake", snake_game.run_snake],
    ["Tetris", tetris_game.run_tetris],
    ["Settings", [
        ["LED", [
            ["LED ON", turn_on_led],
            ["LED OFF", turn_off_led],
            ]],
        ["Sounds", [
            ["Sounds ON", turn_on_sounds],
            ["Sounds OFF", turn_off_sounds],
        ]],
    ]],
]

app = app.App(game_lcd=lcd, keyboard=keyboard, menu=menu_items)

app.run()



