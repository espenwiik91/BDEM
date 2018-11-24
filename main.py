import tweepy
import csv
import logging
from processing import Processing
from nltk.corpus import stopwords
#from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import matplotlib.pyplot as plt
import terminaldialogue as td
import numpy as np
"""
import itertools
import operator
"""

# import nltk
# nltk.download('stopwords')

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


def get_tweets_bulk(api, file):
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
                get_tweet_list(api, tweet_ids)
                tweet_ids = list()


# Takes in csv file with tweet text and tweet times as the columns on each row.
# Writes a new csv file with only tweet times
def get_times(openedcsv):
    times = open("tweet_times.csv", "w")
    for line in openedcsv:
        line = line[-22:]
        times.write(line)


def make_histogram(listOfTuples):
    sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
    df = pd.DataFrame(sorted_data, columns=['frequency', 'word'])
    # print(df)
    # df.plot(kind='bar', logy=True, x='word')
    plt.bar(df['word'], df['frequency'], log=True, width=0.8)
    plt.show()


def make_scatterplot(listOfTuples):
    sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
    df = pd.DataFrame(sorted_data, columns=['frequency', 'word'])
    s = [20 * df['frequency']]
    texts = df['word']
    x = np.random.rand(len(df['word']))
    y = np.random.rand(len(df['word']))
    plt.scatter(x, y, s=s, color='red')
    for i, text in enumerate(texts):
        x_chords = x[i]
        y_chords = y[i]
        plt.scatter(x_chords, y_chords, marker='')
        plt.text(x_chords, y_chords, text, fontsize=20, color="black")
    plt.axis('off')
    plt.show()


def get_tweet_list(api, idlist):
    '''
    Invokes bulk lookup method.
    Raises an exception if rate limit is exceeded.
    '''
    csvWriter = csv.DictWriter
    # fetch as little metadata as possible
    tweets = api.statuses_lookup(id_=idlist, include_entities=False, trim_user=True)
    if len(idlist) != len(tweets):
        Logger.warn('get_tweet_list: unexpected response size %d, expected %d', len(tweets), len(idlist))

    with open('irmaHurricaneTweets.csv', 'a', newline='') as csvFile:
        for tweet in tweets:
            tweetText = tweet.text.encode('utf-8')
            tweetDate = str(tweet.created_at).encode('utf-8')
            writer = csv.writer(csvFile)
            writer.writerows(zip([tweetText], [tweetDate]))
            print(tweetText)
            print(tweetDate)
            csvFile.flush()
    return csvFile


def main():
    sparky = Processing()
    logging.basicConfig(level=logging.WARN)
    global Logger

    """These function calls has to be done the first time running the program.
    They are used to write twitter texts to the file "irmaHurricaneTweets.csv
    Logger = logging.getLogger('get_tweets_by_id')
    get_tweets_bulk(api=authentication(), file="irma_tweet_ids.txt")
    #get_times(tweet_reader, tweet_times)
    """
    td.dialogue(sparky)
    sparky.stopspark()


if __name__ == '__main__':
    main()
