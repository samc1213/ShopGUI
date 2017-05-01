import Tkinter as tk
from Constants import BACKGROUND_COLOR, TEXT_COLOR


class TextInput(tk.Entry):
    def __init__(self, master, row, column, screen_height, font_fraction):
        tk.Entry.__init__(self, master, font=('Helvetica', int(font_fraction * screen_height)),
                          background=BACKGROUND_COLOR, foreground=TEXT_COLOR)
        self.grid(row=row, column=column)
        self.screen_height = screen_height

    def clearText(self):
        self.delete(0, 'end')

    def getText(self):
        return self.get()

    def updateBackground(self, newColor):
        self.configure(background=newColor)

    def updateTextSize(self, newSize):
        self.configure(font=('Helvetica', int(newSize * self.screen_height)))
