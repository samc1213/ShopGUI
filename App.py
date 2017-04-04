import Tkinter as tk
from Constants import BIG_FONT_HEIGHT_FRACTION, BACKGROUND_COLOR
from ShopLabel import ShopLabel
from DisplayMessage import DisplayMessage
from FileReader import FileReader


text = 'this'


if __name__ == '__main__':
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)
    displayMessage = DisplayMessage(root, root.winfo_screenheight())
    displayMessage.updateText('weoo')

    reader = FileReader('textFile.txt', displayMessage)
    reader.startTimer()

    root.mainloop()
