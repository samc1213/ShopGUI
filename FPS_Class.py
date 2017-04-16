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
directory='/home/pi/Desktop/FPS_GPIO3'
filename=directory+'/template_database'


class FPS_Class(object):
        def __init__(self):
                pass




        def calcChecksum(self, package):	# <4>
                checksum = 0
                for byte in package:
                        checksum += ord(byte)
                return int(checksum)

        def sendCmd(self, cmd, param = 0):	# <5>
                package = chr(STX1)+chr(STX2)+struct.pack('<hih', 1, param, cmd)	# <6>
                checksum = self.calcChecksum(package)
                package += struct.pack('<h',checksum)	# <7>

                sent = port.write(package)

                if(sent != len(package)):
                        print "Error communicating"
                        return -1

                recv = port.read(sent)	# <8>
                recvPkg = struct.unpack('cchihh',recv)	# <9>

                if recvPkg[4] == NACK:
                        if recvPkg[3]==4106:
                                print('Found no templates to remove')
                        else:
                                print("error: %s" % recvPkg[3])
                        return -2
                time.sleep(.1)
                return recvPkg[3]

        def get_template(self, cmd,ID_N,overwrite=0,param = 0):	# <5>

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

                database.write_template(filename,ID_N,strdata,overwrite) #write to text file with accompanying ID



                time.sleep(1)
                return recvPkg[3]

        def set_template(self,cmd,ID_N,param=0):

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
                template=database.check_database(filename,ID_N)
                if template==0:
                        print('ID not found in database')
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

                time.sleep(1)
                return recvPkg[3]


        def startScanner(self):
                print("Open scanner communications")
                self.sendCmd(CMD_OPEN)

        def stopScanner(self):
                print("Close scanner communications")
                self.sendCmd(CMD_CLOSE)


        def led(self,status = True):
                if status:
                        self.sendCmd(CMD_LED,1)
                else:
                        self.sendCmd(CMD_LED,0)

        def enrollFail(self):
                print("Enroll failed")
                self.led(False)
                self.stopScanner()

        def identFail(self):
                print("Ident failed")
                self.led(False)
                self.stopScanner()

        def startEnroll(self,ident):
                self.sendCmd(CMD_ENROLL_START,ident)

        def waitForFinger(self,state):
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

        def FPS_Get_Template(self,ID_N,overwrite=0): #saves fingerprint template with ID number
            self.CheckIDsize(ID_N)
            self.FPS_RemoveAll()
            self.FPS_Enroll_user()
            self.startScanner()
            print("Saving template to database: ID = %d" % ID_N)
            ident=0# identity number on fingerprint scanner always zero
            self.get_template(CMD_GET_TEMPLATE, ID_N,overwrite,ident)
            self.stopScanner()

        def FPS_Upload_Template(self,ID_N):
            self.CheckIDsize(ID_N)
            self.startScanner()
            self.removeAll()
            print("Uploading template to scanner: ID = %d" % ID_N)
            ident=0
            self.set_template(CMD_SET_TEMPLATE,ID_N,ident)
            self.stopScanner()


        def FPS_RemoveAll(self):
            self.startScanner()

            self.removeAll()

            self.stopScanner()

        def FPS_Identify(self,ID_N):
            self.FPS_Upload_Template(ID_N)
            self.startScanner()
            self.led()

            print("Press finger to identify")
            self.waitForFinger(False)
            if self.captureFinger() < 0:	# <10>
                self.identFail()
                return
            ident = self.identifyUser()
            if(ident == 0):	# <11>
                print("Identity found: %d" % ID_N)
                result=1
            else:
                print("User not found")
                result=0
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
                    return
            self.enroll(1)
            print("Remove finger")
            self.waitForFinger(True)


            print("Press finger again")
            self.waitForFinger(False)
            if self.captureFinger() < 0:
                    self.enrollFail()
                    return
            self.enroll(2)
            print("Remove finger")
            self.waitForFinger(True)

            print("Press finger again")
            self.waitForFinger(False)
            if self.captureFinger() < 0:
                    self.enrollFail()
                    return

            if self.enroll(3) != 0:
                    self.enrollFail()
                    return

            print("Remove finger")
            self.waitForFinger(True)

            print("Press finger again to identify")
            self.waitForFinger(False)
            if self.captureFinger() < 0:	# <10>
                    self.identFail()
                    return
            ident = self.identifyUser()
            if(ident >= 0 and ident < 200):	# <11>


                    print("Identity found: %d" % ident)
            else:
                    print("User not found")
            self.led(False)
            self.stopScanner()
