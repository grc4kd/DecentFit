import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DARK_BLUE = (0, 71, 132)
LIGHT_BLUE = (162, 222, 251)
GREY_GREEN = (108, 119, 94)
MAGENTA = (185, 119, 232)
RED = (251, 20, 3)
ORANGE = (251, 127, 24)
YELLOW = (251, 251, 59)

# Tetromino shapes and colors in a dictionary keyed by letter
PIECES = ["S", "J", "Z", "L", "O", "I", "T"]

COLORS = {
    "S": DARK_BLUE,
    "J": LIGHT_BLUE,
    "Z": GREY_GREEN,
    "L": MAGENTA,
    "O": RED,
    "I": ORANGE,
    "T": YELLOW,
}

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[1, 1, 1], [0, 1, 0]],
    "J": [[1, 1, 1], [1, 0, 0]],
    "L": [[1, 1, 1], [0, 0, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
}


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Decent Fit")


class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self, board):
        # Create a new rotated shape
        rotated = []
        for i in range(len(self.shape[0])):
            row = []
            for j in range(len(self.shape) - 1, -1, -1):
                row.append(self.shape[j][i])
            rotated.append(row)

        # Check if rotation is valid
        if self.is_valid_position(rotated, self.x, self.y, board):
            self.shape = rotated

    def is_valid_position(self, shape, x, y, board):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if (
                        x + j < 0
                        or x + j >= GRID_WIDTH
                        or y + i >= GRID_HEIGHT
                        or (y + i >= 0 and board[y + i][x + j])
                    ):
                        return False
        return True


def create_board():
    return [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def generate_tetromino():
    piece = random.choice(PIECES)
    return Tetromino(SHAPES[piece], COLORS[piece])


def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    cell,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )


def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    tetromino.color,
                    (
                        (tetromino.x + x) * BLOCK_SIZE,
                        (tetromino.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )


def is_inside_bounds(tetro, x, y):
    """Check if a piece is within bounds of the game board at position [x, y]"""
    return (0 <= x < BOARD_WIDTH - len(tetro.shape[0]) + 1) and (
        0 <= y < BOARD_HEIGHT - len(tetro.shape) + 1
    )


def has_board_collision(tetro, board, x, y):
    """Check if filled squares on the game board collide with a piece at position [x, y]"""
    for j, row in enumerate(tetro.shape):
        for i, cell in enumerate(row):
            if cell and (
                y + j >= BOARD_HEIGHT
                or x + i < 0
                or x + i >= BOARD_WIDTH
                or board[y + j][x + i] != (0, 0, 0)
            ):
                return True

    return False


def move_tetromino(tetro, board, dx=0, dy=0):
    """Move the tetromino and check for collisions."""
    new_x = tetro.x + dx
    new_y = tetro.y + dy

    if is_inside_bounds(tetro, new_x, new_y) and not has_board_collision(tetro, board, new_x, new_y):
        tetro.x = new_x
        tetro.y = new_y
        return True

    return False


def check_lines(board):
    lines_to_remove = []
    for y in range(GRID_HEIGHT):
        if all(board[y]):
            lines_to_remove.append(y)

    # Remove completed lines
    for y in lines_to_remove:
        del board[y]
        board.insert(0, [False for _ in range(GRID_WIDTH)])


def main():
    """Main game loop with independent FPS and game speed."""
    # Game state
    board = create_board()
    current_tetro = generate_tetromino()
    game_over = False
    last_drop_time = pygame.time.get_ticks()
    drop_interval = 1000  # ms

    while True:
        # Handle events (input is checked every frame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_tetromino(current_tetro, board, -1, 0)
                    elif event.key == pygame.K_RIGHT:
                        move_tetromino(current_tetro, board, 1, 0)
                    elif event.key == pygame.K_DOWN:
                        move_tetromino(current_tetro, board, 0, 1)
                    elif event.key == pygame.K_RCTRL:
                        current_tetro.rotate(board)
                    elif event.key == pygame.K_r and game_over:
                        # Restart game
                        board = create_board()
                        current_tetro = generate_tetromino()
                        game_over = False

        if not game_over:
            # Check for game speed-based drop
            current_time = pygame.time.get_ticks()
            if current_time - last_drop_time >= drop_interval:
                if not move_tetromino(current_tetro, board, 0, 1):
                    # Piece landed
                    for y, row in enumerate(current_tetro.shape):
                        for x, cell in enumerate(row):
                            if cell:
                                board[current_tetro.y + y][
                                    current_tetro.x + x
                                ] = current_tetro.color

                    # Generate new piece
                    current_tetro = generate_tetromino()

                    # Check for game over
                    if not move_tetromino(current_tetro, board, 0, 0):
                        game_over = True

                    # Reset drop timer
                    last_drop_time = current_time
                else:
                    # Successfully moved down, update timer
                    last_drop_time = current_time

            # Check for completed lines
            check_lines(board)

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw board and current piece
        draw_board(board)
        if not game_over:
            draw_tetromino(current_tetro)

        # Show game over screen
        if game_over:
            font = pygame.font.SysFont(None, 50)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

            font_small = pygame.font.SysFont(None, 30)
            restart_text = font_small.render(
                "Press R to restart", True, (255, 255, 255)
            )
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

        # Update display
        pygame.display.flip()

        # Cap FPS at 60 (independent of game speed)
        clock.tick(60)


if __name__ == "__main__":
    main()
