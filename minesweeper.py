# Python Version 2.7.3
# File: minesweeper.py

from tkinter import * 
from tkinter import messagebox as tkMessageBox
import random
from collections import deque
import time
from threading import Thread

class Minesweeper():

    def __init__(self, master):

        self.master = master
         #Frame.__init__(self)
        # import images
        self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
        self.tile_mine = PhotoImage(file = "images/tile_mine.gif")
        self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
        self.tile_no = []
        for x in range(1, 9):
            self.tile_no.append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

        # set up frame
        frame = Frame(master)
        frame.pack()

        # show "Minesweeper" at the top
        """self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = 10)
        tkMessageBox.showinfo("Hello!","You have 1 minute to finish this game")
        self.time = time.strftime("%H:%M:%S")
        print(self.time)"""
        
        # create flag and clicked tile variables
        self.flags = 0
        self.correct_flags = 0
        self.clicked = 0

        self.state = 'none'
        self.num = 0
             
        
        # create buttons
        self.buttons = dict({})
        self.mines = 0
        x_coord = 1
        y_coord = 0
        for x in range(0, 100):
            mine = 0
            # tile image changeable for debug reasons:
            gfx = self.tile_plain
            # currently random amount of mines
            if random.uniform(0.0, 1.0) < 0.1:
                mine = 1
                self.mines += 1
            # 0 = Button widget
            # 1 = if a mine y/n (1/0)
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
            # 3 = button id
            # 4 = [x, y] coordinates in the grid
            # 5 = nearby mines, 0 by default, calculated after placement in grid
            self.buttons[x] = [ Button(frame, image = gfx),
                                mine,
                                0,
                                x,
                                [x_coord, y_coord],
                                0 ]
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))

            # calculate coords:
            y_coord += 1
            if y_coord == 10:
                y_coord = 0
                x_coord += 1

        
        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key][0].grid( row = self.buttons[key][4][0], column = self.buttons[key][4][1] )

        # find nearby mines and display number on tile
        for key in self.buttons:
            nearby_mines = 0
            if self.check_for_mines(key-9):
                nearby_mines += 1
            if self.check_for_mines(key-10):
                nearby_mines += 1
            if self.check_for_mines(key-11):
                nearby_mines += 1
            if self.check_for_mines(key-1):
                nearby_mines += 1
            if self.check_for_mines(key+1):
                nearby_mines += 1
            if self.check_for_mines(key+9):
                nearby_mines += 1
            if self.check_for_mines(key+10):
                nearby_mines += 1
            if self.check_for_mines(key+11):
                nearby_mines += 1
            # store mine count in button data list
            self.buttons[key][5] = nearby_mines
            #if self.buttons[key][1] != 1:
            #    if nearby_mines != 0:
            #        self.buttons[key][0].config(image = self.tile_no[nearby_mines-1])

        #add mine and count at the end
        self.label2 = Label(frame, text = "Mines: "+str(self.mines))
        self.label2.grid(row = 11, column = 0, columnspan = 5)

        self.label3 = Label(frame, text = "Flags: "+str(self.flags))
        self.label3.grid(row = 11, column = 4, columnspan = 5)


        #self.label2 = Label(frame, text = "Timer: "+str(self.mines))
        self.label2 = Label(frame)
        self.label2.grid(row = 12, column = 2, columnspan = 5)

        
        self.countdown(120)
        
    
    ## End of __init__
        
    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining
    
        if self.remaining <= 0:
            self.label2.configure(text="time's up!")
            self.gameover()
        #elif self.clicked != 100 - self.mines:
        elif self.state =='won':
            self.label2.configure(text="Timer: %d" % self.remaining)
        elif self.state == 'lost':
            self.label2.configure(text="Timer: %d" % self.remaining)        
        else:
            self.label2.configure(text="Timer: %d" % self.remaining)
            self.remaining = self.remaining - 1
            self.master.after(1000, self.countdown)
            
            
            
    def check_for_mines(self, key):
        try:
            if self.buttons[key][1] == 1:
                return True
        except KeyError:
            pass

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(self.buttons[x])

    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(self.buttons[x])

    def lclicked(self, button_data):
        if button_data[1] == 1: #if a mine
            # show all mines and check for flags
            for key in self.buttons:
                if self.buttons[key][1] != 1 and self.buttons[key][2] == 2:
                    self.buttons[key][0].config(image = self.tile_wrong)
                if self.buttons[key][1] == 1 and self.buttons[key][2] != 2:
                    self.buttons[key][0].config(image = self.tile_mine)
            # end game
            self.gameover()
        else:
            #change image
            if button_data[5] == 0:
                button_data[0].config(image = self.tile_clicked)
                self.clear_empty_tiles(button_data[3])
            else:
                button_data[0].config(image = self.tile_no[button_data[5]-1])
            # if not already set as clicked, change state and count
            if button_data[2] != 1:
                button_data[2] = 1
                self.clicked += 1
            if self.clicked == 100 - self.mines:
                self.victory()

    def rclicked(self, button_data):
        # if not clicked
        if button_data[2] == 0:
            button_data[0].config(image = self.tile_flag)
            button_data[2] = 2
            button_data[0].unbind('<Button-1>')
            # if a mine
            if button_data[1] == 1:
                self.correct_flags += 1
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif button_data[2] == 2:
            button_data[0].config(image = self.tile_plain)
            button_data[2] = 0
            button_data[0].bind('<Button-1>', self.lclicked_wrapper(button_data[3]))
            # if a mine
            if button_data[1] == 1:
                self.correct_flags -= 1
            self.flags -= 1
            self.update_flags()

    def check_tile(self, key, queue):
        try:
            if self.buttons[key][2] == 0:
                if self.buttons[key][5] == 0:
                    self.buttons[key][0].config(image = self.tile_clicked)
                    queue.append(key)
                else:
                    self.buttons[key][0].config(image = self.tile_no[self.buttons[key][5]-1])
                self.buttons[key][2] = 1
                self.clicked += 1
        except KeyError:
            pass

    def clear_empty_tiles(self, main_key):
        queue = deque([main_key])

        while len(queue) != 0:
            key = queue.popleft()
            self.check_tile(key-9, queue)      #top right
            self.check_tile(key-10, queue)     #top middle
            self.check_tile(key-11, queue)     #top left
            self.check_tile(key-1, queue)      #left
            self.check_tile(key+1, queue)      #right
            self.check_tile(key+9, queue)      #bottom right
            self.check_tile(key+10, queue)     #bottom middle
            self.check_tile(key+11, queue)     #bottom left
    
    def gameover(self):
        self.state = 'lost'
        top = Toplevel()
        top.title("You lose! ")
        #top.grab_set()
        top.geometry("%dx%d%+d%+d" % (400, 450, 250, 125))
        self.bg_image = PhotoImage(file ="images/source.gif", format="gif -index 2").subsample(3)
        x = Label (top, image = self.bg_image)
        x.pack({"side": "top"})
           
        
        y = Label (top, image = "")

        button = Button(y, text="Quit", command=self.destroyall).grid(row=0, column=0)
        #button.pack()

        button = Button(y, text="Play Again", command=playagain).grid(row=0, column=1)
        #button.pack()
        y.pack({"side": "top"})
        #w.pack()
        
        #commented below code for experimenting wt icon in msgbox
        #once figured it needs to be uncommented
        #end of it
            
    def victory(self):
        self.state = 'win'
        top = Toplevel()
        top.title("You Win! ")
        #top.grab_set()
        
        top.geometry("%dx%d%+d%+d" % (600, 450, 250, 125))
        canvas = Canvas(top, width=200, height=200)
        canvas.pack(expand = YES, fill = BOTH)
        
        
        gif1 = PhotoImage(file = 'images/win2.gif')
        canvas.create_image(50, 10, image = gif1, anchor = NW)
       
        #x = Label (top, image = self.bg_image)
        
           
        
        #y = Label (top, image = "")

        button = Button(top, text="Quit", command=self.destroyall).grid(row=50, column=0)
        #button.pack()

        button = Button(top, text="Play Again", command=playagain).grid(row=50, column=1)
        #button.pack()
        #.pack({"side": "top"})
        #w.pack()
        
       
        #end of it

    def update_flags(self):
        self.label3.config(text = "Flags: "+str(self.flags))

    def destroyall(self):
        global root
        root.destroy()
    


def playagain():
    global root
    root.destroy()
    root = Tk()
    root.title("Minesweeper2")
    minesweeper = Minesweeper(root)
    root.mainloop()


            
            
        
### END OF CLASSES ###

def main():
    global root
    # create Tk widget
    root = Tk()
    # set program title
    root.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(root)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()

