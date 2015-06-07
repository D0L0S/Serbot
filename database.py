#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import MySQLdb as mdb
import sys

config = {}
execfile("Control.conf", config) 

class Database:

	def __init__(self):
		self.user='serbot'
		self.password='password'
		self.host='127.0.0.1'
		self.database='serbot'
		self.con = mdb.connect(config["dbhost"], config["dbuser"], config["dbpassword"],config["database"],)
		#self.host, self.user, self.password, self.database);

	def query(self, q):
		try:
			with self.con:
				cur = self.con.cursor()
				cur.execute(q)
                
				rows = cur.fetchall()
				return rows

		except Exception as e:
			print e
	def __del__(self):
		self.con.close()


if __name__=="__main__":
	sys.stdout = Logger("Database.log")
	sys.stderr = Logger("DBError.log")
	db=Database()
