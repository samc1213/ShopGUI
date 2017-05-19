#!/usr/bin/python

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
import os
from GuiObserver import GuiObserver
from Thread_Data_Object import Thread_Data

def test(reader):
    reader.updateState('ID_Echo')

def mainGuiLoop(root):
    root.mainloop()

def setUp(Working_directory):
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)
    TD = Thread_Data()
    observer = GuiObserver()
    reader = FileReader(root, Working_directory +'/dbFile.txt', Working_directory + '/inputFile.txt', Working_directory + '/outputFile.txt', observer, Working_directory,TD)

    return reader, root, observer,TD


if __name__ == '__main__':
    try:
        running=True
        print('sys.argv[0] =', sys.argv[0])             
        pathname = os.path.dirname(sys.argv[0])
        print('full path =', os.path.abspath(pathname)) 
        Working_directory = os.path.abspath(pathname)
        reader, root, observer, TD = setUp(Working_directory)

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
                handler = Handler(reader, observer,running)
                handler.StartWorkerThreads()
        else:
            handler = Handler(reader, observer,Working_directory,running,root,TD)
            handler.StartWorkerThreads()
            mainGuiLoop(root)
    except Exception as e:
        print e

    finally:
        print "end of App \n"
