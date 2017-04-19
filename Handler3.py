#!/usr/bin/env python

import threading
import time
import logging
import sys
import serial
from GPIO_Class import GPIO_Class
from Thread_Data_Object import Thread_Data
from FPS_Class import FPS_Class
GPIO = GPIO_Class()

class Handler(object):
    def __init__(self, guiEditor, observer):
		
		self.TD = Thread_Data(guiEditor)
		self.fps = FPS_Class()
		self.guiEditor = guiEditor

		self.port = serial.Serial(
				"/dev/ttyAMA0",
				baudrate=9600,
				timeout=None)	# <12>port = None

		#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

		self.running = False
		self.observer = observer
		self.observer.addTimeoutListener(self.onTimeout)
		pass

    def onTimeout(self):
        print 'THE HANDLER NOW KNOWS ABOUT A TIMEOUT :D'

    def DoWorkerThread(self):
        threads = []
        
        C = threading.Thread(name='Csense', target=self.Csense)
        F = threading.Thread(name='FPS', target=self.Fingerprint)
        T = threading.Thread(name='Timer', target=self.Timer, args=(300,))


        threads.append(C)
        threads.append(F)
        threads.append(T)

        
        C.start()
        F.start()
        T.start()
        while self.TD.get_Sec_Count() < 100:
            if self.TD.get_Sec_Count() >= 70:
                self.TD.set_Sys_State('shutdown')
            # elif self.TD.get_Sec_Count() >= 40:
            #     self.TD.set_Display_State('HelloWorld')
            # elif self.TD.get_Sec_Count() >= 20:
            #     self.TD.set_Display_State('EyeImage')
            # elif self.TD.get_Sec_Count() >= 0:
            #     self.TD.set_Display_State('HelloWorld')
            #elif self.TD.get_Sec_Count() >= 10 and self.TD.get_Alert_State() != 'green':
                #self.TD.set_Sys_State('identify')
                #self.TD.set_Display_State('Input')
            time.sleep(1)

    def StartWorkerThreads(self):
        self.running = True
        workerThreads = threading.Thread(name='DoWorkerThread', target=self.DoWorkerThread)
        workerThreads.start()

    def Fingerprint(self):
        Sys=self.TD.get_Sys_State()
        counter=0
        while Sys!='shutdown' and self.running:
            logging.debug('IDLE')
            if Sys=='enroll':
                logging.debug('enroll')
                ID=input('Enter 7 digit ID Number: \n')
                OW=input('Enable Overwrite: \n(1-enable, 0-disable)\n')
                self.fps.FPS_Get_Template(ID,OW)
                self.TD.set_Sys_State('idle')
                logging.debug('Changing sys to idle')
            if Sys=='identify':
                logging.debug('IDENTIFY')
                ID = 2765750;
                self.TD.set_Display_State('FingerPrompt')
                if self.fps.FPS_Identify(ID):
                    self.TD.set_Display_State('UserFound')
                    self.TD.set_Alert_State('green')
                    logging.debug('Changing alert to green')
                    self.TD.set_Sys_State('idle')
                    logging.debug('Changing sys to idle')
                else:
                    self.TD.set_Display_State('UserNotFound')
            Sys = self.TD.get_Sys_State()
            time.sleep(.5)
            counter = counter+1
            if counter==300:
                sys.exit(0)
        logging.debug('Fingerprint shutting Down')

    def Alert(self,LED_COLOR):
		logging.debug('updating LED')
		self.TD.set_Alert_State(LED_COLOR)
		GPIO.LED_ON(LED_COLOR)

    def Timer(self, max_seconds):
        counter = 0
        while counter <= max_seconds and self.running:
            #logging.debug(counter)
            time.sleep(.1)
            counter = counter+.1
            self.TD.set_Sec_Count(counter)

        logging.debug('Timer counted to %d seconds', max_seconds)

    def Csense(self):
		Alert=self.TD.get_Alert_State()
		Sys=self.TD.get_Sys_State()
		counter=0
		self.Alert("blue_")

		while Sys!='shutdown' and self.running:
			logging.debug('Checking Button')
			Alert=self.TD.get_Alert_State()
			Sys=self.TD.get_Sys_State()



			if GPIO.ReadButton() and Alert=="blue_":
				self.Alert("red__")
			elif Alert=="red__":
				time.sleep(10)
				self.Alert("blue_")

			time.sleep(.1)
		GPIO.Cleanup()
		logging.debug('Csense shutting Down')
