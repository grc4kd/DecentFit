# Decent Fit - Game Documentation

## Overview
This is a simple board game implemented in Python using the Pygame library. The game features standard mechanics including piece movement, rotation, line clearing, and game over detection. 

## Gameplay Instructions
- **Move Left**: Press `Left Arrow` key to move the current piece left.
- **Move Right**: Press `Right Arrow` key to move the current piece right.
- **Move Down**: Press `Down Arrow` key to move the current piece down faster.
- **Rotate**: Press `Right Ctrl` key to rotate the current piece 90 degrees clockwise.
- **Restart Game**: After game over, press `R` to restart the game.

The game ends when a new tetromino cannot be placed at the top of the board (i.e., the stack has reached the top).

## Key Features
- Random generation of the next puzzle piece
- Collision detection and wall/ground blocking
- Line clearing when a full row is filled
- Game over detection and restart functionality
- State and graphics utilize the `pygame` game development library.

## Development Setup with `python-uv`
1. Ensure you have `uv` installed (a modern Python toolchain). If not, install it via:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   (This installs `uv` globally.)

2. Navigate to your project directory:
   ```bash
   cd path/to/your/decent-fit-project
   ```

3. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
   This will read `pyproject.toml` and install all required packages (including `pygame`).

4. Verify the environment is set up correctly:
   ```bash
   uv run python -c "import pygame; print('Pygame is installed and working')"
   ```

## Running the Game
To run the game, use the following command:
`uv run game.py`

