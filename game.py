import sys
import pygame

from tetrominoes import Tetromino, generate_tetromino

# Tetromino shapes and colors in a dictionary keyed by letter
PIECES = ["S", "J", "Z", "L", "O", "I", "T"]

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
SQUARE_SIZE = SCREEN_WIDTH // BOARD_WIDTH
FPS = 60
MS_PER_MOVE = 100

ms_since_tick = 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Decent Fit")


def create_board():
    return [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def draw_board(board: list[list[tuple[int, int, int]]]):
    """Draw the board on the screen."""
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                if cell != (0, 0, 0):  # Only draw non-empty cells
                    pygame.draw.rect(
                        screen,
                        cell,
                        (
                            x * SQUARE_SIZE,
                            y * SQUARE_SIZE,
                            SQUARE_SIZE - 1,
                            SQUARE_SIZE - 1,
                        ),
                    )


def draw_tetromino(tetro: Tetromino):
    """Draw the current tetromino on the screen."""
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    tetro.color,
                    (
                        tetro.x * SQUARE_SIZE + x * SQUARE_SIZE,
                        tetro.y * SQUARE_SIZE + y * SQUARE_SIZE,
                        SQUARE_SIZE - 1,
                        SQUARE_SIZE - 1,
                    ),
                )


def is_inside_bounds(tetro: Tetromino, x: int, y: int) -> bool:
    """Check if a piece is within bounds of the game board at position [x, y]"""
    return (0 <= x < BOARD_WIDTH - len(tetro.shape[0]) + 1) and (
        0 <= y < BOARD_HEIGHT - len(tetro.shape) + 1
    )


def has_board_collision(tetro: Tetromino, board: list[list[tuple[int, int, int]]], x: int, y: int):
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


def move_tetromino(tetro: Tetromino, board: list[list[tuple[int, int, int]]], dx: int = 0, dy: int = 0):
    """Move the tetromino and check for collisions."""
    new_x = tetro.x + dx
    new_y = tetro.y + dy

    if is_inside_bounds(tetro, new_x, new_y) and not has_board_collision(
        tetro, board, new_x, new_y
    ):
        tetro.x = new_x
        tetro.y = new_y
        return True

    return False


def check_lines(board: list[list[tuple[int, int, int]]]):
    """Check for and remove completed lines."""
    lines_to_remove = [
        y for y, row in enumerate(board) if all(cell != (0, 0, 0) for cell in row)
    ]

    for line in lines_to_remove:
        del board[line]

    for _ in range(len(lines_to_remove)):
        board.insert(0, [(0, 0, 0) for _ in range(BOARD_WIDTH)])


def main():
    """Main game loop with independent FPS and game speed."""
    # Game state
    board = create_board()
    current_tetro = generate_tetromino()
    game_over = False

    # movement events occur less frequently than rendering FPS
    movement_timer = 0
    movement_interval = MS_PER_MOVE
    pending_rotation = False

    while True:
        # Handle events (input is checked every frame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over:
                keys = pygame.key.get_pressed()

                # allow translation movement as often as possible
                if keys[pygame.K_LEFT]:
                    move_tetromino(current_tetro, board, -1, 0)
                if keys[pygame.K_RIGHT]:
                    move_tetromino(current_tetro, board, 1, 0)
                if keys[pygame.K_DOWN]:
                    move_tetromino(current_tetro, board, 0, 1)

                # delay handling of rotation
                if (
                    keys[pygame.K_RCTRL]
                    or keys[pygame.K_LCTRL]
                    or keys[pygame.K_r]
                    or keys[pygame.K_SPACE]
                ):
                    pending_rotation = True

                # quit game keys trigger right away
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    game_over = True

        ms_since_tick = clock.tick(FPS)
        movement_timer += ms_since_tick

        # allow rotation less frequently to slow down rotation speed
        if pending_rotation and movement_timer >= (movement_interval >> 2):
            pending_rotation = False

            if not current_tetro.rotate(board):
                # in case of a failed rotation
                pass

        # Move the tetromino down based on the timer
        if movement_timer >= movement_interval:
            # Move the tetromino to the next location when valid
            valid_move = move_tetromino(current_tetro, board, 0, 1)
            # Handle final piece locations, collisions, and generation of the next piece
            if not valid_move:
                for y, row in enumerate(current_tetro.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            board[current_tetro.y + y][
                                current_tetro.x + x
                            ] = current_tetro.color

                current_tetro = generate_tetromino()

                # edge case - new tetromino causes game over. for example, when the next piece overflows the top of the game board.
                if not move_tetromino(current_tetro, board, 0, 0):
                    game_over = True

            # Reset the movement timer
            movement_timer = 0

            # Check for completed lines on timer end
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
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

            font_small = pygame.font.SysFont(None, 30)
            restart_text = font_small.render(
                "Press R to restart", True, (255, 255, 255)
            )
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            screen.blit(restart_text, restart_rect)

        # Update display
        pygame.display.flip()

        # Control game speed
        ms_since_tick = clock.tick(FPS)

        # Handle game over input
        if game_over:
            for event in pygame.event.get():
                if (
                    event.type == pygame.KEYDOWN
                    and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
                ) or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Restart the game
                    board = create_board()
                    current_tetro = generate_tetromino()
                    game_over = False


if __name__ == "__main__":
    main()
