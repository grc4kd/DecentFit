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
    return [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell != (0, 0, 0):  # Only draw non-empty cells
                pygame.draw.rect(screen, cell, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

def draw_tetromino(tetro):
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetro.color, (tetro.x * SQUARE_SIZE + x * SQUARE_SIZE, tetro.y * SQUARE_SIZE + y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

def move_tetromino(tetro, board, dx=0, dy=0):
    new_x = tetro.x + dx
    new_y = tetro.y + dy

    # Check if the new position is within bounds
    if not (0 <= new_x < BOARD_WIDTH - len(tetro.shape[0]) + 1) or not (0 <= new_y < BOARD_HEIGHT - len(tetro.shape) + 1):
        return False

    # Check only filled squares for collisions
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell and (new_y + y >= BOARD_HEIGHT or new_x + x < 0 or new_x + x >= BOARD_WIDTH or board[new_y + y][new_x + x] != (0, 0, 0)):
                return False

    tetro.x = new_x
    tetro.y = new_y
    return True

def check_lines(board):
    lines_to_remove = [y for y, row in enumerate(board) if all(cell != (0, 0, 0) for cell in row)]

    for line in lines_to_remove:
        del board[line]

    for _ in range(len(lines_to_remove)):
        board.insert(0, [(0, 0, 0) for _ in range(BOARD_WIDTH)])

def main():
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
            move_tetromino(current_tetro, board, -1)
        elif keys[pygame.K_RIGHT]:
            move_tetromino(current_tetro, board, 1)

        if falling:
            if not move_tetromino(current_tetro, board, dy=1):
                for y, row in enumerate(current_tetro.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            board[current_tetro.y + y][current_tetro.x + x] = current_tetro.color

                check_lines(board)
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
