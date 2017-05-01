from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import PhotoImage
import Tkinter as tk
from PIL import Image, ImageTk
from AbstractDisplay import AbstractDisplay


class DisplayImage(tk.Label, AbstractDisplay):
    def __init__(self, master, screen_height, pilPhoto, onInput):
        tk.Label.__init__(self, master, image=pilPhoto)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0)
        self.onInput = onInput
        master.bind("<Return>", self.onReturn)

    def onReturn(self, event):
        self.onInput('')

    def updateImage(self, pilPhoto):
        self.configure(image=pilPhoto)
        self.image = pilPhoto

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid()

    def updateBackground(self, newColor):
        pass

    def updateTextSize(self, newSize):
        pass
