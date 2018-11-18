# imports
import tweepy
import json
from pyspark import SparkContext


logFile = "tweets.csv"
sc = SparkContext.getOrCreate()
lines = sc.textFile(logFile)
lines_nonempty = lines.filter(lambda x: len(x) > 0)
words = lines_nonempty.flatMap(lambda x: x.split())
wordcounts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).map(lambda x: (x[1], x[0])).sortByKey(
    False)
print(wordcounts.take(30))
"""for word in wordcounts.take(30):
    if str(word[1]) in "CrisisLexLexicon/CrisisLexRec.txt":
        print(word[1])
sc.stop()

"""
sc = SparkContext.getOrCreate()
sentences = sc.textFile(logFile) \
    .glom() \
    .map(lambda x: " ".join(x)) \
    .flatMap(lambda x: x.split("."))
bigrams = sentences.map(lambda x: x.split()) \
    .flatMap(lambda x: [((x[i], x[i + 1]), 1) for i in range(0, len(x) - 1)])

freq_bigrams = bigrams.reduceByKey(lambda x, y: x + y) \
    .map(lambda x: (x[1], x[0])) \
    .sortByKey(False)
print(freq_bigrams.take(10))
sc.stop()



# Uses twitter credentials to get connection to twitter. Connection is declared in variable api, which is returned
from tweepy.streaming import json


def tokenization():
    auth = tweepy.OAuthHandler("SQEmFzL7P2C9xe0Bcs8FZh0D3", "DRC5AoeM6wGXkfMD7pZ6HFFfLAqBVIi5Qk0Zo5uwLLA3HPHLKx")
    auth.set_access_token("1051831213109993472-sYqCSmCkPxDWMBmLplmuHR5rHchLwp",
                          "BGQ757siUo8gei8tVgCZxGK3aAlH85TyJBGyzU7zYituN")
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


# Opens and returns a disaster lexicon from CrisisLex
def lex_opener(lexicon):
    lex = open(lexicon)
    lex = lex.read()
    return lex


def create_csv():
    csvfile = open("tweets.csv", "w")
    return csvfile


def lookup_tweets(tweet_IDs, api):
    for status in tweepy.Cursor(api.status_lookup, id=tweet_IDs).items():
        print(json.dumps(status))


def process_or_store(tweet):
    print(json.dumps(tweet))


def read_tweet(file, api):
    file = open(file, "r")
    csvfile = open("tweets.csv", "w+", encoding='utf-8')
    counter = 0
    temp = list()
    # print(temp)
    for line in file:
        try:
            if len(temp) > 200:
                break
            tweet = api.get_status(int(line))
            en = str(tweet.text)
            to = str(tweet.created_at)
            info = str(en + " " + to)
            temp.append(info)
        except:
            pass

    for element in temp:
        csvfile.write(element)
        csvfile.write("\n")
    csvfile.close()


def main():
    api = tokenization()
    lex = lex_opener("CrisisLexLexicon/CrisisLexRec.txt")
    # lookup_tweets("irma_tweet_ids.txt", api)
    wordcounter()
