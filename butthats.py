from tkinter import PhotoImage


class Asshats:
    def __init__(self):
        self.photo_mine = PhotoImage(file="Asshats/mine.png")
        self.photo_closed = PhotoImage(file="Asshats/closed.png")
        self.photo_flag = PhotoImage(file="Asshats/flag.png")
        self.photo_unknown = PhotoImage(file="Asshats/unknown.png")
        self.photo_red_mine = PhotoImage(file="Asshats/red_mine.png")
        self.photo_adj = [
            PhotoImage(file="Asshats/0.png"),
            PhotoImage(file="Asshats/1.png"),
            PhotoImage(file="Asshats/2.png"),
            PhotoImage(file="Asshats/3.png"),
            PhotoImage(file="Asshats/4.png"),
            PhotoImage(file="Asshats/5.png"),
            PhotoImage(file="Asshats/6.png"),
            PhotoImage(file="Asshats/7.png"),
            PhotoImage(file="Asshats/8.png")]
