#!/usr/bin/python

'''
Author: Adam Jenkins
This is the main file for gandalf
'''
#import includes.database as database
#import includes.logging as log
import includes.Scheduler as Scheduler
import sys
import os

#os.setpgid(0,0)

'''
***MAIN SECTION OF PROGRAM
'''


###########################################################################
# configure these paths:
LOGFILE = '/var/log/gandalf.log'
PIDFILE = '/var/run/gandalf.pid'


###########################################################################


import sys, os

class Log:
    """file like for writes with auto flush after each write
    to ensure that everything is logged, even during an
    unexpected exit."""
    def __init__(self, f):
        self.f = f
    def write(self, s):
        self.f.write(s)
        self.f.flush()

def main():
    #change to data directory if needed
    os.chdir("/")
    #redirect outputs to a logfile
    sys.stdout = sys.stderr = Log(open(LOGFILE, 'a+'))
    #ensure the that the daemon runs a normal user
    #os.setegid(103)     #set group first "pydaemon"
    #os.seteuid(103)     #set user "pydaemon"
    #start the user program here:
    #Init the Gandalf system using the path from the console parameters

    schedule = Scheduler.Scheduler(sys.argv[1])
    
    while 1:
        file = schedule.getNextFile()
        os.spawnv(os.P_WAIT,'/usr/bin/mpg321',['mpg321','-o','oss','-a','/dev/audio',file])
    

if __name__ == "__main__":
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            #print "Daemon PID %d" % pid
            open(PIDFILE,'w').write("%d"%pid)
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # start the daemon main loop
    main()



