#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonEncoder import *
	
class Api():
	
	def main(self, string):
		functions = ["accept", "List", "interact", "customDecode", "clientTotal", "listClients"]
		jsonString = Decode().process(string)
		status = Api().status(jsonString)
		if status == "OK":
			command = Api().command(jsonString)
			if command in functions:
				# Call Function based on Command parameter
				a = Api()
				method = getattr(a, command) 
				reply = method(jsonString)
				#return reply
			else: reply = Api().InvalidFunction()
		else:
			reply = Api().error(jsonString)
		return reply

	def InvalidFunction(self):
		print "Invalid"

################################################
################################################
## API FUNCTIONS
################################################
################################################

	def customDecode(self, string, value):
		try:
			st = Decode().process(string)
			result = (st[value])
			return str(result)
		except Exception as error:
			return str(error)
	
	def command(self, string):
		try:
			command = (string["command"])
			return command
		except Exception as error:
			return str(error)
		
	def status(self, string):
		try:
			status = (string["status"])
			return status
		except Exception as error:
			return str(error)
	
	def accept(self, string):
		try:
			reply = (string["reply"])
			return reply
		except Exception as error:
			return str(error)
		
	def List(self, string):
		print "LIST"
		try:
			List = Api().listClients(string)
			return List
		except Exception as error:
			return str(error)
		
	def interact(self, string):
		try:
			reply = Api().command(string)
			return reply
		except Exception as error:
			return str(error)

	def clientTotal(self, string):
		clientNumber = (string["total"])
		return clientNumber
		
	def listClients(self, string):
		clientlist = (string["clients"])
		clientList = Decode().process(clientlist)
		return clientList
		
	def error(self, string):
		error = (string["error"])
		return str(error)		
	
if __name__=="__main__":
	api = Api()