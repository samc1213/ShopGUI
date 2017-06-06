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

#function tests display states, use when running "python App.py GUI" on command line
def test(reader): 
    reader.updateState('Mod3')

#TK GUI loop keeps the main thread running
def mainGuiLoop(root):
    root.mainloop()

#function prepares GUI settings, 
#creates initialization classes including 
#   thread data(refered as TD in most of the code) used for storing global variables
#   GUI Observer, listens to events from timeout timers or keypad inputs
#   FileReader, initializes display state classes including display state factory
def setUp(Working_directory):

    #Tk GUI settings
    root = tk.Tk()
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    root.configure(background=BACKGROUND_COLOR)

    #Class inits
    TD = Thread_Data()
    observer = GuiObserver()
    reader = FileReader(root, Working_directory +'/dbFile.txt', Working_directory + '/inputFile.txt', Working_directory + '/outputFile.txt', observer, Working_directory,TD)
   
    #return reference to objects
    return reader, root, observer,TD


if __name__ == '__main__': #if this is the main script
    try:
        running=True #variable used to shut down Current sensor thread when false

        #figures out the working directory 
        print('sys.argv[0] =', sys.argv[0])             
        pathname = os.path.dirname(sys.argv[0])
        print('full path =', os.path.abspath(pathname)) 
        Working_directory = os.path.abspath(pathname)

        #initializes important classes
        reader, root, observer, TD = setUp(Working_directory)

        #optional test run of GUI, test run of handler no longer works, handler cannot run independent of the GUI
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
            handler = Handler(reader, observer,Working_directory,running,root,TD) #initialize handler, pass reference to clases
            handler.StartWorkerThreads() #run additional handler initializations
            mainGuiLoop(root) #loop to maintain thread active
    except Exception as e:
        print e

    finally:
        print "end of App \n"
