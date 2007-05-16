"""
Scheduler.py

By Tim Saylor & Adam Jenkins

This implements the Scheduler class, which interfaces with a script object and
a music database to determine which song should be played next.  The primary 
interface with this class is the method "getNextFile()", which returns 
information about the next song to be played.
"""

from Script import Script
import logging as log
import database
import time

print "HI"

class Scheduler:
    def __init__(self, file):
        self._script = Script(file)
        self._segment = self._script.getCurrentSegment()
        self._ruleString = self._segment.getNextRule()
        self._cursor = database.connect()
        self._repeat = 0
        self._songcounter = -1
        self._ruleNew = 1
        
        timelist = time.localtime()
        
        if 'repeat' in self._ruleString:
            self._repeat = 1
        
        
        print "Current Day: "+str(timelist[6])
        
        
    def getNextFile(self):
        
        while 1:
            #print "getting file"
            #Check for stopped status
            while 1:
                self._cursor.execute('select switch from commands where type="1"')
                result = self._cursor.fetchone()
                if result["switch"] == "0":
                    time.sleep(1)
                else:
                    break
                    
            #Check to see if any time left in segment
            if self._segment.getTimeLeft() <= 0:
                #No time left, go to next segment
                self._repeat = 0
                self._songcounter = 0
                self._segment = self._script.getNextSegment()
                self._ruleString = self._segment.getNextRule()
                self._ruleNew = 1
            else:
                #time left
                if self._repeat == 0 and self._songcounter == 0:
                    #no repeating, just get next rule
                    self._ruleString = self._segment.getNextRule()
                    self._ruleNew = 1
                    print "Got Next Rule: "+self._ruleString
                elif self._songcounter > 0:
                    #song counter, drop it down one
                    print "Song Counter Minus: ",
                    self._songcounter -= 1
                    print self._songcounter
                    
            #Now we have to interprate the rule
            if 'repeat' in self._ruleString:
                self._repeat = 1
                self._songcounter = 0
                self._ruleNew = 0
            rule = self._ruleString.split('"')
            parameter = rule[-2:]
            #print parameter
            if self._ruleNew == 1:
                print "Set counter"
                if parameter[-1] != '' and self._repeat != 1:
                    self._songcounter = int(parameter[-1])-1
                    print "Sound counter Set: "+str(self._songcounter)
                else:
                    self._songcounter = 0
                self._ruleNew = 0
            
            del parameter[-1]
            del rule[-2:]
            rule = rule[0].split()
            
            import sys
            
            if rule[0] == 'random':
                print "Random Rule"
                if rule[1] == 'genre':
                    print "Genre: "+str(parameter[0])
                    print "Counter: "+str(self._songcounter)
                    sql = 'select f.path,f.title,f.artist from files f, genres g where f.id = g.id and g.genre = "'+parameter[0]+'"and f.length <= "'+str(self._segment.getTimeLeft())+'" ORDER BY RAND() LIMIT 1'
                    print sql
                    self._cursor.execute(sql)
                    if self._cursor.rowcount == 0:
                        print "No song: "+parameter[0]
                        #No song can fit into our timeframe, goto next segment
                        self._repeat = 0
                        self._songcounter = -1
                        self._segment = self._script.getNextSegment()
                        self._ruleString = self._segment.getNextRule()
                        self._ruleNew = 1
                        continue
                    
                    #Get our row
                    row = self._cursor.fetchone()
                    #log our song
                    log.addLog(row["artist"],row["title"],self._cursor)
                    return row["path"]
                
                if rule[1] == 'comment':
                    print "Comment"
                    sql = 'select path,title,artist from files where comment = "'+parameter[0]+'"and length <= "'+str(self._segment.getTimeLeft())+'" ORDER BY RAND() LIMIT 1'
                    print sql
                    self._cursor.execute(sql)
                    if self._cursor.rowcount == 0:
                        print "No song: "+parameter[0]
                        #No song can fit into our timeframe, goto next segment
                        self._repeat = 0
                        self._songcounter = -1
                        self._segment = self._script.getNextSegment()
                        self._ruleString = self._segment.getNextRule()
                        self._ruleNew = 1
                        continue
                    #Get our row
                    row = self._cursor.fetchone()
                    #log our song
                    log.addLog(row["artist"],row["title"],self._cursor)
                    return row["path"]
            
            elif rule[0] == 'title':
                print "Title"
                sql = 'select path,title,artist from files where title = "'+parameter[0]+'"'
                print sql
                self._cursor.execute(sql)
                if self._cursor.rowcount == 0:
                    print "Why"
                    print "No song: "+parameter[0]
                    #No song found
                    self._repeat = 0
                    self._songcounter = -1
                    self._segment = self._script.getNextSegment()
                    self._ruleString = self._segment.getNextRule()
                    self._ruleNew = 1
                    continue
                #Get our row
                row = self._cursor.fetchone()
                #log our song
                log.addLog(row["artist"],row["title"],self._cursor)
                return row["path"]
            
            elif rule[0] == 'filelist':
                pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def changeScript(self):
        pass
        



if __name__ == "__main__":
    sched = Scheduler('/gandalf/testscript.txt')
    stuff = sched.getNextFile()
    print stuff
    
