from Constants import DEFAULT_DISPLAYIMAGE_FILEPATH
from DisplayMessage import DisplayMessage
from DisplayImage import DisplayImage
from DisplayVideo import DisplayVideo
from DisplayChoices import DisplayChoices
from DisplayEntry import DisplayEntry
from PIL import Image, ImageTk


class DisplayStateFactory(object):
    def __init__(self, root):
        self.currentDisplayState = None
        self.displayMessage = DisplayMessage(root, root.winfo_screenheight())
        photo = Image.open(DEFAULT_DISPLAYIMAGE_FILEPATH)
        pilPhoto = ImageTk.PhotoImage(photo)
        self.displayImage = DisplayImage(root, root.winfo_screenheight(), pilPhoto)
        self.displayVideo = DisplayVideo(root, root.winfo_screenheight(), pilPhoto)
        self.displayChoices = DisplayChoices(root, root.winfo_screenheight())
        self.displayEntry = DisplayEntry(root, root.winfo_screenheight())
        self.clearDisplay()

    def clearDisplay(self):
        self.currentDisplayState = None
        self.displayImage.hide()
        self.displayMessage.hide()
        self.displayVideo.hide()
        self.displayChoices.hide()
        self.displayEntry.hide()

    def updateDisplayState(self, databaseEntry):
        if self.currentDisplayState != databaseEntry:
            self.clearDisplay()
        if databaseEntry['templateNo'] == 1:
            self.displayMessage.updateText(databaseEntry['stringList'][0])
            self.currentDisplayState = databaseEntry
            self.displayMessage.show()
        elif databaseEntry['templateNo'] == 2:
            photo = Image.open(databaseEntry['fileAddress'])
            pilPhoto = ImageTk.PhotoImage(photo)
            self.displayImage.updateImage(pilPhoto)
            self.displayImage.show()
            self.currentDisplayState = databaseEntry
        elif databaseEntry['templateNo'] == 3:
            self.displayVideo.show()
            self.currentDisplayState = databaseEntry
            self.displayVideo.playVideo(databaseEntry['fileAddress'])
        elif databaseEntry['templateNo'] == 4:
            self.displayChoices.updateText(databaseEntry['stringList'])
            self.currentDisplayState = databaseEntry
            self.displayChoices.show()
        elif databaseEntry['templateNo'] == 5:
            self.currentDisplayState = databaseEntry
            self.displayEntry.show()
        else:
            raise 'Invalid templateNo: {0}'.format(databaseEntry['templateNo'])
