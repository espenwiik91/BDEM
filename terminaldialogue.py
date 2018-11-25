import csv
from collections import Counter
from nltk.corpus import stopwords
from filters import filter_by_crisislex_for_bigrams, filter_by_crisislex
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import psutil


#These to rows have to be run the first time one uses the stopword filtering method: filter_by_stopwords()
#import nltk
#nltk.download('stopwords')


stopWords = set(stopwords.words('english'))
# adding 'RT, 'http', '@', '\\n\\n' to the set of stopwords because such information is non-informative for
# several analysis purposes.
stopWords.update(['RT', 'http', '@', '\\n\\n', '.', ',', ':', ';', '/', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '|'])
tempsetadjusted = False
crisislex = "CrisisLexLexicon/CrisisLexRec.txt"

#Initiates a terminal-based dialogue with the program user. Takes a SparkContext object as argument.
#Based on the decicions of the user, the program proceeds to whole_set() or divide_dataset().
#When whole_set() or divide_dataset() is called, the SparkContext object is passed on as argument
#in addition to a reader object for the csv file "irmaHurricaneTweets".
#Dialogue() is called in the main function of the app class.
def dialogue(sc):
    tweetcsv = open("irmaHurricaneTweets.csv", "r")
    readtweets = tweetcsv.readlines()
    first = readtweets[0][-22:]
    last = readtweets[-1][-22:]
    print("################################################################# \n"
          "Welcome to this tool for twitter analysis of disaster events")
    print("In this program, tweets from the irma hurricane are analyzed. \n"
          "The dataset contains tweets in the time period from", first, "to", last, "and it contains: ", len(readtweets),
          "number of tweets.")
    print(" Enter 1 to analysis on the full dataset (1). Enter 2 to choose a subset for analysis(2).")
    while True:
        try:
            datasetchoice = int(input("1 or 2\n"))
            assert datasetchoice == 1 or datasetchoice == 2
            break
        except:
            print("Type 1 or 2")
    if datasetchoice == 2:
        divide_dataset(sc, readtweets)
        return
    if datasetchoice == 1:
        whole_set(sc, readtweets)
        return

