
# Connect 4 Game

A digital version of the classic Connect 4 game! This project includes two gameplay modes:
1. **Play with a Friend**: Compete against another player locally.
2. **Play with AI**: Challenge an AI agent, powered by a genetic algorithm, for a unique, competitive experience.

## Game Description

Connect 4 is a two-player game where each player takes turns dropping colored discs into a vertical grid. The objective is to be the first to form a line of four of your discs in any direction: horizontally, vertically, or diagonally.

## Features

- **Single-Player Mode**: Compete against an AI that learns strategies via genetic algorithms, adjusting its moves to maximize its chances of winning.
- **Two-Player Mode**: Play with a friend on the same device.
- **Pygame UI**: The game board and interface are designed using Pygame for an engaging, interactive experience.

## Requirements

- Python 3.6+
- Pygame
- Numpy

To install dependencies, run:
```bash
pip install pygame numpy
```

## How to Play

### Starting the Game
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/connect4
   ```
2. Navigate to the project directory:
   ```bash
   cd connect4
   ```
3. Choose a mode to play:
   - **Two-Player Mode**: Run `game1.py` to play with a friend.
   - **Single-Player Mode**: Run `game2.py` to play against the AI.

### Gameplay

- **Two-Player Mode**:
  1. Players take turns clicking on a column where they want to drop their disc.
  2. The first player to connect four of their pieces in a line wins!

- **AI Mode**:
  1. The AI uses a genetic algorithm to evolve its strategy over multiple plays.
  2. Challenge the AI and see if you can outsmart it!

## Game Logic

### Genetic Algorithm for AI

The AI mode utilizes a genetic algorithm to refine its decision-making process:
- **Selection**: Evaluates game states to select optimal moves.
- **Mutation and Crossover**: Introduces random variations and combines strategies to enhance future game decisions.

### Winning Conditions
The game checks for winning patterns after each move to determine if a player has connected four pieces in a row, either horizontally, vertically, or diagonally.


