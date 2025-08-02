import random


# Define board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20


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

    def rotate(self, board):
        """Rotate the tetromino 90 degrees clockwise and check for collisions."""
        # Save original shape and position
        original_shape = [row[:] for row in self.shape]
        original_x, original_y = self.x, self.y

        # Perform rotation
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]
        
        # Check if rotated shape fits within bounds and doesn't collide
        for y, row in enumerate(rotated):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x
                    new_y = self.y + y
                    if (new_x < 0 or new_x >= BOARD_WIDTH or 
                        new_y >= BOARD_HEIGHT or 
                        (new_y >= 0 and board[new_y][new_x] != (0, 0, 0))):
                        # Restore original shape and position
                        self.shape = original_shape
                        self.x, self.y = original_x, original_y
                        return False  # Rotation failed

        # Apply rotation
        self.shape = rotated
        return True


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
