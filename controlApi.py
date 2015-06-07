#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonEncoder import *
	
class Api():
	
	def main(self, string):
		functions = ["accept", "List", "interact", "reply", "customDecode", "clientTotal", "listClients", "authenticate"]
		jsonString = Decode().process(string)
		status = Api().status(jsonString)
		if status == "OK":
			command = Api().command(jsonString)
			if command in functions:
				# Call Function based on Command parameter
				a = Api()
				method = getattr(a, command) 
				password = method(jsonString)
				return password
			else: Api().InvalidFunction()
		else:
			reply = Api().errorDecode(jsonString)
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
			reply = Api().command(string)
			return reply
		except Exception as error:
			return str(error)
		
	def List(self, string):
		try:
			reply = Api().command(string)
			return reply
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
		clientList = (string["clients"])
		clientList = Decode().process(clientList)
		return clientList
		
	def error(self, string):
		error = (string["error"])
		return str(error)
	
	def authenticate(self, string):
		print "String: " + str(string)
		print "Type: " + str(type(string))
		password = (str(string["password"]))
		return password
		
	
if __name__=="__main__":
	api = Api()
controlApi.py