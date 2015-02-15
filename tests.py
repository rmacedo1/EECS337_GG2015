import emojiProcessing as ep
import GoldenGlobesNLP as gg

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

def main():
	fn = "gg2013.json"
	tweets = gg.loadParsedTweets(fn)
	dups = findDuplicates(tweets)
	checkForDuplicates(tweets)
	import operator
	dups = sorted(dups.items(), key=operator.itemgetter(1))
	for x in dups:
		print x
	

if __name__ == "__main__":
    main()