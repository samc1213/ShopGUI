from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import PhotoImage
import Tkinter as tk
from PIL import Image, ImageTk


class DisplayImage(tk.Label):
    def __init__(self, master, screen_height, pilPhoto):
        tk.Label.__init__(self, master, image=pilPhoto)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0)

    def updateImage(self, pilPhoto):
        self.configure(image=pilPhoto)
        self.image = pilPhoto

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid()
