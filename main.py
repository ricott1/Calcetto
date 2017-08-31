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
        self.engines = [__import__(eng1), __import__(eng2)]
        self.colors = ['red', 'blue']
        self.w = w
        self.h = h

        self.initialize()

    def initialize(self):
        self.knots = np.array([[0 for y in xrange(self.h+1)] for x in xrange(self.w+1)], dtype=object) 
        moves = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        
        for x in xrange(len(self.knots)):
            for y in xrange(len(self.knots[0])):
            	my_moves = list(moves)
                if x == 0:
                    my_moves = [m for m in my_moves if m[0] == 1]
                if x == self.w:
                    my_moves = [m for m in my_moves if m[0] == -1]
                if y == 0:
                    my_moves = [m for m in my_moves if m[1] == 1]
                if y == self.h:
                    my_moves = [m for m in my_moves if m[1] == -1]
                #take out corners
                if x == 1 and y == 1:
                    my_moves = [m for m in my_moves if m != (-1, -1)]
                if x == 1 and y == self.h - 1:
                    my_moves = [m for m in my_moves if m != (-1, 1)]
                if x == self.w - 1 and y == 1:
                    my_moves = [m for m in my_moves if m != (1, -1)]
                if x == self.w - 1 and y == self.h - 1:
                    my_moves = [m for m in my_moves if m != (1, 1)]
                self.knots[x][y] = my_moves
       
    def update_moves(self, pos, a, b):
        self.knots[pos[0]][pos[1]] = [m for m in self.knots[pos[0]][pos[1]] if m != (a,b)]
        self.knots[pos[0] + a][pos[1] + b] = [m for m in self.knots[pos[0] + a][pos[1] + b] if m != (-a,-b)]    
        
    def move_ball(self, pos, a, b, col):
        #a,b are the moves in x-y direction
        self.pitch.draw_move(pos, a, b, col)
        new_pos = [pos[0] + a, pos[1] + b]        
        self.pitch.draw_ball(new_pos)
        return new_pos

    def play(self):
    	pos = [int(self.w/2.),int(self.h/2.)]
    	turn = 0
    	visited = [list(pos)]
    	self.pitch.reset_button['state'] = 'disabled'      
    	self.pitch.draw_ball(pos) 
        while True:
            print self.engines[turn], turn
            raw_input()
            a,b = self.engines[turn].move(pos, self.knots, turn)
            
            self.update_moves(pos, a, b)
            pos = self.move_ball(pos, a,b, self.colors[turn]) 
               
            winner = self.check_winner(pos)
            if winner:
            	break
            else:
                if pos not in visited: 
                	visited.append(list(pos))
                	if pos[0] not in (0, self.w) and pos[1] not in (0, self.h):
                		turn = (turn+1)%2

                if len(self.knots[pos[0]][pos[1]]) == 0: 
                    print 'Draw'
                    break
        self.pitch.reset_button['state'] = 'normal'       
               
    def check_winner(self, pos):
        if pos == [int(self.w/2)-1,0] or pos ==  [int(self.w/2)+1,0]:
            print 'player2 won'
            return True
        elif pos == [int(self.w/2)-1,self.h] or pos == [int(self.w/2)+1,self.h]:
            print 'player1 won'
            return True
        return False

    def reset(self):
    	self.initialize()
        self.play()

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
        self.pitch_frame.add_names(eng1, eng2)
        self.game = Game(self, w, h, eng1, eng2)
        self.game.play()

    def reset(self):
    	self.game.reset()
        

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
        self.moves = []
        self.reset_button = Button(self,text='Reset',command=self.reset, state=DISABLED)        
        self.reset_button.pack(side=TOP)
        self.name_frame = Frame(self)
        self.name_frame.pack(side=BOTTOM)
        self.name1_label = Label(self.name_frame, text="", bg = 'red', fg = 'black')
        self.name1_label.pack(side=LEFT)
        Label(self.name_frame, text = '  vs  ').pack(side=LEFT)
        self.name2_label = Label(self.name_frame, text="", bg = 'blue', fg = 'white')
        self.name2_label.pack(side=LEFT)
        self.field = Canvas(self, width = 2 * self.offset + self.w * self.R, height =  2 * (self.outer + self.offset) + self.h * self.R)
        self.field.create_rectangle(self.offset, self.offset + self.outer, self.w  * self.R + self.offset, self.h  * self.R + self.offset + self.outer, fill='azure')
        self.field.create_rectangle(self.offset + (int(self.w/2)-1)*self.R, self.offset, self.offset + (int(self.w/2)+1)*self.R, self.outer + self.offset, fill='cornflower blue')
        self.field.create_rectangle(self.offset + (int(self.w/2)-1)*self.R, self.h  * self.R + self.offset + self.outer, self.offset+(int(self.w/2)+1)*self.R, self.outer + self.h * self.R + self.outer + self.offset, fill='cornflower blue')
        
        for i in xrange(self.w-1):
            self.field.create_line(self.offset + self.outer + self.R*i, self.offset + self.outer, self.offset + self.outer + self.R*i, self.h * self.R + self.offset + self.outer, fill='purple')
        for i in xrange(self.h-1):
            self.field.create_line(self.offset, self.offset + self.outer + self.outer+ self.R * i, self.w * self.R + self.offset, self.offset + self.outer + self.outer+ self.R *i, fill='purple')
        self.field.pack()

    def draw_ball(self, pos):        
        x = self.offset + pos[0]*self.R
        y = self.offset + (pos[1]+1)*self.R
        try:
            self.field.delete(self.in_ball)
            self.field.delete(self.out_ball)
        except:
            pass
        self.out_ball = self.field.create_oval(x - self.out_radius, y - self.out_radius, x + self.out_radius, y + self.out_radius, width=0,fill='black')
        self.in_ball = self.field.create_oval(x - self.in_radius, y - self.in_radius, x + self.in_radius, y + self.in_radius, width=0,fill='white')
        
    def draw_move(self, pos, a, b, col):
        self.moves.append(self.field.create_line(self.offset + pos[0]*self.R, self.offset +(pos[1]+1)*self.R, self.offset+(pos[0]+a)*self.R, self.offset+(pos[1]+1+b)*self.R, fill=col,width=2))
    
    def reset(self):
    	for m in self.moves:
    		self.field.delete(m)
    	self.master.reset()

    def add_names(self, name1, name2):
    	self.name1_label['text'] = name1
    	self.name2_label['text'] = name2

class LoadFrame(Frame):
    """docstring for LoadFrame"""
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        Label(self, text="width").pack(side=LEFT)
        self.width_entry = Entry(self, width = 4)
        self.width_entry.pack(side=LEFT)
        Label(self, text="Height").pack(side=LEFT)
        self.height_entry = Entry(self, width = 4)        
        self.height_entry.pack(side=LEFT)
        self.load_entry = Listbox(self,selectmode=MULTIPLE)
        self.load_entry.pack(side=RIGHT)
        self.output = subprocess.check_output('ls engine/', shell=True)
        for i in xrange(len(self.output.split())):
            if self.output.split()[i].split('.')[1] == 'py': #only py files
                self.load_entry.insert(END,self.output.split()[i])
        
        self.start_button = Button(self,text='start',command=self.start, width=20, height = 8)        
        self.start_button.pack(side=BOTTOM)

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

