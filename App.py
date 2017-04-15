import Tkinter as tk
from Constants import BIG_FONT_HEIGHT_FRACTION, BACKGROUND_COLOR
from TextLabel import TextLabel
from FileReader import FileReader
import time


if __name__ == '__main__':
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)

    reader = FileReader(root, 'dbFile.txt', 'inputFile.txt', 'outputFile.txt')
    reader.startTimer()

    root.bind("<W>", tit)
    root.mainloop()
