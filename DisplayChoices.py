from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import StringVar


class DisplayChoices(object):
    def __init__(self, master, screen_height):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.sv = StringVar()
        self.bigLabel = TextLabel(master, self.sv, 0, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)

    def updateText(self, listOfChoices):
        displayString = listOfChoices[0] + '\n'
        for choiceIndex in range(1, len(listOfChoices)):
            displayString += '{0} - {1}\n'.format(choiceIndex, listOfChoices[choiceIndex])
        self.sv.set(displayString)

    def hide(self):
        self.bigLabel.grid_forget()

    def show(self):
        self.bigLabel.grid()
