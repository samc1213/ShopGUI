# fingerprint_scanner.py - learn and recognize fingerprints with GT-511C3
# (c) BotBook.com - Karvinen, Karvinen, Valtokari

import time
import serial
import struct
import sys

STX1 = 0x55	# <1>
STX2 = 0xAA

CMD_OPEN = 				0x01	# <2>
CMD_CLOSE = 			0x02
CMD_LED = 				0x12
CMD_GET_ENROLL_COUNT = 	0x20
CMD_ENROLL_START = 		0x22
CMD_ENROLL_1 = 			0x23
CMD_ENROLL_2 = 			0x24
CMD_ENROLL_3 = 			0x25
CMD_IS_FINGER_PRESSED = 0x26
CMD_DELETE_ALL = 		0x41
CMD_IDENTIFY = 			0x51
CMD_CAPTURE_FINGER = 	0x60
CMD_GET_TEMPLATE= 0x70
CMD_SET_TEMPLATE=0x71

DATA1=0x5A
DATA2=0xA5


ACK = 0x30	# <3>
NACK = 0x31

port = serial.Serial(
        "/dev/ttyAMA0",
        baudrate=9600,
        timeout=None)	# <12>port = None

from Database import template_database as DB
database=DB()



class FPS_Class(object):
        def __init__(self,thread_data):
                self.thread_data=thread_data #pass global data to FPS to retrieve globally stored fingerprint templates
                pass




        def calcChecksum(self, package):	# checks to make sure data package is appropiate size
                checksum = 0
                for byte in package:
                        checksum += ord(byte)
                return int(checksum)

        def sendCmd(self, cmd, param = 0):	# sends data package to sensor
                package = chr(STX1)+chr(STX2)+struct.pack('<hih', 1, param, cmd)	# preparing the data package
                checksum = self.calcChecksum(package) #is data package appropiate size
                package += struct.pack('<h',checksum)	# #put size at the end of data package ( this is expected by sensor)

                sent = port.write(package) #serial write

                if(sent != len(package)):
                        print "Error communicating"
                        return -1

                recv = port.read(sent)	# expecting to receive acklowedgement
                recvPkg = struct.unpack('cchihh',recv)	# #unpacking the data package

                if recvPkg[4] == NACK: #negative acknowledgement
                        if recvPkg[3]==4106: #specific error code
                                print('Found no templates to remove')
                        else:
                                print("error: %s" % recvPkg[3]) #other error codes
                        return -2
                time.sleep(.1)
                return recvPkg[3] #return error code

        def get_template(self, cmd,ID_N,overwrite=0,param = 0):	# very specific commands to retrieve fingerprint template from sensor

                package = chr(STX1)+chr(STX2)+struct.pack('<hih', 1, param, cmd)	# send get template commande
                checksum = self.calcChecksum(package)  #creates last part of package to be sent to FPS
                package += struct.pack('<h',checksum)	#adds checksum to package

                sent = port.write(package) #writes package via serial

                if(sent != len(package)): #error check
                        print "Error communicating"
                        return -1

                recv = port.read(sent)	# receives aknowledgement or no acknowledgement from FPS
                recvPkg = struct.unpack('cchihh',recv)	# <9>

                if recvPkg[4] == NACK:
                        print("error: %s" % recvPkg[3])
                        return -2

                recvdata = port.read(4+498+2)	# #receives data1 byte, data 2 byte, device I 2bytes, 498 byte fingerprint template , 2 byte checksum at end

                package_data=list(recvdata)

                strdata=''
                for item in package_data:
                        item=item.encode("hex")

                        strdata +=item

                self.thread_data._UserTemplate = strdata; #store fingerprint template on global thread data

                #time.sleep(1)
                return recvPkg[3]

        def set_template(self,cmd,ID_N,param=0): #store fingerprint template on sensor

                #send command
                package = chr(STX1)+chr(STX2)+struct.pack('<hih', 1, param, cmd)	# send get template commande
                checksum = self.calcChecksum(package)  #creates last part of package to be sent to FPS
                package += struct.pack('<h',checksum)	#adds checksum to package


                sent = port.write(package) #writes package via serial

                if(sent != len(package)): #error check
                        print "Error communicating"
                        return -1
                #receive command ack
                recv = port.read(sent)	# receives aknowledgement or no acknowledgement from FPS
                recvPkg = struct.unpack('cchihh',recv)	# <9>

                if recvPkg[4] == NACK:
                        print("error: %s" % recvPkg[3])
                        return -2
                        
                template = self.thread_data._UserTemplate;
                if template=='notemplate':
                        print('ID not found in database')
                        return 0
                else:

                        data_list=map(ord,template.decode("hex")) #decodes the hex template into list of numbers
                        data_package= ''
                        for item in data_list:
                                data_package+=struct.pack('c',chr(item)) #encodes list of numbers into string of characters

                        sent2 = port.write(data_package) #writes package via serial
                        if(sent2 != len(data_package)): #error check
                                print "Error communicating"
                                return -1
                        recv = port.read(sent)	# receives aknowledgement or no acknowledgement from FPS
                        recvPkg = struct.unpack('cchihh',recv)	# <9>

                        if recvPkg[4] == NACK:
                                print("error: %s" % recvPkg[3])
                                return -2

                time.sleep(.1)
                return 1


        def startScanner(self): #open scanner communications
                print("Open scanner communications")
                self.sendCmd(CMD_OPEN)

        def stopScanner(self):
                print("Close scanner communications")
                self.sendCmd(CMD_CLOSE)


        def led(self,status = True): #turn on or off LED, no input means status is true
                if status:
                        self.sendCmd(CMD_LED,1)
                else:
                        self.sendCmd(CMD_LED,0)

        def enrollFail(self): #due this if enroll failed 
                print("Enroll failed")
                self.led(False)
                self.stopScanner()

        def identFail(self): #failed to identify user
                print("Ident failed")
                self.led(False)
                self.stopScanner()

        def startEnroll(self,ident): #sepcific command to begin enrolling
                self.sendCmd(CMD_ENROLL_START,ident)

        def waitForFinger(self,state): #very important, this section of the code stops waiting for a finger after 30 seconds!
            counter=0
            if(state):
                while(self.sendCmd(CMD_IS_FINGER_PRESSED) == 0 and counter<30):
                    time.sleep(0.9)
                    counter=counter+1
            else:
                while(self.sendCmd(CMD_IS_FINGER_PRESSED) > 0 and counter<30):
                    time.sleep(0.9)
                    counter=counter+1
            if counter==30:
                print("Stopped waiting for finger after 30 seconds")

        def captureFinger(self):
            return self.sendCmd(CMD_CAPTURE_FINGER)

        def enroll(self,state):
            if state == 1:
                return self.sendCmd(CMD_ENROLL_1)
            if state == 2:
                return self.sendCmd(CMD_ENROLL_2)
            if state == 3:
                return self.sendCmd(CMD_ENROLL_3)

        def identifyUser(self):
            return self.sendCmd(CMD_IDENTIFY)

        def getEnrollCount(self):
            return self.sendCmd(CMD_GET_ENROLL_COUNT)

        def removeAll(self):
            print("Removing all identities from scanner")
            return self.sendCmd(CMD_DELETE_ALL)
        def CheckIDsize(self,ID_N):
            if ID_N>=1000000 and ID_N <=9999999:
                return 1
            else:
                raise ValueError('ID number must be seven digits')

        def FPS_Get_Template(self,ID_N,overwrite=1): #saves fingerprint template with ID number
            self.CheckIDsize(ID_N)
            self.FPS_RemoveAll()
            result = self.FPS_Enroll_user()
            self.startScanner()
            print("Saving template to database: ID = %d" % ID_N)
            ident=0# identity number on fingerprint scanner always zero
            self.get_template(CMD_GET_TEMPLATE, ID_N,overwrite,ident)
            self.stopScanner()
            return result

        def FPS_Upload_Template(self,ID_N):
            self.CheckIDsize(ID_N)
            self.startScanner()
            self.removeAll()
            print("Uploading template to scanner: ID = %d" % ID_N)
            ident=0
            status = self.set_template(CMD_SET_TEMPLATE,ID_N,ident)
            self.stopScanner()
            return status


        def FPS_RemoveAll(self):
            self.startScanner()

            self.removeAll()

            self.stopScanner()

        def FPS_Identify(self,ID_N):
            status = self.FPS_Upload_Template(ID_N)
            if status == 0:
                return 0 #user was not found in database
            self.startScanner()
            self.led()

            print("Press finger to identify")
            self.waitForFinger(False)
            if self.captureFinger() < 0:	# <10>
                self.identFail()
                result = 2 #finger not detected
            ident = self.identifyUser()
            if(ident == 0):	# <11>
                print("Identity found: %d" % ID_N)
                result = 1 #identification was a success 
            else:
                print("User did not match")
                result = 3 #did not match
            self.led(False)
            self.stopScanner()
            return result

        def FPS_Enroll_user(self):
            self.startScanner()
            self.led()

            print("Start enroll")
            newID = self.getEnrollCount()
            print(newID)

            self.startEnroll(newID)
            print("Press finger to start enroll")
            self.waitForFinger(False)
            if self.captureFinger() < 0:
                    self.enrollFail()
                    return 0
            self.enroll(1)
            print("Remove finger")
            self.waitForFinger(True)


            print("Press finger again")
            self.waitForFinger(False)
            if self.captureFinger() < 0:
                    self.enrollFail()
                    return 0
            self.enroll(2)
            print("Remove finger")
            self.waitForFinger(True)

            print("Press finger again")
            self.waitForFinger(False)
            if self.captureFinger() < 0:
                    self.enrollFail()
                    return 0

            if self.enroll(3) != 0:
                    self.enrollFail()
                    return 0

            print("Remove finger")
            self.waitForFinger(True)

            print("Press finger again to identify")
            self.waitForFinger(False)
            if self.captureFinger() < 0:	# <10>
                    self.identFail()
                    return 0
            ident = self.identifyUser()
            if(ident >= 0 and ident < 200):	# <11>


                    print("Identity found: %d" % ident)
                    found = 1
            else:
                    print("User not found")
                    found = 0
            self.led(False)
            self.stopScanner()
            return found