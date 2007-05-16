'''
Author: Adam Jenkins
This include abstracts the database connection
'''

import MySQLdb

def connect():
	db = MySQLdb.connect(host="localhost", user="gandalf", passwd="astari", db="gandalf")
	cursor = db.cursor (MySQLdb.cursors.DictCursor)
        print "Connected to Database"
	return cursor
