import JakeFunctions as JF 
import GoldenGlobesNLP as GG
import naiveBayesProcessing as NB
import random, json

goodwords = ["beautiful","handsome","dressed", "dress"]
badwords = ["a","the","and"]

def getTrainingData(tweets):

	hotness = JF.hardfiltertweets(tweets, goodwords,["ugly","heinous","hideous"])
	hot_mess = JF.hardfiltertweets(tweets, badwords, goodwords + ["good"])

	print len(hotness)
	print len(hot_mess)

	results = NB.labelTweets(hotness[:500], "Hotness") + NB.labelTweets(hot_mess[:500], "Hot mess")
	random.shuffle(results)
	return results


def main():
	fn = "gg2013.json"
	tweets = GG.loadParsedTweets(fn)
	urls = JF.hardfiltertweets(tweets, ["://"], [])
	print len(urls)
	
	(classifier, processor) = NB.train(tweets, getTrainingData)
	
	c = NB.classifyTweets2(urls[:200], processor, classifier, "Hotness")
	print ["".join(tweet) for tweet in c]




if __name__ == "__main__":
	main()
