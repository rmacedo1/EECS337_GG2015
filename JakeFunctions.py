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

def hardfiltertweets(tweets,goodwords,badwords):
	return [tweet for tweet in tweets if any(x in tweet for x in goodwords) and not any(x in tweet for x in badwords)]

def softfiltertweets(tweets,goodwords,badwords,w):
	goodcount = len(goodwords)
	badcount = len(badwords)
	return [tweet for tweet in tweets if (badcount*sum(tweet.count(x) for x in goodwords) - w*goodcount*sum(tweet.count(x) for x in badwords)) >= 0]

def buildworddict(tweets,badwords):
	namedict = dict()
	for tweet in tweets:
		for word in tweet:
			if word[0].isupper():
				if word not in badwords:
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

def buildnamedict(tweets,badwords):
	capnamedict = dict()
	for tweet in tweets:
		tweetnames = re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'," ".join(tweet))
		for name in tweetnames:
			if name not in badwords:
				if name not in capnamedict:
					capnamedict[name] = 0
				capnamedict[name] += 1
	return capnamedict

def filternamelist(namelist, badlist):
	return [name for name in namelist if not any(x in name for x in badlist)]

def filterworddict(worddict, badlist):
	return {key: worddict[key] for key in worddict if key not in badlist}

def filternamedict(namedict,name):
	return {key: namedict[key] for key in namedict if name not in key}

def printtopdictvals(printdict,num):
	itr = 0
	for word in sorted(printdict, key=printdict.get, reverse=True):
		if (itr < num):
			print word, printdict[word]
			itr += 1

def predictNames(worddict,namedict,num):
	winners = dict()
	tempwords = worddict.copy()
	tempnames = namedict.copy()
	for i in range(num):
		currentWinner = ""
		currentVal = -1
		for word in sorted(tempwords, key=tempwords.get, reverse=True):
			for name in sorted(tempnames, key=tempnames.get, reverse=True):
				if word in name:
					if tempnames[name] + tempwords[word] > currentVal:
						currentVal = tempnames[name] + tempwords[word]
						currentWinner = name
		winners[currentWinner] = currentVal
		tempwords = filterworddict(tempwords, currentWinner.split())
		tempnames = filternamedict(tempnames, currentWinner)
	return winners
