from Tkinter import *
import sys
import numpy as np

import time
import random
import subprocess
class Game:
    def __init__(self, game_frame, w, h, eng1, eng2):
        self.game_frame = game_frame
        self.pitch = self.game_frame.pitch_frame
        path = list(sys.path)
        sys.path.insert(0, 'engine')
        self.eng1 = __import__(eng1)
        self.eng2 = __import__(eng2)
        self.turn = 1
        self.w = w
        self.h = h
        #self.knots = [[0 for x in xrange(pitch.w+1)] for y in xrange(pitch.h+1)]
        self.knots = np.array([0 for x in xrange(self.w+1)], dtype=object)
        adj = np.array([0 for x in xrange(self.w+1)], dtype=object)
        for i in xrange(self.h):
            self.knots = np.vstack((self.knots,adj))#create the matrix
        #legal moves array
        middleMoves = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        
        for i in xrange(self.w-1):
            for j in xrange(self.h-1):
                self.knots[j+1][i+1] = middleMoves
            self.knots[0][i+1] = [m for m in middleMoves if m[0] == 1]
            self.knots[self.h][i+1] = [m for m in middleMoves if m[0] == -1]
        for j in xrange(self.h-1):
            self.knots[j+1][0] = [m for m in middleMoves if m[1] == 1]
            self.knots[j+1][self.w] = [m for m in middleMoves if m[1] == -1]
        #self.knots[1][1] = [m for m in middleMoves if m != (-1,-1)]
        #self.knots[1][-2] = [m for m in middleMoves if m != (-1,1)]
        #self.knots[-2][1] = [m for m in middleMoves if m != (1,-1)]
        #self.knots[-2][-2] = [m for m in middleMoves if m != (1,1)]
        #print self.knots
        self.ball_pos = [0,0]

        #self.play()


    def updateLegal(self):
        pass
    
    
        
    def moveBall(self,a,b,col):
        #a,b are the moving directions
        self.ball_pos[0] += a
        self.ball_pos[1] += b

        self.pitch.draw_ball(self.ball_pos)

    def play(self):
        while True:
            print self.ball_pos, self.knots[self.ball_pos[0]][self.ball_pos[1]]
            raw_input()
            if self.turn == 1:
                a,b = self.eng1.move(self.ball_pos, self.knots)
                col = 'red'
                
            elif self.turn == -1:
                a,b = self.eng2.move(self.ball_pos, self.knots)
                col = 'blue'
            self.knots[self.ball_pos[0]][self.ball_pos[1]] = [m for m in self.knots[self.ball_pos[0]][self.ball_pos[1]] if m != (a,b)]
            self.moveBall(a,b,col)    
            if self.ball_pos == [int(pitch.w/2)-1,0] or self.ball_pos ==  [int(pitch.w/2)+1,0]:
                Label(self.master,text = 'player2 won').pack(side=TOP) 
                break
            elif self.ball_pos == [int(pitch.w/2)-1,pitch.h] or self.ball_pos == [int(pitch.w/2)+1,pitch.h]:
                Label(self.master,text = 'player1 won').pack(side=TOP)
                break
            if len(self.knots[self.ball_pos[0]][self.ball_pos[1]])==8: #does not work for the precorners
                self.turn *= -1
            if len(self.knots[self.ball_pos[0]][self.ball_pos[1]])==0: #does not work for the precorners
                Label(self.master,text = 'Draw').pack(side=TOP)
                break
            self.knots[self.ball_pos[0]][self.ball_pos[1]] = [m for m in self.knots[self.ball_pos[0]][self.ball_pos[1]] if m != (-a,-b)]
            
            self.field.update()
            
class GameFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.load_frame = LoadFrame(self)
        self.load_frame.pack()
        self.pack()
    
        
    def start(self, w, h, eng1, eng2):
    	self.load_frame.pack_forget()
        self.pitch_frame = PitchFrame(self, w, h)
        self.pitch_frame.pack()
        print "{} vs {}".format(eng1, eng2)
        self.game = Game(self, w, h, eng1, eng2)
        

