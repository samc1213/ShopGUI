import RPi.GPIO as GPIO
from time import sleep
import sys


#GPIO.setwarnings(False) uncomment if using multiple GPIO programs on one PI

#setup
blue=37
red=15
green=13
yellow=22
off=0
on=1
channel_list=[blue,red,green,yellow]
button=18

class GPIO_Class(object):
    def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(channel_list,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(button,GPIO.IN)
		pass

    def All_off(self):
        for LED in channel_list:
            GPIO.output(LED,off)
    def LED_ON(self,color):
        channels=self.Color2ChannelList(color)
        self.All_off()
        
        for LEDChannel in channels:
            if LEDChannel!=0:
                GPIO.output(LEDChannel,on)
            
        
        
    def Color2ChannelList(self,color):
        null=0
        if color=='blue':
            return ([blue,null])
        if color=='red':
            return [red,0]
        if color=='green':
            return [green,null]
        if color=='yellow':
            return ([yellow,0])
        else:
            print("color not defined")
            exit(0)
    def ReadButton(self):
        return GPIO.input(button)
    def Cleanup(self):
        GPIO.cleanup()


        



