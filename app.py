import tweepy
import csv
import logging
from processing import Processing
from nltk.corpus import stopwords
import terminaldialogue as td

"""
import itertools
import operator
"""

# import nltk
# nltk.download('stopwords')

"""
    Initiates different variables to be used by programs later. 
"""

global Logger
logFile = "irmaHurricaneTweets.csv"
tweet_reader = open(logFile, "r")
proxy = "temp.csv"
crisislex = "CrisisLexLexicon/CrisisLexRec.txt"
stopWords = set(stopwords.words('english'))

CONSUMER_KEY = 'er2Gj89d8Mzcx0Uy6enUGY5Pl'
CONSUMER_SECRET = 'toow54gCrcGut2OdH3CWCxOqsBDVphk6UMKUTVudNLnMRUnSMR'
OAUTH_TOKEN = '1053267399309438976-A5b36TUs8H525zZAwDJsmqt7tun6D0'
OAUTH_TOKEN_SECRET = '0kbdfB6sdfgfG7xis3Fp2UjVlHcNEQEXclyLinOmPut1R'

# Twitter API Limit.
batch_size = 100


def authentication():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def get_tweet_id(line):
    tweet_id_raw = line.decode('utf-8').strip()
    tweet_id = tweet_id_raw + ','
    print(tweet_id)
    return tweet_id


def get_tweets_bulk(api, file, outputcsvfile):
    '''
    Fetches content for tweet IDs in a file using bulk request method,
    which vastly reduces number of HTTPS requests compared to above;
    however, it does not warn about IDs that yield no tweet.

    `api`: Initialized, authorized API object from Tweepy
    `file`: Path to file containing IDs
    '''
    # process IDs from the file
    tweet_ids = list()
    with open(file, 'rb') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('Enqueing tweet ID %s', tweet_id)
            tweet_ids.append(tweet_id)
            # API limits batch size
            if len(tweet_ids) == batch_size:
                Logger.debug('get_tweets_bulk: fetching batch of size %d', batch_size)
                get_tweet_list(api, tweet_ids, outputcsvfile=outputcsvfile)
                tweet_ids = list()


# Takes in csv file with tweet text and tweet times as the columns on each row.
# Writes a new csv file with only tweet times
def get_times(openedcsv):
    times = open("tweet_times.csv", "w")
    for line in openedcsv:
        line = line[-22:]
        times.write(line)

'''
    Retrieves tweets in bulk. Outputs to a csv file with tweet.text and tweet.created_at.
'''
def get_tweet_list(api, idlist, outputcsvfile):
    # Feeds a list of ids, and sends the request to the Twitter API. Parameters decrease metadata.
    tweets = api.statuses_lookup(id_=idlist, include_entities=False, trim_user=True)
    # Warns users if response size is smaller than expected. < 100.
    if len(idlist) != len(tweets):
        Logger.warn('get_tweet_list: unexpected response size %d, expected %d', len(tweets), len(idlist))
    # Opens csv file and writes rows with the requested twitter data.
    with open(outputcsvfile, 'a', newline='') as csvFile:
        for tweet in tweets:
            tweetText = tweet.text.encode('utf-8')
            tweetDate = str(tweet.created_at).encode('utf-8')
            writer = csv.writer(csvFile)
            writer.writerows(zip([tweetText], [tweetDate]))
    return csvFile


def main():
    sparky = Processing()
    logging.basicConfig(level=logging.WARN)
    global Logger

    # These function calls has to be done the first time running the program.
    # They are used to write twitter texts to the file "irmaHurricaneTweets.csv
    Logger = logging.getLogger('get_tweets_by_id')

    """
        ******************************************
        TWEET COLLECTION;
        IF(!) you want to collect your own dataset instead of the sample.
        The four lines below this comment must be uncommented(remove #) and run.
        Remember to comment back in order to not overwrite the file again when running functionality on dataset 
    
    """
    #fhand = open("irmaHurricaneTweets.csv", "w+")
    #fhand.truncate()
    #fhand.close()
    #get_tweets_bulk(api=authentication(), file="irma_tweet_ids.txt", outputcsvfile="irmaHurircaneTweets.csv")

    td.dialogue(sparky)
    sparky.stopspark()


if __name__ == '__main__':
    main()
