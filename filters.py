from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
import pandas as pd

# These to rows have to be run the first time one uses the stopword filtering method: filter_by_stopwords()
# import nltk
# nltk.download('stopwords')


# Retrieves the stopword set from the ntlk module and adds a number of other string values in addition.
stopWords = set(stopwords.words('english'))
# adding 'RT, 'http', '@', '\\n\\n' to the set of stopwords because such information is non-informative for
# several analysis purposes. This program finds retweets, for instance, in other ways
stopWords.update(
    ['RT', 'http', '@', '\\n\\n', '.', ',', ':', ';', '/', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '|'])


# Takes a list of tuples (ints and strings) and a lexicon for filtering as arguments. Returns a list containing 10 strings
# from the list passed as an argument that exists as strings in the lexicon. The 10 chosen strings come from the tuples
# with the greatest belonging ints.
def filter_by_crisislex(wordlist, lex):
    filteredlist = []
    for element in wordlist:
        for word in lex:
            if word in element:
                filteredlist.append(element)
    if len(filteredlist) > 10:
        del filteredlist[10:]
    return filteredlist


# This function does exactely the same as filter_by_crisislex(), but is developed to handle tuples containing an int and a tuple
# with two strings. If one of the two strings exists in the lexicon, the two strings can be passed to the retured list as a
# tuple. The tuples occurring in the tuples with the 10 greatest ints are passed to the returned list.
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


# Takes a list of words and the stopWord set from nltk as arguments. Declares a new list. Adds the 2000 first words from the list
# passed as an argument to the returned list - iff word does not exist in the stopWord set.
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
    reslist = []
    for element in stopwordlist:
        for d in disasterlist:
            # d, element = d.split(","), element.split(",")
            if d[1].lower() in element[1].lower():
                reslist.append(element[1])
    return reslist
