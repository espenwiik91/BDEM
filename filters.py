from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
import pandas as pd

"""
These to rows have to be run the first time one uses the stopword filtering method: filter_by_stopwords()
import nltk
nltk.download('stopwords')
"""

stopWords = set(stopwords.words('english'))
# adding 'RT, 'http', '@', '\\n\\n' to the set of stopwords because such information is non-informative for
# several analysis purposes. This program finds retweets, for instance, in other ways
stopWords.update(
    ['RT', 'http', '@', '\\n\\n', '.', ',', ':', ';', '/', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '|'])


# print(stopWords)


def filter_whole_file(source_file, dest_name, lex):
    writer = csv.writer(dest_name)
    lex = open(lex, "r")
    lex = lex.readlines()
    for row in csv.reader(source_file):
        suitable = True
        row = row.split("\t")
        for col in row:
            for word in lex:
                if word in col:
                    suitable = False
        if suitable == True:
            writer.writerow(row)


def filter_by_crisislex(wordlist, lex):
    filteredlist = []
    for element in wordlist:
        for word in lex:
            if word in element:
                filteredlist.append(element)
    if len(filteredlist) > 10:
        del filteredlist[10:]
    return filteredlist


def filter_by_crisislex_for_bigrams(wordlist, lex):
    filteredlist = []
    stoplist = ['RT', 'http', '@', '//n', '\\n\\n']
    for i in range(0, len(wordlist)):
        for word in wordlist[i][1]:
            for lexword in lex:
                if lexword in wordlist[i][1][0] or lexword in wordlist[i][1][1]:
                    filteredlist.append(wordlist[i])
    filteredlist2 = []
    for element in filteredlist:
        bothstringsinformative = True
        for word in element[1]:
            for s in stoplist:
                if s in word:
                    bothstringsinformative = False
        if bothstringsinformative != False:
            filteredlist2.append(element)
    filteredlist2 = set(filteredlist2)
    filteredlist2 = list(filteredlist2)
    filteredlist2.sort()
    filteredlist2.reverse()
    if len(filteredlist2) > 10:
        del filteredlist2[10:]
    return filteredlist2


def filter_RT_for_bigrams(wordlist):
    lex = ['RT']
    filteredlist = []
    for i in range(0, len(wordlist)):
        for word in wordlist[i][1]:
            for lexword in lex:
                if lexword in wordlist[i][1][0] or lexword in wordlist[i][1][1]:
                    filteredlist.append(wordlist[i])
    return filteredlist


def filter_by_stopwords(listofwords, stopWords):
    filteredlist = []
    for word in listofwords:
        containsstopword = False
        for stop in stopWords:
            if stop.lower() in word[1].lower():
                # print(stop, word)
                containsstopword = True
        if containsstopword == False:
            filteredlist.append(word)
    if len(filteredlist) > 10:
        del filteredlist[2000:]
    return filteredlist

def find_crisis_word_in_total_word(stopwordlist, disasterlist):
    for element in stopwordlist:
        for d in disasterlist:
            #d, element = d.split(","), element.split(",")
            if d[1].lower() in element[1].lower():
                print("yolo")



