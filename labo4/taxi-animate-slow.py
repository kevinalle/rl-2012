from Tkinter import *
from random import *
import time
# http://www.pythonware.com/media/data/an-introduction-to-tkinter.pdf

# video game version of taxi problem

print sys.argv[1]

master = Tk()

Width = 100
(x,y) = (5,5)

board = Canvas(master, width=x*Width, height=y*Width)
#Taxi = (randint(0,4), randint(0,4))
Taxi = (2,2)

Special = [(0,4,"yellow"), (0,0,"red"), (3,4,"blue"), (4,0,"green")]
#passIn = randint(0,3)
#passTo = randint(0,3)
passIn=1
passTo=3

while passTo == passIn:
  passTo = randint(0,3)
Walls = [(2,0),(2,1),(1,3),(3,3),(1,4),(3,4)]

def rendergrid():
  global Special, Walls, Width, x, y, me
  for i in range(x):
    for j in range(y):
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white",width=1)
  for (i,j,c) in Special:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c,width=1)
  # board.create_rectangle(0*Width, 0*Width, (x+1)*Width, (y+1)*Width, width=10)
  for (i,j) in Walls:
        board.create_line(i*Width, j*Width, (i)*Width, (j+1)*Width, width=10)

rendergrid()

def tryMove(dx,dy):
  global Taxi, me, x, y, it, passIn
  global totalsteps
  totalsteps = totalsteps + 1
  newX = Taxi[0] + dx
  newY = Taxi[1] + dy
  if (newX >= 0) and (newX < x) and (newY >= 0) and (newY < y) and (not bump(Taxi,dx)):
    board.coords(me, (newX)*Width+Width*2/10, (newY)*Width+Width*2/10, 
	(newX)*Width+Width*8/10, (newY)*Width+Width*8/10)
    Taxi = (newX,newY)
    if passIn == 4:
      board.coords(it, newX*Width+Width*4/10, newY*Width+Width*4/10,
	newX*Width+Width*6/10, newY*Width+Width*6/10)

def callUp(event):
        tryUp()
        
def tryUp():
  tryMove(0,-1)

def callDown(event):
        tryDown()

def tryDown():
	tryMove(0,1)

def callLeft(event):
        tryLeft()
        
def tryLeft():
	tryMove(-1,0)

def callRight(event):
        tryRight()

def tryRight():
	tryMove(1,0)

def callPickup(event):
        tryPickup()
        
def tryPickup():
  global passIn, passTo, Taxi, Special, totalsteps, it
  totalsteps = totalsteps + 1
  if passIn == 4: return
  (i,j,c) = Special[passIn]
  if (i,j) != Taxi: return
  passIn = 4
  board.coords(it, i*Width+Width*4/10, j*Width+Width*4/10,
	i*Width+Width*6/10, j*Width+Width*6/10)

def callPutdown(event):
        tryPutdown()

def tryPutdown():
  global passIn, passTo, Taxi, Special, totalsteps, it
  totalsteps = totalsteps + 1
  if passIn != 4: return
  (i,j,c) = Special[passTo]
  if i == Taxi[0] and j == Taxi[1]:
    passIn = passTo
    board.coords(it, i*Width+Width*3/10, j*Width+Width*3/10,
          i*Width+Width*7/10, j*Width+Width*7/10)
    if passIn == passTo:
      print "Success!  Total steps:", totalsteps
      master.quit()

def tryPutdownAnyLoc():
  global passIn, passTo, Taxi, Special, totalsteps, it
  totalsteps = totalsteps + 1
  if passIn != 4: return
  for index in range(len(Special)):
    (i,j,c) = Special[index]
    if i == Taxi[0] and j == Taxi[1]:
       passIn = index
       board.coords(it, i*Width+Width*3/10, j*Width+Width*3/10,
		i*Width+Width*7/10, j*Width+Width*7/10)
       if passIn == passTo:
         print "Success!  Total steps:", totalsteps
         master.quit()

def bump(Taxi,dx):
  global Walls
  for (i,j) in Walls:
    if (j == Taxi[1]) and (dx == -1) and (Taxi[0] == i):
      return True
    if (j == Taxi[1]) and (dx == 1) and (Taxi[0] == i-1):
      return True
  return False

master.bind("<Up>", callUp)
master.bind("<Down>", callDown)
master.bind("<Right>", callRight)
master.bind("<Left>", callLeft)
master.bind("a", callPickup)
master.bind("b", callPutdown)

totalsteps = 0

me = board.create_rectangle(Taxi[0]*Width+Width*2/10, Taxi[1]*Width+Width*2/10,
	Taxi[0]*Width+Width*8/10, Taxi[1]*Width+Width*8/10, fill="orange",width=1,tag="me")
(i,j,dest) = Special[passTo]
(i,j,c) = Special[passIn]
it = board.create_oval(i*Width+Width*3/10, j*Width+Width*3/10,
	i*Width+Width*7/10, j*Width+Width*7/10, fill=dest,width=1,tag="it")

board.grid(row=0,column=0)

f=open(sys.argv[1])
actseq=f.read()
for i in range(len(actseq)):
    action=actseq[i]
    if(action=='0'):
      tryUp()
    elif(action=='1'):
      tryDown()
    elif(action=='2'):
      tryLeft()
    elif(action=='3'):
      tryRight()
    elif(action=='4'):
      tryPickup()
    elif(action=='5'):
      tryPutdown()
    time.sleep(.5)
    master.update()
    
#master.mainloop()
