# sudoku
A simple sudoku puzzle solver

### Running it ###

python solver.py -d 9 -n 20 -t 8

This command does:

1) Create a random puzzle with 20 numbers filled in.
2) Find a solution via brute-force search with 8 concurrent threads.

The random puzzle created is valid. (E.g. it does not break sudoku rules), but it is possible for the puzzle to have no valid solutions.

With the -a True parameter, the solver will look for all possible solutions.  This could take a long time depending on the puzzle.  A problem I have right now is knowing when the threads can quit. E.g. when all the possible boards are exhausted.  I am looking into this issue and will try to come up with a solution.
