from Constants import FILE_POLL_INTERVAL, DATABASE_FILE_DELIMITER, STRING_LIST_DELIMITER
from threading import Timer
from DisplayStateFactory import DisplayStateFactory


class FileReader(object):
    def __init__(self, rootGUIWidget, databaseFilePath, inputFilePath, outputFilePath):
        self.rootGUIWidget = rootGUIWidget
        self.inputFilePath = inputFilePath
        self.outputFilePath = outputFilePath
        self.readDatabaseFile(databaseFilePath)
        self.filePollTimer = Timer(FILE_POLL_INTERVAL, lambda: self.readInputFileAndUpdateState())
        self.timeoutTimer = None
        self.factory = DisplayStateFactory(self.rootGUIWidget)

    def startTimer(self):
        self.filePollTimer.start()

    def readDatabaseFile(self, databaseFilePath):
        print 'Reading Database File'
        with open(databaseFilePath, 'r') as f:
            newText = f.read()
        self.database = {}
        for row in newText.split('\n')[1:]:
            rowSplit = row.split(DATABASE_FILE_DELIMITER)
            if (len(rowSplit) != 5):
                print 'Skipping row. Length Incorrect. {0}'.format(row)
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
            if not self.isDatabaseRowValid(templateNo, stringList, duration):
                print 'Databse row contains invalid data: {0}'.format(row)
                continue
            self.database[displayState] = {'templateNo': templateNo, 'stringList': stringList, 'duration': duration, 'fileAddress': fileAddress}

    def isDatabaseRowValid(self, templateNo, stringList, duration):
        if (templateNo > 5):
            return False
        else:
            return True

    def readInputFileAndUpdateState(self):
        with open(self.inputFilePath) as f:
            fileInput = f.read().strip()
        displayStateIsNew = fileInput != self.factory.currentDisplayState
        self.updateState(fileInput, displayStateIsNew)
        self.restartFilePollTimer()

    def restartFilePollTimer(self):
        self.filePollTimer = Timer(FILE_POLL_INTERVAL, lambda: self.readInputFileAndUpdateState())
        self.filePollTimer.start()

    def updateState(self, fileInput, displayStateIsNew):
        if fileInput in self.database and displayStateIsNew:
            self.writeStatus('NEW FILEINPUT {0}'.format(fileInput))
            print 'New FileInput {0}'.format(fileInput)
            dbEntry = self.database[fileInput]
            self.factory.updateDisplayState(dbEntry)
            self.timeoutTimer = Timer(dbEntry['duration'], lambda: self.onTimeout())
            self.timeoutTimer.start()
        elif displayStateIsNew:
                self.writeStatus('BAD INPUT - NO EXISTY IN DATABASY')
                print 'The input {0} does not exist in the database. Keeping old displayState. Database: {1}'.format(fileInput, self.database)

    def writeStatus(self, status):
        with open(self.outputFilePath, 'w') as f:
            f.write(status)

    def onTimeout(self):
        self.writeStatus('TIMEOUT-SUCCESS')
