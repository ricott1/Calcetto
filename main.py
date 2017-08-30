from Tkinter import *
import sys
import numpy as np

import time
import random
import subprocess
class Game:
	def __init__(self,master, eng1, eng2):
		self.master = master
		self.eng1 = eng1
		self.eng2 = eng2
		self.width = pitch.w*50
		self.height = pitch.h*50
		self.field = Canvas(self.master,width=self.width+20,height=self.height+20 + 100)
		self.field.create_rectangle(10, 60, self.width + 10, self.height + 60, fill='azure')
		self.field.create_rectangle(10 + (int(pitch.w/2)-1)*50, 10, 10+(int(pitch.w/2)+1)*50, 60, fill='cornflower blue')
		self.field.create_rectangle(10 + (int(pitch.w/2)-1)*50, self.height + 60, 10+(int(pitch.w/2)+1)*50, self.height + 110, fill='cornflower blue')
		for i in xrange(pitch.w-1):
			self.field.create_line(10+50+50*i, 60, 10+50+50*i, self.height + 60, fill='purple')
		for i in xrange(pitch.h-1):
			self.field.create_line(10, 10+100+50*i, self.width + 10, 10+100+50*i, fill='purple')
		self.ballPos = [int(pitch.w/2), int(pitch.h/2)]
		print self.ballPos
		self.inBall = self.drawBall()
		self.outBall = self.drawBall(rad=7,col='white')

		self.field.pack(side=BOTTOM)
		self.turn = 1
		
		#self.knots = [[0 for x in xrange(pitch.w+1)] for y in xrange(pitch.h+1)]
		self.knots = np.array([0 for x in xrange(pitch.w+1)], dtype=object)
		adj = np.array([0 for x in xrange(pitch.w+1)], dtype=object)
		for i in xrange(pitch.h):
			self.knots = np.vstack((self.knots,adj))#create the matrix
		#legal moves array
		middleMoves = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
		
		for i in xrange(pitch.w-1):
			for j in xrange(pitch.h-1):
				self.knots[j+1][i+1] = middleMoves
			self.knots[0][i+1] = [m for m in middleMoves if m[0] == 1]
			self.knots[pitch.h][i+1] = [m for m in middleMoves if m[0] == -1]
		for j in xrange(pitch.h-1):
			self.knots[j+1][0] = [m for m in middleMoves if m[1] == 1]
			self.knots[j+1][pitch.w] = [m for m in middleMoves if m[1] == -1]
		#self.knots[1][1] = [m for m in middleMoves if m != (-1,-1)]
		#self.knots[1][-2] = [m for m in middleMoves if m != (-1,1)]
		#self.knots[-2][1] = [m for m in middleMoves if m != (1,-1)]
		#self.knots[-2][-2] = [m for m in middleMoves if m != (1,1)]
		#print self.knots
		
		self.play()
	def updateLegal(self):
		pass
	
	
	def drawBall(self,rad = 9, col = 'black'):
		return self.field.create_oval(10+self.ballPos[0]*50-rad,10+(self.ballPos[1]+1)*50-rad,10+self.ballPos[0]*50+rad,10+(self.ballPos[1]+1)*50+rad,width=0,fill=col)
		
	def moveBall(self,a,b,col):
		#a,b are the moving directions
		self.field.create_line(10+self.ballPos[0]*50, 10 +(self.ballPos[1]+1)*50, 10+(self.ballPos[0]+a)*50, 10+(self.ballPos[1]+1+b)*50, fill=col,width=2)
		self.field.move(self.inBall,(a)*50,(b)*50)
		self.field.move(self.outBall,(a)*50,(b)*50)
		self.ballPos[0] += a
		self.ballPos[1] += b
	def play(self):
		while True:
			raw_input()
			if self.turn == 1:
				a,b = self.eng1.move(self.ballPos, self.knots)
				col = 'red'
				
			elif self.turn == -1:
				a,b = self.eng2.move(self.ballPos, self.knots)
				col = 'blue'
			self.knots[self.ballPos[0]][self.ballPos[1]] = [m for m in self.knots[self.ballPos[0]][self.ballPos[1]] if m != (a,b)]
			self.moveBall(a,b,col)	
			if self.ballPos == [int(pitch.w/2)-1,0] or self.ballPos ==  [int(pitch.w/2)+1,0]:
				Label(self.master,text = 'player2 won').pack(side=TOP) 
				break
			elif self.ballPos == [int(pitch.w/2)-1,pitch.h] or self.ballPos == [int(pitch.w/2)+1,pitch.h]:
				Label(self.master,text = 'player1 won').pack(side=TOP)
				break
			if len(self.knots[self.ballPos[0]][self.ballPos[1]])==8: #does not work for the precorners
				self.turn *= -1
			if len(self.knots[self.ballPos[0]][self.ballPos[1]])==0: #does not work for the precorners
				Label(self.master,text = 'Draw').pack(side=TOP)
				break
			self.knots[self.ballPos[0]][self.ballPos[1]] = [m for m in self.knots[self.ballPos[0]][self.ballPos[1]] if m != (-a,-b)]
			
			self.field.update()
			
