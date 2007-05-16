import time, string


class Segment:
    def __init__(self, day, start, end, rules):
        self._day = int(day) - 1
        self._start = int(start)
        self._end = int(end)
        self._rules = string.split(rules, '\n')
        self._currule = 0

        while "" in self._rules:
            del self._rules[self._rules.index("")]

    def getDay(self):
        return self._day

    def getDuration(self):
        return self._end - self._start
        
    def getTimeLeft(self):
        timelist = time.localtime()
        day = int(timelist[6])
        if day != self._day:
            return 0
        curtime = timelist[3]*3600 + timelist[4]*60 + timelist[5]
        timeleft = self._end - curtime
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
