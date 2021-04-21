import threading
import time


def job():
    while True:
        print('something')
        time.sleep(1.5)


listener = threading.Thread(target=job, name="listener", args=[])
listener.start()

print(threading.)