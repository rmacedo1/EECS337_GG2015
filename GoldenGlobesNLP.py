# February, 2015
# EECS 337 NLP

import json
import nltk
import re
import Category
import JakeFunctions

predictKeywords = ["think", "calling", "want", "predict", "predictions", "if", "hoping",
                   "hope", "which", "Which", "Calling", "Think", "who", "Who", "Want",
                   "Prediction", "Predictions", "prediction", "Predictor", "predictor"
                   "If", "Hope", "please", "Please", "should've", "Should've",
                   "should", "Should", "torn", "prays"]

winnerKeywords = ["wins", "won", "speech",
                  "Wins", "Won",
                  "congrats", "Congrats", "winner", "Winner"]

presentersKeywords = ["presenting", "giving award", "jokes"]
notAllowed = ["#", ".", "@", ":", "http", "://", "/", "co"]

exclude = ["Golden", "Globes", "RT", "Best", "GoldenGlobes", "The", "For",
           "Motion", "Picture", "Drama", "Comedy","Musical", "Series", "TV",
           "Actor", "Actress", "Wins", "Congrats", "A", "Movie",
           "Winner", "Supporting", "Globe", "Or", "At", "I", "G"]

globalBadWords = ["Supporting", "Drama", "Musical", "Comedy", "Actress", "Actor"
                  "Movie", "TV", "Mini-series"]
                  

(categories, nominees, catList) = Category.createCategories()


def getData():
    """input: None
    output: a list of list of tokenized tweets
    """
    with open("C:\Users\Rosio\Desktop\goldenglobes2015NEW.json\gg15trimmed.json") as file:
        tweets = [json.loads(line)["text"] for line in file]
    
    parsedTweets = [nltk.wordpunct_tokenize(tweet) for tweet in tweets]
    
    return parsedTweets

def noPredictions(parsedTweets):
    """
    Takes the entire list of parsed tweets and removes any tweets which contain
    prediction keywords.
    returns a list of trimmed tweets
    """
    noPredTweets = []
    for tweet in parsedTweets:
        if (not any([x in tweet for x in predictKeywords])):
            noPredTweets.append(tweet)
            
    return noPredTweets

def Testing():
    parsedTweets = getData()
    cleanTweets = noPredictions(parsedTweets)
    return cleanTweets

def Testing2(tweets):
    dictionary = splitIntoCategories(tweets)
    detectData(dictionary)
    return
  
def splitIntoCategories(tweets):
    """
    Group up the parsed tweets into the award categories arrays.
    categories: A list of Category class
    return a dictionary with a list of tweets pertaining to each
    category
    """
    listDictionary = []

    #create category arrays
    for x in categories: #category dictionary
        listDictionary = listDictionary + splitTweets(x, tweets, [x.name])

    return listDictionary


def detectData(listDictionary):
    """
    Takes in a dictionary of categories and corresponding tweets.
    Processes tweets further to extract desired information.
    
    Returns a dictionary with Award, Winners, Presenters, and Nominees
    """
    dictionary = dict()
        
    for x in zip(listDictionary, nominees):
        noms = []
        notes = []

        print "The category is "
        print x[0]["Cats"]
        
        #get nominees for category
        if (type(x[1][0]) is dict):
            for person in x[1]:
                noms +=  [person["Person"]]
                notes += [person["Notes"]]
        else:
            noms = x[1]

        #determine category
        category = getCategory(x[0]["Cats"])
        winner = getWinner(x[0]["Tweets"], noms, notes)
        presenters = getPresenter(x[0]["Tweets"])

        #Save all answers
        dictionary[category] = dict()
        dictionary[category]["Winner"] = winner
        dictionary[category]["Presenters"] = presenters
        dictionary[category]["Nominees"] = noms

        print winner
        #print dictionary
        """
        with open("results.json", "w") as file:
            json.dump(dictionary, file)
        """     
    return dictionary

