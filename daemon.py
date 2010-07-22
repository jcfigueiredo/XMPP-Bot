#!/usr/bin/env python

'''
    This module is used to fork the current process into a daemon.
    Almost none of this is necessary (or advisable) if your daemon 
    is being started by inetd. In that case, stdin, stdout and stderr are 
    all set up for you to refer to the network connection, and the fork()s 
    and session manipulation should not be done (to avoid confusing inetd). 
    Only the chdir() and umask() steps remain as useful.
    References:
        UNIX Programming FAQ
            1.7 How do I get my program to act like a daemon?
                http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        Advanced Programming in the Unix Environment
            W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

    History:
      2001/07/10 by Juergen Hermann
      2002/08/28 by Noah Spurrier
      2003/02/24 by Clark Evans
      2003/11/01 by Irmen de Jong --- adapted a bit for Snakelets
                                    (raises exception at certain points)
      2010/04/08 by Lee Li, small change
      
      http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
'''
#@PydevCodeAnalysisIgnore
import sys, os, time
from signal import SIGINT,SIGTERM,SIGKILL

def daemonize(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile=None, startmsg = 'started with pid %s' ):
    '''
        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
    '''

    # flush io
    sys.stdout.flush()
    sys.stderr.flush()

    # Do first fork.
    try: 
        pid = os.fork() 
        if pid > 0: sys.exit(0) # Exit first parent.
    except OSError, e: 
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
        
    # Decouple from parent environment.
    os.chdir("/") 
    os.umask(0) 
    os.setsid() 
    
    # Do second fork.
    try: 
        pid = os.fork() 
        if pid > 0: sys.exit(0) # Exit second parent.
    except OSError, e: 
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    
    # Open file descriptors and print start message
    if not stderr:
        stderr = stdout
    si = file(stdin, 'r')
    so = file(stdout, 'a+') 
    se = file(stderr, 'a+', 0)  #unbuffered
    pid = str(os.getpid())
    sys.stderr.write("\n%s\n" % startmsg % pid)
    sys.stderr.flush()

    print 'LOG File: %s' % stdout
    print 'PID File: %s' % pidfile    
    
    if pidfile:
        file(pidfile,'w+').write("%s\n" % pid)
    
    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


class DaemonizeError(Exception):
    pass


def startstop(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile='pid.txt', startmsg = 'started with pid %s', action=None ):
              
    if not action and len(sys.argv) > 1:
        action = sys.argv[1]

    if action:
        try:
            pf  = file(pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
            
        if 'stop' == action or 'restart' == action:
            if not pid:
                mess = "Could not stop, pid file '%s' missing.\n"
                # raise DaemonizeError(mess % pidfile)
                print mess % pidfile
                exit(-1)
            
            try:
               while 1:
                   print "sending SIGINT to",pid
                   os.kill(pid,SIGINT)
                   time.sleep(2)
                   
                   print "sending SIGTERM to",pid
                   os.kill(pid,SIGTERM)
                   time.sleep(2)
                   
                   print "sending SIGKILL to",pid
                   os.kill(pid,SIGKILL)
                   time.sleep(1)
            except OSError, err:
               print "process has been terminated."
               os.remove(pidfile)
               
               if 'stop' == action:
                   return    ## sys.exit(0)
               action = 'start'
               pid = None
               
        if 'start' == action:
            if pid:
                mess = "Start aborted since pid file '%s' exists. Server still running?\n"
                # raise DaemonizeError(mess % pidfile)
                print mess % pidfile
                exit(-1)
            daemonize(stdout,stderr,stdin,pidfile,startmsg)
            return
        
    # print "usage: %s start|stop|restart" % sys.argv[0]
    help()
    raise DaemonizeError("invalid command")

def help():
    print "usage: %s start|stop|restart" % sys.argv[0]

def test():
    '''
        This is an example main function run by the daemon.
        This prints a count and timestamp once per second.
    '''
    sys.stdout.write ('Message to stdout...')
    sys.stderr.write ('Message to stderr...')
    c = 0
    while 1:
        sys.stdout.write ('%d: %s\n' % (c, time.ctime(time.time())) )
        sys.stdout.flush()
        c = c + 1
        time.sleep(1)
        
def main():
    import init_env
    # from core.init_env import LOG_PATH, PID_PATH    
    # from core.main_manager import main as buniess_main
    from init_env import LOG_PATH, PID_PATH
    from bot import main as bot_main
    
    argvs = sys.argv[1:]
    if not argvs:
        help()
        exit(0)

    startstop(stdout = LOG_PATH, pidfile = PID_PATH)    

    if argvs[0] in ('start', 'restart'):
        # buniess_main()
        # test()
        bot_main()
    
if __name__ == "__main__":
    main()
