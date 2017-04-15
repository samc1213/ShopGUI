#!/usr/bin/env python

import threading
import time
import logging
import sys
import serial
from GPIO_Class import GPIO_Class
from Thread_Data_Object import Thread_Data
from FPS_Class import FPS_Class


class Handler(object):
    def __init__(self):
        self.LED = GPIO_Class()
        self.Button = GPIO_Class()
        self.TD = Thread_Data()
        self.fps = FPS_Class()

        self.port = serial.Serial(
                "/dev/ttyAMA0",
                baudrate=9600,
                timeout=None)	# <12>port = None

        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

        self.running = False

    def DoWorkerThread(self):
        threads = []
        A = threading.Thread(name='Alert', target=self.Alert)
        C = threading.Thread(name='Csense', target=self.Csense)
        F = threading.Thread(name='self.fps', target=self.Fingerprint)
        T = threading.Thread(name='Timer', target=Timer, args=(300,))

        threads.append(A)
        threads.append(C)
        threads.append(F)
        threads.append(T)

        A.start()
        C.start()
        F.start()
        T.start()
        while self.TD.get_Sec_Count()<100:
            if self.TD.get_Sec_Count()>=70:
                self.TD.set_Sys_State('shuself.TDown')
            elif self.TD.get_Sec_Count()>=10 and self.TD.get_Alert_State() != 'green':
                self.TD.set_Sys_State('identify')
            time.sleep(1)

    def StartWorkerThreads(self):
        self.running = True
        workerThreads = threading.Thread(name='DoWorkerThread', target=self.DoWorkerThread)
        workerThreads.start()

    def Fingerprint(self):
        Sys=self.TD.get_Sys_State()
        counter=0
        while Sys!='shuself.TDown' and self.running:
            logging.debug('IDLE')
            if Sys=='enroll':
                logging.debug('enroll')
                ID=input('Enter 7 digit ID Number: \n')
                OW=input('Enable Overwrite: \n(1-enable, 0-disable)\n')
                self.fps.self.fps_Get_Template(ID,OW)
                self.TD.set_Sys_State('idle')
                logging.debug('Changing sys to idle')
            if Sys=='identify':
                logging.debug('IDENTIFY')
                ID=input('Enter 7 digit ID Number: \n')
            if self.fps.self.fps_Identify(ID):
                self.TD.set_Alert_State('green')
                logging.debug('Changing alert to green')
                self.TD.set_Sys_State('idle')
                logging.debug('Changing sys to idle')
            Sys=self.TD.get_Sys_State()
            time.sleep(.5)
            counter=counter+1
            if counter==300:
                sys.exit(0)
        logging.debug('Fingerprint shutting Down')

    def Alert(self):
        Alert=self.TD.get_Alert_State()
        Sys=self.TD.get_Sys_State()
        self.LED.Initself.LED()
        counter=0
        while Sys!='shuself.TDown' and self.running:
            logging.debug('updating self.LED')
            Alert=self.TD.get_Alert_State()
            Sys=self.TD.get_Sys_State()
            self.LED.self.LED_ON(Alert)
            time.sleep(.5)
            counter=counter+1
            if counter==300:
                sys.exit(0)

        self.LED.Cleanup()
        logging.debug('Alert shutting Down')

    def Timer(self, max_seconds):
        counter=0
        while counter<=max_seconds and self.running:
            #logging.debug(counter)
            time.sleep(.1)
            counter=counter+.1
            self.TD.set_Sec_Count(counter)

            logging.debug('Timer counted to %d seconds',max_seconds)

    def Csense(self):
        Alert=self.TD.get_Alert_State()
        Sys=self.TD.get_Sys_State()
        self.Button.Initself.Button()
        counter=0
        while Sys!='shuself.TDown' and self.running:
            logging.debug('Checking_self.Button')
            Alert=self.TD.get_Alert_State()
            Sys=self.TD.get_Sys_State()
            if self.Button.Readself.Button():
                Alert=self.TD.get_Alert_State()
                if Alert=='blue_':
                    self.TD.set_Alert_State('red__')
                    logging.debug('Changing alert to red')
                    time.sleep(.5)
            else:
                if Alert=='red__':
                    time.sleep(2)
                    self.TD.set_Alert_State('blue_')
                    logging.debug('Changing alert to blue')
            time.sleep(.5)
            counter=counter+1
            if counter==300:
                sys.exit(0)
        self.Button.Cleanup()
        logging.debug('Csense shutting Down')
