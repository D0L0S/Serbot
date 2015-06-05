#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

#from database import *

class Encode():
	
	def process(self, string):
		result = json.dumps(string)
		return result
		
class Decode():
	
	def process(self, string):
		jsonString = Decode().parse(string)
		status = Decode().statusDecode(jsonString)
		if status == "OK": 
			command = Decode().commandDecode(jsonString)
			if command == "list":reply = Decode().formatData(jsonString)
			else: reply = Decode().replyDecode(jsonString)
		else:
			reply = Decode().errorDecode(jsonString)
		return reply 
	
	def parse(self, string):
		try:
			parsed_json = json.loads(string)
			return parsed_json
		except Exception as error:
			return str(error)
	
	def customDecode(self, string, value):
		try:
			st = Decode().parse(string)
			result = (st[value])
			return str(result)
		except Exception as error:
			return str(error)
	
	def commandDecode(self, string):
		try:
			command = (string["command"])
			return command
		except Exception as error:
			return str(error)
		
	def statusDecode(self, string):
		try:
			status = (string["status"])
			return status
		except Exception as error:
			return str(error)
			
	def replyDecode(self, string):
		try:
			reply = (string["reply"])
			return reply
		except Exception as error:
			return str(error)
			
	def errorDecode(self, string):
		try:
			error = (st["error"])
			return str(error)
		except Exception as error:
			return str(error)
	
	def cpassword(self, password):
		jsonString = Decode().parse(password)
		password = (jsonString["password"])
		return password
		
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
			return "No Clients Connected"
		
	
if __name__=="__main__":
	decode = Decode()
