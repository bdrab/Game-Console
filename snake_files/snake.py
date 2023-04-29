from snake_files import segment
import random
from settings import *

START_POSITION = (30, 30)
START_POSITION_2 = (26, 30)


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.heading = "RIGHT"
        self.food = segment.Segment((14, 14))

    def create_snake(self):
        self.add_segment(*START_POSITION)
        self.add_segment(*START_POSITION_2)

    def recreate_snake(self):
        self.__init__()

    def add_segment(self, x, y):
        self.segments.append(segment.Segment((x, y)))

    def move_snake(self):
        x, y = self.segments[-1].x, self.segments[-1].y

        for index in range(len(self.segments) - 1, 0, -1):
            self.segments[index].x = self.segments[index - 1].x
            self.segments[index].y = self.segments[index - 1].y

        if self.heading == "UP":
            self.segments[0].x = self.segments[0].x
            self.segments[0].y = self.segments[0].y - 4
        elif self.heading == "DOWN":
            self.segments[0].x = self.segments[0].x
            self.segments[0].y = self.segments[0].y + 4
        elif self.heading == "RIGHT":
            self.segments[0].x = self.segments[0].x + 4
            self.segments[0].y = self.segments[0].y
        elif self.heading == "LEFT":
            self.segments[0].x = self.segments[0].x - 4
            self.segments[0].y = self.segments[0].y

        return x, y

    def move_up(self):
        if self.heading != "DOWN":
            self.heading = "UP"

    def move_down(self):
        if self.heading != "UP":
            self.heading = "DOWN"

    def move_right(self):
        if self.heading != "LEFT":
            self.heading = "RIGHT"

    def move_left(self):
        if self.heading != "RIGHT":
            self.heading = "LEFT"

    def check_win(self):
        end_game = False

        if self.head.x < 2 or self.head.x > SCREEN_RES_X - 6 or self.head.y < 2 or self.head.y > SCREEN_RES_Y - 6:
            end_game = True

        for snake_segment in self.segments[1:]:
            if snake_segment.x == self.head.x and snake_segment.y == self.head.y:
                end_game = True

        return end_game

    def food_has_been_eaten(self):
        if self.head.x == self.food.x and self.head.y == self.food.y:
            self.generate_snake_food()
            return True

    def generate_snake_food(self):
        random_x = random.randrange(2, SCREEN_RES_X - 2, 4)
        random_y = random.randrange(2, SCREEN_RES_Y - 2, 4)

        self.food.x = random_x
        self.food.y = random_y
