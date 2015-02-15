from JakeFunctions import filtertweets

def parseRange(input):
	return [parseHex(format(x, '08x')) for x in range(input[0], input[1] + 1)]		

def parseHex(input):
	input = '\U' + input
	try:
		ans = input.decode('unicode_escape')
		return ans
	except UnicodeDecodeError:
		pass

def prepareEmojiLists():
	""" Positive: """
	positive = {}
	positive["Approval"] = [u"\u2764"]
	positive["Joyful"] = parseRange((0x1F602, 0x1F60A))
	positive["Love"] = parseRange((0x1F618, 0x1F619)) + [u"\u2764"]
	positive["Silly"] = parseRange((0x1F61C, 0x1F61D))


	""" Negative: """
	negative = {}
	negative["Angry"] = parseRange((0x1F61E, 0x1F624))
	negative["Crying"] = parseRange((0x1F625, 0x1F630)) + [u"\U0001f62d"]
	negative["Shocked"] = parseRange((0x1F631, 0x1F635))

	emojiCategories = {"Positive" : positive, "Negative" : negative}
	return emojiCategories

def funnyEmojis():
	return parseRange((0x1F605, 0x1F606)) + parseRange((0x1F61D, 0x1F61D))

def filterRecursive(tweets, superCategory):
	if type(superCategory) == type([]):
		

	
def filterEmojis(tweets):
	emojiCategories = prepareEmojiLists()
	positive = [emoji for key in emojiCategories["Positive"] for emoji in emojiCategories["Positive"][key]]
	negative = [emoji for key in emojiCategories["Negative"] for emoji in emojiCategories["Negative"][key]]

	positiveTweets = filtertweets(tweets,positive,[])
	negativeTweets = filtertweets(tweets,negative,[])
	return {"Positivity score" 	: (len(positiveTweets) + 1.0) / (len(negativeTweets) + 1.0),
			"Dominant emotion" :
			"Negative"	: negativeTweets,
			"Positive"	: positiveTweets}



