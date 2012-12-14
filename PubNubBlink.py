import ConfigParser
from collections import deque
import re
import string
import subprocess
import sys
from threading import Thread
import time

from Pubnub import Pubnub

## Initiate Class
blink_queue = deque(maxlen=5)

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

def receive(data):
    message = data['text']

    for pattern in patterns:
        if re.match(pattern, message):
            blink_queue.append(patterns[pattern])
            break
    return True

def blinker(q):
    while True:
        try:
            args = q.popleft().split()
        except IndexError:
            ##Wait for more work
            time.sleep(blink_wait)
        else:
            subprocess.Popen(
                [blink_app] + args,
                startupinfo=startupinfo,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE)
            ##Wait for the blinking to stop
            time.sleep(blink_wait)

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
