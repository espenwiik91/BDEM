import csv
from collections import Counter
from nltk.corpus import stopwords
import string
from filters import filter_by_crisislex_for_bigrams, \
    filter_by_crisislex, filter_by_stopwords  # filter_by_tweet_jiberish  # filter_whole_file
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

"""
These to rows have to be run the first time one uses the stopword filtering method: filter_by_stopwords()
import nltk
nltk.download('stopwords')
"""

stopWords = set(stopwords.words('english'))
# adding 'RT, 'http', '@', '\\n\\n' to the set of stopwords because such information is non-informative for
# several analysis purposes.
stopWords.update(['RT', 'http', '@', '\\n\\n'])
tempsetadjusted = False
crisislex = "CrisisLexLexicon/CrisisLexRec.txt"


def dialogue(sc):
    tweetcsv = open("irmaHurricaneTweets.csv", "r")
    readtweets = tweetcsv.readlines()
    # print(sc.retweets(readtweets))
    first = readtweets[0][-22:]
    last = readtweets[-1][-22:]
    # print(sc.retweets(readtweets))
    # print(most_common(readtweets))
    print("################################################################# \n"
          "Welcome to this tool for twitter analysis during disaster events")
    print("In this program, tweets from the irma hurricane are analyzed. \n"
          "The dataset contains tweets from", first, "to", last, "\n"
                                                                 "and it contains: ", len(readtweets),
          "number of tweets.")
    print("Do you want to analyze the whole dataset (1), or choose a subset of the dataset(2)?")
    while True:
        try:
            datasetchoice = int(input("1 or 2"))
            print("\n")
            break
        except:
            print("type 1 or 2")
    if datasetchoice == 2:
        divide_dataset(sc, readtweets)
        return
    if datasetchoice == 1:
        whole_set(sc, readtweets)
        return


