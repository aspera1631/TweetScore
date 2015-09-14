
from slistener import SListener
import time, tweepy, sys
from tweepy import OAuthHandler

#username = '' ## put a valid Twitter username here
#password = '' ## put a valid Twitter password here
#auth     = tweepy.auth.BasicAuthHandler(username, password)
#api      = tweepy.API(auth)

# Authentication settings
consumer_key = 'xhCE3HtM6XYWmtlLlLzbtBCVf'
consumer_secret = 'BilV44WczCaJsljmUY4vc79xzgIDcSoOaNgaZ3RM8LywUaP5xq'
access_token = '494451363-KYSKQn5JgPvROwzr46jQJiUJJbD5NpLXzrL72X7M'
access_secret = '2qjIS5qOR2U7f2duj6lw5lfBZZytx5hWqUfUSTc9mV4j6'

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
