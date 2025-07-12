import pygame
import sys
from tetrominoes import generate_tetromino

WIDTH, HEIGHT = 300, 600
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
SQUARE_SIZE = WIDTH // BOARD_WIDTH
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell.color, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

def draw_tetromino(tetro):
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetro.color, (tetro.x * SQUARE_SIZE + x * SQUARE_SIZE, tetro.y * SQUARE_SIZE + y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

def move_tetromino(tetro, dx=0, dy=0):
    new_x = tetro.x + dx
    new_y = tetro.y + dy

    // TODO: account for the width and height of pieces before iteration
    // during collision detection. Check only filled squares for collisions.
    // start from the bottom, but check x-axis and y-axis boundaries
    if not (0 <= new_x < BOARD_WIDTH) or not (0 <= new_y < BOARD_HEIGHT):
        return False

    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
	    // BUG: crashes here with stack trace -> line 74, if not move_tetromino(current_tetro, dy=1):
            //                                                       ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
            // IndexError: list index out of range
            //  if cell and board[new_y + y][new_x + x]:
            //              ~~~~~^^^^^^^^^^^
            if cell and board[new_y + y][new_x + x]:
                return False

    tetro.x = new_x
    tetro.y = new_y
    return True

def check_lines():
    global board
    lines_to_remove = [y for y, row in enumerate(board) if all(row)]

    for line in lines_to_remove:
        del board[line]

    for _ in range(len(lines_to_remove)):
        board.insert(0, [0 for _ in range(BOARD_WIDTH)])

def main():
    global board
    board = create_board()
    current_tetro = generate_tetromino()

    falling = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_tetromino(current_tetro, -1)
        elif keys[pygame.K_RIGHT]:
            move_tetromino(current_tetro, 1)

        if falling:
            if not move_tetromino(current_tetro, dy=1):
                for y, row in enumerate(current_tetro.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            board[current_tetro.y + y][current_tetro.x + x] = current_tetro.color

                check_lines()
                current_tetro = generate_tetromino()
                falling = False

        screen.fill((0, 0, 0))
        draw_board(board)
        draw_tetromino(current_tetro)
        pygame.display.flip()

        if not falling:
            pygame.time.wait(300)
            falling = True

        clock.tick(FPS)

if __name__ == "__main__":
    main()
