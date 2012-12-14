PubNubBlink
===========

Connects [PubNub][1] messages to the [blink(1)][2] if they match a pattern

PubNubBlink subscribes to a PubNub channel, listens for all messages, matches them against a list of regular expressions, and if there is a match it calls the blink1-tool and passes a set of arguments.  With this simple setup you can wire up a host of real time alerts that trigger the blink(1) and you can distribute your configuration file to several people (allowing you to leverage PubNub's global reach without adding any extra load to your web server)

This is written in Python and shouldn't have any OS specific dependencies.  It runs anywhere you have internet access and the [blink1-tool][3].

Configuration is easy (although I'm sure I'm abusing [ConfigParser][4] here), define your PubNub credentials, point it at your blink1-tool, set an interval to blink (you want to set it to about 1 seconds longer than your slowest blink pattern) and then define patterns of message to blink to.  If a message is received that doesn't match any pattern then that message will be ignored.

[1]: http://www.pubnub.com/
[2]: http://blink1.thingm.com/
[3]: https://github.com/todbot/blink1
[4]: http://docs.python.org/2/library/configparser.html
