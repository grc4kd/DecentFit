import pygame
import sys
from tetrominoes import generate_tetromino, Tetromino

WIDTH, HEIGHT = 300, 600
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
SQUARE_SIZE = WIDTH // BOARD_WIDTH
FPS = 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def create_board():
    """Create an empty board."""
    return [[(0, 0, 0) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def draw_board(board):
    """Draw the board on the screen."""
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell != (0, 0, 0):  # Only draw non-empty cells
                pygame.draw.rect(screen, cell, (x * SQUARE_SIZE,
                                 y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))


def draw_tetromino(tetro):
    """Draw the current tetromino on the screen."""
    for y, row in enumerate(tetro.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetro.color, (tetro.x * SQUARE_SIZE + x * SQUARE_SIZE,
                                 tetro.y * SQUARE_SIZE + y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))


def move_tetromino(tetro, board, dx=0, dy=0):
    """Move the tetromino and check for collisions."""
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
    """Check for and remove completed lines."""
    lines_to_remove = [y for y, row in enumerate(
        board) if all(cell != (0, 0, 0) for cell in row)]

    for line in lines_to_remove:
        del board[line]

    for _ in range(len(lines_to_remove)):
        board.insert(0, [(0, 0, 0) for _ in range(BOARD_WIDTH)])


def main():
    """Main game loop."""
    board = create_board()
    current_tetro = generate_tetromino()
    
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if not game_over:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                move_tetromino(current_tetro, board, -1, 0)
            if keys[pygame.K_RIGHT]:
                move_tetromino(current_tetro, board, 1, 0)
            if keys[pygame.K_DOWN]:
                move_tetromino(current_tetro, board, 0, 1)
            if keys[pygame.K_RCTRL]:
                # Rotate the tetromino when right Ctrl is pressed
                if not current_tetro.rotate(board):
                    pass
                    
            # Check if the piece has landed
            if not move_tetromino(current_tetro, board, 0, 1):
                # Place the piece on the board
                for y, row in enumerate(current_tetro.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            board[current_tetro.y + y][current_tetro.x + x] = current_tetro.color
                
                # Generate a new piece
                current_tetro = generate_tetromino()
                
                # Check for game over (new piece can't be placed)
                if not move_tetromino(current_tetro, board, 0, 0):
                    # Game over
                    game_over = True
                    # Don't break the loop - we want to show the game over screen
                    # But don't process any more input
                    # We'll handle game over in the event loop below
                
            # Check for completed lines
            check_lines(board)
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the board and current piece
        draw_board(board)
        if not game_over:
            draw_tetromino(current_tetro)
        
        # Show game over message if game is over
        if game_over:
            font = pygame.font.SysFont(None, 50)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            
            # Show restart instructions
            font_small = pygame.font.SysFont(None, 30)
            restart_text = font_small.render("Press R to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Control game speed
        clock.tick(FPS)
        
        # Handle game over input
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Restart the game
                    board = create_board()
                    current_tetro = generate_tetromino()
                    game_over = False


if __name__ == "__main__":
    main()
