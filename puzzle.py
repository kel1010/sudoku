import math
import copy
import pickle
import sys

class Puzzle(object):
    """ A sudoku puzzle """

    CHECKERS = dict()

    @staticmethod
    def checkers(dim):
        """ create indexes for checking rows/columns/squares """
        if not dim in Puzzle.CHECKERS:
            checkers = dict()
            sqrtdim = int(math.sqrt(dim))
            rows = [None]*dim
            cols = [None]*dim
            sqrs = [None]*dim
            sqrs_map = dict()
            for i in range(dim):
                #rows
                rows[i] = map(lambda j: j+i*dim, range(dim))
                #columns
                cols[i] = map(lambda j: j*dim+i, range(dim))
                #squares
                x0 = i%sqrtdim
                y0 = i/sqrtdim
                indexes = [0]*dim
                for j in range(dim):
                    x = j%sqrtdim
                    y = j/sqrtdim
                    index = ((y0*sqrtdim)+y)*dim + x0*sqrtdim + x
                    indexes[j] = index
                    sqrs_map[index] = i
                sqrs[i] = indexes

            checkers['rows'] = rows
            checkers['cols'] = cols
            checkers['sqrs'] = sqrs
            checkers['sqrs_map'] = sqrs_map
            Puzzle.CHECKERS[dim] = checkers

        return Puzzle.CHECKERS[dim]

    @staticmethod
    def input(_in):
        data = ''
        temp = _in.read(1000);
        while temp:
            data = data + temp
            temp = _in.read(1000);
        board = map(lambda x: int(x.strip()), data.split())
        return Puzzle(board)

    def __init__(self, board):
        # make sure the board is a square
        assert math.sqrt(len(board)) == math.floor(math.sqrt(len(board))), \
            'Puzzle needs be square'

        self.board = board
        self.dim = int(math.sqrt(len(board)))
        self.next_free = 0 # next spot on the board without a number.  lazy initalized

        # make sure the dimension is also a square e.g. 4, 9, 16, ...
        assert math.sqrt(self.dim) == math.floor(math.sqrt(self.dim)), \
            "Puzzle\'s side needs to be a square as well. e.g. 4, 9, 16"

    def is_valid_tile(self, indexes):
        f = [False]*self.dim
        for i in indexes:
            if self.board[i]:
                if f[self.board[i]-1]:
                    return False
                else:
                    f[self.board[i]-1] = True
        return True

    def is_valid(self):
        """ verify the current board is a valid solution """
        checkers = Puzzle.checkers(self.dim)
        for indexes in checkers['rows']+checkers['cols']+checkers['sqrs']:
            if not self.is_valid_tile(indexes):
                return False
        return True

    def free(self):
        """ get the index of the next free spot.  return -1 if the board is full """
        if self.board[self.next_free]==0:
            return self.next_free
        else:
            if self.next_free+1<self.dim*self.dim:
                self.next_free = self.next_free + 1
                return self.free()
            else:
                return -1

    def valid_tile(self, indexes):
        """returns number we can still play"""
        f = [False]*self.dim
        s = set(range(1, self.dim+1))
        for i in indexes:
            if self.board[i]:
                s.remove(self.board[i])
        return s

    def valid_free(self):
        """ get possible for the next free tile space """
        checkers = Puzzle.checkers(self.dim)
        pos = self.free()
        col = pos % self.dim
        row = pos / self.dim
        sqr = checkers['sqrs_map'][pos]

        return self.valid_tile(checkers['cols'][col]) &\
            self.valid_tile(checkers['rows'][row]) &\
            self.valid_tile(checkers['sqrs'][sqr])

    def copy(self):
        """ make a copy of the object """
        new_board = copy.copy(self.board)
        new_puzzle = Puzzle(new_board)
        new_puzzle.next_free = self.next_free
        return new_puzzle

    def _solve(self):
        """ Solve this puzzle. Assuming the current puzzle is valid. """
        Puzzle.counter = Puzzle.counter + 1
        free = self.free()
        if free==-1:
            # A valid full board is a solution
            return self
        else:
            puzzle = self.copy()
            for i in puzzle.valid_free():
                puzzle.board[free] = i # use [1:self.dim] instead of [0:self.dim)
                solved = puzzle._solve()
                if solved:
                    return solved
        return False

    def solve(self):
        """ Solve this puzzle
        This is a single threaded solution
        Return a solution Puzzle object or return False if no solution is possible """
        return self._solve() if self.is_valid() else False

    def output(self, _out=sys.stdout):
        for i in range(self.dim*self.dim):
            _out.write('%2d ' % self.board[i],) # comma at the end prevents a new line
            if (i+1)%self.dim==0:
                _out.write('\n')
        _out.write('\n')
