"""
Script.py

By Tim Saylor

Implements a script object that parses a script and makes 
it available in segment objects.  It can also be used to 
generate a new script file from rules generated at runtime.
"""

import string, sys, Segment, gtime

class Script:
    def __init__(self, filename):
        """
        Takes a script file, parses it into segments, and 
        stores the rules and times for retrieval.
        """
        
        self._times = []        # list of interrupt times
        self._rules = {}        # dictionary of interrupt times to rule strings
        self._cursegment = 0
        
        file = open(filename)
        lines = file.readlines()

        if lines == []:
            print "ERROR: Script file was empty"
            sys.exit()          # Script file was empty.  Error out.

        for line in lines:
            #print line
            line = string.split(line)
            
            if line == []:
                pass
            elif string.lower(line[0]) == "interrupt":
                day = int(line[1])
                self._times += [ (day, gtime.timeToSecs(int(line[2]))) ]
            else:
                self._rules[self._times[-1]] = self._rules.get(self._times[-1], '') + string.join(line) + "\n"
        
        self._times.sort()
        
    def getCurrentSegment(self, day, time):
        """
        Returns the segment that should currently be playing.
        Time should be specified in seconds from the 
        beginning of the day.
        """
        
        curseg = 0
        for i in self._times:
            if i[1] < time and i[0] == day:
                curseg = i
                
        return getSegment(time=curseg)
    
    def getSegment(self, index=-9999, time=(-1, -9999) ):
        """
        Returns a segment object with the given index or 
        given time.  One of these values is required.  If 
        both are given, index is given precedence.
        """
        
        if index != -9999:
            (day, time) = self._times[index]
        elif time != (-1, -9999):
            index = self._times.index(time)
        else:
            print "you must specify either index or time"
            return

        rules = self._rules.get((day, time), "no key found")

        if rules != "no key found":
            end = self._times[index + 1][1]
            if end < time:
                end = 86400
            #if end[-4:] == "0000":
            #    end = string.translate(end[:1], string.maketrans("0123456","6012345")) + " 2400"
            seg = Segment.Segment(day, time, end, rules)
        else: 
            print "invalid index or time given"
            print index
            print time
            print self._times
            print self._rules
            return

        return seg


    def getNextSegment(self):
        """
        Returns the next segment from the script in a 
        segment object.
        """
        
        (day, time) = self._times[self._cursegment]
        rules = self._rules[(day, time)]
        nextindex = (self._cursegment + 1) % len(self._times)
        end = self._times[nextindex][1]
        if end < time:
            end = 86400
        #if end[-4:] == "0000":
        #    end = string.translate(end[:1], string.maketrans("0123456","6012345")) + " 2400"
        seg = Segment.Segment(day, time, end, rules)
        self._cursegment = (self._cursegment + 1) % len(self._times)
        return seg
        
    def addSegment(self, day, time, rules):
        """
        Adds a segment to the script, then modifies 
        the current segment reference to ensure that 
        it still points to the same segment.
        """

        if (day, time) in self._times:
            print "Cannot add a segment that already exists.  Delete first, then re-add."
            return

        (curday, curtime) = self._times[self._cursegment]
        if day == curday:
            if time > curtime:
                self._times.append((day, time))
                self._rules[(day, time)] = rules
            elif time < curtime:
                self._times.append((day, time))
                self._times.sort()
                self._cursegment += 1
                self._rules[(day, time)] = rules
            else: 
                print "This should never print. OMG IDENTIFYING MARK SJGIODJSV"
        elif day < curday:
            self._times.append((day, time))
            self._times.sort()
            self._cursegment += 1
            self._rules[(day, time)] = rules
        elif day > curday:
            self._times.append((day, time))
            self._rules[(day, time)] = rules
            
    def addSegmentObject(self, segment):
        """
        Adds a segment to the script, then modifies 
        the current segment reference to ensure that 
        it still points to the same segment.

        This method takes a segment object as its parameter
        """
        
        day = segment.getDay()
        time = segment.getStart()
        rules = segment.getRules()
        addSegment(self, day, time, rules)

    def deleteSegment(self, index=-9999, time=(-1, -9999) ):
        """
        Deletes a segment to the script, then modifies the 
        current segment reference to ensure that it still 
        points to the same segment.
        """
        
        if index != -9999:
            time = self._times[index]
        elif time != (-1, -9999):
            index = self._times.index(time)
        else:
            print "you must specify either index or time"
            return
        
        if time != (-1, -9999) and time not in self._times:
            print "There is no segment with that time."
            return
        (day, time) = time
        (curday, curtime) = self._times[self._cursegment]
        if day == curday:
            if time > curtime:
                del self._times[index]
                del self._rules[(day, time)]
            elif time < curtime:
                del self._times[index]
                self._times.sort()
                self._cursegment -= 1 # this could cause _cursegment to go negative, but a negative list index still works, so I'm not fixing it.
                del self._rules[(day, time)]
            elif time == curtime:
                print "deleting the current segment is not allowed.  \nThis could be done, but I chose not to implement it."
                return -1
            else: 
                print "This should never print.  OMG THIS IS UNIQUE JOSDJGISD"
                print "time: %s" % str(time)
                print "curtime: %s" % str(curtime)
        elif day < curday:
            del self._times[index]
            self._times.sort()
            self._cursegment -= 1 # this could cause _cursegment to go negative, but a negative list index still works, so I'm not fixing it.
            del self._rules[(day, time)]
        elif day > curday:
            del self._times[index]
            del self._rules[(day, time)]
        
    def writeScript(self, filename):
        """
        Writes out the current script to a specified file.
        """
        
        outfile = open(filename, "w")
        for daytime in self._times:
            outfile.write("interrupt %s\n" % (str(daytime)))
            outfile.write(self._rules[daytime])
        
        

