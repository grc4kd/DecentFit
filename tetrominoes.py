import random

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = 5
        self.y = 0

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[1, 1, 1], [0, 1, 0]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = {
    'I': (231, 117, 60),
    'O': (170, 17, 17),
    'T': (238, 231, 139),
    'S': (5, 161, 0),
    'Z': (74, 208, 187),
    'J': (30, 51, 138),
    'L': (183, 47, 204)
}

def generate_tetromino():
    shape = random.choice(list(SHAPES.keys()))
    return Tetromino(SHAPES[shape], COLORS[shape])
