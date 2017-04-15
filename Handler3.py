#!/usr/bin/env python

import threading
import time
import logging
import sys
import serial
from App import mainGuiLoop

from GPIO_Class import GPIO_Class
LED=GPIO_Class()
Button=GPIO_Class()

from Thread_Data_Object import Thread_Data
TD=Thread_Data()

from FPS_Class import FPS_Class
fps=FPS_Class()

port = serial.Serial(
        "/dev/ttyAMA0",
        baudrate=9600,
        timeout=None)	# <12>port = None

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

running = False

def Fingerprint():

  Sys=TD.get_Sys_State()
  counter=0
  while Sys!='shutdown' and running:
      logging.debug('IDLE')
      if Sys=='enroll':
          logging.debug('enroll')
          ID=input('Enter 7 digit ID Number: \n')
          OW=input('Enable Overwrite: \n(1-enable, 0-disable)\n')
          fps.FPS_Get_Template(ID,OW)
          TD.set_Sys_State('idle')
          logging.debug('Changing sys to idle')
      if Sys=='identify':
         logging.debug('IDENTIFY')
         ID=input('Enter 7 digit ID Number: \n')
         if fps.FPS_Identify(ID):
             TD.set_Alert_State('green')
             logging.debug('Changing alert to green')
         TD.set_Sys_State('idle')
         logging.debug('Changing sys to idle')
      Sys=TD.get_Sys_State()
      time.sleep(.5)
      counter=counter+1
      if counter==300:
          sys.exit(0)
  logging.debug('Fingerprint shutting Down')

def Alert():
  Alert=TD.get_Alert_State()
  Sys=TD.get_Sys_State()
  LED.InitLED()
  counter=0
  while Sys!='shutdown' and running:
      logging.debug('updating LED')
      Alert=TD.get_Alert_State()
      Sys=TD.get_Sys_State()
      LED.LED_ON(Alert)
      time.sleep(.5)
      counter=counter+1
      if counter==300:
          sys.exit(0)

  LED.Cleanup()
  logging.debug('Alert shutting Down')

def Timer(max_seconds):
  counter=0
  while counter<=max_seconds and running:
      #logging.debug(counter)
      time.sleep(.1)
      counter=counter+.1
      TD.set_Sec_Count(counter)

  logging.debug('Timer counted to %d seconds',max_seconds)



def Csense():
  Alert=TD.get_Alert_State()
  Sys=TD.get_Sys_State()
  Button.InitButton()
  counter=0
  while Sys!='shutdown' and running:
      logging.debug('Checking_Button')
      Alert=TD.get_Alert_State()
      Sys=TD.get_Sys_State()
      if Button.ReadButton():
          Alert=TD.get_Alert_State()
          if Alert=='blue_':
            TD.set_Alert_State('red__')
            logging.debug('Changing alert to red')
            time.sleep(.5)
      else:
        if Alert=='red__':
            time.sleep(2)
            TD.set_Alert_State('blue_')
            logging.debug('Changing alert to blue')
      time.sleep(.5)
      counter=counter+1
      if counter==300:
          sys.exit(0)

  Button.Cleanup()
  logging.debug('Csense shutting Down')


threads=[]
def main():
  A=threading.Thread(name='Alert',target=Alert)
  C=threading.Thread(name='Csense',target=Csense)
  F=threading.Thread(name='FPS',target=Fingerprint)
  T=threading.Thread(name='Timer',target=Timer,args=(300,))
  G=threading.Thread(name='GUI', target=mainGuiLoop)

  threads.append(A)
  threads.append(C)
  threads.append(F)
  threads.append(T)
  threads.append(G)
  A.start()
  C.start()
  F.start()
  T.start()
  G.start()
  while TD.get_Sec_Count()<100:

        if TD.get_Sec_Count()>=70:
            TD.set_Sys_State('shutdown')
        elif TD.get_Sec_Count()>=10 and TD.get_Alert_State()!='green':
            TD.set_Sys_State('identify')
        time.sleep(1)



if __name__ == "__main__":
    try:
        running = True
        main()
    except Exception as e:
        print e
        port.close()
    finally:
        time.sleep(2)
        port.close()
        print("Handler_Shutting_Down")
        running = False
