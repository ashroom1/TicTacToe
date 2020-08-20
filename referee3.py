#
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

from player08 import Player08 as P1
from player import Player as P2

NOT_DONE = 99
BSIZE = 9

winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class Referee:

    def __init__(self, p1, p2):

        #
        # select who gets 'X', who gets 'O'
        #

        self.player1 = p1(1)
        self.player2 = p2(2)

        print('Player 1:', self.player1)
        print('Player 2:', self.player2)

        self.board = [0] * BSIZE
        self.reset()  # sets up self.board, self.turn, self.gameover vars

    def isgameover(self):

        val = self.boardvalue(self.turn)  # returns 0 (tie), 1 ('X'), 2 ('O'), or NOTDONE

        if val == self.turn:  # the new move won the game
            self.gameover = True
            return self.turn
        elif val == 0:  # the new move filled the board
            self.gameover = True
            return 0
        return -1

    def printboard(self):
        for i in range(0, 9, 3):
            print(self.board[i:i + 3])

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
            rv = self.isgameover()
            if rv < 0:
                self.turn = 3 - self.turn
            else:
                self.player1.gameover(self.board, rv)
                self.player2.gameover(self.board, rv)
                #           self.printboard()
                return rv


if __name__ == "__main__":

    ngames = 100 if len(sys.argv) == 1 else int(sys.argv[1])

    tally = [0, 0, 0]

    ref1 = Referee(P1, P2)
    ref2 = Referee(P2, P1)
    for i in range(ngames // 2):
        rv = ref1.playgame()
        tally[rv] += 1
        rv = ref2.playgame()
        tally[rv if rv == 0 else (3 - rv)] += 1
        print("{0:4d} {1:4d} {2:4d}".format(tally[0], tally[1], tally[2]))
    ref1.player1.datadump()
    ref1.player2.datadump()
    ref2.player1.datadump()
    ref2.player2.datadump()


