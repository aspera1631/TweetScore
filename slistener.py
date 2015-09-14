## class for listening to the Twitter stream

from tweepy import StreamListener
import json, time, sys

# Creates a file with at most max_tweets tweets
max_tweets = 100000;

# This is an instance of the StreamListener class
class SListener(StreamListener):

    def __init__(self, api=None, fprefix='streamer'):
        # Don't know what else could go here
        self.api = api
        # Counts the recorded tweets
        self.counter = 0
        # file prefix
        self.fprefix = fprefix
        # Build the output
        self.output = open(fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        # Creates another text that records which tweets have "delete" = True
        self.delout = open('delete.txt', 'a')

    def on_data(self, data):

        if 'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return False

    def on_status(self, status):
        # We only want to record English tweets
        # First, convert the tweet to json format so we can parse it
        stat_json = json.loads(status)
        # If it's in english
        if stat_json.get("retweeted_status", stat_json).get("lang") == "en":
            # record the tweet and a newline
            self.output.write(status + "\n")
            # Increment the counter
            self.counter += 1

        if self.counter >= max_tweets:
            # Once we get the right number of tweets, close the file
            self.output.close()
            # Open a new file and start recording. This doesn't work for stream.sample() because twitter closes the stream.
            self.output = open('../streaming_data/' + self.fprefix + '.'
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            # Reset the counter once the new file starts
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return