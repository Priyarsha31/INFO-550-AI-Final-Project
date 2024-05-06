# INFO-550-AI-Final-Project

## AI CSP Escape Room Challenge

Welcome to the AI CSP Escape Room Challenge! This project presents a collection of puzzle games designed to test your logic, problem-solving skills, and ability to think outside the box. Can you solve each puzzle and escape the room?

## How to Run the Game

### Prerequisites
- Python 3.x installed on your system
- Pygame library installed (pip install pygame)
- Clone or download this repository to your local machine

### Running the Game
Navigate to the project directory in your terminal or command prompt.

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```
This will install the necessary dependencies, including the Pygame library.

After installing the dependencies, run the main.py file by executing the following command:

```bash
python main.py
```

The game window will open, displaying the welcome screen and instructions.

### Solve each puzzle presented to you:

1. Color Mapping Puzzle: Click on tiles to change colors. No two adjacent tiles should have the same color.

2. Logic Puzzle: Solve the equation LOCK + LOCK = OPEN. Click on each box to enter numbers. Each letter represents a unique number.

3. Jigsaw Puzzle: Rearrange the jumbled tiles to form the complete image.

4. Sudoku Game: Fill in the Sudoku grid correctly. Each row, column, and 3x3 subgrid must contain all digits from 1 to 9.


Once you've successfully solved all puzzles, the game will end.

## Files and Structure
### 'main.py'
This file contains the main entry point for the game. It initializes the Pygame window, displays the welcome screen, and orchestrates the flow of the game by calling puzzle-solving functions.

### 'settings.py'
This file defines various constants used throughout the game, such as window dimensions, colors, and FPS (frames per second).

### 'requirements.txt'
Contains a list of Python dependencies required to run the game.

### 'utils.py'
This module provides utility functions used for image loading and manipulation, as well as drawing tiles on the game window.

### 'puzzles.py'
This module contains functions for each puzzle type:

- Color Mapping Puzzle: Allows players to solve a color-matching puzzle.
- Logic Puzzle: Presents players with a logic-based puzzle to solve an equation.
- Jigsaw Puzzle: Implements a jigsaw puzzle where players must rearrange pieces to form an image.
- Sudoku Game: Provides a Sudoku puzzle for players to solve.

### 'scary.jpg'
This image file is used as the background image for the jigsaw puzzle.