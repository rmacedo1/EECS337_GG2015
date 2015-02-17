import nltk
import JakeFunctions as JF 
import GoldenGlobesNLP as GG
import random
import json
import pickle, dill

presenters = ["will ferrell", "kate hudson", "sacha baron cohen", "john krasinski", "aziz ansari", "julia roberts", "don cheadle", "kristen wiig", "arnold schwarzenegger", "lucy liu", "nathan fillion", "jay leno", "sylvester stallone", "jonah hill", "jimmy fallon", "kiefer sutherland", "jason statham", "jessica alba", "george clooney", "dennis quaid", "robert pattinson", "halle berry", "kristen bell", "lea michele", "salma hayek", "jennifer lopez", "dustin hoffman", "amanda seyfried", "kerry washington", "debra messing", "eva longoria", "jennifer garner", "megan fox", "paul rudd", "jason bateman", "bradley cooper", "robert downey, jr."]


def getTrainingData(tweets):
	presenters_split = []
	for p in presenters:
		presenters_split = presenters_split + p.split(" ") 

	other_words = ["Wins", "Won", "congrats", "Congrats", "winner", "Winner"]
	presenting = JF.hardfiltertweets(tweets, presenters_split, [])
	non_presenting = JF.hardfiltertweets(tweets, other_words, presenters_split)

	print len(presenting)
	print len(non_presenting)

	results = labelTweets(non_presenting, False) + labelTweets(presenting, True)
	random.shuffle(results)
	return results

def labelTweets(tweets, isPresenting):
	return [(tweet, isPresenting) for tweet in tweets]

def createWordList(tweets):
	results = []
	for tweet in tweets:
		results = results + tweet[0]
	return results

def getWordFeatures(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

def extract_features(tweet, word_features):
	uniqWords = set(tweet)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in uniqWords)
	return features

def make_e_f(words):
	word_features = getWordFeatures(words)
	extract_features_l = extract_features;
	return lambda tweet : extract_features_l(tweet, word_features)


# Label tweets as presenting and non-presenting
def train(tweets, getTrainingData):
	processed_tweets = getTrainingData(tweets)
	training_tweets = processed_tweets[:len(processed_tweets)/2]
	test_tweets = processed_tweets[len(processed_tweets)/2:]
	words = createWordList(training_tweets)

	processor = make_e_f(words)
	print "Got word features"
	training_set = nltk.classify.apply_features(processor, training_tweets)
	classifier = nltk.NaiveBayesClassifier.train(training_set)

	test_set = [(processor(t), b) for (t, b) in training_tweets]
	print "Accuracy: " + str(nltk.classify.accuracy(classifier, test_set))

	return (classifier, processor)

def classifyTweets(tweets):
	with open("classifier.json", "rb") as fp:
		obj = pickle.load(fp);
		classifier = obj["classifier"]
		processor = obj["processor"]
	
	return classifyTweets2(tweets, processor, classifier, True)

def classifyTweets2(tweets, processor, classifier, cat):
	test_set = [processor(t) for t in tweets]
	labeled_tweets = [(original, classifier.classify(processor(tweet))) for tweet, original in zip(test_set, tweets)]
	return [bundle[0] for bundle in labeled_tweets if bundle[1] == cat]

def main():
	fn = "gg2013.json"
	print "Loading tweets"
	tweets = GG.loadParsedTweets(fn)
	print "Training"
	(classifier, processor) = train(tweets)
	print "Done training"

	print classifier.classify(processor(JF.hardfiltertweets(tweets, ["happy"], [])[0]))

	with open("classifier.json", "w+") as outfile:
		pickle.dump({"classifier" : classifier, "processor" : processor}, outfile)



if __name__ == "__main__":
	main()




