import gevent
from gevent import monkey
import time

monkey.patch_all()


def job():
    while True:
        print('something')
        time.sleep(1.5)


greenlet = gevent.spawn(job)

# ... perhaps interaction with the user here

# this will wait for the operation to complete (optional)
time.sleep(3)
# alternatively if the image display is no longer important, this will abort it:
greenlet.kill()
