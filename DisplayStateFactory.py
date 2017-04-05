from DisplayMessage import DisplayMessage
from PIL import Image, ImageTk
from DisplayImage import DisplayImage


class DisplayStateFactory(object):
    def getDisplayState(self, root, templateNo, stringList, duration, fileAddress):
        if templateNo == 1:
            displayMessage = DisplayMessage(root, root.winfo_screenheight())
            displayMessage.updateText(stringList[0])
            return displayMessage
        elif templateNo == 2:
            photo = Image.open(fileAddress)
            pilPhoto = ImageTk.PhotoImage(photo)
            displayImage = DisplayImage(root, root.winfo_screenheight(), pilPhoto)
            displayImage.img = pilPhoto
        else:
            raise 'I only know one TemplateNo'
