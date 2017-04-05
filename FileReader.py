from Constants import FILE_POLL_INTERVAL, DATABASE_FILE_DELIMITER, STRING_LIST_DELIMITER
from threading import Timer
from DisplayStateFactory import DisplayStateFactory


class FileReader(object):
    def __init__(self, root, databaseFilePath, inputFilePath):
        self.root = root
        self.inputFilePath = inputFilePath
        self.readDatabaseFile(databaseFilePath)
        self.t = Timer(FILE_POLL_INTERVAL, lambda: self.readInputFile())
        self.factory = DisplayStateFactory(self.root)

    def startTimer(self):
        self.t.start()

    def readDatabaseFile(self, databaseFilePath):
        print 'Reading Database File'
        with open(databaseFilePath) as f:
            newText = f.read()
        self.database = {}
        for row in newText.split('\n')[1:]:
            rowSplit = row.split(DATABASE_FILE_DELIMITER)
            if (len(rowSplit) != 5):
                print 'Skipping row. Length Incorrect. {0}'.format(row)
                continue
            displayState = rowSplit[0].strip()
            templateNo = int(rowSplit[1].strip())
            stringList = rowSplit[2].split(STRING_LIST_DELIMITER)
            duration = int(rowSplit[3].strip())
            fileAddress = rowSplit[4].strip()
            if not self.isDatabaseRowValid(templateNo, stringList, duration):
                print 'ERROR WITH ROW:' + row
                continue
            print 'reading DB row'
            self.database[displayState] = {'templateNo': templateNo, 'stringList': stringList, 'duration': duration, 'fileAddress': fileAddress}

    def isDatabaseRowValid(self, templateNo, stringList, duration):
        return True

    def readInputFile(self):
        with open(self.inputFilePath) as f:
            fileInput = f.read().strip()
        print 'Reading fileinput: {0}'.format(fileInput)
        displayStateIsNew = fileInput != self.factory.currentDisplayState
        if fileInput in self.database and displayStateIsNew:
            dbEntry = self.database[fileInput]
            self.factory.updateDisplayState(dbEntry)
        else:
            if displayStateIsNew:
                print 'The input {0} does not exist in the database. Keeping old displayState. Database: {1}'.format(fileInput, self.database)
            else:
                print 'Old displayState'
        self.t = Timer(FILE_POLL_INTERVAL, lambda: self.readInputFile())
        self.t.start()