def whole_set(sc, readtweets):
    crisislexlist = lex_to_list(crisislex)
    while True:
        try:
            choice = int(input("Which data do you want to see? \n"
                               " Do you want to find the most popular words(1), bigrams(2), retweets(3), URLs(4) or all four(5)"))
            print("\n")
            break
        except:
            print("Type 1, 2, 3 or 4")
    if choice == 1:
        print("Here are the n most disaster-related words in this dataset")
        res1 = sc.wordcounter("irmaHurricaneTweets.csv", 500)
        filtered1 = filter_by_crisislex(res1, crisislexlist)
        make_table(filtered1, "word", "frequency")
        print("\n")
    if choice == 2:
        print("Here are the n most disaster-related combintion of two words in this dataset")
        res3 = (sc.bigram("irmaHurricaneTweets.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res3, crisislexlist))
        make_table(filtered2, "word", "frequency")
        print("\n")
    if choice == 3:
        rtword = str(input(
            ("This function lets you find the most retweeted tweets\n"
             "You can either choose to find the five most retweeted tweets in general, or choose to search for a keyword\n"
             "Type a word to search for a chosen keyword, or press enter if you the most retweeted overall\n"
             "Chosen keywords will not always give a result"
             "Type a word, or hit enter. \n")))
        if len(rtword) != 0:
            print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", rtword))
            while True:
                print("Type a new word if you want to try another keyword, or hit enter to proceed")
                choice = str(input("Type a word or hit enter"))
                if len(choice) != 0:
                    print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", choice))
                else:
                    break
        else:
            retweets = top5_tweets("irmaHurricaneTweets.csv")
            for tweet in retweets:
                print(tweet)
        print("\n")
    if choice == 4:
        print("You will now be shown the most popular URLs")
        urls = top5_tweets_with_filterword("irmaHurricaneTweets.csv", "http")
        finalurls = []
        for url in urls:
            url = url[0]
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
            for element in url:
                finalurls.append(element)
        for link in finalurls:
            print(link)
    if choice == 5:
        res4 = sc.wordcounter("irmaHurricaneTweets.csv", 500)
        res5 = sc.bigram("irmaHurricaneTweets.csv", 500)
        filtered3 = filter_by_crisislex(res4, crisislexlist)
        filtered4 = filter_by_crisislex_for_bigrams(res5, crisislexlist)
        print("Here are the n most disaster-related words in this dataset")
        make_table(filtered3, "word", "frequency")
        print("\n")
        print("Here are the n most disaster-related words combination of two words in this dataset")
        make_table(filtered4, "word", "frequency")
        print("\n")
        print("You will now be shown the most popular URLs")
        urls = top5_tweets_with_filterword("irmaHurricaneTweets.csv", "http")
        finalurls = []
        for url in urls:
            url = url[0]
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
            for element in url:
                finalurls.append(element)
        for link in finalurls:
            print(link)
        rtword = str(input(
            ("This function lets you find the most retweeted tweets\n"
             "You can either choose to find the five most retweeted tweets in general, or choose to search for a keyword\n"
             "Type a word to search for a chosen keyword, or press enter if you the most retweeted overall\n"
             "Chosen keywords will not always give a result"
             "Type a word, or hit enter. \n")))
        if len(rtword) != 0:
            print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", rtword))
            while True:
                print("Type a new word if you want to try another keyword, or hit enter to proceed")
                choice = str(input("Type a word or hit enter"))
                if len(choice) != 0:
                    print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", choice))
                else:
                    break
        else:
            retweets = top5_tweets("irmaHurricaneTweets.csv")
            for tweet in retweets:
                print(tweet)
        print("\n")
    try:
        repeat = int(input(
            "Do you want to stop analyzing(1), do another analysis on this dataset(2), or do an anlysis on a subset of the dataset (3)"))
    except:
        print("type 1, 2 or 3")
    if repeat == 1:
        print("Finished")
    if repeat == 2:
        whole_set(sc, readtweets)
    if repeat == 3:
        divide_dataset(sc, readtweets)


def divide_dataset(sc, readtweets):
    print("Which intervall of the ", len(readtweets), " tweets do you want to extract? Type a number to decide where\n"
                                                      "the subset starts, and a number to decide where it ends \n"
                                                      "It should at least contain 10 000 tweets")
    try:
        start = int(input("start"))
        stop = int(input("stop"))
    except:
        print("type two numbers")
    global tempsetadjusted
    if tempsetadjusted == False:
        adjust_csv(readtweets, start, stop)

    else:
        temp = open("temp.csv", "w+")
        adjust_csv(temp, start, stop)
    chosenfirst = readtweets[start][-22:]
    chosenlast = readtweets[stop][-22:]
    print("You will now analyse tweets from ", chosenfirst, " to ", chosenlast)
    crisis = lex_to_list(crisislex)
    while True:
        try:
            choice = int(input(
                "Do you want to find the most popular words(1), bigrams(2), retweets(3), URLs(4), or all four(5)"))
            print("\n")
            break
        except:
            print("Type an int: 1, 2 or 3")
    if choice == 1:
        res1 = sc.wordcounter("temp.csv", 500)
        filtered1 = (filter_by_crisislex(res1, crisis))
        print("Here are the 10 most disaster-related words in this dataset")
        make_table(filtered1, "word", "frequency")
        print("\n")
    if choice == 2:
        res2 = (sc.bigram("temp.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res2, crisis))
        print("Here are the 10 most disaster-related words combination of two words in this dataset")
        make_table(filtered2, "word", "frequency")
        print("\n")
    if choice == 3:
        rtword = str(input(
            ("This function lets you find the most retweeted tweets\n"
             "You can either choose to find the five most retweeted tweets in general, or choose to search for a keyword\n"
             "Type a word to search for a chosen keyword, or press enter if you the most retweeted overall\n"
             "Chosen keywords will not always give a result"
             "Type a word, or hit enter. \n")))
        if len(rtword) != 0:
            print(top5_tweets_with_filterword("temp.csv", rtword))
            while True:
                print("Type a new word if you want to try another keyword, or hit enter to proceed")
                choice = str(input("Type a word or hit enter"))
                if len(choice) != 0:
                    print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", choice))
                else:
                    break
        else:
            retweets = top5_tweets("temp.csv")
            for tweet in retweets:
                print(tweet)
        print("\n")
    if choice == 4:
        print("You will now be shown the most popular URLs")
        urls = top5_tweets_with_filterword("temp.csv", "http")
        finalurls = []
        for url in urls:
            url = url[0]
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
            for element in url:
                finalurls.append(element)
        for link in finalurls:
            print(link)
    if choice == 5:
        res3 = sc.wordcounter("temp.csv", 500)
        res4 = sc.bigram("temp.csv", 500)
        filtered3 = filter_by_crisislex(res3, crisis)
        filtered4 = filter_by_crisislex_for_bigrams(res4, crisis)
        print("Here are the 10 most disaster-related words in this dataset")
        make_table(filtered3, "word", "frequency")
        print("Here are the 10 most disaster-related words combination of two words in this dataset")
        make_table(filtered4, "word", "frequency")
        print("\n")
        print("You will now be shown tweets containing the most popular URLs")
        print("You will now be shown the most popular URLs")
        urls = top5_tweets_with_filterword("temp.csv", "http")
        finalurls = []
        for url in urls:
            url = url[0]
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
            for element in url:
                finalurls.append(element)
        for link in finalurls:
            print(link)
        print("\n")
        rtword = str(input(
            ("This function lets you find the most retweeted tweets\n"
             "You can either choose to find the five most retweeted tweets in general, or choose to search for a keyword\n"
             "Type a word to search for a chosen keyword, or press enter if you the most retweeted overall\n"
             "Chosen keywords will not always give a result"
             "Type a word, or hit enter. \n")))
        if len(rtword) != 0:
            print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", rtword))
            while True:
                print("Type a new word if you want to try another keyword, or hit enter to proceed")
                choice = str(input("Type a word or hit enter"))
                if len(choice) != 0:
                    print(top5_tweets_with_filterword("temp.csv", choice))
                else:
                    break
        else:
            retweets = top5_tweets("temp.csv")
            for tweet in retweets:
                print(tweet)
        print("\n")
    try:
        repeat = int(input(
            "Do you want to stop analyzing(1), do another anlysis on another subset of the dataset (2), "
            "or do an analysis on the whole dataset (3)"))
    except:
        print("type 1, 2 or 3")
    if repeat == 1:
        print("Finished")
    if repeat == 2:
        divide_dataset(sc, readtweets)
    if repeat == 3:
        whole_set(sc, readtweets)

    print("Finished")


def adjust_csv(source_file, start, end):
    temp = open("temp.csv", "w+")
    writer = csv.writer(temp)
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


def top5_tweets_with_filterword(csvFileWithTweetTextAndTweetDate, filterword):
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


def top5_tweets(csvFileWithTweetTextAndTweetDate):
    df = pd.read_csv(csvFileWithTweetTextAndTweetDate,
                     names=['TweetText', 'TweetDate'],
                     encoding='utf-8')
    filtered_tweetText = []
    for line in df['TweetText'][:100].values:
        row = pd.Series([line])
        filtered = row.str.contains(" ", regex=True, flags=re.IGNORECASE)
        if filtered[0] == True:
            filtered_tweetText.append(line)
    counter = Counter(filtered_tweetText).most_common(5)
    return counter


def make_histogram(listOfTuples):
    sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
    df = pd.DataFrame(sorted_data, columns=['frequency', 'word'])
    df.plot(kind='bar', logy=True, x='word')
    plt.bar(df['word'], df['frequency'], log=True, width=0.8)
    plt.show()


def make_table(listOfTuples, firstheader, secondheader):
    sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
    df = pd.DataFrame(sorted_data, columns=[firstheader, secondheader])
    print(df)


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
