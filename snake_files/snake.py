from snake_files import segment
START_POSITION = (30, 30)


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
    
    def create_snake(self):
        self.segments.append(segment.Segment(START_POSITION))
        
