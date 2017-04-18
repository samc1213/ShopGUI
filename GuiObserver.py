

class GuiObserver(object):
    def guiTimeout(self):
        print 'GUI timeout fired'

    def guiInput(self, input):
        print 'GUI input fired. Value: {0}'.format(input)
