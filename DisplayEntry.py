from Constants import BIG_FONT_HEIGHT_FRACTION
from TextInput import TextInput
from TextLabel import TextLabel
from Tkinter import PhotoImage, StringVar
import Tkinter as tk
from PIL import Image, ImageTk
from AbstractDisplay import AbstractDisplay


class DisplayEntry(AbstractDisplay):
    def __init__(self, master, screen_height, onInput):
        master.grid_columnconfigure(0, weight=1)
        # padding row
        master.grid_rowconfigure(0, weight=1)
        # input prompt row
        master.grid_rowconfigure(1, weight=1)
        # input row
        master.grid_rowconfigure(2, weight=1)
        # padding row
        master.grid_rowconfigure(3, weight=1)
        self.input = TextInput(master, 2, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)
        self.sv = StringVar()
        self.sv.set('')
        self.prompt = TextLabel(master, self.sv, 1, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)
        self.onInput = onInput
        master.bind("<Return>", self.onReturn)

    def onReturn(self, event):
        text = self.input.getText()
        self.onInput(text)

    def hide(self):
        self.input.clearText()
        self.input.grid_forget()

    def show(self):
        self.input.grid()

    def updatePrompt(self, newText):
        self.sv.set(newText)
