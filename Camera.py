#!/usr/bin/python3.4.2

from picamera import PiCamera
from time import sleep
import sys
import os
import datetime

print('sys.argv[0] =', sys.argv[0])             
pathname = os.path.dirname(sys.argv[0])
print('full path =', os.path.abspath(pathname)) 
Working_directory = os.path.abspath(pathname)


camera=PiCamera()

global picnum
picnum=1
camera.start_preview(alpha=0)
while (picnum<2):
	sleep(2)
	directory= Working_directory + '/Camera/'
	#filename= "test_image%s.jpg" % picnum
	Cdate='{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())
	filename = Cdate +'.jpg'
	print (directory + filename)
	camera.capture(Working_directory + filename)
	picnum=picnum+1
	print("picture taken")
    
camera.stop_preview()
sys.exit()


#camera.rotation=180 #use to change angle
