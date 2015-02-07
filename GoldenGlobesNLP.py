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


def getData():
    """input: 
    output: 
    """
    with open("C:\Users\Rosio\Desktop\goldenglobes2015.json\goldenglobes2015_1.json") as file:
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
    award2Tweets = []
    award3Tweets = []
    #ect.
    
    return


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

def results():
    """Return a dictionary with the Hosts and Winners,
    Presenters, Nominees for each Award.
    """
    
    return answersDict;



"""
Also need a Readme file with
-Library citations
-Consulted repositories
-What was done to make the system adaptable
"""
