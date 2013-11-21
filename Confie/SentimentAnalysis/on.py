from __future__ import division
import nltk
from nltk.corpus import stopwords
from twython import Twython, TwythonError,TwythonStreamer

 
APP_KEY='QKvB6siChGmTzsFJI3ANCA'
APP_SECRET='ynvs7PVDjJssynFSqJ6ms52gLxubQI5uSorkVF27Z0'
OAUTH_TOKEN='105572257-x6M2JpHc7qDW4Ru5jf4LnKOAxJiUJ34OCk1Tmqh8'
OAUTH_TOKEN_SECRET='a4O7FRdjKJi5jTxZ37jAPiXnqKgG1N8nbsF0DPML9oI'

customstopwords = ['show','they', 'them','but','conference',',','code','weekend']
twitterCustomwords= ['rt', ',','@']
counter=0
score=0
PositiveCount=0
NegativeCount=0
 
#Load positive tweets into a list
p = open('postweets.txt', 'r')
positivetxt = p.readlines()
 
#Load negative tweets into a list
n = open('negtweets.txt', 'r')
Negativetxt = n.readlines()

NegativeList = []
positiveList = []
 
#Create a list of 'negatives' with the exact length of our negative tweet list.
for i in range(0,len(Negativetxt)):
	NegativeList.append('negative')
 
#Likewise for positive.
for i in range(0,len(positivetxt)):
	positiveList.append('positive')
 
#Creates a list of tuples, with sentiment tagged.
positiveTagged = zip(positivetxt, positiveList)
NegativeTagged = zip(Negativetxt, NegativeList)
 
#Combines all of the tagged tweets to one large list.
taggedtweets = positiveTagged + NegativeTagged

tweets = []
 
#Create a list of words in the tweet, within a tuple.
for (word, sentiment) in taggedtweets:
	word_filter = [i.lower() for i in word.split()]
	tweets.append((word_filter, sentiment))
 
#Pull out all of the words in a list of tagged tweets, formatted in tuples.
def getwords(tweets):
	allwords = []
	for (words, sentiment) in tweets:
		allwords.extend(words)
	return allwords
 
#Order a list of tweets by their frequency.
def getwordfeatures(listoftweets):
	#Print out wordfreq if you want to have a look at the individual counts of words.
	wordfreq = nltk.FreqDist(listoftweets)
	words = wordfreq.keys()
	return words
 
#Calls above functions - gives us list of the words in the tweets, ordered by freq.
print getwordfeatures(getwords(tweets))

wordList = [i for i in getwordfeatures(getwords(tweets)) if not i in stopwords.words('english')]
wordList = [i for i in getwordfeatures(getwords(tweets)) if not i in customstopwords]

def extractFeature(doc):
	docwords = set(doc)
	features = {}
	for i in wordList:
		features['contains(%s)' % i] = (i in docwords)
	return features
 
#Creates a training set - classifier learns distribution of true/falses in the input.
training_set = nltk.classify.apply_features(extractFeature, tweets)


classifier = nltk.NaiveBayesClassifier.train(training_set)


#filename='/home/ayush/Desktop/Tweets'+ str(datetime.now())+ ".txt";
#strConference = raw_input("Pleased enter the conference name:");
strConference=strConference.lstrip().rstrip()
#strConference=''.join(strConference.split())
#strConference= '#'+ strConference
#print strConference

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    search_results = twitter.search(q=strConference, count=10000,include_rts=0)
except TwythonError as e:
    print e


for tweet in search_results['statuses']:
    counter+=1;
    
    FetchTweet = tweet['text'].encode('utf-8').lower().split()
    FetchTweet = [a for a in FetchTweet if not a in stopwords.words('english')]
    FetchTweet = [b for b in FetchTweet if not b in twitterCustomwords]
    
    print tweet['text'].encode('utf-8'),'---output--', classifier.classify(extractFeature(FetchTweet))
    if classifier.classify(extractFeature(FetchTweet)) == 'positive':
	PositiveCount+=1
    else:
	NegativeCount+=1

 
print 'Total Number of tweets with keyword ',strConference,'found were', counter,'\n'
print 'Positive:',PositiveCount
print 'Negative:',NegativeCount

if PositiveCount==0:
	score=0
else:
	score=float(PositiveCount)/float(counter)*100	


#print 'Total Score', score

if score>90:
	print 'MUST GO!'
elif score>=80 and score<=90:
	print 'GO!'
elif score>=50 and score<=80:
	print 'FAIR!' 
elif score<=50 and counter>0:
	print 'USELESS!'
elif counter==0:
	print 'SORRY, CAN\'T SAY'

p.close()
n.close()
