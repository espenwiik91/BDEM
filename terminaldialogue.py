import csv
import pandas as pd
from main import make_scatterplot, make_histogram
from filters import filter_by_crisislex_for_bigrams, filter_by_crisislex # filter_by_tweet_jiberish  # filter_whole_file

crisislex = "CrisisLexLexicon/CrisisLexRec.txt"


def dialogue(sc):
    tweetcsv = open("irmaHurricaneTweets.csv", "r")
    temp = open("temp.csv", "w+")
    readtweets = tweetcsv.readlines()
    #print(sc.retweets(readtweets))
    first = readtweets[0][-22:]
    last = readtweets[-1][-22:]
    # print(sc.retweets(readtweets))
    # print(most_common(readtweets))
    print("The dataset contains tweets from", first, "to", last)
    print("The dataset contains: ", len(readtweets), "number of tweets.")
    print("Do you want to analyze the whole dataset (1), or choose a subset of the dataset(2)?")
    while True:
        try:
            datasetchoice = int(input("1 or 2"))
            break
        except:
            print("type 1 or 2")
    if datasetchoice == 2:
        divide_dataset(readtweets, temp, sc)
        return
    if datasetchoice == 1:
        whole_set(sc, tweetcsv)
        return


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


def whole_set(sc, tweetscsv):
    temp = lex_to_list(crisislex)
    print("Here are the most used words and combination of two words")
    while True:
        try:
            choice = int(input("Do you want to find the most popular words(1), bigrams(2) or both(3)"))
            break
        except:
            print("Type an int: 1, 2 or 3")
    if choice == 1:
        res1 = sc.wordcounter("irmaHurricaneTweets.csv", 400)
        filtered1 = (filter_by_crisislex(res1, temp))
        make_histogram(filtered1)
        make_scatterplot(filtered1)
        res2 = sc.wordcounter("irmaHurricaneTweets.csv", 20)
        #res2 = filter_by_tweet_jiberish(res2)
        print(res2)
        print(filtered1)
    if choice == 2:
        res2 = (sc.bigram("irmaHurricaneTweets.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res2, temp))
        print(filtered2)
    if choice == 3:
        res3 = sc.wordcounter("irmaHurricaneTweets.csv", 500)
        res4 = sc.bigram("irmaHurricaneTweets.csv", 500)
        filtered3 = filter_by_crisislex(res3, temp)
        filtered4 = filter_by_crisislex_for_bigrams(res4, temp)
        make_histogram(filtered3)
        print(filtered3)
        print(filtered4)
    print("Finished")


def divide_dataset(readtweets, temp, sc):
    print("Which intervall of the ", len(readtweets), " tweets do you want to extract? Type a number to decide where"
                                                      "the subset starts, and a number to decide where it ends")
    start = int(input("num1"))
    stop = int(input("num2"))
    adjust_csv(readtweets, start, stop, temp)
    chosenfirst = readtweets[start][-22:]
    chosenlast = readtweets[stop][-22:]
    print("You will now analyse tweets from ", chosenfirst, " to ", chosenlast)
    temp = lex_to_list(crisislex)
    while True:
        try:
            choice = int(input("Do you want to find the most popular words(1), bigrams(2) or both(3)"))
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
        print(filtered2)
    if choice == 3:
        res3 = sc.wordcounter("temp.csv", 500)
        res4 = sc.bigram("temp.csv", 300)
        filtered3 = filter_by_crisislex(res3, temp)
        filtered4 = filter_by_crisislex_for_bigrams(res4, temp)
        print(filtered3)
        print(filtered4)
        make_histogram(filtered3)
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