class Pitch(Frame):
	def __init__(self,master):
		Frame.__init__(self,master)
		self.master = master
		self.widthEntry = Entry(self)
		self.heightEntry = Entry(self)
		self.widthEntry.pack(side=LEFT)
		self.heightEntry.pack(side=LEFT)
		self.load_entry = Listbox(self,selectmode=MULTIPLE)
		self.load_entry.pack(side=RIGHT)
		self.output = subprocess.check_output('ls engine/', shell=True)
		for i in xrange(len(self.output.split())):
			if self.output.split()[i].split('.')[1] == 'py': #only py files
				self.load_entry.insert(END,self.output.split()[i])
		
		self.createButton = Button(self,text='create',command=self.create)		
		self.createButton.pack()
		
		self.pack()
	def create(self):
		try:
			self.w = int(self.widthEntry.get())
		except ValueError:
			self.w = 6
		try:
			self.h = int(self.heightEntry.get())
		except ValueError:
			self.h = 8
		
		self.loadEngine()
		
	def create_field(self):
		self.field = Canvas(self.master,width=self.width+20,height=self.height+20 + 100)
		self.field.create_rectangle(10, 60, self.width + 10, self.height + 60, fill='azure')
		self.field.create_rectangle(10 + (int(pitch.w/2)-1)*50, 10, 10+(int(pitch.w/2)+1)*50, 60, fill='cornflower blue')
		self.field.create_rectangle(10 + (int(pitch.w/2)-1)*50, self.height + 60, 10+(int(pitch.w/2)+1)*50, self.height + 110, fill='cornflower blue')
		for i in xrange(pitch.w-1):
			self.field.create_line(10+50+50*i, 60, 10+50+50*i, self.height + 60, fill='purple')
		for i in xrange(pitch.h-1):
			self.field.create_line(10, 10+100+50*i, self.width + 10, 10+100+50*i, fill='purple')
		self.ballPos = [int(pitch.w/2), int(pitch.h/2)]
		print self.ballPos
		self.inBall = self.drawBall()
		self.outBall = self.drawBall(rad=7,col='white')
	def loadEngine(self):
		index = self.load_entry.curselection() #index of the choosen engines
		if len(self.load_entry.curselection())==2:
   			loading1 = self.load_entry.get(int(index[0])).split('.')[0]#take module name
   			loading2 = self.load_entry.get(int(index[1])).split('.')[0]
   			print loading1, loading2
   			path = list(sys.path)
    			sys.path.insert(0, 'engine')
			eng1 = __import__(loading1)
			eng2 = __import__(loading2)
			self.pack_forget()
			game = Game(self.master, eng1, eng2)
		else:
			Label(self,text='Choose two engines, asshole').pack(side=BOTTOM)
		
def main():
	root = Tk()
	pitch = Pitch(root)

	root.mainloop()

if __name__ == '__main__':
	main()
