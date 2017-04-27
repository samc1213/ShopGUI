import Tkinter as tk
from Constants import BIG_FONT_HEIGHT_FRACTION, BACKGROUND_COLOR
from TextLabel import TextLabel
from FileReader import FileReader
import time
try:
    from Handler3 import Handler
except ImportError:
    pass
import threading
import sys
from GuiObserver import GuiObserver


def test(reader):
    reader.updateState('Welcome1')
    time.sleep(5)
    reader.updateState('PromptUserID')
    time.sleep(5)
    reader.updateState('OkGo')
    # time.sleep(3)
    # reader.updateState('EyeImage')
    # time.sleep(1)
    # reader.updateState('Input')

def mainGuiLoop(root):
    root.mainloop()

def setUp():
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    #root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)

    observer = GuiObserver()
    reader = FileReader(root, 'dbFile.txt', 'inputFile.txt', 'outputFile.txt', observer)

    return reader, root, observer


if __name__ == '__main__':
    try:
        reader, root, observer = setUp()

        if len(sys.argv) == 2:
            arg = sys.argv[1]
            if arg.lower() == "gui":
                print 'Running in GUI test mode...'
                testThread = threading.Thread(name='Alert', target=test, args=(reader,))
                testThread.start()
                mainGuiLoop(root)
            elif arg.lower() == "handler":
                #testing push
                print 'Running in handler test mode...'
                handler = Handler(reader, observer)
                handler.StartWorkerThreads()
        else:
            handler = Handler(reader, observer)
            handler.StartWorkerThreads()
            mainGuiLoop(root)
    except Exception as e:
        print e
    finally:
        time.sleep(2)
        running = False
        raise
