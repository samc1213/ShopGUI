from Constants import FILE_POLL_INTERVAL, DATABASE_FILE_DELIMITER, STRING_LIST_DELIMITER
from threading import Timer
from DisplayStateFactory import DisplayStateFactory
import time


class FileReader(object):
    def __init__(self, rootGUIWidget, databaseFilePath, inputFilePath, outputFilePath, guiObserver):
        self.rootGUIWidget = rootGUIWidget
        self.inputFilePath = inputFilePath
        self.outputFilePath = outputFilePath
        self.readDatabaseFile(databaseFilePath)
        self.factory = DisplayStateFactory(self.rootGUIWidget, self.onInput)
        self.observer = guiObserver
        self.timeoutTimer = None
        self.timeoutTimer =Timer(10,  lambda: self.initialTimer())

    def onInput(self, input):
        print 'input received from display, {0}'.format(input)
        self.observer.guiInput(input)

    def readDatabaseFile(self, databaseFilePath):
        print 'Reading database file'
        with open(databaseFilePath, 'r') as f:
            newText = f.read()
        self.database = {}
        for row in newText.split('\n')[1:]:
            rowSplit = row.split(DATABASE_FILE_DELIMITER)
            if (len(rowSplit) != 5):
                print 'Skipping row. Length incorrect. {0}'.format(row)
                continue
            try:
                displayState = rowSplit[0].strip()
                templateNo = int(rowSplit[1].strip())
                stringList = rowSplit[2].split(STRING_LIST_DELIMITER)
                duration = int(rowSplit[3].strip())
                fileAddress = rowSplit[4].strip()
            except Exception as ex:
                print 'There was a problem parsing the database row: {0}. {1}'.format(row, str(ex))
                continue
            self.database[displayState] = {'templateNo': templateNo, 'stringList': stringList, 'duration': duration, 'fileAddress': fileAddress}

    def updateState(self, fileInput):
        displayStateIsNew = fileInput != self.factory.currentDisplayState
        print 'DisplayStateIsNew: {0}'.format(displayStateIsNew)
        if fileInput in self.database and displayStateIsNew:
            self.writeStatus('NEW FILEINPUT {0}'.format(fileInput))
            print 'New FileInput {0}'.format(fileInput)
            dbEntry = self.database[fileInput]
            self.factory.updateDisplayState(dbEntry, fileInput)
            self.timeoutTimer.cancel()
            self.timeoutTimer = None
            self.timeoutTimer = Timer(dbEntry['duration'], lambda: self.onTimeout())
            self.timeoutTimer.start()
        elif displayStateIsNew:
            self.writeStatus('BAD INPUT - NO EXISTY IN DATABASY')
            print 'The input {0} does not exist in the database. Keeping old displayState. Database: {1}'.format(fileInput, self.database)

    def writeStatus(self, status):
        with open(self.outputFilePath, 'w') as f:
            f.write(status)

    def onTimeout(self):
        self.observer.guiTimeout()
    def initialTimer(self):
    	print 'initial timer'

