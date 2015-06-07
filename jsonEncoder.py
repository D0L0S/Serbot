#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Encode():
	def process(self, string):
		result = json.dumps(string)
		return result


class Decode():
	def process(self, string):
		jsonString = json.loads(string)
		return jsonString
		
if __name__=="__main__":
	decode = Decode()
	encode = Encode()