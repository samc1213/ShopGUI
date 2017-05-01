import Tkinter as tk
from Constants import BACKGROUND_COLOR, TEXT_COLOR


class TextLabel(tk.Label):
    def __init__(self, master, textvariable, row, column, screen_height, font_fraction):
        tk.Label.__init__(self, master, textvariable=textvariable, font=('Helvetica', int(font_fraction * screen_height)),
                            background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
        self.grid(row=row, column=column)
        self.screen_height = screen_height

    def updateBackground(self, newColor):
        self.configure(background=newColor)

    def updateTextSize(self, newSize):
        self.configure(font=('Helvetica', int(newSize * self.screen_height)))
