from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import PhotoImage
import Tkinter as tk
import imageio
from PIL import Image, ImageTk
import time
import os


class DisplayVideo(tk.Label):
    def __init__(self, master, screen_height, pilPhoto):
        tk.Label.__init__(self, master, image=pilPhoto)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0)

    def playVideo(self, videoPath):
        number = 1
        path = videoPath.replace('{NUMBER}', format(number, '04d'))
        while (os.path.exists(path)):
            photo = Image.open(path)
            pilPhoto = ImageTk.PhotoImage(photo)
            self.configure(image=pilPhoto)
            self.image = pilPhoto
            time.sleep(.9)
            number += 1
            path = videoPath.replace('{NUMBER}', format(number, '04d'))

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid()
