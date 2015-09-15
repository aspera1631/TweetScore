__author__ = 'bdeutsch'
import re
import json


def emoji_txt(text):
    m = re.findall('(\\\U\w{8}|\\\u\w{4})', text)
    #m = re.findall('', text.encode)
    if m:
        return len(m)
    else: return 0



test = "@all1dcrew  fav this ifb &amp; im close to 5k \U0001f36d\U0001f3c \ua4fd\ua45w"
# Define path to raw tweet file


print emoji_txt(test)

#tweets['text'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("text", {}).replace('\n', ''), tweets_data)
