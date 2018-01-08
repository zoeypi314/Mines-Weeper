from tkinter import Tk, Label, Button, LEFT, Frame, TOP, BOTTOM, StringVar
from butthats import Asshats
from board import Board, Marker
from config import *


class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Mines-Weeper by Agent Orange')

        self.menu_frame = Frame(master)
        self.menu_frame.pack(side=TOP)

        self.rem_mines = StringVar()
        self.rem_mines_label = Label(self.menu_frame, textvariable=self.rem_mines)
        self.rem_mines_label.pack(side=LEFT)
        
        self.reset_button = Button(self.menu_frame, text='Reset', command=self.board_reset)
        self.reset_button.pack(side=LEFT)

        self.easy_button = Button(self.menu_frame, text='easy', command=self.easy)
        self.easy_button.pack(side=LEFT)
        
        self.intermediate_button = Button(self.menu_frame, text='intermediate', command=self.intermediate)
        self.intermediate_button.pack(side=LEFT)

        self.hard_button = Button(self.menu_frame, text='hard', command=self.hard)
        self.hard_button.pack(side=LEFT)

        self.grid_squares = []
        self.asshats = Asshats()

        self.board_reset(EASY)

    def init_board_frame(self):
        # noinspection PyAttributeOutsideInit
        self.board_frame = Frame(self.master)
        self.board_frame.pack(side=BOTTOM)
        self.grid_squares = []
        for x in range(self.config.x):
            for y in range(self.config.y):
                square = SquareButton(self.board_frame, x, y, self)
                square.config(image=self.asshats.photo_closed, width='20', height='20')
                square.grid(row=y, column=x)
                self.grid_squares.append(square)

    # noinspection PyAttributeOutsideInit
    def board_reset(self, config: Config=None):
        if len(self.grid_squares) > 0:
            self.board_frame.pack_forget()
        if config is not None:
            self.config = config
        else:
            config = self.config
        self.board = Board(config.x, config.y, config.n)
        self.init_board_frame()
        self.update_counter()

    def update_counter(self):
        if self.board.rem_mines < 0:
            self.rem_mines_label.configure(foreground='red')
        else:
            self.rem_mines_label.configure(foreground='black')
        self.rem_mines.set('{}/{}'.format(self.board.rem_mines, self.board.num_mines))
        root.update_idletasks()

    def easy(self):
        self.board_reset(EASY)
         
    def intermediate(self):
        self.board_reset(INTERMEDIATE)

    def hard(self):
        self.board_reset(HARD)


class SquareButton(Button):
    def __init__(self, master, x: int, y: int, gui: GUI):
        super().__init__(master)  # this already does the whole self.master = master thing
        self.x = x
        self.y = y
        self.gui = gui
        self.bind("<Button-3>", self.mark)

    def expose(self):
        pass

    def mark(self, event):
        new_mark = self.gui.board.mark(self.x, self.y)
        if new_mark is None:
            pass
        elif new_mark == Marker.unknown:
            self.config(image=self.gui.asshats.photo_unknown, width='20', height='20')
        elif new_mark == Marker.flag:
            self.config(image=self.gui.asshats.photo_flag, width='20', height='20')
        elif new_mark == Marker.clear:
            self.config(image=self.gui.asshats.photo_closed, width='20', height='20')
        self.gui.update_counter()


root = Tk()
gui = GUI(root)
root.mainloop()
