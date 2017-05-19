from Constants import DEFAULT_DISPLAYIMAGE_FILEPATH
from DisplayImage import DisplayImage
from DisplayVideo import DisplayVideo
#from DisplayPowerPoint import DisplayPowerPoint
from DisplayChoices import DisplayChoices
from DisplayEntry import DisplayEntry
from DisplayRunTimeMessage import DisplayRunTimeMessage
from PIL import Image, ImageTk


class DisplayStateFactory(object):
    def __init__(self, root, onInput,Working_directory,TD):
        self.ThreadData = TD
        self.root = root
        self.currentDisplayState = None
        self.onInput = onInput
        self.displayRunTimeMessage = DisplayRunTimeMessage(root, root.winfo_screenheight(), self.onInput)
        photo = Image.open(Working_directory+'/'+DEFAULT_DISPLAYIMAGE_FILEPATH)
        pilPhoto = ImageTk.PhotoImage(photo)
        self.displayImage = DisplayImage(root, root.winfo_screenheight(), pilPhoto, self.onInput)
        self.displayVideo = DisplayVideo(root, root.winfo_screenheight(), pilPhoto)
        #self.displayPowerPoint = DisplayPowerPoint(root, root.winfo_screenheight(), pilPhoto)
        self.displayChoices = DisplayChoices(root, root.winfo_screenheight(), self.onInput)
        self.displayEntry = DisplayEntry(root, root.winfo_screenheight(), onInput)
        root.bind("<Key>", self.onKeyPressed)
        self.clearDisplay()

    def onKeyPressed(self, event):
        #print event.keysym
        if event.keysym == "Return" or event.keysym == "KP_Enter":
            # print "Enter was Pressed: giving display entry control"
            self.displayEntry.onReturn(event)
        elif event.keysym == "KP_4" or event.keycode == 81:
            #self.displayPowerPoint.updateNumber(-1)
            print "Powerpoint_left"
        elif event.keysym == "KP_6" or event.keycode == 83:
            print "Powerpoint_right"
            #self.displayPowerPoint.updateNumber(1)
        else: 
            # print "Enter was not pressed giving display choices control"
            self.displayChoices.onKeyPressed(event)

    def clearDisplay(self):
        self.currentDisplayState = None
        self.displayImage.hide()
        self.displayVideo.hide()
        #self.displayPowerPoint.hide()
        self.displayChoices.hide()
        self.displayEntry.hide()
        self.displayRunTimeMessage.hide()

    def updateDisplayState(self, databaseEntry, fileInput):
        if self.currentDisplayState != fileInput:
            self.clearDisplay()
            self.root.configure(background=databaseEntry['color'])
        if databaseEntry['templateNo'] == 1:
            self.displayRunTimeMessage.updateText(databaseEntry['stringList'],self.ThreadData.RunTimeMessage)
            self.currentDisplayState = fileInput
            self.displayRunTimeMessage.show()
            self.displayRunTimeMessage.updateBackground(databaseEntry['color'])
            self.displayRunTimeMessage.updateTextSize(databaseEntry['textSize'])
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
            self.displayChoices.updateText(databaseEntry['stringList'],self.ThreadData.RunTimeMessage)
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
        elif databaseEntry['templateNo'] == 6:
            #self.displayPowerPoint.show()
            self.currentDisplayState = fileInput
            #self.displayPowerPoint.playPowerPoint(databaseEntry['fileAddress'])
        else:
            raise 'Invalid templateNo: {0}'.format(databaseEntry['templateNo'])
