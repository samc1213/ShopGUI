

class GuiObserver(object):
    def __init__(self):
        self.inputListeners = []
        self.timeoutListeners = []

    def guiTimeout(self):
        print 'GUI timeout fired'
        for listener in self.timeoutListeners:
            listener()

    def addInputListener(self,listener):
        self.inputListeners.append(listener)

    def addTimeoutListener(self,listener):
        self.timeoutListeners.append(listener)

    def guiInput(self, input):
        print 'GUI input fired. Value: {0}'.format(input)
        for listener in self.inputListeners:
            listener(input)
