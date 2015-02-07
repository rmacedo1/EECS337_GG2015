# February 7, 2015
# EECS 337 NLP

import json
import nltk

awards = [];    #hard coding
nominees = [];  #hard coding
predictKeywords = ["think", "calling", "want", "predict", "deserves", "predictions", "if", "hoping",
                   "hope"]
winnerKeywords = ["wins", "won", "speech", "gave speech", "thanks", "thanked"]
presentersKeywords = ["presenting", "giving award", "jokes"]
notAllowed = ["#", ".", "@", ":", "http", "://", "/", "co"];


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
    for tweet in parsedTwees:
        if (not any([x in tweet for x in predictKeywords])):
            noPredTweets.append(tweet)
            
    return noPredTweets
    
def splitIntoCategories(noPredTweets, categories):
    """
    Group up the parsed tweets into the award categories arrays.
    return?
    """
    BestMotionPictureTweets = []
    category2tweets = []
    category2tweets = []
    #ect.
    
    return

def getCount(tweets):
    """
    Takes in a list of tweets and returns a dictionary
    with the frequency of each word
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
