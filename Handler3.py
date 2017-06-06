#!/usr/bin/env python
import subprocess
import threading
import time
import logging
import sys
import os
import serial
from GPIO_Class import GPIO_Class
from FPS_Class import FPS_Class
from Database import template_database
from Client_Class import Net_DB_Client
GPIO = GPIO_Class()
threads = []


#Handler is a class that handles the majority of the overall system logic, its most important functions 
#include 
#	resetting the GUI loop by checking the last display template and updating the display template
#	Starting a thread that communicates with the fingerprint sensor
#	Starting a thread that polls the machine status current sensor
#	connecting to the server and retrieving data using client class

class Handler(object):
	def __init__(self, guiEditor, observer,Working_directory, Running,root,TD):
		self.directory = Working_directory;
		self.TD = TD
		self.fps = FPS_Class(self.TD)
		self.guiEditor = guiEditor
		self.root = root
		self.port = serial.Serial(
				"/dev/ttyAMA0",
				baudrate=9600,
				timeout=None)	# <12>port = None
		self.running = Running
		self.observer = observer

		#GUI observer calls onTimeout when it detects a kernel timeout event
		self.observer.addTimeoutListener(self.onTimeout) 

		#GUI observer calls onInput_H when it detects user has pressed a key,
		#	note that Display State factory also receives notice of on input and it actually processes the input,
		#	handler is just made aware an input event occurred
		self.observer.addInputListener(self.onInput_H) 
		pass

	def onTimeout(self):
		print 'THE HANDLER NOW KNOWS ABOUT A TIMEOUT :D'
		#on timeout call flow logic to reset the GUI loop,
		self.FlowLogic(self.TD.get_Display_State(),1,9999)#9999 is placeholder input for timeout

		
	def onInput_H(self,input_from_GUI):
                print 'THE HANDLER NOW KNOWS ABOUT AN INPUT :D'
                #on input call flow logic to reset the GUI loop, flow logic resets the timer by updating the display state
                self.FlowLogic(self.TD.get_Display_State(),0,input_from_GUI)
                



	def DoWorkerThread(self):
		#turn LEDs on for testing on startup
		GPIO.LED_ON("yellow")
		time.sleep(.5)
		GPIO.LED_ON("blue")
		time.sleep(.5)
		GPIO.LED_ON("red")
		time.sleep(.5)
		GPIO.LED_ON("green")
		time.sleep(.5)
		GPIO.LED_ON("blue")

		#initialize current sensing looping thread
		C = threading.Thread(name='Csense', target=self.Csense)
		threads.append(C)
		C.start()

		#start the GUI loop with welcome 1
		self.FlowLogic('Welcome1',1,9999)

	def StartWorkerThreads(self):
		#runs slow handler initializations on a separate thread so GUI loop starts before worker threads is finished
		self.running = True
		workerThreads = threading.Thread(name='DoWorkerThread', target=self.DoWorkerThread)
		workerThreads.start()
		
	def Fingerprint(self):
		#identifies user on a separate thread, if the sensor freezes the GUI doesnt freeze
		ID=self.TD._ID #gets ID number from Global Data
		print 'entering identify thread'
		FPS_Return = self.fps.FPS_Identify(ID) #uses FPS class to identify user
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
			self.TD.set_Display_State('NotRead')
			self.guiEditor.updateState('NotRead')

		elif FPS_Return==3:
			print "ID did not match fingerprint"
			self.TD.set_Display_State('NoMatch')
			self.guiEditor.updateState('NoMatch')
		else: 
			self.TD.set_Display_State('NoMatch')
			self.guiEditor.updateState('NoMatch')





	def Alert(self,LED_COLOR): #changes LED color and also change global variable describing alert condition
		print LED_COLOR
		self.TD.set_Alert_State(LED_COLOR)
		GPIO.LED_ON(LED_COLOR)


	def Csense(self): #loop while polling the current sensor, ignore sys states they dont do anything anymore, 
		Alert=self.TD.get_Alert_State()
		Sys=self.TD.get_Sys_State()
		time.sleep(3)

		while Sys!='shutdown' and self.running:
			Alert=self.TD.get_Alert_State()
			Sys=self.TD.get_Sys_State()
			result =0 
			for i in range (1,200):
				result += GPIO.ReadButton()
				time.sleep(.01)
			print result
			if result>50 and Alert =="blue": #if C sense reports high signals above threshold 50 and alert is blue, change condition to red
				self.Alert("red")
				self.TD.set_Display_State('TurnOff')
				self.guiEditor.updateState('TurnOff')
				self.TakePicture()

			time.sleep(.1)
		GPIO.Cleanup() #cleanup and shutdown occur when running is set to false, when Enrolling a user
		print ("Csense shutting down")
		logging.debug('Csense shutting Down')
		
	def FlowLogic(self,display_state,timeout_condition,flow_input):
		#this is a very long function but it is pretty simple, it just repeats a lot. 
		#	first it will try to convert the flow input to a number, the user may have presed + or - keys so it will fail, catch the exception, and move on
		#	Then it checks the previous display
		#		if the previous display state ended on a timeout, then a certain display state should be next 
		#		if the previous display state ended on an input, use the input, or assume it was enter to determine next display state
		#	This logic is hard to follow but it identical to the flow logic diagram on the product architecture section of the report
		try:
			try: 
				if type(flow_input)==type(''):
					if len(flow_input)>0:
						flow_input=int(flow_input)
			except Exception as e:
				print e
				flow_input = ' '


			if display_state=='Welcome1': #Do this after welcome has finished
					if timeout_condition: #function called on timeout
						self.Alert("blue")
						self.TD.set_Display_State("Welcome2") 
						self.guiEditor.updateState('Welcome2')#stay on welcome screen
					else:
						self.TD.set_Display_State("PromptUserID")        
						self.guiEditor.updateState('PromptUserID')#if user has pressed 1, move on

			elif display_state=='Welcome2': #Do this after welcome has finished
					if timeout_condition: #function called on timeout
						self.Alert("blue")
						self.TD.set_Display_State("Welcome1") 
						self.guiEditor.updateState('Welcome1')#stay on welcome screen
					else:
						self.TD.set_Display_State("PromptUserID") 
						self.guiEditor.updateState('PromptUserID')#if user has pressed 1 move on

			elif display_state=='PromptUserID': #Do this after PromptUserID has finished
				ID = flow_input
				if timeout_condition: #function called on timeout
						self.TD.set_Display_State("Welcome1") 
						self.guiEditor.updateState('Welcome1')#go to  welcome screen
				elif self.Check_ID_is_7_digits(ID):
					try:
						Training_Level=self.AuthorizationDatabase(ID)
						self.TD._ID=ID
						if Training_Level==0:
							self.TD.set_Display_State("UserNotFound") 
							self.guiEditor.updateState('UserNotFound')
						elif Training_Level==1 or Training_Level==2 or Training_Level==3 or Training_Level==4:
							self.TD.RunTimeMessage = str(ID)
							self.TD.set_Display_State('ID_Echo')
							self.guiEditor.updateState('ID_Echo')
					except Exception as e: 
						print e 
				else: #if ID is not 7 digits
					self.TD.set_Display_State("ID_Not_Valid") 
					self.guiEditor.updateState('ID_Not_Valid')

			elif display_state=='ID_Echo':
					if timeout_condition:
						self.TD.set_Display_State('Logout')
						self.guiEditor.updateState('Logout')
					else: 
						if flow_input==1:
							ID=self.TD._ID
							Training_Level=self.TD._Training_Level
							if Training_Level==1:
								self.TD.set_Display_State("NotAuthorized")
								self.guiEditor.updateState('NotAuthorized')
							elif Training_Level==2:
								self.TD.set_Display_State('ConditionalAuthorization')
								self.guiEditor.updateState('ConditionalAuthorization')
							elif Training_Level==3:
								self.TD.set_Display_State('AuthorizedGreen')
								self.guiEditor.updateState('AuthorizedGreen')
							elif Training_Level==4:
								self.TD.set_Display_State('AuthorizedSupervisor')  
								self.guiEditor.updateState('AuthorizedSupervisor')                           
						elif flow_input==2:
							self.TD.set_Display_State('PromptUserID')
							self.guiEditor.updateState('PromptUserID')

			elif display_state=='ID_Not_Valid':
					if timeout_condition: #function called on timeout
					        self.TD.set_Display_State('Logout')
					        self.guiEditor.updateState('Logout')
					else:
						if flow_input==1:
				        		self.TD.set_Display_State("PromptUserID") 
			                	self.guiEditor.updateState('PromptUserID')
				        if flow_input==2:
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
					        if flow_input==2:
					                self.TD.set_Display_State('Logout')
					                self.guiEditor.updateState('Logout')

			elif display_state =='NotAuthorized':#Do this after NotAuthorized has finished
					self.TD.set_Display_State('Logout')
					self.guiEditor.updateState('Logout')

			elif display_state =='Logout': #Do this after NotAuthorized has finished
					self.Alert('blue')
					self.TD.set_Display_State('Welcome1')
					self.guiEditor.updateState('Welcome1')

			elif display_state=='ConditionalAuthorization':
					if timeout_condition:
						self.TD.set_Displapy_State('Logout')
						self.guiEditor.updateState('Logout')
					else:
						self.TD.set_Display_State('ModOption')
						self.guiEditor.updateState('ModOption')


			elif display_state=='ModOption':
					if timeout_condition:
					        self.TD.set_Displapy_State('Logout')
					        self.guiEditor.updateState('Logout')
					else:
						if flow_input==1:
							self.TD.set_Display_State('ModPrep1')
							self.guiEditor.updateState('ModPrep1')
						if flow_input==2:
							self.TD.set_Display_State('ModPrep2')
							self.guiEditor.updateState('ModPrep2')
						if flow_input==3:
							self.TD.set_Display_State('ModPrep3')
							self.guiEditor.updateState('ModPrep3')

			elif display_state=='ModPrep1':
					self.TD.set_Display_State('ModClear1')
					self.guiEditor.updateState('ModClear1')

			elif display_state=='ModPrep2':
					self.TD.set_Display_State('ModClear2')
					self.guiEditor.updateState('ModClear2')

			elif display_state=='ModPrep3':
					self.TD.set_Display_State('ModClear3')
					self.guiEditor.updateState('ModClear3')

			elif display_state=='ModClear1':
				if timeout_condition:
					self.TD.set_Display_State('Mod1')
					self.guiEditor.updateState('Mod1')

			elif display_state=='ModClear2':
				if timeout_condition:
					self.TD.set_Display_State('Mod2')
					self.guiEditor.updateState('Mod2')

			elif display_state=='ModClear3':
				if timeout_condition:
					self.TD.set_Display_State('Mod3')
					self.guiEditor.updateState('Mod3')

			elif display_state=='Mod1':
					self.TD.set_Display_State('Rewatch')
					self.guiEditor.updateState('Rewatch')

			elif display_state=='Mod2':
					self.TD.set_Display_State('Rewatch')
					self.guiEditor.updateState('Rewatch')

			elif display_state=='Mod3':
					self.TD.set_Display_State('Rewatch')
					self.guiEditor.updateState('Rewatch')

			elif display_state=='Rewatch':
				if timeout_condition:
					self.TD.set_Display_State('Logout')
					self.guiEditor.updateState('Logout')
				else:
					if flow_input==1:
						self.TD.set_Display_State('ModOption')
						self.guiEditor.updateState('ModOption')
					if flow_input==2:
						self.IdentifyUser()
						time.sleep(1.5)
						self.TD.set_Display_State('FPSinput')
						self.guiEditor.updateState('FPSinput')			

			elif display_state=='AuthorizedGreen':
				if flow_input==1:
					self.TD.set_Display_State('ModOption')
					self.guiEditor.updateState('ModOption')
				if flow_input==2:
					self.IdentifyUser()
					time.sleep(1.5)
					self.TD.set_Display_State('FPSinput')
					self.guiEditor.updateState('FPSinput')

			elif display_state=='AuthorizedSupervisor':
					self.Alert('green')
					self.TD.set_Display_State('UseMachineGreen')
					self.guiEditor.updateState('UseMachineGreen')
	                
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


			elif display_state=='TurnOff':
					if timeout_condition:
						self.Alert("blue")
						self.TD.set_Display_State('Welcome1')
						self.guiEditor.updateState('Welcome1')
					else:
						self.Alert("blue")
						self.TD.set_Display_State('Welcome1')
						self.guiEditor.updateState('Welcome1')

			elif display_state=='NoMatch':
					if timeout_condition:
					    self.TD.set_Display_State('Logout')
					    self.guiEditor.updateState('Logout')
					else:
					    if flow_input==1:
							self.IdentifyUser()
							time.sleep(1.5)
							self.TD.set_Display_State('FPSinput')
							self.guiEditor.updateState('FPSinput')
					    elif flow_input==2:
							self.TD.set_Display_State('Logout')
							self.guiEditor.updateState('Logout')

			elif display_state=='NotRead':
					if timeout_condition:
					    self.TD.set_Display_State('Logout')
					    self.guiEditor.updateState('Logout')
					else:
					    if flow_input==1:
							self.IdentifyUser()
							time.sleep(1.5)
							self.TD.set_Display_State('FPSinput')
							self.guiEditor.updateState('FPSinput')
					    elif flow_input==2:
							self.TD.set_Display_State('Logout')
							self.guiEditor.updateState('Logout')

			elif display_state=='ServerDown':
						self.TD.set_Display_State('Logout')
						self.guiEditor.updateState('Logout')
                        
		except Exception as e:
			print e
                        

	def Check_ID_is_7_digits(self,ID): #function makes sure ID number is 7 digits with no initial zeros
		if ID>999999:
			return ID<10000000
	def AuthorizationDatabase(self,ID): #function reads database for training level
		if ID==9999999:
			self.EnrollUser()
			self.TD._Training_Level = 0
		elif ID==7777777:
			self.TD.set_Display_State('AuthorizedSupervisor')  
			self.guiEditor.updateState('AuthorizedSupervisor')  
			self.TD._Training_Level = 5
		# elif ID==1234567: #for prototype presentation
		# 	self.TD._Training_Level = 2
		# elif ID==7654321: #for prototype presenation
		# 	self.TD._Training_Level = 3
		else:
			try: #try to connect to the client
				Network_Client = Net_DB_Client()
				Network_Client.Connect()
				Data = Network_Client.Request_User_Data(ID)
				self.TD._Training_Level = int(Data[1]) #if succesful store the users training level and
				self.TD._UserTemplate = Data[2]# users fingerprint template globally for using when scanning
				Network_Client = None #reset network client to None class
			except Exception as e:
				print e
				self.TD._Training_Level = 5 #5 is not a valid training and this removes the permission number of the previous user 
				self.TD._UserTemplate = 'notemplate' #failure to retrieve template means no template can be scanned
				self.TD.set_Display_State('ServerDown') #create server down display state
				self.guiEditor.updateState('ServerDown') 
				raise e #raise the exception
		return self.TD._Training_Level

		
	def IdentifyUser(self): #function uses sensor to identify user
		F = threading.Thread(name='FPS', target=self.Fingerprint)
		threads.append(F)
		F.start()

	def EnrollUser(self): #function kills app to enroll a new user,this a sloppy way of enrolling a user because App doesnt like to be terminated in this fashion
		self.running=False #stop running C sense
		time.sleep(5)
		self.root.destroy() #destroy the full screen display
		subprocess.call('python '+ self.directory +'/Enroll.py', shell=True) #call another process to enroll the user

	def TakePicture(self):
		subprocess.call('/usr/bin/python3 '+ self.directory +'/Camera.py', shell=True)



