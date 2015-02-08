# February 7, 2015
# EECS 337 NLP

import json
import nltk
import re
import Category
import JakeFunctions

predictKeywords = ["think", "calling", "want", "predict", "deserves", "predictions", "if", "hoping",
                   "hope", "which", "Which", "Calling", "Think", "who", "Who", "Want",
                   "Prediction", "Predictions", "prediction", "Predictor", "predictor"
                   "If", "Hope", "please", "Please"]

winnerKeywords = ["wins", "won", "speech", "gave speech", "thanks", "thanked",
                  "Wins", "Won", "Speech", "Gave Speech", "Thanks", "Thanked",
                  "congrats", "Congrats"]

presentersKeywords = ["presenting", "giving award", "jokes"]
notAllowed = ["#", ".", "@", ":", "http", "://", "/", "co"]
"""
categories = ["Best Motion Picture", "Best Performance by an Actor in a Motion Picture",
              "Best Performance by an Actress in a Motion Picture",
              "Best Performance by an Actor in a Supporting Role in a Motion Picture",
              "Best Performance by an Actress in a Supporting Role in a Motion Picture",
              "Best Director", "Best Screen Play", "Best Original Song",
              "Best Original Score", "Best Foreign Language Film", "Best Animated Feature Film"
              "Best Performance by an Actor in a Television Series",
              "Best Performance by an Actor in a Mini-Series or a Motion Picture Made for Television"
              "Best Performance by an Actor in a Television Series",
              "Best Performance by an Actress in a Television Series",
              "Best Performance by an Actress in a Mini-Series or a Motion Picture Made for Television"
              "Best Performance by an Actor in a Supporting Role in a Series, Mini-Series, or Motion Picture Made for Television",
              "Best Performance by an Actress in a Supporting Role in a Series, Mini-Series, or Motion Picture Made for Television",
              "Best Televison Series", "Best Mini-Series or Motion Picture Made for Television"]

"""
#globalBadWords = ["Supporting", "Drama", "Musical or Comedy", 

(categories, nominees) = Category.createCategories()


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
  
def splitIntoCategories(tweets):
    """
    Group up the parsed tweets into the award categories arrays.
    categories: A list of Category class
    return?
    """

    countDict = []
    listDictionary = []

    #create category arrays

    for x in categories: #category dictionary
        listDictionary = listDictionary + splitTweets(x, tweets, [x.name])
    
    for x in zip(listDictionary, nominees): 

        winTweets = winnerTweets(x[0]["Tweets"])


        #get word frequencies
        countDict = getCount(winTweets)
        print countDict

        #get nominees for category
        if (type(x[1]) is list):
            noms = x[1]
        else:
            noms =  x[1]["Person"] #getNominees(x["Cats"])
        
        #try and find winner
        winner = predictWinner(countDict, noms)

        print winner
        
    return 



def splitTweets (category, tweets, catName):
    """
    Takes an object of type Category class, a list of tweets, and a list containing the category name
    Returns a list of dictionaries with tweets pertaining to that category
    """
    level = 0;
    
    if (category.subcats == []):
        return [ {"Cats": catName, "Tweets": tweets} ]
    else:

        keywords = buildCategoryKeywords(category.name)
        
        print keywords
        badwords = []
            
        relTweets = filtertweets(tweets, keywords, badwords)

        listTweets = []

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
    
    catKeywords = re.findall('[A-Z][^A-Z]*', categoryname)

    for word in catKeywords:
        noSpaceWord = word.replace(" ", "")
        catKeywords2.append(noSpaceWord)
        
    return catKeywords2
    
"""
def getTweets(tweets, goodkeywords):
    
    Takes in a list of tweets and keywords
    Returns a list of tweets relevant to the given keywords

    Kristin's Code

    catTweets = []

    for tweet in tweets:
        if (any ([x in keywords for x in tweet]s)):
            catTweets.append(tweet)
            
    return catTweets
"""
""" NOT NEEDED ANYMORE HOPEFULLY
def getNominees(category):
    
    Takes in a string (or a list of appended name) of the category name for which it
    will return the nominees

    Hard-coded for now
    
    
    
    bestActorMusicalComedy = ["Ralph Fiennes", "Michael Keaton", "Bill Murray", "Joaquin Phoenix", "Christoph Waltz"]
    bestActressMusicalComedy = ["Amy Adams", "Emily Blunt", "Helen Mirren", "Julianne Moore", "Quvenzhane Wallis"]
    bestPictureComedy = ["Birdman", "The Grand Budapest Hotel", "Into the Woods", "Pride", "St. Vincent"]
    bestPictureMusicalComedy = ["Birdman", "The Grand Budapest Hotel", "Into the Woods", "Pride", "St. Vincent"]
    

    with open("categories_nominees_winners.json") as infile:
        awards = json.load(infile)["Awards"]

    for line in awards:        
"""

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

def getCount(tweets):
    """
    Takes in a list of tweets and returns a dictionary
    with the frequency of each word
    
    Kristin's dictionary code
    """
    diction = dict()
    
    for tweet in tweets:
        for word in tweet:
            if word[0].isupper():
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

def predictWinner(namedict, noms):
    """
    Takes a dictionary of words and their count/frequency and
    a list of category nominees and returns the predicted winner.
    
    Jake's winner predictor function
    """
    print "Length of dictionary with results" + len(namedict)
    
    for word in sorted(namedict, key=namedict.get, reverse=True):
       for name in noms:
           if word in noms:
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
