from Constants import BIG_FONT_HEIGHT_FRACTION
from TextInput import TextInput
from Tkinter import PhotoImage
import Tkinter as tk
from PIL import Image, ImageTk
from AbstractDisplay import AbstractDisplay


class DisplayEntry(AbstractDisplay):
    def __init__(self, master, screen_height):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.input = TextInput(master, 0, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)

    def hide(self):
        self.input.grid_forget()

    def show(self):
        self.input.grid()
