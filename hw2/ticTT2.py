from Tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk
from random import randint

'''
GUI Tic Tac Toe game with complete AI code (commented and documented) version
By Daniel Tan
23/7/2013

This version contains the complete version of the AI.
The previous ticTT.py omitted the OFFENSE part of the game AI and thus is easier to win.
When designing the AI, I first created the double player to play with myself
And then recorded details of what I thought, what I did, at what conditions

My style is to use functions where code is repeated, if it is worth the effort.
This keeps the code clean and easy to maintain.
'''

class main:

    def __init__(self,master):
        #master frame
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)

        #canvas where the game is played on
        self.canvas = Canvas(self.frame, width=300, height=300)
        self.canvas.pack(fill="both", expand=True)

        #Shows status of game
        self.label=Label(self.frame, text='Tic Tac Toe Game', height=6, bg='black', fg='blue')
        self.label.pack(fill="both", expand=True)

        #frame to contain the buttons
        self.frameb=Frame(self.frame)
        self.frameb.pack(fill="both", expand=True)

        #Buttons to initiate the game
        self.Start1=Button(self.frameb, text='Click here to start\ndouble player', height=4, command=self.start1,bg='white', fg='purple')
        self.Start1.pack(fill="both", expand=True, side=RIGHT)
        self.Start2=Button(self.frameb, text='Click here to start\nsingle player', height=4, command=self.start2,bg='purple', fg='white')
        self.Start2.pack(fill="both", expand=True, side=LEFT)

        #canvas board drawing function call
        self._board()

    def start1(self):
        #Starts double player

        #refresh canvas
        self.canvas.delete(ALL)
        self.label['text']=('Tic Tac Toe Game')

        #function call on click
        self.canvas.bind("<ButtonPress-1>", self.sgplayer)
        self._board()

        #Starts the matrix to do calculations
        #of the positions of circles and crosses.
        self.TTT=[[0,0,0],[0,0,0],[0,0,0]]

        #counter of turns
        self.i=0

        #trigger to end game
        self.j=False

    def start2(self):
        #Starts single player
        self.canvas.delete(ALL)
        self.label['text']=('Tic Tac Toe Game')
        self.canvas.bind("<ButtonPress-1>", self.dgplayer)
        self._board()
        self.TTT=[[0,0,0],[0,0,0],[0,0,0]]
        self.i=0
        self.j=False
        #Trigger to check the validity of the move
        self.trigger=False

    def end(self):
        #Ends the game
        self.canvas.unbind("<ButtonPress-1>")
        self.j=True


    def _board(self):
        #Creates the board
        self.canvas.create_rectangle(0,0,300,300, outline="black")
        self.canvas.create_rectangle(100,300,200,0, outline="black")
        self.canvas.create_rectangle(0,100,300,200, outline="black")

    def sgplayer(self,event):
        #Double player game loop
        for k in range(0,300,100):
            for j in range(0,300,100):
                #checks if the mouse input is in a bounding box
                if event.x in range(k,k+100) and event.y in range(j,j+100):
                    #checks if there is nothing in the bounding box
                    if self.canvas.find_enclosed(k,j,k+100,j+100)==():
                        #Player plays first
                        if self.i%2==0:
                            #draws circle
                            #no need to create a new function since there is just two cases where this code is used
                            X=(2*k+100)/2
                            Y=(2*j+100)/2
                            X1=int(k/100)
                            Y1=int(j/100)
                            self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")
                            self.TTT[Y1][X1]+=1
                            self.i+=1
                        else:
                            #creates the cross.
                            #I don't use the self.cross function here because k and j are not compatible
                            X=(2*k+100)/2
                            Y=(2*j+100)/2
                            X1=int(k/100)
                            Y1=int(j/100)
                            self.canvas. create_line( X+20, Y+20, X-20, Y-20, width=4, fill="black")
                            self.canvas. create_line( X-20, Y+20, X+20, Y-20, width=4, fill="black")
                            self.TTT[Y1][X1]+=9
                            self.i+=1
        #After everything, remember to check for wins/losts/draws
        self.check()

    def dgplayer(self,event):
        for k in range(0,300,100):
            for j in range(0,300,100):
                if self.i%2==0:
                    if event.x in range(k,k+100) and event.y in range(j,j+100):
                        if self.canvas.find_enclosed(k,j,k+100,j+100)==():
                            X=(2*k+100)/2
                            Y=(2*j+100)/2
                            X1=int(k/100)
                            Y1=int(j/100)
                            self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")
                            self.TTT[Y1][X1]+=1
                            self.i+=1
                            self.check()
                            self.trigger=False
                else:
                    print(self.i)
                    #check for wins/losts/draws first
                    #before allowing the computer to make its turn
                    self.check()
                    #Game AI code
                    self.AIcheck()
                    #refresh validity of move
                    self.trigger=False





    def check(self):
        #horizontal check
        for i in range(0,3):
            if sum(self.TTT[i])==27:
                self.label['text']=('2nd player wins!')
                self.end()
            if sum(self.TTT[i])==3:
                self.label['text']=('1st player wins!')
                self.end()
        #vertical check
        #the matrix below transposes self.TTT so that it could use the sum function again
        #for vertical rows
        self.ttt=[[row[i] for row in self.TTT] for i in range(3)]
        for i in range(0,3):
            if sum(self.ttt[i])==27:
                self.label['text']=('2nd player wins!')
                self.end()
            if sum(self.ttt[i])==3:
                self.label['text']=('1st player wins!')
                self.end()
        #check for diagonal wins
        if self.TTT[1][1]==9:
            if self.TTT[0][0]==self.TTT[1][1] and self.TTT[2][2]==self.TTT[1][1] :
                self.label['text']=('2nd player wins!')
                self.end()
            if self.TTT[0][2]==self.TTT[1][1] and self.TTT[2][0]==self.TTT[1][1] :
                self.label['text']=('2nd player wins!')
                self.end()
        if self.TTT[1][1]==1:
            if self.TTT[0][0]==self.TTT[1][1] and self.TTT[2][2]==self.TTT[1][1] :
                self.label['text']=('1st player wins!')
                self.end()
            if self.TTT[0][2]==self.TTT[1][1] and self.TTT[2][0]==self.TTT[1][1] :
                self.label['text']=('1st player wins!')
                self.end()
        #check for draws
        if self.j==False:
            a=0
            for i in range(0,3):
                a+= sum(self.TTT[i])
            #As the player starts with a circle(value=1),
            #There will be a total of 5(1) and 4(9)=41
            if a==41:
                self.label['text']=("It's a pass!")
                self.end()


    '''Note for AI game programming:
    There are only three sides to AI actions: Offense, Defense, Neutral
    Offense is what the AI does to win
    In the TTT case, the computer will add another cross to two crosses in a row to win

    Defense is what the AI does to prevent the other guy from winning
    In this case, the computer will add another cross to two circles in a row to block

    Neutral is when it can't do neither.
    However, we can't really let it do nothing, so instead, we let it do a random move.
    '''

    def AIcheck(self):
        #Offense should come before defense so that the AI will try to win if possible
        #This is built on the self.check function
        self.ttt=[[row[i] for row in self.TTT] for i in range(3)]
        #OFFENSE
        #this is the vertical checklist
        for h in range(0,3):
            k=0
            j=0
            if sum(self.TTT[h])==18:
                while k <3:
                    if k==h:
                        while j <3:
                            if self.trigger==False:
                                if self.TTT[k][j]==0:
                                    self.cross(j,k)
                                    break
                            j+=1
                    k+=1
        #this is the horizontal checklist
        for h in range(0,3):
            k=0
            j=0
            if sum(self.ttt[h])==18:
                while k <3:
                    if k==h:
                        while j <3:
                            if self.trigger==False:
                                if self.ttt[k][j]==0:
                                    self.cross(k,j)
                                    break
                            j+=1
                    k+=1
        '''In this case, while I could have used a for loop,
        I preferred not to, since there are just four cases, and
        designing a for loop is not worth the effort.
        You can see that from the length of the code, it's just simple
        copy and paste.
        '''
        #this is the diagonal checklist
        if self.TTT[1][1]==9:
            if self.TTT[0][0]==9:
                if self.trigger==False:
                    if self.TTT[2][2]==0:
                        self.cross(2,2)
            if self.TTT[0][2]==9:
                if self.trigger==False:
                    if self.TTT[2][0]==0:
                        self.cross(0,2)
            if self.TTT[2][0]==9:
                if self.trigger==False:
                    if self.TTT[0][2]==0:
                        self.cross(2,0)
            if self.TTT[2][2]==9:
                if self.trigger==False:
                    if self.TTT[0][0]==0:
                        self.cross(0,0)
        #DEFENSE
        #this is the horizontal checklist
        for h in range(0,3):
            k=0
            j=0
            if sum(self.TTT[h])==2:
                while k <3:
                    if k==h:
                        while j <3:
                            if self.trigger==False:
                                if self.TTT[k][j]==0:
                                    self.cross(j,k)
                                    break
                            j+=1
                    k+=1
        #this is the vertical checklist
        for h in range(0,3):
            k=0
            j=0
            if sum(self.ttt[h])==2:
                while k <3:
                    if k==h:
                        while j <3:
                            if self.trigger==False:
                                if self.ttt[k][j]==0:
                                    self.cross(k,j)
                                    break
                            j+=1
                    k+=1
        #this is the diagonal checklist
        if self.TTT[1][1]==1:
            if self.TTT[0][0]==1:
                if self.trigger==False:
                    if self.TTT[2][2]==0:
                        self.cross(2,2)
            if self.TTT[0][2]==1:
                if self.trigger==False:
                    if self.TTT[2][0]==0:
                        self.cross(0,2)
            if self.TTT[2][0]==1:
                if self.trigger==False:
                    if self.TTT[0][2]==0:
                        self.cross(2,0)
            if self.TTT[2][2]==1:
                if self.trigger==False:
                    if self.TTT[0][0]==0:
                        self.cross(0,0)
        #NEUTRAL
        '''The crux of the game is in the center
        So, the computer should get the center when it gets the chance.
        Other than that, it will just do a random move if nothing else works.
        That's  why this code is at the bottom.
        '''
        if self.TTT[1][1]==0:
            if self.trigger==False:
                self.cross(1,1)
                self.trigger=True
        else:
            if self.trigger==False:
                self.randmove()

    def cross(self, k, j):
        # k is the x coords
        # j is the y coords
        X=(200*k+100)/2
        Y=(200*j+100)/2
        X1=int(k)
        Y1=int(j)
        self.canvas. create_line( X+20, Y+20, X-20, Y-20, width=4, fill="black")
        self.canvas. create_line( X-20, Y+20, X+20, Y-20, width=4, fill="black")
        self.TTT[Y1][X1]+=9
        self.check()
        self.i+=1
        self.trigger=True


    def randmove(self):
        # In case there's nothing for the computer to do
        while True:
            k=(randint(0,2))
            j=(randint(0,2))
            if self.TTT[j][k]==0:
                self.cross(k,j)
                break
            else:
                k=(randint(0,2))*100
                j=(randint(0,2))*100




#initiate the class
root=Tk()
app=main(root)
root.mainloop()