if __name__ == "__main__":
    test = Script("testscript.txt")
    
    print "test._times"
    print test._times
   
    print "test._cursegment"
    print test._cursegment
   
    print "test._rules[i]"
    for i in test._rules.keys():
        print i
        print test._rules[i]
        
    print "test.getSegment(index=0)"
    print test.getSegment(index=0)
    
    print "test._cursegment"
    print test._cursegment
    
    print "test.getNextSegment()"
    print test.getNextSegment()
    
    print "test._cursegment"
    print test._cursegment
   
    print test.getNextSegment()
    
    print "test._cursegment"
    print test._cursegment
   
    print "test.addSegment"
    test.addSegment(3, 18000, """random genre hip-hop
file mymp3.mp3
file myplaylist.pls""")
    print test._times
    for i in test._rules.keys():
        print i
        print test._rules[i]
    
    print "test.deleteSegment(time=(3,18000))"
    print test.deleteSegment(time=(3,18000))
    print test._times
    for i in test._rules.keys():
        print i
        print test._rules[i]

    test.writeScript("testscript-out.txt")    
    
    print "End Script test, begin Segment test"
    
    seg = test.getNextSegment()
    print "start:               %s" % seg.getStart()
    print "set start = 12345"
    seg.setStart(12345)
    print "start:               %s" % seg.getStart()
    print "end:                 %s" % seg.getEnd()
    print "duration:            %s" % seg.getDuration()
    print "time left:           %s" % seg.getTimeLeft()
    print "rules:               %s" % seg.getRules()
    print "next rule:           %s" % seg.getNextRule()
    print "next rule:           %s" % seg.getNextRule()
    print "set next rule = 'random genre hippidy-hop'"
    seg.setNextRule("random genre hippidy-hop")
    print "rules:               %s" % seg.getRules()
    print "set next rule (ovr) = 'random genre rapcore'"
    seg.setNextRule("random genre rapcore", overwrite=1)
    print "next rule:           %s" % seg.getNextRule()
    print "rules:               %s" % seg.getRules()
