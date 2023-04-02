from tetris_files import tetris
from lib import pcd8544_fb
from keyboard_files import keyboard
from lib import buzzer_music
import _thread
import time


class TetrisGame:
    def __init__(self,
                 game_lcd: pcd8544_fb.PCD8544_FB,
                 game_keyboard: keyboard.Keyboard,
                 game_song: buzzer_music.music):

        self.tetris = tetris.Tetris()
        self.lcd = game_lcd
        self.keyboard = game_keyboard

        self.move_direction = False
        self.rotate = False

        self.play_sound = False
        self.song = game_song

    def play_audio(self):
        while self.play_sound:
            # # disabled only for testing purposes
            # self.song.tick()
            time.sleep(0.04)

    def run_tetris(self):
        game_is_end = False
        self.play_sound = True
        _thread.start_new_thread(self.play_audio, ())
        self.tetris.recreate_tetris()

        previous_time_game = time.ticks_ms()
        previous_time_key = time.ticks_ms()
        previous_time_move = time.ticks_ms()

        while not game_is_end:
            time_passed_game = time.ticks_diff(time.ticks_ms(), previous_time_game)
            if time_passed_game >= 600:
                self.lcd.fill(0)
                self.tetris.tetromino.tetromino_fall()
                self.draw_frame()
                self.draw_tetris_board()
                self.draw_tetromino()

                game_is_end, new_element = self.tetris.check_collision()

                if new_element:
                    self.tetris.check_and_delete_filled_line()
                    self.tetris.generate_new_element()

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
                game_is_end, new_element = self.tetris.check_collision()
                if new_element:
                    self.tetris.check_and_delete_filled_line()
                    self.tetris.generate_new_element()
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

                elif not self.keyboard.button_back.value():
                    game_is_end = True
                    time.sleep_ms(200)
                previous_time_key = time.ticks_ms()

        self.play_sound = False
        self.song.restart()

    def draw_frame(self):
        self.lcd.hline(0, 0, 84, 1)
        self.lcd.hline(0, 1, 84, 1)
        self.lcd.hline(0, 46, 84, 1)
        self.lcd.hline(0, 47, 84, 1)
        self.lcd.vline(0, 0, 48, 1)
        self.lcd.vline(1, 0, 48, 1)
        self.lcd.vline(83, 0, 48, 1)
        self.lcd.vline(82, 0, 48, 1)

    def draw_tetris_board(self):
        for element in self.tetris.tetris_segments:
            self.lcd.fill_rect(element.x, element.y, 4, 4, 1)

    def draw_tetromino(self):
        for element in self.tetris.tetromino.tetromino_segments:
            self.lcd.fill_rect(element.x, element.y, 4, 4, 1)
