from tetris_files import tetris
from lib import ssd1306
from keyboard_files import keyboard
from lib import buzzer_music
import _thread
import time
from tetris_files.tetris_settings import *


class TetrisGame:
    def __init__(self,
                 game_lcd: ssd1306.SSD1306_I2C,
                 game_keyboard: keyboard.Keyboard,
                 game_song: buzzer_music.music):

        self.tetris = tetris.Tetris()
        self.lcd = game_lcd
        self.keyboard = game_keyboard

        self.move_direction = False
        self.rotate = False

        self.game_is_end = True
        self.tetris_is_end = False
        self.play_sound = True

        self.song = game_song

    def play_audio(self):
        while self.play_sound:
            # # disabled only for testing purposes
            # self.song.tick()
            time.sleep(0.04)

    def run_tetris(self):
        _thread.start_new_thread(self.play_audio, ())

        previous_time_game = time.ticks_ms()
        previous_time_key = time.ticks_ms()
        previous_time_move = time.ticks_ms()

        while not self.tetris_is_end:
            self.draw_menu()
            while not self.game_is_end:
                time_passed_game = time.ticks_diff(time.ticks_ms(), previous_time_game)
                if time_passed_game >= 600:
                    self.lcd.fill(0)
                    self.tetris.tetromino.tetromino_fall()
                    self.draw_frame()
                    self.draw_tetris_board()
                    self.draw_tetromino()

                    self.game_is_end, new_element = self.tetris.check_collision()

                    if new_element:
                        self.tetris.check_and_delete_filled_line()
                        self.game_is_end = self.tetris.generate_new_element()

                    self.lcd.show()
                    previous_time_game = time.ticks_ms()

                time_passed_move = time.ticks_diff(time.ticks_ms(), previous_time_move)
                if time_passed_move >= 300:
                    self.lcd.fill(0)

                    if self.move_direction:
                        self.move_direction = self.tetris.tetromino.tetromino_move(self.tetris.tetris_segments,
                                                                                   direction=self.move_direction)

                    if self.rotate:
                        self.rotate = self.tetris.tetromino.rotate(self.rotate)

                    self.draw_frame()
                    self.draw_tetris_board()
                    self.draw_tetromino()
                    self.game_is_end, new_element = self.tetris.check_collision()
                    if new_element:
                        self.tetris.check_and_delete_filled_line()
                        self.game_is_end = self.tetris.generate_new_element()
                    self.lcd.show()
                    previous_time_move = time.ticks_ms()

                time_passed_key = time.ticks_diff(time.ticks_ms(), previous_time_key)
                if time_passed_key >= 50:
                    if not self.keyboard.button_left.value():
                        self.move_direction = "left"

                    elif not self.keyboard.button_right.value():
                        self.move_direction = "right"

                    elif not self.keyboard.button_up.value():
                        self.rotate = "left"

                    elif not self.keyboard.button_down.value():
                        self.rotate = "right"

                    elif not self.keyboard.button_arrow_left.value():
                        self.game_is_end = True
                        time.sleep_ms(200)
                    previous_time_key = time.ticks_ms()

            if not self.keyboard.button_up.value():
                self.game_is_end = False
                self.tetris.recreate_tetris()

            elif not self.keyboard.button_arrow_left.value():
                self.tetris_is_end = True
                time.sleep_ms(200)

        self.play_sound = False
        self.song.restart()

    def draw_frame(self):
        self.lcd.hline(2, 0, BOARD_X, 1)
        self.lcd.hline(2, 1, BOARD_X, 1)
        self.lcd.hline(2, SCREEN_RES_Y - 2, BOARD_X, 1)
        self.lcd.hline(2, SCREEN_RES_Y - 1, BOARD_X, 1)

        self.lcd.vline(0, 0, SCREEN_RES_Y, 1)
        self.lcd.vline(1, 0, SCREEN_RES_Y, 1)
        self.lcd.vline(BOARD_X + BORDERS, 0, SCREEN_RES_Y, 1)
        self.lcd.vline(BOARD_X + BORDERS + 1, 0, SCREEN_RES_Y, 1)

    def draw_menu(self):
        self.lcd.fill(0)
        self.draw_frame()
        self.lcd.text("press UP", 45, 10)
        self.lcd.text("to start", 45, 20)
        self.lcd.show()

    def draw_tetris_board(self):
        for element in self.tetris.tetris_segments:
            self.lcd.fill_rect(element.x, element.y, 4, 4, 1)

    def draw_tetromino(self):
        for element in self.tetris.tetromino.tetromino_segments:
            self.lcd.fill_rect(element.x, element.y, 4, 4, 1)