def getWinner(tweets, nominees, notes):
    """
    Returns the predicted winner given the nominees
    and category related tweets
    """
    countDict = []
    winTweets = winnerTweets(tweets)
    #get word frequencies
    countDict = getCount(winTweets)
    winner = predictWinner(countDict, nominees, notes)
    return winner

def getPresenter(tweets):
    """
    Returns the predicted winner according to given tweets
    category relevant tweets
    """
    countDict = []
    presTweets = presenterTweets(tweets)
    countDict = getCount(presTweets)    
    presenters = predictPresenters(countDict)
    return presenters


def getCategory(listOfCat):
    """
    Returns the award category string
    """
    for category in catList:
        if (all ([words in category for words in listOfCat])):
            return category
    
    
def splitTweets (category, tweets, catName):
    """
    Takes an object of type Category class, a list of tweets, and a list containing the category name
    Returns a list of dictionaries with tweets pertaining to that category
    """
    keywords = []
    listTweets = []

    if (category.subcats == []):
        keywords = keywords + buildCategoryKeywords(category.name)

        badwords = []
        for word in globalBadWords:
            if word not in keywords:
                badwords = badwords + [word]
        
        relTweets = filtertweets(tweets, keywords, [])

        #print keywords
        
        return [ {"Cats": catName, "Tweets": relTweets} ]
    else:
        keywords = keywords + buildCategoryKeywords(category.name)
        
        badwords = []

        relTweets = filtertweets(tweets, keywords, badwords)

        for cat in category.subcats:
            listTweets = listTweets + splitTweets(cat, relTweets, catName + [cat.name])
            
        return listTweets

        
def buildCategoryKeywords(categoryname):
    """
    Takes in a category name and splits it up into individual keywords
    returns a list of the keywords
    """
    catKeywords = []
    catKeywords2 =[]
    
    catKeywords = re.findall('[A-Z]+[^A-Z ]*', categoryname)

    for word in catKeywords:
        noSpaceWord = word.replace(" ", "")
        catKeywords2.append(noSpaceWord)
        
    return catKeywords2


def winnerTweets(tweets):
    """"
    Selects the tweets that are likely to pertain to winners according to
    winner kewords list.
    Returns an array that has matches to winner keywords
    """
    winTweets = []
    
    for tweet in tweets:
        if (any ([x in winnerKeywords for x in tweet])):
            winTweets.append(tweet)

    return winTweets

def presenterTweets(tweets):
    """
    Should return tweets dealing with presenters
    """
    presenterTweets = []
    return presenterTweets

def predictPresenters(dictionary):
    """
    Return a list of predicted presenters
    """
    return []                     

def getCount(tweets):
    """
    Takes in a list of tweets and returns a dictionary
    with the frequency of each word
    
    Kristin's dictionary code
    """
    diction = dict()
    
    for tweet in tweets:
        for word in tweet:
            if word[0].isupper() and word not in exclude:
                if word in diction:
                    diction[word] += 1
                else:
                   diction[word] = 1

    return diction

def sortCountDict(dictionary):
    """
    Create a list of lists with sorted word, count pairs
    """
    sortedLists = [];
    
    for  word in sorted(diction, key = diction.get, reverse = True):
        line = (word, dictionary[word])
        sortedLists.append(line)

    return sortedLists

def predictWinner(namedict, noms, notes):
    """
    Takes a dictionary of words and their count/frequency and
    a list of category nominees and returns the predicted winner.
    
    Jake's winner predictor function
    """
    count = 20
    
    for word in sorted(namedict, key=namedict.get, reverse=True):
        for name in noms:
            if word in name:
                return name


# Text interaction and results
def results():
    """Return a dictionary with the Hosts and Winners,
    Presenters, Nominees for each Award.
    """
    
    return answersDict;

def menu():
    """ Presents users with menu options
    for selecting to veiw results of the Golden
    Globes Awards Ceremony
    """

    print("Welcome!")
    print(" 1. Who were the hosts?")
    print(" 2. Who presented each award?")
    #ect.
    
    choice = input("Please enter your option")
    return



"""
Also need a Readme file with
-Library citations
-Consulted repositories
-What was done to make the system adaptable
"""
