# Battle of the giants:
#   referee TTT match between two player modules
#
# Module interface:
#     __init__ : send 1 or 2 ( for 'X' or 'O')
#     getmove  : send (a copy of) the board, a list of 9 integers in [0,1,2]
#     gameover : send board and winner, could reset game for player   <-- in the future
#

import time  # impose time limit   <-- in the future
import sys

from player08 import Player08 as P2  # random mover
from player import Player as P1  # random mover, prefers center, then corners

NOT_DONE = 99
BSIZE = 9

winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class Referee:

    def __init__(self):

        #
        # select who gets 'X', who gets 'O'
        #

        self.player1 = P1(1)
        self.player2 = P2(2)

        self.tally = [0, 0, 0]
        self.board = [0] * BSIZE
        self.reset()  # sets up self.board, self.turn, self.gameover vars

    def isgameover(self):

        val = self.boardvalue(self.turn)  # returns 0 (tie), 1 ('X'), 2 ('O'), or NOTDONE

        if val == self.turn:  # the new move won the game
            self.gameover = True
            self.tally[self.turn] += 1  # keep track of who wins
            return True
        elif val == 0:  # the new move filled the board
            self.gameover = True
            self.tally[0] += 1  # count ties
            return True
        return False

    def boardvalue(self, who):

        for win in winners:  # check all possible winning configurations
            if all([self.board[x] == who for x in win]):
                return who

        if not 0 in self.board:  # no zeros in board? then the board is filled
            return 0
        return NOT_DONE

    def reset(self):  # restart game

        self.turn = 1
        self.gameover = False
        self.board = [0] * BSIZE

    def playgame(self):

        self.reset()  # possibly redundant
        while True:
            if self.gameover:  # show X wins, O wins, ties
                print("{0:4d} {1:4d} {2:4d}".format(self.tally[1], self.tally[2], self.tally[0]))
                return
            boardcopy = [x for x in self.board]  # copy the board, since we don't trust the players
            if self.turn == 1:
                mov = self.player1.getmove(boardcopy)
            else:
                mov = self.player2.getmove(boardcopy)
            if self.board[mov] != 0:
                print('error from getmove:', mov, self.board)
                print('player', self.turn, 'is buggy')
                sys.exit(0)
            self.board[mov] = self.turn  # put move on our copy of the board
            if not self.isgameover():
                self.turn = 3 - self.turn


if __name__ == "__main__":

    ngames = 10000 if len(sys.argv) == 1 else int(sys.argv[1])

    ref = Referee()
    for i in range(ngames):
        ref.playgame()

