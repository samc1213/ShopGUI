from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import StringVar
from AbstractDisplay import AbstractDisplay


class DisplayMessage(AbstractDisplay):
    def __init__(self, master, screen_height):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.sv = StringVar()
        self.sv.set('Enter some text!')
        self.bigLabel = TextLabel(master, self.sv, 0, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)

    def updateText(self, newText):
        self.sv.set(newText)

    def hide(self):
        self.bigLabel.grid_forget()

    def show(self):
        self.bigLabel.grid()
