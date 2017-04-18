from Constants import BIG_FONT_HEIGHT_FRACTION
from TextInput import TextInput
from Tkinter import PhotoImage
import Tkinter as tk
from PIL import Image, ImageTk
from AbstractDisplay import AbstractDisplay


class DisplayEntry(AbstractDisplay):
    def __init__(self, master, screen_height, onInput):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.input = TextInput(master, 0, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)
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
