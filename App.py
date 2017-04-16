import Tkinter as tk
from Constants import BIG_FONT_HEIGHT_FRACTION, BACKGROUND_COLOR
from TextLabel import TextLabel
from FileReader import FileReader
import time
from Handler3 import Handler
import threading


def mainGuiLoop(root):
    root.mainloop()

def setUp():
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    # root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)

    reader = FileReader(root, 'dbFile.txt', 'inputFile.txt', 'outputFile.txt')

    return reader, root


if __name__ == '__main__':
    try:
        reader, root = setUp()
        handler = Handler(reader)
        handler.StartWorkerThreads()
        mainGuiLoop(root)
    except Exception as e:
        print e
        port.close()
    finally:
        time.sleep(2)
        port.close()
        print("Handler_Shutting_Down")
        running = False
