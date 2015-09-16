__author__ = 'bdeutsch'
import re

test = '''u'text': u'@daus_yunus i know i knowwww \U0001f60f', u'in_r'''
m = re.search('"text":"(.+?)","', test)

# search for retweet
#print text
m = re.search('''text(.+?), u'\w''', test)
if m:
    print m.group(1)
    n = re.findall('(\\\U\w{8}|\\\u\w{4})', m.group(1))
    if n:
        print n