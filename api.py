#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

#from database import *

class Decode():
	
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
			st = Decode().parse(string)
			status = (st["status"])
			if status == "OK": Decode().replyDecode(st)
			else: Decode().errorDecode(string)
		except Exception as error:
			return str(error)
			
	def replyDecode(self, string):
		try:
			reply = (st["reply"])
			return str(reply)
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
