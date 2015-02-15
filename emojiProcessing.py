from JakeFunctions import hardfiltertweets

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

def filterRecursive(tweets, superCategory, name):
	if type(superCategory) == type([]):
		filtered = hardfiltertweets(tweets,superCategory,[])
		return (filtered, {"Name" : name, "Emojis" : superCategory})
	elif type(superCategory) == type({}):
		types = {}
		domEmotion = {};
		max = 0;
		for subcat in superCategory:
			emojiList = getEmojis(superCategory[subcat])
			filteredTweets = hardfiltertweets(tweets,emojiList,[])
			(filtered, domDict) = filterRecursive(filteredTweets, superCategory[subcat], subcat)
			types[subcat] = filteredTweets
			l = len(domDict["Emojis"])
			if l > max:
				max = l
				domEmotion = domDict;
		return (types, domEmotion)

def getEmojis(superCategory):
	if type(superCategory) == type([]):
		return superCategory
	else:
		ans = []
		for subcat in superCategory:
			ans = ans + getEmojis(superCategory[subcat])
		return ans

	
def filterEmojis(tweets):
	emojiCategories = prepareEmojiLists()

	(types, domEmotion) = filterRecursive(tweets, emojiCategories, "")

	return {"Positivity score" 	: (len(types["Positive"]) + 1.0) / (len(types["Negative"]) + 1.0),
			"Dominant emotion" : domEmotion,
			"Negative"	: types["Negative"],
			"Positive"	: types["Positive"]}



