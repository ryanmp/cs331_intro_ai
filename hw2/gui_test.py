from Tkinter import *

def callback(number):
    print "button", number

for i in xrange(9):
  Button(padx=2, pady=2, width=2, height=2, text="x", command=lambda x=i: callback(x)).pack()

mainloop()
