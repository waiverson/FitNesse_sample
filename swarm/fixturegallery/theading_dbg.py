__author__ = 'Administrator'

import threading
import time

def myfunc(a, delay):
    print "i will calculate square of %s after delay for %s" %(a, delay)
    time.sleep(delay)
    print "calculate begins..."
    result = a*a
    print result
    return result

t1 = threading.Thread(target=myfunc, args=(2, 5))
t2 = threading.Thread(target=myfunc, args=(6, 8))
print t1.isDaemon()
print t2.isDaemon()
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()




