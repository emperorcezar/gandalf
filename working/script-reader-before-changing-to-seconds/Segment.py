import time, string


class Segment:
    def __init__(self, start, end, rules):
        self._start = start
        self._end = end
        endh = int(self._end[2:-2])
        starth = int(self._start[2:-2])
        endm = int(self._end[-2:])
        startm = int(self._start[-2:])
        durh=endh-starth        
        durm=endm-startm
        if endh != starth:
            durm -= 40
        print "durm %s" % durm
        self._duration = self._end[:2] + str(durh) + str(durm)
        self._rules = string.split(rules, '\n')
        self._currule = 0

        while "" in self._rules:
            del self._rules[self._rules.index("")]


    def getDuration(self):
        return self._duration
        
    def getTimeLeft(self):
        timelist = time.localtime()
        day = timelist[6]
        print day
        print self._end[:1]
        if int(day) != int(self._end[:1]):
            return 0
        curtime = str(timelist[3]) + str(timelist[4])
        timeleft = int(self._end[-4:]) - int(curtime)
        return timeleft
        
    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end
        
    def getRules(self):
        return self._rules

    def getNextRule(self):
        ret = self._rules[self._currule]
        self._currule = (self._currule + 1) % len(self._rules)
        return ret
        
    def setNextRule(self, rule, overwrite=0):
        if overwrite == 0:
            self._rules.insert(self._currule, rule)
        else:
            self._rules[self._currule] = rule
        
    def setStart(self, newstart):
        self._start = newstart
        self._duration = int(self._end[-4:]) - int(self._start[-4:])