#This function is called in either dialogue() or divide_dataset(). It takes a SparkContext object and a csv reader
#of the csv file "irmaHurricaneTweets" as arguments. Whole_set() is a continuation of dialogue() or divide_dataset().
# When the function is called, the user can choose to retrieve the most popular words, bigrams, urls and RTs of the
# whole dataset. When suitable, different visualizations are provided in bar charts. Towards the end of the function,
# the user can choose to stop the running of the program in (in the main function in the app), run whole_set() again,
# or to run divide_dataset().
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
        print("Here are the 10 most disaster-related words in this dataset")
        res1 = sc.wordcounter("irmaHurricaneTweets.csv", 500)
        filtered1 = filter_by_crisislex(res1, crisislexlist)
        make_table(filtered1, "word", "frequency")
        make_histogram(filtered1)
        make_scatterplot(filtered1)
        print("\n")
    if choice == 2:
        print("Here are the 10 most disaster-related combintion of two words in this dataset")
        res3 = (sc.bigram("irmaHurricaneTweets.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res3, crisislexlist))
        make_table(filtered2, "word", "frequency")
        make_histogram(filtered2)
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
        print("Here are the 10 most disaster-related words in this dataset")
        make_table(filtered3, "word", "frequency")
        make_histogram(filtered3)
        print("\n")
        print("Here are the 10 most disaster-related words combination of two words in this dataset")
        make_table(filtered4, "word", "frequency")
        make_histogram(filtered4)
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
                    print(top5_tweets_with_filterword("irmaHurricaneTweets.csv", choice))
                else:
                    break
        else:
            retweets = top5_tweets("irmaHurricaneTweets.csv")
            for tweet in retweets:
                print(tweet)
        print("\n")
    while True:
        try:
            repeat = int(input(
                "Do you want to stop analyzing(1), do another analysis on this dataset(2), or do an anlysis on a subset of the dataset (3)"))
            assert repeat == 1 or repeat == 2 or repeat == 3
            break
        except:
            print("Type 1, 2 or 3")
    if repeat == 1:
        print("Finished")
    if repeat == 2:
        whole_set(sc, readtweets)
    if repeat == 3:
        divide_dataset(sc, readtweets)

#This function is called in either dialogue() or divide_dataset(). It takes a SparkContext object and a csv reader
#of the csv file "irmaHurricaneTweets" as arguments. Whole_set() is a continuation of dialogue() or divide_dataset().
#The exact same functionality as in whole_set() is provided here, but the user of the system is allowed to choose
#a subset of the csv file "irmaHurricaneTweets" and overwrite "temp.csv" with this content. Towards the end of
# the function, the user can choose to stop the running of the program in (in the main function in the app),
# to run divide_dataset() again, or to run divide_dataset().
def divide_dataset(sc, readtweets):
    print("Which intervall of the ", len(readtweets), " tweets do you want to extract? Type a number to decide where\n"
                                                      "the subset starts, and a number to decide where it ends \n"
                                                       "It should at least contain 10 000 tweets")
    while True:
        try:
            start = int(input("start"))
            stop = int(input("stop"))
            assert start >= 0 and start < stop and stop <= len(readtweets)
            break
        except:
            print("Type two valid numbers")
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
        print("Here are the 10 most disaster-related words in this dataset"
              ". A bar chart is shown in SciView")
        make_table(filtered1, "word", "frequency")
        make_histogram(filtered1)
        print("\n")
    if choice == 2:
        res2 = (sc.bigram("temp.csv", 500))
        filtered2 = (filter_by_crisislex_for_bigrams(res2, crisis))
        print("Here are the 10 most disaster-related words combination of two words in this dataset"
              ". A bar chart is shown in SciView")
        make_table(filtered2, "word", "frequency")
        make_histogram(filtered2)
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
        print("Here are the 10 most disaster-related words in this dataset"
              ". A bar chart is shown in SciView")
        make_table(filtered3, "word", "frequency")
        make_histogram(filtered3)
        print("Here are the 10 most disaster-related words combination of two words in this dataset"
              ". A bar chart is shown in SciView")
        make_table(filtered4, "word", "frequency")
        make_histogram(filtered4)
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
    while True:
        try:
            repeat = int(input(
                "Do you want to stop analyzing(1), do another anlysis on another subset of the dataset (2), "
                "or do an analysis on the whole dataset (3)"))
            assert repeat == 1 or repeat == 2 or repeat == 3
            break
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



# takes a txt file as argument and writes strings to a list, which is returned
def lex_to_list(lex):
    lex = open(lex, "r")
    lex = lex.readlines()
    res = []
    for word in lex:
        word = word[:-1]
        res.append(word)
    return res

#Takes a csv file with tweet text and tweet date and a string as arguments. Returns a Counter object that contains
#a list with the five most frequent RTs containing the specific string.
def top5_tweets_with_filterword(csvFileWithTweetTextAndTweetDate, filterword):
    df = pd.read_csv(csvFileWithTweetTextAndTweetDate,
                     names=['TweetText', 'TweetDate'],
                     encoding='utf-8')
    filtered_tweetText = []
    for line in df['TweetText'].values:
        row = pd.Series([line])
        filtered = row.str.contains(filterword, regex=True, flags=re.IGNORECASE)
        if filtered[0] == True:
            filtered_tweetText.append(line)
    counter = Counter(filtered_tweetText).most_common(5)
    return counter
"""
    takes a csv file as argument, and returns a list with the five most frequent RTs in the csv file.
"""
def top5_tweets(csvFileWithTweetTextAndTweetDate):
    df = pd.read_csv(csvFileWithTweetTextAndTweetDate,
                     names=['TweetText', 'TweetDate'],
                     encoding='utf-8')
    filtered_tweetText = []
    for line in df['TweetText'].values:
        row = pd.Series([line])
        filtered = row.str.contains(" ", regex=True, flags=re.IGNORECASE)
        if filtered[0] == True:
            filtered_tweetText.append(line)
    counter = Counter(filtered_tweetText).most_common(5)
    return counter


"""
   Versatile function that can take in any list of tuples and visualize using a bar chart. Functions on both single words
   and bigrams.
"""

# Functions that plots out a bar chart from input of tuples.
def make_histogram(listOfTuples):
   # Sorts according to integer in first column.
   sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
   # Adds it to a pandas DataFrame for further manipulation.
   df = pd.DataFrame(sorted_data, columns=['frequency', 'word'])
   # Plots the final result with a LogScale.
   df.plot(kind='bar', logy=True, x='word', width=0.4)
   # Displays the finished plot.
   plt.show()

#make_histogram(data)

def make_scatterplot(listOfTuples):
    # Takes in a list of tuples and sorts it from large to small.
    sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
    # Creates a pandas DataFrame to manipulate the data easily. Creates the columns frequency and word.
    df = pd.DataFrame(sorted_data, columns=['frequency', 'word'])
    s = [df['frequency']]
    words = df['word']
    # Plot figure size.
    plt.figure(figsize=(10, 10), dpi=80)
    # Possible positions for the circles. Pre-assigned to help readability.
    x = (7, 15, 22, 22, 7, 27, 10)
    y = (7, 15, 22, 7, 15, 15, 23)
    # Set axes lengths.
    axes = plt.gca()
    axes.set_xlim([0, 30])
    axes.set_ylim([0, 30])
    # Creates a random value that later is used to create randomized colors.
    vals = np.linspace(0, 1, 256)
    np.random.shuffle(vals)
    # Plots the scatterplot with x and y. s=size, c=color.
    plt.scatter(x[:len(df['word'])], y[:len(df['word'])], s=s, c=vals[:len(df['word'])])
    # Iterates through list of words and adds text.
    for i, word in enumerate(words):
        x_chords = x[i]
        y_chords = y[i]
        # Adds text and adds border color.
        txt = plt.text(x_chords-1, y_chords, word, fontfamily="serif",
                       fontsize=15, fontweight="extra bold", color="black",
                       multialignment="center")
        txt.set_path_effects([pe.withStroke(linewidth=4, foreground='w')])
    plt.axis('off')
    plt.show()

#Takes a list of tuples and strings for headers in a table as arguments. Prints a table presenting the list of tuples.
def make_table(listOfTuples, firstheader, secondheader):
    sorted_data = sorted(listOfTuples, key=lambda x: x[0], reverse=True)
    df = pd.DataFrame(sorted_data, columns=[firstheader, secondheader])
    print(df)


