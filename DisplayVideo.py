from Constants import BIG_FONT_HEIGHT_FRACTION, VIDEO_SLEEP_TIME
from TextLabel import TextLabel
from Tkinter import PhotoImage
import Tkinter as tk
import imageio
from PIL import Image, ImageTk
import time
import os
from AbstractDisplay import AbstractDisplay


class DisplayVideo(tk.Label, AbstractDisplay):
    def __init__(self, master, screen_height, pilPhoto):
        tk.Label.__init__(self, master, image=pilPhoto)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0)

    def playVideo(self, videoPath):
        number = 1
        path = videoPath.replace('{NUMBER}', format(number, '04d'))
        print os.path.exists(path)
        print path
        while (os.path.exists(path)):
            start_time = time.time()
            photo = Image.open(path)
            pilPhoto = ImageTk.PhotoImage(photo)
            self.configure(image=pilPhoto)
            self.image = pilPhoto
            elapsed_time = time.time() - start_time
            sleep_time = VIDEO_SLEEP_TIME - elapsed_time
            print elapsed_time
            if sleep_time < 0:
                sleep_time = 0
            time.sleep(sleep_time)
            number += 1
            path = videoPath.replace('{NUMBER}', format(number, '04d'))

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid()

    def updateBackground(self, newColor):
        pass

    def updateTextSize(self, newSize):
        pass
