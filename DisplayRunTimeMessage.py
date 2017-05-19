from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import StringVar
from AbstractDisplay import AbstractDisplay


class DisplayRunTimeMessage(AbstractDisplay):
    def __init__(self, master, screen_height, onInput):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.sv = StringVar()
        self.sv.set('')
        self.bigLabel = TextLabel(master, self.sv, 0, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)
        self.onInput = onInput

    def updateText(self, messagelist,RunTimeMessage):
        newlist=[]
        for line in messagelist:
            line = line.replace('{Run_Time_Message}', RunTimeMessage)
            newlist.append(line)
        self.sv.set('\n'.join(newlist))

    def hide(self):
        self.bigLabel.grid_forget()

    def show(self):
        self.bigLabel.grid()

    def updateBackground(self, newColor):
        self.bigLabel.updateBackground(newColor)

    def updateTextSize(self, newSize):
        self.bigLabel.updateTextSize(newSize)
