import sys
import os
import subprocess
from Thread_Data_Object import Thread_Data
from FPS_Class import FPS_Class
from Client_Class import Net_DB_Client

def PingPong():
	network_client = Net_DB_Client('localhost',8089)
	network_client.Connect()
	network_client.Ping()
	network_client = None



print('sys.argv[0] =', sys.argv[0])             
pathname = os.path.dirname(sys.argv[0])
print('full path =', os.path.abspath(pathname)) 
Working_directory = os.path.abspath(pathname)
TD=Thread_Data()
fps=FPS_Class(TD)




try: 
	while(1):
		PingPong()
		network_client = Net_DB_Client('localhost',8089)
		network_client.Connect()
		ID= input("Enter ID Number: \n")
		fps.FPS_Get_Template(ID)
		Mill_TL = input ("Mill training level: \n")
		Lathe_TL= input ("Lathe training level: \n")
		network_client.Send_User_Data(ID,Lathe_TL,Mill_TL, TD._UserTemplate )
		Continue = input("press 1 if you would like to continue or 0 to enroll again \n")
		network_client = None
		PingPong()
		if Continue:
			subprocess.call('python '+ Working_directory +'/App.py', shell=True)
			break
except Exception as e:
	print e

