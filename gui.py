from tkinter import Tk, Label, Button, LEFT, Frame, TOP, BOTTOM, StringVar, ttk, Entry
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

        self.custom_button = Button(self.menu_frame, text='custom', command=self.custom)
        self.custom_button.pack(side=LEFT)

        self.bar_colour = self.hard_button.cget("background")
        self.win_lose = [
            self.reset_button, self.easy_button, self.intermediate_button, self.hard_button, self.custom_button]
        self.grid_squares = []
        self.asshats = Asshats()

        self.board_reset(EASY)

    def init_board_frame(self):
        # noinspection PyAttributeOutsideInit
        self.board_frame = Frame(self.master)
        self.board_frame.pack(side=BOTTOM)
        self.grid_squares = []
        for y in range(self.config.y):
            current_row = []
            for x in range(self.config.x):
                square = SquareButton(self.board_frame, x, y, self)
                square.config(image=self.asshats.photo_closed, width='20', height='20')
                square.grid(row=y, column=x)
                current_row.append(square)
            self.grid_squares.append(current_row)

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
        self.reset_bar_color()

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

    def change_bar_color(self, is_fail: bool):
        color = 'red' if is_fail else 'green'
        for butt in self.win_lose:
            butt.configure(background=color)

    def reset_bar_color(self):
        for butt in self.win_lose:
            butt.configure(background=self.bar_colour)

    def custom(self):
        CustomPopUp(self)


class SquareButton(Button):
    def __init__(self, master, x: int, y: int, gui: GUI):
        super().__init__(master)  # this already does the whole self.master = master thing
        self.x = x
        self.y = y
        self.gui = gui
        self.bind("<Button-3>", self.mark)
        self.bind("<Button-1>", self.expose)

    def expose(self, event):
        is_fail = False
        exposed = self.gui.board.expose(self.x, self.y)
        for x, y, adj in exposed:
            if adj == -1:
                is_fail = True
                self.gui.grid_squares[y][x].config(image=self.gui.asshats.photo_mine)
                if self.x == x and self.y == y:
                    self.gui.grid_squares[y][x].config(image=self.gui.asshats.photo_red_mine)
            else:
                self.gui.grid_squares[y][x].config(image=self.gui.asshats.photo_adj[adj])
        if not self.gui.board.is_active:
            self.gui.change_bar_color(is_fail)

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


class CustomPopUp(Tk):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.new_config = Config(StringVar(), StringVar(), StringVar())
        self.new_config.x.set('')
        self.new_config.y.set('')
        self.new_config.n.set('')
        self.wm_title('Custom Board')
        w_label = Label(self, text='Width')
        w_label.grid(row=0, column=0)
        self.w_box = Entry(self, textvariable=self.new_config.x)
        self.w_box.grid(row=0, column=1)
        h_label = Label(self, text='Height')
        h_label.grid(row=1, column=0)
        h_box = Entry(self, textvariable=self.new_config.y)
        h_box.grid(row=1, column=1)
        n_label = Label(self, text='Mines')
        n_label.grid(row=2, column=0)
        n_box = Entry(self, textvariable=self.new_config.n)
        n_box.grid(row=2, column=1)

        b1 = Button(self, text="Okay", command=self.okay)
        b1.grid(row=3, columnspan=2, column=0)
        self.mainloop()

    def okay(self):
        config = Config(int(self.new_config.x.get()), int(self.new_config.y.get()), int(self.new_config.n.get()))
        self.gui.board_reset(config)
        self.destroy()


root = Tk()
gui = GUI(root)
root.mainloop()
