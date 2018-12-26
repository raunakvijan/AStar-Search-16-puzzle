# Heuristic Search 16 puzzle

## Part 1: The 16-puzzle (20 pts)
Here’s a variant of the 15-puzzle that we studied in class. The game board consists of a 4x4 grid, but with
no empty space, so there are 16 tiles instead of 15. In each turn, the player can either (1) choose a row of
the puzzle and slide the entire row of tiles left or right, with the left- or right-most tile “wrapping around”
to the other side of the board, or (2) choose a column of the puzzle and slide the entire the column up or
down, with the top- or bottom-most tile “wrapping around.” 

The goal of the puzzle is to find the shortest sequence of moves that restores the canonical configuration (on
the left above) given an initial board configuration. We’ve written an initial implementation of a program
to solve these puzzles — find it in your github repository. You can run the program like this:
./solver16.py [input-board-filename]
where input-board-filename is a text file containing a board configuration in a format like:
5 7 8 1
10 2 4 3
6 9 11 12
15 13 14 16
We’ve included a few sample test boards in your repository. While the program works, the problem is that
it is quite slow for complicated boards. Using this code as a starting point, implement a faster version, using
A* search with a suitable heuristic function that guarantees finding a solution in is few moves as possible.
The program can output whatever you’d like, except that the last line of output should be a machine-readable
representation of the solution path you found, in this format:
[move-1] [move-2] ... [move-n]
where each move is encoded as a letter L, R, U, or D for left, right, up, or down, respectively, and a row
or column number (indexed beginning at 1). For instance, the two moves in the picture above would be
represented as:
R2 D2
