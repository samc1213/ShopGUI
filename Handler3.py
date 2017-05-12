#!/usr/bin/env python
import subprocess
import threading
import time
import logging
import sys
import serial
from GPIO_Class import GPIO_Class
from Thread_Data_Object import Thread_Data
from FPS_Class import FPS_Class
from Database import template_database
from Client_Class import Net_DB_Client
GPIO = GPIO_Class()
threads = []



class Handler(object):
	def __init__(self, guiEditor, observer,Working_directory, Running,root):
		self.directory = Working_directory;
		self.TD = Thread_Data()
		self.fps = FPS_Class(self.TD)
		self.guiEditor = guiEditor
		self.root = root
		self.host = 'localhost'
		self.NetworkPort = 8089
		self.port = serial.Serial(
				"/dev/ttyAMA0",
				baudrate=9600,
				timeout=None)	# <12>port = None



		#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

		self.running = Running
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
		GPIO.LED_ON("yellow")
		time.sleep(.5)
		GPIO.LED_ON("blue")
		time.sleep(.5)
		GPIO.LED_ON("red")
		time.sleep(.5)
		GPIO.LED_ON("green")
		time.sleep(.5)
		GPIO.LED_ON("blue")

		C = threading.Thread(name='Csense', target=self.Csense)
		
		T = threading.Thread(name='Timer', target=self.Timer, args=(300,))


		threads.append(C)
		threads.append(T)


		C.start()
		T.start()

		self.FlowLogic('Welcome1',1,9999)

	def StartWorkerThreads(self):
		self.running = True
		workerThreads = threading.Thread(name='DoWorkerThread', target=self.DoWorkerThread)
		workerThreads.start()
		

	def Fingerprint(self):
		ID=self.TD._ID
		print 'entering identify thread'
		FPS_Return = self.fps.FPS_Identify(ID)
		if FPS_Return == 1:
			print "userfound"
			if self.TD._Training_Level == 3:
				self.Alert('green')
				self.TD.set_Display_State('UseMachineGreen')
				self.guiEditor.updateState('UseMachineGreen')
			else:
				self.Alert('yellow')
				self.TD.set_Display_State('UseMachineYellow')
				self.guiEditor.updateState('UseMachineYellow')
		elif FPS_Return==2:
			print "finger was not detected"
			self.TD.set_Display_State('Logout')
			self.guiEditor.updateState('Logout')

		elif FPS_Return==3:
			print "ID did not match fingerprint"
			self.TD.set_Display_State('NoMatch1')
			self.guiEditor.updateState('NoMatch1')
		elif FPS_Return==0:
			print "user not found in database"
			self.TD.set_Display_State('NoMatch1')
			self.guiEditor.updateState('NoMatch1')
		else: 
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
		self.Alert("blue")

		while Sys!='shutdown' and self.running:
			logging.debug('Checking Button')
			Alert=self.TD.get_Alert_State()
			Sys=self.TD.get_Sys_State()



			# if GPIO.ReadButton() and Alert=="blue":
			# 	self.Alert("red")
			# 	self.TD.set_Display_State('TurnOff')
			# 	self.guiEditor.updateState('TurnOff')


			time.sleep(.1)
		GPIO.Cleanup()
		print ("Csense shutting down")
		logging.debug('Csense shutting Down')
		
	def FlowLogic(self,display_state,timeout_condition,flow_input):
		if type(flow_input)==type(''):
			if len(flow_input)>0:
				flow_input=int(flow_input)

		if display_state=='Welcome1': #Do this after welcome has finished
				if timeout_condition: #function called on timeout
					self.Alert('blue')
					self.TD.set_Display_State("Welcome2") 
					self.guiEditor.updateState('Welcome2')#stay on welcome screen
				else:
					self.TD.set_Display_State("PromptUserID")        
					self.guiEditor.updateState('PromptUserID')#if user has pressed 1, move on

		elif display_state=='Welcome2': #Do this after welcome has finished
				if timeout_condition: #function called on timeout
					self.Alert('blue')
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
						print Training_Level
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
						elif Training_Level==3:
							self.TD._ID=ID
							self.TD.set_Display_State('AuthorizedGreen')
							self.guiEditor.updateState('AuthorizedGreen') 
                             
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
				self.Alert('blue')
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
				self.TD.set_Display_State('VidOption')
				self.guiEditor.updateState('VidOption')

		elif display_state=='AuthorizedGreen':
				self.IdentifyUser()
				self.TD.set_Display_State('fpsInput1')
				self.guiEditor.updateState('fpsInput1')


                
		elif display_state=='UseMachineGreen':
				if timeout_condition:
				        self.TD.set_Display_State('Logout')
				        self.guiEditor.updateState('Logout')
				else:
				        self.TD.set_Display_State('Logout')
				        self.guiEditor.updateState('Logout')

		elif display_state=='UseMachineYellow':
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

                elif display_state=='TurnOff':
                        if timeout_condition:
                                self.TD.set_Display_State('Logout')
                                self.guiEditor.updateState('Logout')
                        else:
                                self.TD.set_Display_State('Logout')
                                self.guiEditor.updateState('Logout')
        
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

		elif display_state=='ServerDown':
			    self.TD.set_Display_State('Logout')
			    self.guiEditor.updateState('Logout')


                        
                        

	def Check_ID_is_7_digits(self,ID): #function makes sure ID number is correct
		if ID>999999:
			return ID<10000000
	def AuthorizationDatabase(self,ID): #function reads database for training level
		#function not yet implemented, enter a training level to return for testing purposes
		if ID==9999999:
			self.EnrollUser()
			self.TD._Training_Level = 0
		else:
			try:
				Network_Client = Net_DB_Client(self.host,self.NetworkPort)
				Network_Client.Connect()
				Data = Network_Client.Request_User_Data(ID)
				self.TD._Training_Level = int(Data[1]) 
				self.TD._UserTemplate = Data[2]
				Network_Client = None
			except Exception as e:
				print e
				self.TD._Training_Level = 5
				self.TD._UserTemplate = 'notemplate'
				self.TD.set_Display_State('ServerDown')
				self.guiEditor.updateState('ServerDown') 
		return self.TD._Training_Level

		
	def IdentifyUser(self): #function reads database for fingerprint template
		F = threading.Thread(name='FPS', target=self.Fingerprint)
		threads.append(F)
		F.start()

	def EnrollUser(self):
		self.running=False
		time.sleep(5)
		self.root.destroy()
		subprocess.call('python '+ self.directory +'/Enroll.py', shell=True)
		os._exit(1)



