from snake_files import segment
START_POSITION = (30, 30)
START_POSITION_2 = (26, 30)


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.heading = "RIGHT"

    def create_snake(self):
        self.segments.append(segment.Segment(START_POSITION))
        self.segments.append(segment.Segment(START_POSITION_2))

    def move_snake(self):
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
