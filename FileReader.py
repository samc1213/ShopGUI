from Constants import FILE_POLL_INTERVAL
from threading import Timer


class FileReader(object):
    def __init__(self, filePath, displayMessage, displayImage):
        self.displayMessage = displayMessage
        self.filePath = filePath
        self.t = Timer(FILE_POLL_INTERVAL, lambda: self.readFileAndWrite())

    def startTimer(self):
        self.t.start()

    def readFileAndWrite(self):
        with open(self.filePath) as f:
            newText = f.read()
        self.displayMessage.updateText(newText)
        self.t = Timer(FILE_POLL_INTERVAL, lambda: self.readFileAndWrite())
        self.t.start()
