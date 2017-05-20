from Constants import BIG_FONT_HEIGHT_FRACTION, VIDEO_SLEEP_TIME
from TextLabel import TextLabel
from Tkinter import PhotoImage
import Tkinter as tk
import imageio
from PIL import Image, ImageTk
import time
import os
from AbstractDisplay import AbstractDisplay


class DisplayPowerPoint(tk.Label, AbstractDisplay):
    def __init__(self, master, screen_height, pilPhoto):
        tk.Label.__init__(self, master, image=pilPhoto)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0)
        self.number = 1

    def playPowerPoint(self, videoPath):
        self.number = 1
        oldnum=0
        path = videoPath.replace('{NUMBER}', format(self.number, '04d'))
        while (1):
            currentnumber = self.number
            path = videoPath.replace('{NUMBER}', format(currentnumber, '04d'))
            if (os.path.exists(path))==0:
                print "power point path does not exist"
                currentnumber = oldnum
                self.number = oldnum
            elif oldnum != currentnumber:
                photo = Image.open(path)
                pilPhoto = ImageTk.PhotoImage(photo)
                self.configure(image=pilPhoto)
                self.image = pilPhoto
                oldnum=self.number
                print path
            time.sleep(.05)

    def hide(self):
        self.grid_forget()

    def show(self):
        self.grid()

    def updateBackground(self, newColor):
        pass

    def updateTextSize(self, newSize):
        pass

    def updateNumber(self,increment):
        num = self.number + increment
        print increment
        if num == 0:
            self.number = 1
        else:
            self.number = num
        print num


