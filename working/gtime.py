import time

def getCurSecs():
    """
    Returns the current time in a tuple.  The first
    element is the day number, and the second element
    is the time in seconds from the beginning of the
    day.
    """
    
    timelist = time.localtime()
    day = timelist[6]
    curtime = timelist[3]*3600 + timelist[4]*60 + timelist[5]
    return (day,curtime)

def timeToSecs(time):
    h = time/100
    m = time%100
    assert h < 24, "timeToSecs: hours >= 24"
    assert m < 60, "timeToSecs: minutes >= 60"
    return h*3600+m*60

def secsToTime(secs):
    '''m = secs/60
    m_r = secs%60
    h = m/60
    h_r = m%60
    if h < 10:
        hours = "0" + str(h)
    else:
        hours = str(h)
    m = m + h_r
    '''
    print "function gtime.secsToTime() is unimplemented"
    pass
    