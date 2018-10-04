import time
from time import strftime, gmtime
import random
from string import Template
import threading
from threading import Thread

# Need to be installed
import requests  

camera_attr = dict(camera_name='camera1', location='playground')

log = {}

# Thread 1 - Long-Polling
def long_polling():
    while True:
        headers = {'Prefer': 'wait=60'} # Restart every 60 seconds
        cam_info = {'cam': camera_attr.get('camera_name')}
        response = requests.get('http://proxy:7999/check_user_request', headers=headers, params=cam_info) # start long-polling
        if response.status_code == 200:  
            print(response.json())
            process_response(response.json()) 
        else: # Server is throwing errors, back off some seconds 
            time.sleep(10)  
            continue
        time.sleep(0.1)  # Immediately restart a new polling after each process

# Thread 2 - Generating Logs
def generate_logs():
    while True:
        camera_attr['students_count'] = random.randint(1, 50)
        message = Template('$camera_name -> $students_count students just arrived the $location').substitute(camera_attr)
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        log[timestamp] = message
        time.sleep(10)

# If asked, offer logs to API server 
def process_response(response_data):
    if response_data.get('event') == 'USER_REQUESTED':
        cam_info = {'cam': camera_attr.get('camera_name')}
        requests.post("http://proxy:7999/receive_log", data=log, params=cam_info)

# Start running threads
if __name__ == '__main__':
    Thread(target = long_polling).start()
    Thread(target = generate_logs).start()

