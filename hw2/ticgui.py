# Original code from Daniel Tan
# Cleaned up for the assignment by Aaron Johnson.
# ...Slightly modified by Ryan Phillips

import os
from Tkinter import *
import ttk
from random import randint
import time

# Ryan's tictactoe project
from tictactoe import *

class main:

    def __init__(self, master, args = None):

        # start edit (ryan)
        self.s1 = game([[0,0,0],[0,0,0],[0,0,0]])
        self.whose_turn = 1
        self.t = generate_game_tree(self.s1, self.whose_turn)
        self.current_node = self.t
        # end edit (ryan)

        # master frame
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        self.canvas_width = 300
        self.canvas_height = 300

        # canvas where the game is played on
        self.canvas = Canvas(self.frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill="both", expand=True)

        # shows status of game
        self.label = Label(self.frame, text='Tic Tac Toe Game', height=2, bg='black', fg='grey')
        self.label.pack(fill="both", expand=True)

        # frame to contain the buttons and drop downs
        self.bframe = Frame(self.frame)
        self.bframe.pack(fill="both", expand=True)

        self.player_choices = ['human','random','minimax']

        # frame to contain drop downs
        self.cframe = Frame(self.bframe)
        self.cframe.pack(fill="both", expand=True, side=LEFT)

        # player1 dropdown
        self.p1_chose = StringVar()
        self.p1_choice = ttk.Combobox(self.cframe, textvariable=self.p1_chose,
            height = 2, values = self.player_choices)
        self.p1_choice.pack(fill="both", expand=True, side=TOP)

        # player2 dropdown
        self.p2_chose = StringVar()
        self.p2_choice = ttk.Combobox(self.cframe, textvariable=self.p2_chose,
            height = 2, values = self.player_choices)
        self.p2_choice.pack(fill="both", expand=True, side=BOTTOM)


        # button to initiate the game
        self.start = Button(self.bframe, text='Click here to start',
            height=2, command=self.start_clicked, bg='white', fg='purple')
        self.start.pack(fill="both", expand=True, side=RIGHT)

        # canvas board drawing function call
        self._board()

        # set defaults upon receiving command line input, and run game without click
        if args is not None:
        	self.p1_chose.set(args[0])
        	self.p2_chose.set(args[1])
        	self.start_clicked()

    def start_clicked(self):
        '''Starts a new game.'''

        # ryan
        self.s1 = game([[0,0,0],[0,0,0],[0,0,0]])
        self.current_node = self.t
        self.whose_turn = 1
        # END ryan

        # refresh canvas
        self.canvas.delete(ALL)

        # function call on click
        self._board()

        # logical game board
        self.TTT = [[None,None,None],[None,None,None],[None,None,None]]

        # RMP - init
        self.s1.print_state()
        # end RMP

        # validate user choices and initialize the game!
        if self.p1_chose.get() != '' and self.p2_chose.get() != '':
            self.players = [self.p1_chose.get(), self.p2_chose.get()]
            if 'human' in self.players:
                self.canvas.bind("<ButtonPress-1>", self.human_clicked)
            print('Game start - ' + ' vs. '.join(self.players))
            self.cur_player = 0
            self.moves_total = 0
            self.move_next()
        else:
            print('Error: you must choose player types')


    def _board(self):
        '''Creates or clears the board and gridlines.'''
        self.canvas.create_rectangle(0,0,self.canvas_width,self.canvas_height, outline="black")
        # dividing lines can be simply two rectangles intersecting
        self.canvas.create_rectangle(self.canvas_width//3, self.canvas_height,
            2*self.canvas_width//3,0, outline="black")
        self.canvas.create_rectangle(0, self.canvas_height//3,
            self.canvas_width,2*self.canvas_height//3, outline="black")


    def draw_mark(self, row, column):
        '''Draw an X for player 0, an O for player 1'''
        y = row*self.canvas_width//3 + self.canvas_width//6
        x = column*self.canvas_height//3 + self.canvas_height//6
        if self.cur_player == 0:
            self.canvas.create_line( x+20, y+20, x-20, y-20, width=4, fill="black")
            self.canvas.create_line( x-20, y+20, x+20, y-20, width=4, fill="black")
        elif self.cur_player == 1:
            self.canvas.create_oval( x+25, y+25, x-25, y-25, width=4, outline="black")


    def human_clicked(self, event):
        '''A human clicked on the canvas - decide what happens next.'''

        if self.players[self.cur_player] != 'human':
        	print('Other player is still moving')
        	return

        where = self.where_clicked(event)
        if where is not None:
            self.move_human(where[0], where[1])


    def where_clicked(self, event):
        '''Find where on the logical grid (x, y) was clicked.'''
        w = self.canvas_width
        h = self.canvas_height

        for column, k in enumerate(range(0, w, w//3)):
            for row, j in enumerate(range(0, h, h//3)):
                #checks if the mouse input is in a bounding box
                if event.x in range(k,k+w//3) and event.y in range(j,j+h//3):
                    #checks if there is nothing in the bounding box
                    if self.canvas.find_enclosed(k, j, k+w//3, j+h//3) == ():
                        return row, column


    def proceed_next_player(self):
        '''Set cur_player to the next player.'''
        self.cur_player = (self.cur_player + 1) % 2

        #RMP
        self.whose_turn *= -1

        print self.whose_turn


    def game_is_over(self):
        '''Check if the game is over - whether it be a draw or win scenario.'''
        # check the 8 ways to win
        t = self.TTT
        # through center
        if t[1][1] is not None                        \
            and ((t[1][1] == t[0][0] == t[2][2]) or   \
                (t[1][1] == t[0][2] == t[2][0]) or    \
                (t[0][1] == t[1][1] == t[2][1]) or    \
                (t[1][0] == t[1][1] == t[1][2])):
                return self.game_over(t[1][1])
        # through top-left
        elif t[0][0] is not None                      \
            and ((t[0][0] == t[0][1] == t[0][2]) or   \
                (t[0][0] == t[1][0] == t[2][0])):
                return self.game_over(t[0][0])
        # through bottom-right
        elif t[2][2] is not None                      \
            and ((t[2][2] == t[2][1] == t[2][0]) or   \
                (t[2][2] == t[1][2] == t[0][2])):
                return self.game_over(t[2][2])
        # no winner and full board means draw
        if self.moves_total >= 9:
            return self.game_over(-1)
        return False


    def game_over(self, winner):
        '''The game is over - end the game and display the winner.'''
        if winner < 0:
            s = 'Draw between ' + ' and '.join(self.players)
        else:
            s = 'Game over - player ' + str(self.cur_player + 1) + " wins (" + self.players[self.cur_player] + ")"
        print(s)
        # print('Board end-configuration:')
        # print(self.TTT)
        self.label['text']=(s)
        self.canvas.unbind("<ButtonPress-1>")
        return True


    def move_next(self):
        '''Determine who has the next move, and move appropriately.'''
        s = 'Player ' + str(self.cur_player + 1) + "'s move (" + self.players[self.cur_player] + ")"
        self.label['text'] = (s)

        # draw now, not later
        self.canvas.update_idletasks()

        if self.players[self.cur_player] == 'human':
            return # wait for human GUI input
        elif self.players[self.cur_player] == 'random':
            self.move_random()
        elif self.players[self.cur_player] == 'minimax':
            self.move_minimax()

        self.moves_total += 1
        if self.game_is_over():
            return
        self.proceed_next_player()
        self.move_next()


    def move_human(self, r, c):
        '''The human chose the position r, c as their next move.'''
        if self.TTT[r][c] is not None:
            return # there is already a mark there
        else:
            # update logical board
            self.TTT[r][c] = self.cur_player
            # update GUI board
            self.draw_mark(r, c)

            self.current_node = move(self.current_node,(r,c),self.whose_turn)

            # end-move tasks
            print('Human chose ' + str((r, c)))
            self.moves_total += 1
            if self.game_is_over():
                return
            self.proceed_next_player()
            self.move_next()


    def move_random(self):
        self.current_node = move(self.current_node,'random',self.whose_turn)

        r = -1
        c = -1

        temp = [[0,0,0],[0,0,0],[0,0,0]]

        for i in xrange(3):
            for j in xrange(3):
                if self.current_node.data.data[i][j] == 1: temp[i][j] = 0
                if self.current_node.data.data[i][j] == -1: temp[i][j] = 1
                if self.current_node.data.data[i][j] == 0: temp[i][j] = None

        for i in xrange(3):
            for j in xrange(3):
                if temp[i][j] != self.TTT[i][j]:
                    r = i
                    c = j

        self.TTT[r][c] = self.cur_player
        self.draw_mark(r, c)
        print('Random chose ' + str((r, c)))
        return
        print('Random move errored')

    def move_minimax(self):

        self.current_node = move(self.current_node,'minimax',self.whose_turn)

        r = -1
        c = -1

        temp = [[0,0,0],[0,0,0],[0,0,0]]

        for i in xrange(3):
            for j in xrange(3):
                if self.current_node.data.data[i][j] == 1: temp[i][j] = 0
                if self.current_node.data.data[i][j] == -1: temp[i][j] = 1
                if self.current_node.data.data[i][j] == 0: temp[i][j] = None

        for i in xrange(3):
            for j in xrange(3):
                if temp[i][j] != self.TTT[i][j]:
                    r = i
                    c = j

        self.TTT[r][c] = self.cur_player
        self.draw_mark(r, c)
        print('Minimax chose ' + str((r, c)))
        return
        print('Minimax move errored')


def valid(args):
	p = ['human','random','minimax']
	return all((x in p for x in args))


if __name__ == "__main__":
    args = os.sys.argv[1:]
    if len(args) == 0:
        root=Tk()
        app=main(root)
        root.mainloop()
    elif len(args) == 2 and valid(args):
        root=Tk()
        app=main(root, args)
        root.mainloop()
    else:
        print("Usage: " + os.sys.argv[0] + " <player 1 type> <player 2 type>")
        print("       where player type = human, random, or minimax")
