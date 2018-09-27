import threading
import time
import datetime as dt
from myrecorder import recorder

#  sleep_fun waits the dedicated amount of time (num_sec) before executing the function
def sleep_fun(func, num_sec, duration, instream, file_name):
    time.sleep(num_sec)
    func(duration, instream, file_name)

# schedule creates a new thread for each sheduling request
def schedule(func, num_sec, duration, instream, file_name):
    t = threading.Thread(target=sleep_fun, args=(func, num_sec, duration, instream, file_name))
    t.start()

# takes in the time to start recording, duration of recording, url of incoming audio, and the file name
# to be saved to.
# calculates the difference in seconds between current time and start of recording.
# schedules the function to be executed
def runtest(schedtime,duration,instream, file_name):
	now = dt.datetime.now()
	sleeptime = (schedtime-now).total_seconds()
	schedule(recorder.scheduled_recording, sleeptime, duration, instream, file_name)
