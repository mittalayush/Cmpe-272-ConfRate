from twython import Twython, TwythonError,TwythonStreamer
APP_KEY=''
APP_SECRET=''
OAUTH_TOKEN=''
OAUTH_TOKEN_SECRET=''

strConference = raw_input("Pleased enter the conference name:");

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    search_results = twitter.search(q='strConference', count=1000)
except TwythonError as e:
    print e

for tweet in search_results['statuses']:
    print tweet['text'].encode('utf-8'), '\n'
