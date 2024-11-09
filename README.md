# Jumping Maze

A Python implementation of a maze solver that uses DFS (Depth-First Search) and Uniform Cost algorithms to find paths in a jumping maze where each cell contains a number indicating how many steps you can move in any direction.

## Prerequisites

- Python 3.x
- Pygame

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install pygame
```

## Usage

Run the program with an input file:

```bash
python src/main.py input.txt
```

The input file should follow this format:

- First line: M N START_X START_Y END_X END_Y
    - M, N: Maze dimensions
    - START_X, START_Y: Starting position
    - END_X, END_Y: Goal position
- Next M lines: Grid of numbers representing jump distances
- End with a line containing "0"