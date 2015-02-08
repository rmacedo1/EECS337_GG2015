import json
import nltk
import re

def tweetsfromfile(filename):
	with open(filename) as file:
		return [nltk.wordpunct_tokenize(json.loads(line)["text"]) for line in file]

def filtertweets(tweets,goodwords,badwords):
	return [tweet for tweet in tweets if any(x in tweet for x in goodwords) and not any(x in tweet for x in badwords)]

def buildnamedict(tweets):
	namedict = dict()
	for tweet in tweets:
		for word in tweet:
			if word[0].isupper():
				if word not in namedict:
					namedict[word] = 0
				namedict[word] += 1
	return namedict

def buildnamelist(tweets):
	namelist = []
	for tweet in tweets:
		tweetnames = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)'," ".join(tweet))
		for name in tweetnames:
			if name not in namelist:
				namelist.append(name)
	return namelist

def printtopdictvals(namedict,num):
	itr = 0
	for word in sorted(namedict, key=namedict.get, reverse=True):
		if (itr < num):
			print word, namedict[word]
			itr += 1

def predictWinner(namedict,names):
	for word in sorted(namedict, key=namedict.get, reverse=True):
		for name in names:
			if word in name:
				return name
