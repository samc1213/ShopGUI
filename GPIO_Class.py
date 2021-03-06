import RPi.GPIO as GPIO
from time import sleep
import sys


#GPIO.setwarnings(False) uncomment if using multiple GPIO programs on one PI

#setup
blue=37
red=15
green=13
yellow=22
LargeRed=38
off=0
on=1
channel_list=[blue,red,green,yellow]
button=18

class GPIO_Class(object):
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel_list,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(LargeRed,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        pass

    def All_off(self):
        for LED in channel_list:
            GPIO.output(LED,off)
        GPIO.output(LargeRed,1);
    def LED_ON(self,color):
        channels=self.Color2ChannelList(color)
        self.All_off()
        
        for LEDChannel in channels:
            if LEDChannel!=0:
                if LEDChannel == LargeRed:
                    GPIO.output(LargeRed,0)
                else:
                    GPIO.output(LEDChannel,on)
            
        
        
    def Color2ChannelList(self,color):
        null=0
        if color=='blue':
            return ([blue,null])
        if color=='red':
            return [red,LargeRed]
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


        



