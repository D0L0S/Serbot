#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from ConfigParser import SafeConfigParser
import os
import sys
import time
from socket import *
import StringIO

from controlApi import *
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

		login = {"status":"OK", "command":"authenticate", 'password':str(args.password)}
		login = Encode().process(login)
		login = encryption().encrypt(login, config["password"])
		s.send(login)

		while True:
			command = raw_input("Serbot$ ")
			try:
				if(command == "clear"):
					if sys.platform == "win32": os.system("cls")
					else: os.system("clear")
				elif(command == "help"):
					print config["allcommands"]
				else:
					answers = command.split(' ')
					if answers[0] == "interact" and len(answers) == 2:
						Cmd = {"status":"OK", "command": answers[0], "client":str(answers[1])}
					else: Cmd = {"status":"OK", "command": answers[0]}
					Cmd = Encode().process(Cmd)
					Cmd = encryption().encrypt(Cmd, config["password"])
					s.send(Cmd)
					reply = s.recv(20480)
					reply = encryption().decrypt(reply, config["password"])
					print "Reply: " + str(reply)
					Reply = Api().main(reply)
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
	parser.add_argument('-v', '--version', action='version', version= config["_version"])
	args = parser.parse_args()
	if sys.platform == 'win32': os.system("cls")
	else: os.system("clear")
	print config["intro"]
	control().main()
