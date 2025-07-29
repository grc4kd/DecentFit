import random


class Tetromino:
    """Represents a tetromino piece."""

    def __init__(self, shape, color):
        """Initializes a new Tetromino instance.

        Args:
            shape (list of lists): The shape of the tetromino.
            color (tuple): The color of the tetromino.
        """
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
    'S': (15, 127, 0),
    'J': (150, 186, 220),
    'Z': (60, 114, 201),
    'L': (127, 63, 255),
    'O': (170, 17, 17),
    'I': (255, 127, 63),
    'T': (255, 255, 127)
}


def generate_tetromino():
    """Generate a random tetromino."""
    shape = random.choice(list(SHAPES.keys()))
    return Tetromino(SHAPES[shape], COLORS[shape])
