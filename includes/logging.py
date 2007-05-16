'''
Author: Adam Jenkins
This include is for logging functions.
For now you can only add to the database
'''

#This function adds a song to the DB. Path is the song path, and cursor is the database cursor.
def addLog(artist,title,cursor):
	sql = 'INSERT INTO logs (date,song) VALUES(now(),"'+artist+' - '+title+'")'
	cursor.execute(sql)