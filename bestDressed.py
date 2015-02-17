import JakeFunctions as JF 
import GoldenGlobesNLP as GG

def main():
	fn = "gg2013.json"
	tweets = GG.loadParsedTweets(fn)
	dressed = ["dressed", "dress"]
	goodwords = ["beautiful"]
	badwords = ["hideous"]
	dress_tweets = JF.hardfiltertweets(tweets, dressed, [])[0:10]

	print JF.hardfiltertweets(dress_tweets, goodwords, [])[0:10]
	print JF.hardfiltertweets(dress_tweets, badwords, [])[0:10]



if __name__ == "__main__":
	main()
