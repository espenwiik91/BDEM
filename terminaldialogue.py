import csv
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
from main import make_scatterplot, make_histogram
from filters import filter_by_crisislex_for_bigrams, \
    filter_by_crisislex, filter_by_stopwords  # filter_by_tweet_jiberish  # filter_whole_file
import re

"""
These to rows have to be run the first time one uses the stopword filtering method: filter_by_stopwords()
import nltk
nltk.download('stopwords')
"""

stopWords = set(stopwords.words('english'))
# adding 'RT, 'http', '@', '\\n\\n' to the set of stopwords because such information is non-informative for
# several analysis purposes.
stopWords.update(['RT', 'http', '@', '\\n\\n'])

crisislex = "CrisisLexLexicon/CrisisLexRec.txt"


def dialogue(sc):
    tweetcsv = open("irmaHurricaneTweets.csv", "r")
    temp = open("temp.csv", "w+")
    readtweets = tweetcsv.readlines()
    # print(sc.retweets(readtweets))
    first = readtweets[0][-22:]
    last = readtweets[-1][-22:]
    # print(sc.retweets(readtweets))
    # print(most_common(readtweets))
    print("################################################################# \n"
          "Welcome to this tool for twitter analysis during disaster events")
    print("In this program, tweets from the irma hurricane is analyzed. \n"
          "The dataset contains tweets from", first, "to", last)
    print("and it contains: ", len(readtweets), "number of tweets.")
    print("Do you want to analyze the whole dataset (1), or choose a subset of the dataset(2)?")
    while True:
        try:
            datasetchoice = int(input("1 or 2"))
            break
        except:
            print("type 1 or 2")
    if datasetchoice == 2:
        divide_dataset(sc, readtweets, temp)
        return
    if datasetchoice == 1:
        whole_set(sc, readtweets, temp)
        return


def whole_set(sc, readtweets, temp):
    crisislexlist = lex_to_list(crisislex)
    while True:
        try:
            choice = int(input("Which data do you want to see? \n"
                               " Do you want to find the most popular words(1), bigrams(2), retweets on a chosen word(3), or all three(4)"))
            break
        except:
            print("Type 1, 2, 3 or 4")
    if choice == 1:
        res1 = sc.wordcounter("irmaHurricaneTweets.csv", 400)
        filtered1 = filter_by_crisislex(res1, crisislexlist)
        print(filter_by_stopwords(res1, stopWords))
        make_histogram(filtered1)
        make_scatterplot(filtered1)
        res2 = sc.wordcounter("irmaHurricaneTweets.csv", 20)
        print(res2)
        print(filtered1)
    if choice == 2:
        res3 = (sc.bigram("irmaHurricaneTweets.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res3, crisislexlist))
        print(filtered2)
    if choice == 3:
        try:
            rtword = str(input(
                "This function lets you find the most retweeted tweets containing a chosen word. Type a word"))
        except:
            print("Type a word")
        retweets = top5_tweets("irmaHurricaneTweets.csv", rtword)
        for tweet in retweets:
            print(tweet)
    if choice == 4:
        res4 = sc.wordcounter("irmaHurricaneTweets.csv", 500)
        res5 = sc.bigram("irmaHurricaneTweets.csv", 500)
        filtered3 = filter_by_crisislex(res4, temp)
        filtered4 = filter_by_crisislex_for_bigrams(res5, crisislexlist)
        make_histogram(filtered3)
        print(filtered3)
        print(filtered4)
    try:
        repeat = int(input(
            "Do you want to stop analyzing(1), do another analysis on this dataset(2), or do an anlysis on a subset of the dataset (3)"))
    except:
        print("type 1, 2 or 3")
    if repeat == 1:
        print("Finished")
    if repeat == 2:
        whole_set(sc, readtweets, temp)
    if repeat == 3:
        divide_dataset(sc, readtweets, temp)


def divide_dataset(sc, readtweets, temp):
    print("Which intervall of the ", len(readtweets), " tweets do you want to extract? Type a number to decide where"
                                                      "the subset starts, and a number to decide where it ends \n"
                                                      "It should at least contain 10 000 tweets")
    start = int(input("start"))
    stop = int(input("stop"))
    adjust_csv(readtweets, start, stop, temp)
    chosenfirst = readtweets[start][-22:]
    chosenlast = readtweets[stop][-22:]
    print("You will now analyse tweets from ", chosenfirst, " to ", chosenlast)
    temp = lex_to_list(crisislex)
    while True:
        try:
            choice = int(input(
                "Do you want to find the most popular words(1), bigrams(2), retweets containing a chosen word(3), or all three(4)"))
            break
        except:
            print("Type an int: 1, 2 or 3")
    if choice == 1:
        res1 = sc.wordcounter("temp.csv", 500)
        filtered1 = (filter_by_crisislex(res1, temp))
        make_histogram(filtered1)
        print(filtered1)
    if choice == 2:
        res2 = (sc.bigram("temp.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res2, temp))
        # make_histogram(filtered2)
        print(filtered2)
    if choice == 3:
        try:
            rtword = str(input(
                "This function lets you find the most retweeted tweets containing a chosen word. Type a word"))
        except:
            print("Type a word")
        retweets = top5_tweets("irmaHurricaneTweets.csv", rtword)
        for tweet in retweets:
            print(tweet)
    if choice == 4:
        res3 = sc.wordcounter("temp.csv", 500)
        res4 = sc.bigram("temp.csv", 300)
        filtered3 = filter_by_crisislex(res3, temp)
        filtered4 = filter_by_crisislex_for_bigrams(res4, temp)
        print(filtered3)
        print(filtered4)
        make_histogram(filtered3)
    try:
        repeat = int(input(
            "Do you want to stop analyzing(1), do another anlysis on a subset of the dataset (2), or do an analysis on the whole dataset (3)"))
    except:
        print("type 1, 2 or 3")
    if repeat == 1:
        print("Finished")
    if repeat == 2:
        divide_dataset(sc, readtweets, temp)
    if repeat == 3:
        whole_set(sc, readtweets, temp)

    print("Finished")


def adjust_csv(source_file, start, end, dest_name):
    writer = csv.writer(dest_name)
    count = 0
    for row in csv.reader(source_file):
        if start <= count <= end:
            writer.writerow(row)
        count += 1


# takes a csv file as argument and writes lines to a list, which is returned
def lex_to_list(lex):
    lex = open(lex, "r")
    lex = lex.readlines()
    res = []
    for word in lex:
        word = word[:-1]
        res.append(word)
    return res


def top5_tweets(csvFileWithTweetTextAndTweetDate, filterword):
    df = pd.read_csv(csvFileWithTweetTextAndTweetDate,
                     names=['TweetText', 'TweetDate'],
                     encoding='utf-8')
    filtered_tweetText = []
    for line in df['TweetText'][:100].values:
        row = pd.Series([line])
        filtered = row.str.contains(filterword, regex=True, flags=re.IGNORECASE)
        if filtered[0] == True:
            filtered_tweetText.append(line)
    counter = Counter(filtered_tweetText).most_common(5)
    return counter


"""
def load_tweets(tweet_file):
    tweet_df = pd.read_csv(tweet_file)
    tweet_df = tweet_df.sort_values(by='retweets', ascending=False)
    tweet_df = tweet_df.reset_index(drop=True)
    print('Mean retweets:', round(tweet_df['retweets'].mean(), 2), '\n')
    print('Top 5 RTed tweets:')
    for i in range(5):
        print(tweet_df['Tweet text'].ix[i], '-', tweet_df['retweets'].ix[i])

    # return tweet_df


# load_tweets("irmaHurricaneTweets.csv")
"""
