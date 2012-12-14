import ConfigParser
from Queue import Queue
import re
import string
import subprocess
import sys
from threading import Thread
import time

from Pubnub import Pubnub

## Initiate Class
blink_queue = Queue()

config = ConfigParser.ConfigParser()
config.read('PubNubBlink.cfg')

blink_app = config.get('Blink1', 'blink-app')
blink_wait = float(config.get('Blink1', 'blink-wait'))
patterns = config._sections['Patterns']
patterns.pop("__name__")

"""Prevent a window from opening each time you call the blink1-tool"""
subprocess.STARTF_USESHOWWINDOW = 1
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

pubnub = Pubnub(
    config.get('PubNub', 'pub-key'),
    config.get('PubNub', 'sub-key'),
    None,
    False)

print("My UUID is: "+pubnub.uuid)

channel = config.get('PubNub', 'channel')

def receive(data) :
    message = data['text']

    for pattern in patterns:
        if re.match(pattern, message):
            blink_queue.put(patterns[pattern])
            break
    return True

def blinker(q) :
    while True:
        args = q.get().split()
        subprocess.Popen(
            [blink_app] + args,
            startupinfo=startupinfo,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE)
        time.sleep(blink_wait)
        q.task_done()

def subscribe():
    print("Listening for messages on '%s' channel..." % channel)
    pubnub.subscribe({
        'channel'  : channel,
        'callback' : receive
    })

blink_worker = Thread(target=blinker, args=(blink_queue,))
blink_worker.daemon=True
blink_worker.start()

sub_thread = Thread(target=subscribe)
sub_thread.daemon=True
sub_thread.start()

sub_thread.join()
