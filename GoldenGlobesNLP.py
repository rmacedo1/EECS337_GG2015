# February 7, 2015
# EECS 337 NLP

import json
import nltk
import re

awards = [];    #hard coding
nominees = [];  #hard coding
predictKeywords = ["think", "calling", "want", "predict", "deserves", "predictions", "if", "hoping",
                   "hope"]
winnerKeywords = ["wins", "won", "speech", "gave speech", "thanks", "thanked"]
presentersKeywords = ["presenting", "giving award", "jokes"]
notAllowed = ["#", ".", "@", ":", "http", "://", "/", "co"];


bestActorMusicalComedy = ["Ralph Fiennes", "Michael Keaton", "Bill Murray", "Joaquin Phoenix", "Christoph Waltz"]
bestActressMusicalComedy = ["Amy Adams", "Emily Blunt", "Helen Mirren", "Julianne Moore", "Quvenzhane Wallis"]
bestPictureComedy = ["Birdman", "The Grand Budapest Hotel", "Into the Woods", "Pride", "St. Vincent"]
bestPictureMusicalComedy = ["Birdman", "The Grand Budapest Hotel", "Into the Woods", "Pride", "St. Vincent"]


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

  
def splitIntoCategories(tweets, categories):
    """
    Group up the parsed tweets into the award categories arrays.
    return?
    """

    #create category arrays
    for x in categories:
        keywords = buildCategoryKeywords(x);
        
        name = x.replace(" ", "")
        name = []
        
        name = getTweets(noPredTweets, keywords)
        print name
        
    return 


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
    

def getTweets(tweets, keywords):
    """
    Takes in a list of tweets and keywords
    Returns a list of tweets relevant to the given keywords
    """
    catTweets = []

    for tweet in tweets:
        if (any ([x in keywords for x in tweet])):
            catTweets.append(tweet)
            
    return catTweets

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
