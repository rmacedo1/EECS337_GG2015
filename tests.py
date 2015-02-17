import emojiProcessing as ep
from Category import Category
from GoldenGlobesNLP import *
from JakeFunctions import softfiltertweets, hardfiltertweets 

def findDuplicates(tweets):
	seen = set()
	duplicates = {}
	for tweet in tweets:
		x = " ".join(tweet)
		if x not in seen:
			seen.add(x)
		else:
			try:
				duplicates[x] = duplicates[x] + 1
			except KeyError:
				duplicates[x] = 2
	return duplicates

def checkForDuplicates(tweets):
    seen = set()
    uniq = []
    for tweet in tweets:
        x = " ".join(tweet)
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return float(len(tweets))/float(len(uniq))

def testDuplicateRatio(tweets):
	feelings = ep.filterEmojis(tweets)
	print checkForDuplicates(feelings["Positive"])

def showDuplicates(tweets):
	dups = findDuplicates(tweets)
	checkForDuplicates(tweets)
	import operator
	dups = sorted(dups.items(), key=operator.itemgetter(1))
	for x in dups:
		print x

def findDiff(tweetsSmall, tweetsLarge):
	tweetsSmall = [" ".join(x) for x in tweetsSmall]
	tweetsLarge = [" ".join(x) for x in tweetsLarge]
	smallSet = set(tweetsSmall)
	intersection = []
	difference = []
	for tweet in tweetsLarge:
		if tweet not in smallSet:
			difference.append(tweet)
		else:
			intersection.append(tweet)
	return (intersection, difference)


def myFilter(tweets,goodwords,badwords,w):
	goodcount = len(goodwords)
	badcount = len(badwords)
	results = []
	for tweet in tweets:
		measure = sum([tweet.count(x) for x in goodwords]) - w*sum([tweet.count(x) for x in badwords])
		#print str(measure) + " " + str(goodcount) + " " + str(badcount)
		if measure > 0:
			results = results + [tweet]
	return results

def filterTests(tweets):
	print len(tweets)

	s = softfiltertweets(tweets, ["just","testing"], [], 1)
	m = myFilter(tweets, ["just","testing"], [], 1)
	(intersection, difference) = findDiff(s, m)

	print len(s)
	print len(m)
	print len(intersection)
	print len(difference)

	print len(softfiltertweets([x.split(" ") for x in difference], ["just"], [], 0))
	print len(softfiltertweets(m, ["just"], [], 0))

def main():
	fn = "gg2013.json"
	tweets = loadParsedTweets(fn)

	words = ["julia", "roberts", "Roberts", "Julia"];
	print(hardfiltertweets(tweets, words, [])[1:20])

	


	

if __name__ == "__main__":
    main()