import Tkinter as tk
from Constants import BIG_FONT_HEIGHT_FRACTION, BACKGROUND_COLOR
from TextLabel import TextLabel
from DisplayMessage import DisplayMessage
from DisplayImage import DisplayImage
from FileReader import FileReader
import time


if __name__ == '__main__':
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)

    # mainFrame = tk.Frame(root).pack(expand=1)

    # displayMessage = DisplayMessage(root, root.winfo_screenheight())
    # displayMessage.updateText('weoo')

    # displayMessage2 = DisplayMessage(root, root.winfo_screenheight())
    # displayMessage2.updateText('weoo34')
    # time.sleep(10)

    reader = FileReader(root, 'dbFile.txt', 'inputFile.txt')
    reader.startTimer()

    root.mainloop()
