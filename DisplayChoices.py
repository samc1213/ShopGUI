from Constants import BIG_FONT_HEIGHT_FRACTION
from TextLabel import TextLabel
from Tkinter import StringVar
from AbstractDisplay import AbstractDisplay


class DisplayChoices(AbstractDisplay):
    def __init__(self, master, screen_height, onInput):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        self.sv = StringVar()
        self.bigLabel = TextLabel(master, self.sv, 0, 0, screen_height, BIG_FONT_HEIGHT_FRACTION)
        self.onInput = onInput
        master.bind("<Key>", self.onKeyPressed)

    def onKeyPressed(self, event):
        if self.choices is not None and event.char in [str(i) for i in range(1, len(self.choices))]:
            self.onInput(event.char)

    def updateText(self, listOfChoices):
        self.choices = listOfChoices
        displayString = listOfChoices[0] + '\n'
        for choiceIndex in range(1, len(listOfChoices)):
            displayString += '{0}\n'.format(listOfChoices[choiceIndex])
        self.sv.set(displayString)

    def hide(self):
        self.choices = None
        self.bigLabel.grid_forget()

    def show(self):
        self.bigLabel.grid()

    def updateBackground(self, newColor):
        self.bigLabel.updateBackground(newColor)

    def updateTextSize(self, newSize):
        self.bigLabel.updateTextSize(newSize)
