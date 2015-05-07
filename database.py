#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector

class Database:

	def __init__(self):
		user='serbot'
		host='127.0.0.1'
		database='serbot'
		self.cnx = mysql.connector.connect(user=self.user, host=self.host, database=self.database)

	def query(self, q):
		cursor = self.cnx.cursor()
		cursor.execute(q)
		columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
		result = []
		for row in cursor:
			result.append(dict(zip(columns, row)))
		return result

	def __del__(self):
		self.cnx.close()


if __name__=="__main__":
	sys.stdout = Logger("Database.log")
	sys.stderr = Logger("DBError.log")
	db=Database()
