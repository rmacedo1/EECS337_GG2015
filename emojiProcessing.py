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
	Approval = [u"\u2764"]
	Joyful = parseRange((0x1F602, 0x1F60A))
	Love = parseRange((0x1F618, 0x1F619)) + [u"\u2764"]
	Silly = parseRange((0x1F61C, 0x1F61D))
	positive = Silly + Approval + Joyful + Love


	""" Negative: """
	Angry = parseRange((0x1F61E, 0x1F624))
	Crying = parseRange((0x1F625, 0x1F630)) + [u"\U0001f62d"]
	Shocked = parseRange((0x1F631, 0x1F635))
	negative = Angry + Crying + Shocked

	return (positive, negative)

def filterEmojis(tweets):
	(positive, negative) = prepareEmojiLists();
	positiveTweets = filtertweets(tweets,positive,[])
	negativeTweets = filtertweets(tweets,negative,[])
	return {"Positivity score" 	: (len(positiveTweets) + 1) / (len(negativeTweets) + 1),
			"Negative"	: negativeTweets,
			"Positive"	: positiveTweets}


