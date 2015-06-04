#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

#from database import *

class Decode():
	
	def process(self, string):
		jsonString = Decode().parse(string)
		status = Decode().statusDecode(jsonString)
		if status == "OK": 
			reply = Decode().replyDecode(jsonString)
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
		
	
if __name__=="__main__":
	decode = Decode()
