from Constants import DEFAULT_DISPLAYIMAGE_FILEPATH
from DisplayMessage import DisplayMessage
from DisplayImage import DisplayImage
from DisplayVideo import DisplayVideo
from DisplayChoices import DisplayChoices
from DisplayEntry import DisplayEntry
from PIL import Image, ImageTk


class DisplayStateFactory(object):
    def __init__(self, root, onInput):
        self.root = root
        self.currentDisplayState = None
        self.onInput = onInput
        self.displayMessage = DisplayMessage(root, root.winfo_screenheight(), self.onInput)
        photo = Image.open(DEFAULT_DISPLAYIMAGE_FILEPATH)
        pilPhoto = ImageTk.PhotoImage(photo)
        self.displayImage = DisplayImage(root, root.winfo_screenheight(), pilPhoto, self.onInput)
        self.displayVideo = DisplayVideo(root, root.winfo_screenheight(), pilPhoto)
        self.displayChoices = DisplayChoices(root, root.winfo_screenheight(), self.onInput)
        self.displayEntry = DisplayEntry(root, root.winfo_screenheight(), onInput)
        self.clearDisplay()

    def clearDisplay(self):
        self.currentDisplayState = None
        self.displayImage.hide()
        self.displayMessage.hide()
        self.displayVideo.hide()
        self.displayChoices.hide()
        self.displayEntry.hide()

    def updateDisplayState(self, databaseEntry, fileInput):
        if self.currentDisplayState != fileInput:
            self.clearDisplay()
            self.root.configure(background=databaseEntry['color'])
        if databaseEntry['templateNo'] == 1:
            self.displayMessage.updateText(databaseEntry['stringList'])
            self.currentDisplayState = fileInput
            self.displayMessage.show()
            self.displayMessage.updateBackground(databaseEntry['color'])
            self.displayMessage.updateTextSize(databaseEntry['textSize'])
        elif databaseEntry['templateNo'] == 2:
            photo = Image.open(databaseEntry['fileAddress'])
            pilPhoto = ImageTk.PhotoImage(photo)
            self.displayImage.updateImage(pilPhoto)
            self.displayImage.show()
            self.currentDisplayState = fileInput
        elif databaseEntry['templateNo'] == 3:
            self.displayVideo.show()
            self.currentDisplayState = fileInput
            self.displayVideo.playVideo(databaseEntry['fileAddress'])
        elif databaseEntry['templateNo'] == 4:
            self.displayChoices.updateText(databaseEntry['stringList'])
            self.currentDisplayState = fileInput
            self.displayChoices.updateBackground(databaseEntry['color'])
            self.displayChoices.updateTextSize(databaseEntry['textSize'])
            self.displayChoices.show()
        elif databaseEntry['templateNo'] == 5:
            self.currentDisplayState = fileInput
            self.displayEntry.updatePrompt(databaseEntry['stringList'][0])
            self.displayEntry.updateBackground(databaseEntry['color'])
            self.displayEntry.updateTextSize(databaseEntry['textSize'])
            self.displayEntry.show()
        else:
            raise 'Invalid templateNo: {0}'.format(databaseEntry['templateNo'])
