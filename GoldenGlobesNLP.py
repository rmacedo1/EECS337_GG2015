# February, 2015
# EECS 337 NLP

import json
import nltk
import re
import Category
import JakeFunctions as JF
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

presentersKeywords = ["presenting", "giving", "presenters", "Presenters",
                      "Presenting"]
notAllowed = ["#", ".", "@", ":", "http", "://", "/", "co"]

exclude = ["Golden", "Globes", "RT", "Best", "GoldenGlobes", "The", "For",
           "Motion", "Picture", "Drama", "Comedy","Musical", "Series", "TV",
           "Actor", "Actress", "Wins", "Congrats", "A", "Movie",
           "Winner", "Supporting", "Globe", "Or", "At", "I", "G"]

globalBadWords = ["Supporting", "Actors", "Actress"]

hostKeywords = ["hosts", "Hosts", "hosting", "Hosting"]

gYear = 0

def main():
    try:
        filename = sys.argv[1]

        print "Loading tweets"
        (parsedTweets, categories, nominees, catList) = loadTweetsCategoriesNominees(filename)
        print "Doing analysis"
        (answers, interfaceDict, funGoals) = searchCorpus(parsedTweets, categories, nominees, catList)

        with open("answers.json", "w+") as file:
            json.dump(answers, file)
        with open("interfaceDict.json", "w+") as file:
            json.dump(interfaceDict, file)
        with open("funGoals.json", "w+") as file:
            json.dump(funGoals, file)
    except IndexError:
        print "Give a json file containing tweets as the first argument"


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
    global gYear
    if ("15" in filename):
        gYear = 2015
        (categories, nominees, catList) = Category.createCategories(fn + ".json")
    elif ("13" in filename):
        gYear = 2013
        (categories, nominees, catList) = Category.createCategories(fn + "_2013.json")
    else:
        yr = re.search('\d\d\d\d', filename).group(0);
        gYear= yr
        if yr:
            scrapedResults = scrapeResultsforYear(yr, toFile=False)
            (categories, nominees, catList) = Category.createCategories(dict=scrapedResults)
        else: # Just do with 2015 results
            (categories, nominees, catList) = Category.createCategories(fn + ".json")
            
    return (tweets, categories, nominees, catList)

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
    hosts = getHosts(tweets)
    (resultsDict, interfaceDict, funGoals) = detectData(dictionary, categories, nominees, catList, hosts)
    return (resultsDict, interfaceDict, funGoals)
  
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

def removeDuplicates(tweets):
    seen = set()
    uniq = []
    for tweet in tweets:
        x = " ".join(tweet)
        if x not in seen:
            uniq.append(tweet)
            seen.add(x)
    return uniq

def detectData(listDictionary, categories, nominees, catList, hosts):
    """
    Takes in a dictionary of categories and corresponding tweets.
    Processes tweets further to extract desired information.
    
    Returns a dictionary with Award, Winners, Presenters, and Nominees
    """
    dictionary = {}
    answers = getMetaData({})
    funGoals = {}
    winnersList = []
    categoryList = []
    presentersList = []
    nomineesList = []

    answers["data"] = dict()
    answers["data"]["unstructured"] = dict()
    answers["data"]["unstructured"]["hosts"] = hosts
    answers["data"]["structured"]= dict()
    

    for x in zip(listDictionary, nominees):

        noms = []
        notes = []

        category = getCategory(x[0]["Cats"], catList)
        print category
        
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
        print "length of tweets is"
        print len(x[0]["Tweets"])
        (winner, feelings) = getWinner(x[0]["Tweets"], noms, notes)
        presenters = getPresenters(x[0]["Tweets"], noms)

        #import tests
        #print "Duplicates in fungoals: " + str(tests.checkForDuplicates(feelings["Positive"]))

        #Prepare fungoals
        funGoals[category] = {};
        funGoals[category]["Winner"] = winner
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
        

    answers["data"]["unstructured"]["winners"] = winnersList
    answers["data"]["unstructured"]["awards"] = categoryList
    answers["data"]["unstructured"]["presenters"] = presentersList
    answers["data"]["unstructured"]["nominees"] = nomineesList
    
    return (answers, dictionary, funGoals)

def getMetaData(dictionary):
    dictionary["metadata"] = dict()

    dictionary["metadata"]["year"] = gYear
    
    dictionary["metadata"]["hosts"] = dict()
    dictionary["metadata"]["hosts"]["method"] = "detected"
    dictionary["metadata"]["hosts"]["method_description"] = "detected Hosts"

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
    winTweets = JF.hardfiltertweets(tweets, winnerKeywords, [])
    
    feelings = filterEmojis(removeDuplicates(winTweets))

    countDict = getCount(winTweets)
    winner = predictWinner(countDict, nominees, notes)
    return (winner, feelings)

def getPresenters(tweets, noms):
    """
    Returns the predicted presenters according to given
    category relevant tweets
    """
    badwords = ["Golden Globes"] + noms
    uniqueTweets = removeDuplicates(tweets)
    
    presTweets = JF.hardfiltertweets(uniqueTweets, presentersKeywords, [])
    print len(presTweets)
    wordDict = JF.buildworddict(presTweets, exclude)
    nameList = JF.buildnamedict(presTweets, badwords)

    presenters = JF.predictNames(wordDict, nameList, 2)
    return presenters


def getHosts(tweets):
    """
    Takes the corpus of tweets and returns a list of the predicted hosts
    """
    hostTweets = JF.hardfiltertweets(tweets, hostKeywords, [] )
    badwords = ["Golden Globes"]
    wordDict = JF.buildworddict(hostTweets, exclude)
    nameList = JF.buildnamedict(hostTweets, badwords)

    hosts = JF.predictNames(wordDict, nameList, 2)

    return hosts

def getCategory(listOfCat, catList):
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
    keywords = buildCategoryKeywords(category.name)

    if (category.subcats == []):    
        badwords = []
        for word in globalBadWords:
            if word not in keywords:
                badwords = badwords + [word]
                
        print keywords
        retTweets = JF.softfiltertweets(tweets, keywords, badwords, 0.5)
        
        return [ {"Cats": catName, "Tweets": retTweets} ]
    else:
        badwords = []

        relTweets = JF.softfiltertweets(tweets, keywords, badwords, 1)
        
        for cat in category.subcats:
            listTweets = listTweets + splitTweets(cat, relTweets, catName + [cat.name])

        print  "listTweets in else"
        print len(listTweets)
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



if __name__ == "__main__":
    main()   
