import random
from tetris_files.tetris_settings import *

tetrominoes = [
    [
        [["", "x", "", ""],
         ["", "x", "", ""],
         ["", "x", "", ""],
         ["", "x", "", ""]],

        [["", "", "", ""],
         ["x", "x", "x", "x"],
         ["", "", "", ""],
         ["", "", "", ""]],

        [["", "", "x", ""],
         ["", "", "x", ""],
         ["", "", "x", ""],
         ["", "", "x", ""]],


        [["", "", "", ""],
         ["", "", "", ""],
         ["x", "x", "x", "x"],
         ["", "", "", ""]],
    ],

    [
        [["x", "", ""],
         ["x", "x", "x"],
         ["", "", ""]],

        [["", "x", "x"],
         ["", "x", ""],
         ["", "x", ""]],

        [["", "", ""],
         ["x", "x", "x"],
         ["", "", "x"]],

        [["", "x", ""],
         ["", "x", ""],
         ["x", "x", ""]],
    ],

    [
        [["", "", "x"],
         ["x", "x", "x"],
         ["", "", ""]],

        [["", "x", ""],
         ["", "x", ""],
         ["", "x", "x"]],

        [["", "", ""],
         ["x", "x", "x"],
         ["x", "", ""]],

        [["x", "x", ""],
         ["", "x", ""],
         ["", "x", ""]],
    ],

    [
        [["", "x", "x", ""],
         ["", "x", "x", ""],
         ["", "", "", ""]],

        [["", "x", "x", ""],
         ["", "x", "x", ""],
         ["", "", "", ""]],

        [["", "x", "x", ""],
         ["", "x", "x", ""],
         ["", "", "", ""]],

        [["", "x", "x", ""],
         ["", "x", "x", ""],
         ["", "", "", ""]],
    ],

    [
        [["", "x", "x"],
         ["x", "x", ""],
         ["", "", ""]],

        [["", "x", ""],
         ["", "x", "x"],
         ["", "", "x"]],

        [["", "", ""],
         ["", "x", "x"],
         ["x", "x", ""]],

        [["x", "", ""],
         ["x", "x", ""],
         ["", "x", ""]],
    ],

    [
        [["", "x", ""],
         ["x", "x", "x"],
         ["", "", ""]],

        [["", "x", ""],
         ["", "x", "x"],
         ["", "x", ""]],

        [["", "", ""],
         ["x", "x", "x"],
         ["", "x", ""]],

        [["", "x", ""],
         ["x", "x", ""],
         ["", "x", ""]],
    ],

    [
        [["x", "x", ""],
         ["", "x", "x"],
         ["", "", ""]],

        [["", "", "x"],
         ["", "x", "x"],
         ["", "x", ""]],

        [["", "", ""],
         ["x", "x", ""],
         ["", "x", "x"]],

        [["", "x", ""],
         ["x", "x", ""],
         ["x", "", ""]],
    ],
]


class Segment:
    def __init__(self, x, y):
        self.size = 4
        self.x = x
        self.y = y


class Tetromino:

    def __init__(self):
        self.tetromino_random = random.choice(list(range(0, 7)))
        self.rotation = random.choice(list(range(0, 4)))
        self.tetromino_type = None
        self.tetromino_segments = []
        self.offset_x = 14
        self.offset_y = 2
        self.create_segments()

    def create_segments(self):
        self.tetromino_segments = []
        self.tetromino_type = tetrominoes[self.tetromino_random][self.rotation]
        for row_index, row in enumerate(self.tetromino_type):
            for column_index, element in enumerate(row):
                if element == "x":
                    self.tetromino_segments.append(Segment(column_index * 4 + self.offset_x, row_index * 4 + self.offset_y))

    def rotate(self, direction):
        if direction == "left":
            self.rotation = self.rotation - 1
            if self.rotation == -1:
                self.rotation = 3
            self.create_segments()

        elif direction == "right":
            self.rotation = self.rotation + 1
            if self.rotation == 4:
                self.rotation = 0

            self.create_segments()
        return False

    def tetromino_fall(self):
        for element in self.tetromino_segments:
            element.y = element.y + 4
        self.offset_y = self.offset_y + 4

    def tetromino_move(self, elements, direction):

        # check if tetromino element collide with tetris segments on the board
        for tetris_board_element in elements:
            for element in self.tetromino_segments:
                if direction == "left":
                    if (element.x - 4) == tetris_board_element.x and element.y == tetris_board_element.y:
                        return False

                elif direction == "right":
                    if (element.x + 4) == tetris_board_element.x and element.y == tetris_board_element.y:
                        return False

        # check if tetromino element collide with walls
        for element in self.tetromino_segments:
            if direction == "left":
                if (element.x - 4) < 2:
                    return False

            elif direction == "right":
                if (element.x + 4) > BOARD_X + BORDERS - 4:
                    return False

        if direction == "left":
            for element in self.tetromino_segments:
                element.x = element.x - 4
            self.offset_x = self.offset_x - 4

        elif direction == "right":
            for element in self.tetromino_segments:
                element.x = element.x + 4
            self.offset_x = self.offset_x + 4

        return False


class Tetris:
    def __init__(self):
        self.tetris_segments = []
        self.tetromino = Tetromino()

    def recreate_tetris(self):
        self.__init__()

    def generate_new_element(self):
        collision_detected_end_game = False

        self.tetromino = Tetromino()

        for tetris_segment in self.tetris_segments:
            for segment in self.tetromino.tetromino_segments:
                if segment.x == tetris_segment.x and segment.y == tetris_segment.y:
                    collision_detected_end_game = True

        return collision_detected_end_game

    def check_collision(self):
        collision_detected_new_tetromino = False
        collision_detected_end_game = False

        for element in self.tetromino.tetromino_segments:
            if element.y >= BOARD_Y - BORDERS:
                collision_detected_new_tetromino = True
                for segment in self.tetromino.tetromino_segments:
                    self.tetris_segments.append(segment)

                self.tetris_segments = sorted(self.tetris_segments, key=lambda item: item.y)
                break
            for tetris_segment in self.tetris_segments:
                if element.y + 4 == tetris_segment.y and element.x == tetris_segment.x:
                    collision_detected_new_tetromino = True
                    for segment in self.tetromino.tetromino_segments:
                        self.tetris_segments.append(segment)

                    self.tetris_segments = sorted(self.tetris_segments, key=lambda item: item.y)
                    break

        return collision_detected_end_game, collision_detected_new_tetromino

    def check_and_delete_filled_line(self):

        last_tetromino_ys = sorted(list(set([segment.y for segment in self.tetromino.tetromino_segments])), reverse=True)
        tetris_segments_coordinates = [(segment.x, segment.y) for segment in self.tetris_segments]

        for y in last_tetromino_ys.copy():
            for x in range(2, BOARD_X + BORDERS - 4, 4):
                if (x, y) not in tetris_segments_coordinates:
                    last_tetromino_ys.remove(y)
                    break

        for segment in self.tetris_segments.copy():
            for y in last_tetromino_ys:
                if segment.y == y:
                    self.tetris_segments.remove(segment)

        for last_tetromino_y in last_tetromino_ys:
            for index, segment in enumerate(self.tetris_segments):
                if segment.y < last_tetromino_y:
                    self.tetris_segments[index].y = self.tetris_segments[index].y + 4
