#
# CS475 - Jan 25, 2019
#
# GUI for TTT, continuation of the version done on the 'video'
#

from tkinter import *
import player08 as playerr
import time
import referee3 as ref

NOT_DONE = 99
BSIZE = 9

symbol = (' ', 'X', 'O')

winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class Board:

    def __init__(self, win):

        # 1 == 'X' and 2 == 'O'

        self.human = 1
        self.computer = 2

        # create Player object (from player.py module -- in this directory)

        #self.player = player.Player(self.computer)
        self.player = playerr.Player08(self.computer)

        # vars for remember whose turn it is, whether game is over, and a copy of the board
        # call this the 'logical' board, on the screen is the 'graphics' board

        self.turn = 1
        self.gameover = False
        self.board = [0] * BSIZE

        # configure main window -- background color, fonts for labels and buttons

        win.configure(bg='#000')
        win.option_add("*Label.font", ("Helvetica", 32))
        win.option_add("*Button.font", ("Helvetica", 28))
        self.mess = Label(win, text='Click on Move to make computer move.', bg='#000', fg='#ff0',
                          font=('Helvetica', 20))

        # put the message label on the top row of the app
        self.mess.grid(row=0, column=0, columnspan=3)

        # we need to save a list of labels -- one for each square of the TTT board

        self.lablist = []
        for i in range(BSIZE):
            lab = Label(win, text='', relief=RAISED, width=7, height=3)
            lab.grid(row=1 + i // 3, column=i % 3)
            lab.bind('<Button-1>', self.callback)
            lab.pos = i
            self.lablist.append(lab)

        # add bottom row of buttons. you may ask why I didn't use buttons for the TTT board?  that could work.

        self.quit = Button(win, text='Quit', bg='#0ff', fg='#fff', command=win.destroy)
        self.quit.grid(row=4, column=0, sticky=N + S + E + W)
        self.quit = Button(win, text='Reset', bg='#ff0', fg='#fff', command=self.reset)
        self.quit.grid(row=4, column=1, sticky=N + S + E + W)
        self.quit = Button(win, text='Move', bg='#0ff', fg='#fff', command=self.mover)
        self.quit.grid(row=4, column=2, sticky=N + S + E + W)

        self.clock = Label(win, text='', bg='#000', fg='#ff0', font=('Helvetica', 20))
        self.clock.grid(row=5, column=0, columnspan=3)

    # method (function) to determine if the game is over after the move just made
    # boardvalue returns:
    #         0 --> tie game (board full)
    #         1 --> X wins
    #         2 --> O wins
    #  NOT_DONE --> game not over (NOT_DONE is actually 99, anything not in [0,1,2] is good)
    #
    def isgameover(self):
        val = self.boardvalue(self.turn)
        if val == self.turn:
            self.mess.configure(text=symbol[self.turn] + ' wins')
            self.gameover = True
            return True
        elif val == 0:
            self.mess.configure(text='Tie game.')
            self.gameover = True
            return True
        return False

    # this is the method that responds to clicks on the board, nothing happens unless
    # (1) it's the human's move, (2) the game is not over, and (3) the square is empty

    def callback(self, event):
        if self.turn != self.human:  # is it human's turn?
            return
        if self.gameover:  # is the game over?
            return
        pos = event.widget.pos
        if self.board[pos] != 0:  # is the board square empty?
            return
        self.board[pos] = self.turn
        print(self.board)
        event.widget.configure(text=symbol[self.turn])
        if not self.isgameover():
            self.turn = 3 - self.turn

    def boardvalue(self, who):
        for win in winners:
            if all([self.board[x] == who for x in win]):  # Python list comprehensions are faster than for loops.
                return who  # I'll prove this in class if you remind me.
        if not 0 in self.board:  # tie game
            return 0
        return NOT_DONE  # game not over

    # Button functions

    # reset starts a new game, resets all the vars and clears the graphical board

    def reset(self):
        self.turn = 1
        self.gameover = False
        self.board = [0] * BSIZE  # new logical board
        self.mess.configure(text='')
        for lab in self.lablist:
            lab.configure(text='')

    # clicking on Move method tells the computer to think of a move

    def mover(self):
        if self.turn != self.computer:  # make sure it's the computer's move
            return
        t0 = time.time()
        string_board = []
        for x in self.board:
            string_board.append(str(x))
        mov = self.player.getmove(string_board)  # Get the move.  We probably should not trust the player object
        self.clock.configure(text="{0:10.6f}".format(time.time() - t0))

        if self.board[mov] != 0:  # with the real board, it would be better to send a copy.  I will
            print('error from getmove', board, mov)  # will fix this.
            win.destroy()
        self.board[mov] = self.computer
        self.lablist[mov].configure(text=symbol[self.turn])
        if not self.isgameover():
            self.turn = 3 - self.turn


if __name__ == "__main__":
    ref1 = ref.Referee()
    for i in range(4000):
        ref1.playgame()
    win = Tk()
    game = Board(win)
    win.mainloop()