class PitchFrame(Frame):
    """docstring for PitchFrame"""
    def __init__(self, master, w, h):
        Frame.__init__(self, master)
        self.master = master
        self.R = 50
        self.offset = 10
        self.outer = 50
        self.in_radius = 7
        self.out_radius = 9
        self.w = w
        self.h = h
        
        self.field = Canvas(self, width = 2 * self.offset + self.w * self.R, height =  2 * (self.outer + self.offset) + self.h * self.R)
        self.field.create_rectangle(self.offset, self.offset + self.outer, self.w  * self.R + self.offset, self.h  * self.R + self.offset + self.outer, fill='azure')
        self.field.create_rectangle(self.offset + (int(self.w/2)-1)*self.R, self.offset, self.offset + (int(self.w/2)+1)*self.R, self.outer + self.offset, fill='cornflower blue')
        self.field.create_rectangle(self.offset + (int(self.w/2)-1)*self.R, self.h  * self.R + self.offset + self.outer, self.offset+(int(self.w/2)+1)*self.R, self.outer + self.h * self.R + self.outer + self.offset, fill='cornflower blue')
        
        for i in xrange(self.w-1):
            self.field.create_line(self.offset + self.outer + self.R*i, self.offset + self.outer, self.offset + self.outer + self.R*i, self.h * self.R + self.offset + self.outer, fill='purple')
        for i in xrange(self.h-1):
            self.field.create_line(self.offset, self.offset + self.outer + self.outer+ self.R * i, self.w * self.R + self.offset, self.offset + self.outer + self.outer+ self.R *i, fill='purple')

        self.draw_ball((int(self.w/2.), int(self.h/2.)))
        self.field.pack()

    def draw_ball(self, pos):        
        x = self.offset + pos[0]*self.R
        y = self.offset + (pos[1]+1)*self.R
        
        self.field.create_oval(x - self.out_radius, y - self.out_radius, x + self.out_radius, y + self.out_radius, width=0,fill='black')
        self.field.create_oval(x - self.in_radius, y - self.in_radius, x + self.in_radius, y + self.in_radius, width=0,fill='white')
        
    def draw_move(self, pos):
        self.field.create_line(self.offset + pos[0]*self.R, self.offset +(pos[1]+1)*self.R, 10+(pos[0]+a)*self.R, self.offset+(pos[1]+1+b)*self.R, fill=col,width=2)
        
class LoadFrame(Frame):
    """docstring for LoadFrame"""
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.width_entry = Entry(self)
        self.height_entry = Entry(self)
        self.width_entry.pack(side=LEFT)
        self.height_entry.pack(side=LEFT)
        self.load_entry = Listbox(self,selectmode=MULTIPLE)
        self.load_entry.pack(side=RIGHT)
        self.output = subprocess.check_output('ls engine/', shell=True)
        for i in xrange(len(self.output.split())):
            if self.output.split()[i].split('.')[1] == 'py': #only py files
                self.load_entry.insert(END,self.output.split()[i])
        
        self.createButton = Button(self,text='start',command=self.start)        
        self.createButton.pack()

    def start(self):
        index = self.load_entry.curselection() #index of the choosen engines
        if len(index)==2:
            try:
                w = int(self.width_entry.get())
            except ValueError:
                w = 6
            try:
                h = int(self.height_entry.get())
            except ValueError:
                h = 8
            eng1 = self.load_entry.get(int(index[0])).split('.')[0]#take module name
            eng2 = self.load_entry.get(int(index[1])).split('.')[0]
            
            self.master.start(w, h, eng1, eng2)
            
        #else:
        #    Label(self,text='Choose two engines').pack(side=BOTTOM)    


def main():
    root = Tk()
    game_frame = GameFrame(root)

    root.mainloop()

if __name__ == '__main__':
    main()

