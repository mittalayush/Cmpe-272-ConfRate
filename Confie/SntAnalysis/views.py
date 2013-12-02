from __future__ import division
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.http import HttpResponse
from django.template import RequestContext
import httpconnection
from django.db import IntegrityError
from django.core.context_processors import csrf
from SntAnalysis.models import posts
import requests
import json
import sys
import nltk
from nltk.corpus import stopwords
from twython import Twython, TwythonError,TwythonStreamer


def my_view(request):
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response("index.html", c)


def rate(request):
	try:
            if request.POST:
            	strConference = request.POST.get('keyword')  
		print strConference  
	    	payload = { "keyword": strConference }
	    	data=json.dumps(payload)
		#print data
		#response=httpconnection.Home_Connect(data)
                #print "Status code is",response.status_code
		
		#checking if the input received is a correct keyword not junk characters
		if len(strConference)>3 and not strConference in stopwords.words('english') :
			APP_KEY='QKvB6siChGmTzsFJI3ANCA'
			APP_SECRET='ynvs7PVDjJssynFSqJ6ms52gLxubQI5uSorkVF27Z0'
			OAUTH_TOKEN='105572257-x6M2JpHc7qDW4Ru5jf4LnKOAxJiUJ34OCk1Tmqh8'
			OAUTH_TOKEN_SECRET='a4O7FRdjKJi5jTxZ37jAPiXnqKgG1N8nbsF0DPML9oI'
			
			customstopwords = ['show','they', 'them','but','conference',',','code','weekend','this','the', 'conference', 'is', 				'and','are', 'to', 'a', 'they', '!', 'so','my','at','of','it','i','was','for','.']
			twitterCustomwords= ['rt', ',','@','http',':','//']
			counter=0
			score=0
			PositiveCount=0
			NegativeCount=0
			NeutralCount=0
			ListTweet= []
			GraphValList= []
			tmp=0
 
			#Load positive tweets into a list
			p = open('/home/ayush/Documents/Projects/FirstBlog/blog/postweets.txt', 'r')
			positivetxt = p.readlines()
 
			#Load negative tweets into a list
			n = open('/home/ayush/Documents/Projects/FirstBlog/blog/negtweets.txt', 'r')
			Negativetxt = n.readlines()
			
			n = open('/home/ayush/Documents/Projects/FirstBlog/blog/neutaltweets.txt', 'r')
			Neutraltxt = n.readlines()
			
			NegativeList = []
			positiveList = []
			NeutralList=[]
 
			#Create a list of 'negatives' with the exact length of our negative tweet list.
			for i in range(0,len(Negativetxt)):
				NegativeList.append('negative')
 
			#Likewise for positive.
			for i in range(0,len(positivetxt)):
				positiveList.append('positive')

			#for i in range(0,len(Neutraltxt)):
			#	NeutralList.append('neutral')
 
			#Creates a list of tuples, with sentiment tagged.
			positiveTagged = zip(positivetxt, positiveList)
			NegativeTagged = zip(Negativetxt, NegativeList)
			#NeutralTagged = zip(Neutraltxt, NeutralList)
 
			#Combines all of the tagged tweets to one large list.
			taggedtweets = positiveTagged + NegativeTagged 
