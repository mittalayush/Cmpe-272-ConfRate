import nltk
from nltk.corpus import stopwords

customstopwords = ['show', 'they', 'them','He','She','We','i','are','this','the','so','to','me','for','and','was','in','as','about']
 
#Loads the sentiment files
p = open('postweets.txt', 'r')
postxt = p.readlines()
 
n = open('negtweets.txt', 'r')
negtxt = n.readlines()

neglist = []
poslist = []
 
#creates a list of sentiment files with the same length of the sentiment tweet list.

for i in range(0,len(negtxt)):
	neglist.append('negative')
 

for i in range(0,len(postxt)):
	poslist.append('positive')
 
#creates a tuple list with sentiment tagged at the end of sentences.
postagged = zip(postxt, poslist)
negtagged = zip(negtxt, neglist)
 
#appends all the tagged tweets to a common list
taggedtweets = postagged + negtagged

tweets = []
 
#creates a list of words with sentiments.
for (word, sentiment) in taggedtweets:
	word_filter = [i.lower() for i in word.split()]
	tweets.append((word_filter, sentiment))
 
#Pulls out all the words in a list of tagged tweets.
def getwords(tweets):
	allwords = []
	for (words, sentiment) in tweets:
		allwords.extend(words)
	return allwords
 
#uses nltk library to order the list of tweets words pulled out by their frequency.
def getwordfeatures(listoftweets):
	wordfreq = nltk.FreqDist(listoftweets)
	words = wordfreq.keys()
	return words

#calls the baove functions to provide the list of words excluding the custom and stop words, ordered by frequency
wordlist = [i for i in getwordfeatures(getwords(tweets)) if not i in stopwords.words('english')]
wordlist = [i for i in getwordfeatures(getwords(tweets)) if not i in customstopwords]

print wordlist
def feature_extractor(doc):
	docwords = set(doc)
	features = {}
	for i in wordlist:
		features['contains(%s)' % i] = (i in docwords)
	return features
 
#creates the training set to classify on the basis of distribution of true and false in the input.
training_set = nltk.classify.apply_features(feature_extractor, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

while True:
	input = raw_input("Please write a sentence to be tested for sentiment.\n")
	if input == 'exit':
		break
	elif input == 'informfeatures':
		print classifier.show_most_informative_features(n=30)
		continue
	else:
		input = input.lower()
		input = input.split()
		print '\nWe think that the sentiment was ' + classifier.classify(feature_extractor(input)) + ' in that sentence.\n'

p.close()
n.close()

