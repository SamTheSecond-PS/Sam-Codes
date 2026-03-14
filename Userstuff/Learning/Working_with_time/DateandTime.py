import time

def send_emails():
    for i in range(1, 100):
        pass

start = time.time()
send_emails()
end = time.time()
duration = end - start
print(duration)

from datetime import datetime, timedelta

ft1 = datetime(2018, 1, 1)
dt2 = datetime.now()
dur = dt2 - ft1
print(dur)