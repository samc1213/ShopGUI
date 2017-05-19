import socket
import sys
import time


# This file should be edited to communicate with the online database. Request_User_Data currently returns
# a List that includes [ID, training level, encoded fingerprint template] . Any changes to the output of request user data should also be modified
# in the input of AuthorizationDatabase() inside of the Handler object. Furthermore, the input host and port of the Client may be modified in Handler
# or overwritten in the initialization portion of Net_DB Client
MachineType=1

class Net_DB_Client(object): #Network Database Class 
	def __init__(self):
		self.clientsocket = socket.socket()
		self.host = '192.168.1.150'
		self.port = 12345

		pass
		
	def Connect(self):
		try:
			self.clientsocket.connect((self.host, self.port))
		except Exception as e:
			print e
			print "server connection failed"
			raise e

	def Ping(self):
		self.clientsocket.send("ping")
		print "ping"
		data = self.clientsocket.recv(1024)
		print data
		if data != "pong":
			raise



	def Request_User_Data(self, ID):
		print "requesting ID = " + str(ID)
		self.clientsocket.send(str(ID))
		data = self.clientsocket.recv(1200)
		if len(data) > 0:
			if data == "ID not found":
				AuthorizationDatabaseMill = [ID,0,'notemplate']
				return AuthorizationDatabaseMill
			else:
				print data
				dataSplit = data.split(',')
				AuthorizationDatabaseMill = [dataSplit[0],dataSplit[MachineType],dataSplit[3]]
				return AuthorizationDatabaseMill
		else: 
			print "data came back empty"
			raise 

	def Send_User_Data(self,ID,Mill_Tl,Lathe_TL,FPS_Template):
		data = "Enroll User," + str(ID) + ',' + str(Mill_Tl) + ',' + str(Lathe_TL) + ',' + str(FPS_Template)
		self.clientsocket.send(data)

def Test():

	NDC= Net_DB_Client()
	NDC.Connect()
	#NDC.Ping()
	# Send = input( 'send or receive')
	# ID =input("enter ID \n")
	# if Send:
	# 	NDC.Send_User_Data(ID,3,4, "5aa5")
	# else:
	NDC.Request_User_Data('1234567')

if __name__ == '__main__':
	try:
		Test()             
		# s = socket.socket()        
		# host = '192.168.1.150'# ip of raspberry pi 
		# port = 12345               
		# s.connect((host, port))
		# print(s.recv(1024))
		# s.close()
	except Exception as e:
		print e
		raise e




