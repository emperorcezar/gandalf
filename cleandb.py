import MySQLdb
import os

db = MySQLdb.connect(host="localhost", user="gandalf", passwd="astari", db="gandalf")
cursor = db.cursor (MySQLdb.cursors.DictCursor)

cursor.execute("SELECT path FROM files")

remove_songs = []

print "Songs in database: ",cursor.rowcount

while 1:
    result = cursor.fetchone()
    if result == None: break
    if not os.path.isfile(result["path"]):
        print "Song added to remove list: "+result["path"]
        remove_songs.append(result["path"])


for song in remove_songs:
    print song
    sql = 'SELECT id FROM files WHERE path="'+song+'"'
    #print sql
    cursor.execute(sql)
    result = cursor.fetchone()
    sql = 'DELETE FROM genres WHERE id ="'+str(result['id'])+'"'
    #print sql
    cursor.execute(sql)
    sql = 'DELETE FROM files WHERE path="'+song+'"'
    cursor.execute(sql)
