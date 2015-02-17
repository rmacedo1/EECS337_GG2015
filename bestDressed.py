import JakeFunctions as JF 
import GoldenGlobesNLP as GG
import naiveBayesProcessing as NB
import random, json

goodwords = ["beautiful","handsome","dressed","gown","dress"]
badwords = ["ugly","heinous","hideous"]

def getTrainingData(tweets):

	hotness = JF.hardfiltertweets(tweets, goodwords,badwords)
	hot_mess = JF.hardfiltertweets(tweets, badwords, goodwords + ["good"])

	print len(hotness)
	print len(hot_mess)

	results = NB.labelTweets(hotness[:500], True) + NB.labelTweets(hot_mess[:500], False)
	random.shuffle(results)
	return results

def main():
	fn = "gg2013.json"
	tweets = GG.loadParsedTweets(fn)
	random.shuffle(tweets)

	(classifier, processor) = NB.train(tweets, getTrainingData)

	print classifier.classify(processor(goodwords))
	print classifier.classify(processor(badwords))

	c = NB.classifyTweets2(tweets[:1000], processor, classifier, True)

	print len(c)

	wordDict = JF.buildworddict(c, GG.exclude)
	nameList = JF.buildnamedict(c, [])
	presenters = JF.predictNames(wordDict, nameList, 2)

	print presenters



if __name__ == "__main__":
	main()