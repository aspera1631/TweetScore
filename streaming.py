
from slistener import SListener
import time, tweepy, sys
from tweepy import OAuthHandler
import ConfigParser

#username = '' ## put a valid Twitter username here
#password = '' ## put a valid Twitter password here
#auth     = tweepy.auth.BasicAuthHandler(username, password)
#api      = tweepy.API(auth)

'''
config = ConfigParser.RawConfigParser()
config.read('../config/auth_config.cfg')

# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
consumer_key = config.get('SectionOne', 'consumer_key')
consumer_secret = config.getint('SectionOne', 'consumer_secret')
access_token = config.get('SectionOne', 'access_token')
access_secret = config.getint('SectionOne', 'access_secret')
'''

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('../config/config.ini')


# Authentication settings
consumer_key = parser.get('section1', 'consumer_key')
consumer_secret = parser.get('section1', 'consumer_secret')
access_token = parser.get('section1', 'access_token')
access_secret = parser.get('section1', 'access_secret')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def main():
    # Optionally track certain tweets. Not compatible with stream.sample()
    track = ["..."]

    listen = SListener(api, 'data')
    # Call the stream class
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try:
        #stream.filter(track = track)
        #stream.filter(track=["a"])
        stream.sample()
    except:
        # This happens when the file finishes too
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()
