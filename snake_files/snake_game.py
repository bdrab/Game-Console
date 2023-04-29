from snake_files import snake
from lib import ssd1306
from keyboard_files import keyboard
from lib import buzzer_music
import _thread
import time
from settings import SCREEN_RES_X, SCREEN_RES_Y


class SnakeGame:
    def __init__(self,
                 game_lcd: ssd1306.SSD1306_I2C,
                 game_keyboard: keyboard.Keyboard,
                 game_song: buzzer_music.music):
        self.lcd = game_lcd
        self.play_sound = False
        self.keyboard = game_keyboard
        self.snake = snake.Snake()
        self.song = game_song

    def play_audio(self):
        while self.play_sound:
            self.song.tick()
            time.sleep(0.04)

    def run_snake(self):
        game_is_end = False
        self.play_sound = True
        _thread.start_new_thread(self.play_audio, ())
        self.snake.recreate_snake()
        previous_time_game = time.ticks_ms()
        while not game_is_end:
            time_passed_game = time.ticks_diff(time.ticks_ms(), previous_time_game)
            if time_passed_game >= 500:
                self.lcd.fill(0)
                x, y = self.snake.move_snake()
                if self.snake.food_has_been_eaten():
                    self.snake.add_segment(x, y)

                self.draw_frame()
                self.draw_snake()
                self.draw_food()

                game_is_end = self.snake.check_win()
                self.lcd.show()
                previous_time_game = time.ticks_ms()

            if not self.keyboard.button_up.value():
                self.snake.move_up()
            elif not self.keyboard.button_down.value():
                self.snake.move_down()
            elif not self.keyboard.button_left.value():
                self.snake.move_left()
            elif not self.keyboard.button_right.value():
                self.snake.move_right()
        self.play_sound = False
        self.song.restart()

    def draw_frame(self):
        self.lcd.hline(0, 0, SCREEN_RES_X, 1)
        self.lcd.hline(0, 1, SCREEN_RES_X, 1)
        self.lcd.hline(0, SCREEN_RES_Y - 2, SCREEN_RES_X, 1)
        self.lcd.hline(0, SCREEN_RES_Y-1, SCREEN_RES_X, 1)
        self.lcd.vline(0, 0, SCREEN_RES_Y, 1)
        self.lcd.vline(1, 0, SCREEN_RES_Y, 1)
        self.lcd.vline(SCREEN_RES_X - 1, 0, SCREEN_RES_Y, 1)
        self.lcd.vline(SCREEN_RES_X - 2, 0, SCREEN_RES_Y, 1)

    def draw_snake(self):
        for segment in self.snake.segments:
            self.lcd.fill_rect(segment.x, segment.y, segment.size, segment.size, 1)

    def draw_food(self):
        self.lcd.fill_rect(self.snake.food.x, self.snake.food.y, self.snake.food.size, self.snake.food.size, 1)
