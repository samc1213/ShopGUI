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
threads = []

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
		self.observer.addInputListener(self.onInput_H)
		pass

	def onTimeout(self):
		print 'THE HANDLER NOW KNOWS ABOUT A TIMEOUT :D'
		
		self.FlowLogic(self.TD.get_Display_State(),1,9999)#9999 is default for timeout

		
	def onInput_H(self,input_from_GUI):
                print 'THE HANDLER NOW KNOWS ABOUT AN INPUT :D'

                self.FlowLogic(self.TD.get_Display_State(),0,input_from_GUI)
                



	def DoWorkerThread(self):


		C = threading.Thread(name='Csense', target=self.Csense)
		
		T = threading.Thread(name='Timer', target=self.Timer, args=(300,))


		threads.append(C)
		#threads.append(F)
		threads.append(T)


		C.start()
		#F.start()
		T.start()

		self.FlowLogic('Welcome1',1,9999)
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
		ID=self.TD._ID
		print 'entering identify thread'
		if self.fps.FPS_Identify(ID):
			print "userfound"
			self.TD.set_Display_State('UseMachine1')
			self.guiEditor.updateState('UseMachine1')
		else:
			print "usernotfound"
			self.TD.set_Display_State('NoMatch1')
			self.guiEditor.updateState('NoMatch1')


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
		
	def FlowLogic(self,display_state,timeout_condition,flow_input):
		if type(flow_input)==type(''):
			if len(flow_input)>0:
				flow_input=int(flow_input)

		if display_state=='Welcome1': #Do this after welcome has finished
				if timeout_condition: #function called on timeout
					self.TD.set_Display_State("Welcome2") 
					self.guiEditor.updateState('Welcome2')#stay on welcome screen
				else:
					self.TD.set_Display_State("PromptUserID")        
					self.guiEditor.updateState('PromptUserID')#if user has pressed 1, move on

		elif display_state=='Welcome2': #Do this after welcome has finished
				if timeout_condition: #function called on timeout
					self.TD.set_Display_State("Welcome1") 
					self.guiEditor.updateState('Welcome1')#stay on welcome screen
				else:
					self.TD.set_Display_State("PromptUserID") 
					self.guiEditor.updateState('PromptUserID')#if user has pressed 1 move on

		elif display_state=='PromptUserID': #Do this after PromptUserID has finished
				if timeout_condition: #function called on timeout
					self.TD.set_Display_State("Welcome1") 
					self.guiEditor.updateState('Welcome1')#go to  welcome screen
				else:
					ID = flow_input
					if self.Check_ID_is_7_digits(ID):
						Training_Level=self.AuthorizationDatabase(ID)
						if Training_Level==0:
							self.TD.set_Display_State("UserNotFound") 
							self.guiEditor.updateState('UserNotFound')
						elif Training_Level==1:
							self.TD._ID=ID
							self.TD.set_Display_State("NotAuthorized")
							self.guiEditor.updateState('NotAuthorized')
						elif Training_Level==2:
							self.TD._ID=ID
							self.TD.set_Display_State('FurtherTraining')
							self.guiEditor.updateState('FurtherTraining')
						elif Training_Leve==3:
							self.TD._ID=ID
							self.TD.set_Display_State('Authorized')
							self.guiEditor.updateState('Authorized')                             
					else: #if ID is not 7 digits
						self.TD.set_Display_State("ID_Not_Valid") 
						self.guiEditor.updateState('ID_Not_Valid')

		elif display_state=='ID_Not_Valid':
				if timeout_condition: #function called on timeout
				        self.TD.set_Display_State('Logout')
				        self.guiEditor.updateState('Logout')
				else:
				        if flow_input==1:
				                self.TD.set_Display_State("PromptUserID") 
				                self.guiEditor.updateState('PromptUserID')
				        elif flow_input==2:
				                self.TD.set_Display_State('Logout')
				                self.guiEditor.updateState('Logout')

		elif display_state=='UserNotFound':
				if timeout_condition: #function called on timeout
				        self.TD.set_Display_State('Logout')
				        self.guiEditor.updateState('Logout')
				else:
				        if flow_input==1:
				                self.TD.set_Display_State("PromptUserID") 
				                self.guiEditor.updateState('PromptUserID')
				        elif flow_input==2:
				                self.TD.set_Display_State('Logout')
				                self.guiEditor.updateState('Logout')

		elif display_state =='NotAuthorized':#Do this after NotAuthorized has finished
				self.TD.set_Display_State('Logout')
				self.guiEditor.updateState('Logout')

		elif display_state =='Logout': #Do this after NotAuthorized has finished
				self.TD.set_Display_State('Welcome1')
				self.guiEditor.updateState('Welcome1')

		elif display_state=='FurtherTraining':
				if timeout_condition:
					self.TD.set_Displapy_State('Logout')
					self.guiEditor.updateState('Logout')
				else:
					self.TD.set_Display_State('VidOption')
					self.guiEditor.updateState('VidOption')


		elif display_state=='VidOption':
				if timeout_condition:
				        self.TD.set_Displapy_State('Logout')
				        self.guiEditor.updateState('Logout')
				else:
				        if flow_input==1:
							self.TD.set_Display_State('Video_Prep1')
							self.guiEditor.updateState('Video_Prep1')
				        if flow_input==2:
							self.IdentifyUser()
							self.TD.set_Display_State('fpsInput1')
							self.guiEditor.updateState('fpsInput1')

		elif display_state=='Video_Prep1':
				self.TD.set_Display_State('Video1')
				self.guiEditor.updateState('Video1')

		elif display_state=='Video1':
				self.IdentifyUser()
				self.TD.set_Display_State('fpsInput1')
				self.guiEditor.updateState('fpsInput1')

		elif display_state=='Authorized':
				self.IdentifyUser()
				self.TD.set_Display_STate('fpsInput1')
				self.guiEditor.updateState('fpsInput1')

		elif display_state=='fpsInput1':
				self.TD.set_Display_State('Logout')
				self.guiEditor.updateState('Logout')

                
		elif display_state=='UseMachine1':
				if timeout_condition:
				        self.TD.set_Display_State('Logout')
				        self.guiEditor.updateState('Logout')
				else:
				        self.TD.set_Display_State('Logout')
				        self.guiEditor.updateState('Logout')

		# elif display_state=='NotRead1':
		# 		if timeoout_condition:
		# 		        self.TD.set_Display_State('Logout')
		# 		        self.guiEditor.updateState('Logout')
		# 		else:
		# 		        if flow_input==1:
		# 		                self.TD.set_Display_State('fpsInput1')
		# 		                self.guiEditor.updateState('fpsInput1')
		# 		        elif flow_input==2:
		# 		                self.TD.set_Display_State('Logout')
		# 		                self.guiEditor.updateState('Logout')

		elif display_state=='NoMatch1':
				if timeout_condition:
				    self.TD.set_Display_State('Logout')
				    self.guiEditor.updateState('Logout')
				else:
				    if flow_input==1:
						self.IdentifyUser()
						self.TD.set_Display_State('fpsInput1')
						self.guiEditor.updateState('fpsInput1')
				    elif flow_input==2:
						self.TD.set_Display_State('Logout')
						self.guiEditor.updateState('Logout')

		# elif display_state=='UseMachine2':
		# 		if timeout_condition:
		# 		    self.TD.set_Display_State('Logout')
		# 		    self.guieditor.updateState('Logout')
		# 		else:
		# 		    self.TD.set_Display_State('Logout')
		# 		    self.guieditor.updateState('Logout')
		# elif display_state=='NotRead2':
		# 		if timeoout_condition:
		# 		    self.TD.set_Display_State('Logout')
		# 		    self.guiEditor.updateState('Logout')
		# 		else:
		# 		    if flow_input==1:
		# 		        self.TD.set_Display_State('fpsInput2')
		# 		        self.guiEditor.updateState('fpsInput2')
		# 		    elif flow_input==2:
		# 		        self.TD.set_Display_State('Logout')
		# 		        self.guiEditor.updateState('Logout')
		# elif display_state=='NoMatch2':
		# 		if timeout_condition:
		# 		    self.TD.set_Display_State('Logout')
		# 		    self.guieditor.updateState('Logout')
		# 		else:
		# 		    if flow_input==1:
		# 		        self.TD.set_Display_State('fpsInput2')
		# 		        self.guieditor.updateState('fpsInput2')
		# 		    elif flow_input==2:
		# 		        self.TD.set_Display_State('Logout')
		# 		        self.guieditor.updateState('Logout')
                        
                        

	def Check_ID_is_7_digits(self,ID): #function makes sure ID number is correct
		if ID>999999:
			return ID<10000000
	def AuthorizationDatabase(self,ID): #function reads database for training level
		#function not yet implemented, enter a training level to return for testing purposes
		return 2
	def IdentifyUser(self): #function reads database for fingerprint template
                #function returns 0 if not read, 1 if doesn't match, 2 if matches                                                                                                                                                       
                #function not yet implemented, enter a fingerprint template to return for testing purposes
		F = threading.Thread(name='FPS', target=self.Fingerprint)
		threads.append(F)
		F.start()


