from puzzle import Puzzle
from optparse import OptionParser
import Queue
import math
import random
import threading
import time
import sys

class PuzzleSolver:
    """ Multi-threaded solver """

    def __init__(self, nthreads):
        self.nthreads = nthreads

    def runner(self):
        local = threading.local()
        local.counter = 0
        try:
            (blah, blah, puzzle) = self.puzzles.get(True, 2)
        except Queue.Empty:
            puzzle = None
        while puzzle:
            free = puzzle.free()
            if free==-1:
                self.solutions.append(puzzle)
                if not self.find_all:
                    self._quit()
            else:
                for i in puzzle.valid_free():
                    puzzle.board[free] = i
                    self.counter = self.counter + 1
                    local.counter = local.counter + 1
                    if self.counter % 10000 ==0:
                        print 'Boards examined: %s %s' % (self.counter, threading.current_thread().getName())
                    self.puzzles.put((-free, i, puzzle.copy())) # depth first

            try:
                (blah, blah, puzzle) = self.puzzles.get(True, 2)
            except Queue.Empty:
                break;

        print 'Thread %s quitting.  Process %s boards' % (threading.current_thread().getName(), local.counter)

    def _quit(self):
        # tell the threads it is quitting time
        for i in range(self.nthreads):
            self.puzzles.put((-1000000, i, None))

    def solve(self, puzzle, find_all=False):

        if not puzzle.is_valid():
            return []

        self.find_all = find_all
        self.counter = 0

        self.puzzles = Queue.PriorityQueue()

        self.solutions = list()

        assert puzzle.is_valid()
        self.puzzles.put((0, 0, puzzle))

        workers = list()
        for i in range(0, self.nthreads):
            t = threading.Thread(target=self.runner, name='Thread %s' % i)
            t.daemon = True
            t.start()
            workers.append(t)
        for worker in workers:
            worker.join()

        print 'Total boards examined: %s' % self.counter

        return self.solutions

def random_puzzle(dim, num):
    """ create a valid random puzzle """
    assert num <= dim*dim
    tries = 0
    while(True):
        board = [0]*(dim*dim)
        tries = tries + 1
        for i in range(num):
            value = int(math.floor(random.random()*dim))+1
            index = int(math.floor(random.random()*dim*dim))
            while board[index]!=0:
                index = int(math.floor(random.random()*dim*dim))
            board[index] = value
        puzzle = Puzzle(board)
        if puzzle.is_valid():
            print 'Generated a valid puzzle in %s tries' % tries
            puzzle.output()
            return puzzle

def threaded(puzzle, nthreads, find_all):
    return PuzzleSolver(nthreads).solve(puzzle.copy(), find_all=find_all)

def single(puzzle):
    Puzzle.counter = 0
    solution = puzzle.solve()
    print 'Boards examined: %s' % Puzzle.counter
    if solution:
        return [solution]
    else:
        return []

def main(options, args):
    if args:
        f = open(args[0], 'r')
        puzzle = Puzzle.input(f)
    else:
        puzzle = random_puzzle(options.dim, options.num)

    if int(options.nthreads)==0:
        solutions = single(puzzle)
    else:
        solutions = threaded(puzzle, options.nthreads, bool(options.all))

    if solutions:
        if options.outprefix:
            for i, solution in enumerate(solutions):
                fname = '%s_%s' % (options.outprefix, i)
                out = open(fname, 'w')
                solution.output(out)
                out.close()
        else:
            print 'Found %s solutions.  Here is one: ' % len(solutions)
            solutions[0].output()
    else:
        print 'No solution found!'

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-d', '--dimension', dest='dim', default=4, metavar='NUMBER', type='int',
                      help='Single side dimension of the puzzle. (default 9)')
    parser.add_option('-n', '--number',dest='num', default=0, metavar='NUMBER', type='int',
                      help='Number of filled tiles in the random puzzle. (default 0)')
    parser.add_option('-t', '--threads', dest='nthreads', default=2, metavar='NUMBER', type='int',
                      help='Number of threads used for solving the puzzle. 0 for non-threaded version. (defaults 2)')
    parser.add_option('-a', '--all', dest='all', default=False, metavar='BOOLEAN', type='string',
                        help='Find all possible solutions.  Works only with threaded version.')
    parser.add_option('-o', '--outprefix', dest='outprefix',default='',metavar='STRING', help='output sudoku file(s)')

    (options, args) = parser.parse_args()

    main(options, args)