#+ NeutralTagged

			print taggedtweets
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
 			#print 'It should return all the words!'
			#Calls above functions - gives us list of the words in the tweets, ordered by freq.
			print getwordfeatures(getwords(tweets))

			wordList = [i for i in getwordfeatures(getwords(tweets)) if not i in stopwords.words('english')]
			wordList = [i for i in getwordfeatures(getwords(tweets)) if not i in customstopwords]
			
			#print 'The word list excluding junk stop characters'			
			print wordList
			
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
				tmpstr=tweet['user']['screen_name'].encode(encoding='UTF-8',errors='strict'),'Says on',tweet['created_at'],tweet['text'].encode(encoding='UTF-8',errors='strict')
				ListTweet.append(tmpstr)
				
				FetchTweet = tweet['text'].encode('utf-8').lower().split()
    				FetchTweet = [a for a in FetchTweet if not a in stopwords.words('english')]
    				FetchTweet = [b for b in FetchTweet if not b in twitterCustomwords]
    				
    				print tweet['text'].encode('utf-8'),'---output--', classifier.classify(extractFeature(FetchTweet))
    				if classifier.classify(extractFeature(FetchTweet)) == 'positive':
					PositiveCount+=1
    				elif classifier.classify(extractFeature(FetchTweet)) == 'neutral':
					NeutralCount+=1
				else:
					NegativeCount+=1
			print 'length------', len(ListTweet)
	
			if len(ListTweet)<=1:
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				ListTweet.append(' ')
				
		
			print 'Total Number of tweets with keyword ',strConference,'found were', counter,'\n'
			print 'Neutal counts', NeutralCount
			print 'Negatives counts', NegativeCount
			print 'Positive counts', PositiveCount
			print 'Total length-------------',len (ListTweet)

			if counter!=0 and PositiveCount!=0:
				PositivePerc=PositiveCount/(counter)*100			
			else:
				PositivePerc=0

			NegativePerc=100-PositivePerc

			#print 'positive and negative percernatges',PositivePerc,NegativePerc

			if PositiveCount==0:
				score=0
			else:
				score=float(PositiveCount)/float(counter)*100	

			
			for x in range(1, 6):
				if classifier.classify(extractFeature(ListTweet[counter-x]))== 'positive':
					GraphValList.append(10)
				else:
					GraphValList.append(-10)
			print 'graph result feature-----',GraphValList[0],GraphValList[1],GraphValList[2],GraphValList[3],GraphValList[4]
			
			if score>95:
				print 'MUST GO!'
				return render_to_response('success.html',{"positive":PositivePerc,"conferenceName":strConference,"message":"MUST GO !","negativeCount":NegativePerc,"positiveCount":PositivePerc,"tweet0":ListTweet[counter-1],"tweet1":ListTweet[counter-3],"tweet2":ListTweet[counter-5],"tweet3":ListTweet[counter-7],"tweet4":ListTweet[counter-9],"tweet5":ListTweet[counter-11],"tweet6":ListTweet[counter-13],"tweet7":ListTweet[counter-15],"tweet8":ListTweet[counter-17],"tweet9":ListTweet[counter-19],"tweet10":ListTweet[counter-20],"GraphVal4":GraphValList[4],"GraphVal3":GraphValList[3],"GraphVal2":GraphValList[2],"GraphVal1":GraphValList[1],"GraphVal0":GraphValList[0]})
			elif score>90 and score<=95:
				print 'GO!'
				return render_to_response('success.html',{"positive":PositivePerc,"conferenceName":strConference,"message":"GO !","negativeCount":NegativePerc,"positiveCount":PositivePerc,"tweet0":ListTweet[counter-1],"tweet1":ListTweet[counter-3],"tweet2":ListTweet[counter-5],"tweet3":ListTweet[counter-7],"tweet4":ListTweet[counter-9],"tweet5":ListTweet[counter-11],"tweet6":ListTweet[counter-13],"tweet7":ListTweet[counter-15],"tweet8":ListTweet[counter-17],"tweet9":ListTweet[counter-19],"tweet10":ListTweet[counter-20],"GraphVal4":GraphValList[4],"GraphVal3":GraphValList[3],"GraphVal2":GraphValList[2],"GraphVal1":GraphValList[1],"GraphVal0":GraphValList[0]})
			elif score>=75 and score<=90:
				print 'FAIR!' 
				return render_to_response('success.html',{"positive":PositivePerc,"conferenceName":strConference,"message":" FAIR !","negativeCount":NegativePerc,"positiveCount":PositivePerc,"tweet0":ListTweet[counter-1],"tweet1":ListTweet[counter-3],"tweet2":ListTweet[counter-5],"tweet3":ListTweet[counter-7],"tweet4":ListTweet[counter-9],"tweet5":ListTweet[counter-11],"tweet6":ListTweet[counter-13],"tweet7":ListTweet[counter-15],"tweet8":ListTweet[counter-17],"tweet9":ListTweet[counter-19],"tweet10":ListTweet[counter-20],"GraphVal4":GraphValList[4],"GraphVal3":GraphValList[3],"GraphVal2":GraphValList[2],"GraphVal1":GraphValList[1],"GraphVal0":GraphValList[0]})
			elif score<75 and counter>0:
				print 'USELESS!'
				return render_to_response('success.html',{"positive":PositivePerc,"conferenceName":strConference,"message":" USELESS !","negativeCount":NegativePerc,"positiveCount":PositivePerc,"tweet0":ListTweet[counter-1],"tweet1":ListTweet[counter-3],"tweet2":ListTweet[counter-5],"tweet3":ListTweet[counter-7],"tweet4":ListTweet[counter-9],"tweet5":ListTweet[counter-11],"tweet6":ListTweet[counter-13],"tweet7":ListTweet[counter-15],"tweet8":ListTweet[counter-17],"tweet9":ListTweet[counter-19],"tweet10":ListTweet[counter-20],"GraphVal4":GraphValList[4],"GraphVal3":GraphValList[3],"GraphVal2":GraphValList[2],"GraphVal1":GraphValList[1],"GraphVal0":GraphValList[0]})
			elif counter==0:
				print 'SORRY, CAN\'T SAY'
				return render_to_response('success.html',{"positive":PositivePerc,"conferenceName":strConference,"message":"SORRY, CAN\'T SAY","negativeCount":NegativePerc,"positiveCount":PositivePerc,"tweet0":ListTweet[counter-1],"tweet1":ListTweet[counter-3],"tweet2":ListTweet[counter-5],"tweet3":ListTweet[counter-7],"tweet4":ListTweet[counter-9],"tweet5":ListTweet[counter-11],"tweet6":ListTweet[counter-13],"tweet7":ListTweet[counter-15],"tweet8":ListTweet[counter-17],"tweet9":ListTweet[counter-19],"tweet10":ListTweet[counter-20],"GraphVal4":GraphValList[4],"GraphVal3":GraphValList[3],"GraphVal2":GraphValList[2],"GraphVal1":GraphValList[1],"GraphVal0":GraphValList[0]})


		else:
			return render_to_response('error.html')
		
	    else:
                	return render(request, 'rate.html')
	except IntegrityError,e:
        		return render_to_response('error.html')
			


def index(request):
	return render(request, 'index.html')


def success(request):
	return render(request, 'success.html')


def error(request):
	return render(request, 'error.html')
