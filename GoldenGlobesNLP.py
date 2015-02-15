# February, 2015
# EECS 337 NLP

import json
import nltk
import re
import Category
from JakeFunctions import filtertweets
from emojiProcessing import parseRange
from emojiProcessing import parseHex
from emojiProcessing import prepareEmojiLists
from emojiProcessing import filterEmojis
import sys
from Scraping import scrapeResultsforYear

predictKeywords = ["think", "calling", "want", "predict", "predictions", "if", "hoping",
                   "hope", "which", "Which", "Calling", "Think", "who", "Who", "Want",
                   "Prediction", "Predictions", "prediction", "Predictor", "predictor"
                   "If", "Hope", "please", "Please", "should've", "Should've",
                   "should", "Should", "torn", "prays", "predicting", "Predicting"]

winnerKeywords = ["wins", "won", "speech",
                  "Wins", "Won",
                  "congrats", "Congrats", "winner", "Winner"]

presentersKeywords = ["presenting", "giving award", "jokes"]
notAllowed = ["#", ".", "@", ":", "http", "://", "/", "co"]

exclude = ["Golden", "Globes", "RT", "Best", "GoldenGlobes", "The", "For",
           "Motion", "Picture", "Drama", "Comedy","Musical", "Series", "TV",
           "Actor", "Actress", "Wins", "Congrats", "A", "Movie",
           "Winner", "Supporting", "Globe", "Or", "At", "I", "G"]

globalBadWords = ["Supporting"]
                  

def main():
    if len(sys.argv) > 2:
        filename = sys.argv[1]

    (parsedTweets, categories, nominees, catList) = loadTweetsCategoriesNominees(filename)
    (answers, funGoals) = searchCorpus(parsedTweets, categories, nominees, catList)

    with open("answers.json", "w+") as file:
        json.dump(answers, file)
    with open("funGoals.json", "w+") as file:
        json.dump(funGoals, file)


def loadParsedTweets(filename):
    with open(filename) as fl:
        jsonObj = json.load(fl);
        tweets = [tweet["text"] for tweet in jsonObj]
    parsedTweets = [nltk.wordpunct_tokenize(tweet) for tweet in tweets]
    return parsedTweets


def getData(filename):
    """input: filename of the json object with tweets
    output: a list of list of tokenized tweets
    """
    
    tweets = loadParsedTweets(filename);

    # Try to figure out which scraped results to use
    fn = "categories_nominees_winners";
    if ("15" in filename):
        (categories, nominees, catList) = Category.createCategories(fn + ".json")
    elif ("13" in filename):
        (categories, nominees, catList) = Category.createCategories(fn + "_2013.json")
    else:
        yr = re.search('\d\d\d\d', filename).group(0);
        if yr:
            scrapedResults = scrapeResultsforYear(yr, toFile=False)
            (categories, nominees, catList) = Category.createCategories(dict=scrapedResults)
        else: # Just do with 2015 results
            (categories, nominees, catList) = Category.createCategories(fn + ".json")
        
    
    return (parsedTweets, categories, nominees, catList)

def noPredictions(parsedTweets, categories, nominees, catList):
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

def loadTweetsCategoriesNominees(filename):
    (parsedTweets, categories, nominees, catList) = getData(filename)
    cleanTweets = noPredictions(parsedTweets, categories, nominees, catList)
    return (cleanTweets, categories, nominees, catList)

def searchCorpus(tweets, categories, nominees, catList):
    dictionary = splitIntoCategories(tweets, categories)
    (resultsDict, funGoals) = detectData(dictionary, categories, nominees, catList)
    return (resultsDict, funGoals)
  
def splitIntoCategories(tweets, categories):
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


