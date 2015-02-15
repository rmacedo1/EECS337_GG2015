import emojiProcessing as ep
import GoldenGlobesNLP as gg

def checkForDuplicates(tweets):
    seen = set()
    uniq = []
    for tweet in tweets:
        x = " ".join(tweet)
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return float(len(tweets))/float(len(uniq))

def main():
	fn = "gg2013.json"
	tweets = gg.loadParsedTweets(fn)
	feelings = ep.filterEmojis(tweets)
	print checkForDuplicates(feelings["Positive"])

if __name__ == "__main__":
    main()