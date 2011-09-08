import sys, os
import beanstalkc
import random
import pickle
from datetime import datetime, timedelta
from time import sleep

beanstalk = beanstalkc.Connection(host='localhost', port=11300)
next_random = datetime.now()
# infinite loop
# priority queue nature; we could set priority = time as UNIX timestamp
while(True):
    job = beanstalk.peek_ready()
    if job:
        job = beanstalk.reserve(timeout=0)
        file_dict = pickle.loads(job.body)
        if datetime.now() >= file_dict['send_time']:
            # send the file
            # we would send it, then shred the original file and 
            # remove from beanstalk
            # for now, we'll just print the filename and remove the job
            print "-----"
            print "SENT:", file_dict['filename']
            print "  AT:", file_dict['send_time']
            job.delete()

    # time to send random file as well?
    if datetime.now() >= next_random:
        next_random = datetime.now() + timedelta(seconds=5)
        file_dict = {
                'filename': 'tmp',
                'send_time': datetime.now() # would be random
            }
        beanstalk.put(pickle.dumps(file_dict))

    sleep(1)