def detectData(listDictionary, categories, nominees, catList):
    """
    Takes in a dictionary of categories and corresponding tweets.
    Processes tweets further to extract desired information.
    
    Returns a dictionary with Award, Winners, Presenters, and Nominees
    """
    dictionary = dict()
    answers = dict()
    winnersList = []
    categoryList = []
    presentersList = []
    nomineesList = []

    answers = getMetaData(answers)
    answers["data"] = dict()
    answers["data"]["unstructured"] = dict()
    answers["data"]["unstructured"]["hosts"] = ["test1", "test2"]
    answers["data"]["structured"]= dict()

    funGoals = {};
        
    for x in zip(listDictionary, nominees):
        noms = []
        notes = []

        print "The category is "
        print x[0]["Cats"]

        category = getCategory(x[0]["Cats"])
        
        #get nominees for category
        if (type(x[1][0]) is dict):
            for person in x[1]:
                if category in ["Best Screenplay - Motion Picture", "Best Original Score"]:
                    noms += [person["Notes"]]
                else:
                    noms +=  [person["Person"]]
                    notes += [person["Notes"]]
        else:
            noms = x[1]

        #determine winners and presenters
        (winner, feelings) = getWinner(x[0]["Tweets"], noms, notes)
        presenters = getPresenter(x[0]["Tweets"])

        #Prepare fungoals
        funGoals[category] = {};
        funGoals[category]["Sentiment"] = feelings;

        #Save answer for json
        winnersList = winnersList + [winner]
        categoryList = categoryList + [category]
        presentersList = presentersList + presenters
        nomineesList = nomineesList + noms

        #Save all answers for text interface
        nomsOnly = []
        for nom in noms:
            if nom is not winner:
                nomsOnly = nomsOnly + [nom]
                
        dictionary[category] = dict()
        dictionary[category]["Winner"] = winner
        dictionary[category]["Presenters"] = presenters
        dictionary[category]["Nominees"] = noms

        answers["data"]["structured"][category] = dict()
        answers["data"]["structured"][category]["Nominees"] = nomsOnly
        answers["data"]["structured"][category]["Winner"] = winner
        answers["data"]["structured"][category]["Presenters"] = presenters
        
        print winner
        #print dictionary
        """
        with open("results.json", "w") as file:
            json.dump(dictionary, file)
        """
    
    answers["data"]["unstructured"]["winners"] = winnersList
    answers["data"]["unstructured"]["awards"] = categoryList
    answers["data"]["unstructured"]["presenters"] = presentersList
    answers["data"]["unstructured"]["nominees"] = nomineesList


    #print answers
    """
    with open("answers.json", "w") as file:
            json.dump(answers, file)
    """
    return (answers, funGoals)

def getMetaData(dictionary):
    dictionary["metadata"] = dict()

    dictionary["metadata"]["year"] = 2015
    
    dictionary["metadata"]["hosts"] = dict()
    dictionary["metadata"]["hosts"]["method"] = "detected"
    dictionary["metadata"]["hosts"]["method_description"] = " detected Hosts"

    dictionary["metadata"]["nominees"] = dict()
    dictionary["metadata"]["nominees"]["method"] = "scraped"
    dictionary["metadata"]["nominees"]["method_description"] = "scraped To get the nominees TEST"

    dictionary["metadata"]["awards"] = dict()
    dictionary["metadata"]["awards"]["method"] = "scraped"
    dictionary["metadata"]["awards"]["method_description"] = "To scraped get the awards we"

    return dictionary    

def getWinner(tweets, nominees, notes):
    """
    Returns the predicted winner given the nominees
    and category related tweets
    """
    countDict = []
    winTweets = winnerTweets(tweets)

    print "Example of Winner Tweets"
    print winTweets[1]
    
    feelings = filterEmojis(winTweets)
    print feelings["Positivity score"]
    
    #get word frequencies
    countDict = getCount(winTweets)
    winner = predictWinner(countDict, nominees, notes)
    return (winner, feelings)

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
        
        print "Badwords"
        print badwords
        print "Keywords"
        print keywords
        
        relTweets = filtertweets(tweets, keywords, badwords)

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


"""
Also need a Readme file with
-Library citations
-Consulted repositories
-What was done to make the system adaptable
"""
